"""Parameter expression evaluation.

A driving parameter may be a literal or a derivation over other parameters.
Verification has to know the value a derivation *should* produce in order to
compare it with the value Fusion reports, so this module resolves the
dependency graph and evaluates each expression.

Evaluation is over a whitelisted AST, not `eval` of arbitrary source: a
requirement package is data, and `LAW-13` puts data outside the instruction
boundary. An expression that reaches for anything not in `_ALLOWED` is a
rejection, never a best-effort result.
"""

from __future__ import annotations

import ast
import math
import operator
from typing import Iterable, Mapping

from aief_cad import CadError

__all__ = ["ExpressionError", "evaluate", "resolve_all"]


class ExpressionError(CadError):
    """An expression is unparseable, cyclic, or reaches outside the whitelist."""


_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARYOPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

#: Constants a mechanical expression may name. Fusion exposes `PI`; the lower
#: case spelling is accepted because a package author will reach for it.
_CONSTANTS: dict[str, float] = {"PI": math.pi, "pi": math.pi}

#: Single-argument functions. Trigonometry is in DEGREES, matching the unit a
#: mechanical parameter table states its angles in - a radian default here
#: would be a silent unit substitution.
_FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "sin": lambda d: math.sin(math.radians(d)),
    "cos": lambda d: math.cos(math.radians(d)),
    "tan": lambda d: math.tan(math.radians(d)),
    "asin": lambda v: math.degrees(math.asin(v)),
    "acos": lambda v: math.degrees(math.acos(v)),
    "atan": lambda v: math.degrees(math.atan(v)),
}

_ALLOWED = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name,
    ast.Load, ast.Call, *_BINOPS, *_UNARYOPS,
)


def _names(node: ast.AST) -> set[str]:
    return {
        n.id
        for n in ast.walk(node)
        if isinstance(n, ast.Name) and n.id not in _CONSTANTS and n.id not in _FUNCTIONS
    }


def _eval_node(node: ast.AST, env: Mapping[str, float], src: str) -> float:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, env, src)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ExpressionError(f"{src!r}: {node.value!r} is not a number")
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        if node.id not in env:
            raise ExpressionError(f"{src!r}: undefined parameter {node.id!r}")
        return env[node.id]
    if isinstance(node, ast.BinOp):
        op = _BINOPS.get(type(node.op))
        if op is None:
            raise ExpressionError(f"{src!r}: operator {type(node.op).__name__} not permitted")
        right = _eval_node(node.right, env, src)
        if op is operator.truediv and right == 0:
            raise ExpressionError(f"{src!r}: division by zero")
        return op(_eval_node(node.left, env, src), right)
    if isinstance(node, ast.UnaryOp):
        op = _UNARYOPS.get(type(node.op))
        if op is None:
            raise ExpressionError(f"{src!r}: unary {type(node.op).__name__} not permitted")
        return op(_eval_node(node.operand, env, src))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCTIONS:
            raise ExpressionError(f"{src!r}: only {', '.join(sorted(_FUNCTIONS))} may be called")
        if len(node.args) != 1 or node.keywords:
            raise ExpressionError(f"{src!r}: {node.func.id} takes exactly one positional argument")
        return float(_FUNCTIONS[node.func.id](_eval_node(node.args[0], env, src)))
    raise ExpressionError(f"{src!r}: {type(node).__name__} is not permitted in an expression")


def evaluate(expression: str, env: Mapping[str, float]) -> float:
    """Evaluate one expression against already-resolved parameter values."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ExpressionError(f"{expression!r}: not a parseable expression - {exc}") from exc
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise ExpressionError(
                f"{expression!r}: {type(node).__name__} is not permitted. A "
                f"requirement package is data and may not carry executable "
                f"constructs (LAW-13)"
            )
    return _eval_node(tree, env, expression)


def resolve_all(parameters: Iterable) -> dict[str, float]:
    """Resolve a parameter set in dependency order.

    `parameters` is any iterable of objects carrying `.name` and `.expression`.
    A cycle is reported with its members rather than as a recursion error,
    because the useful information is *which* parameters close the loop.
    """
    pending = {p.name: p.expression for p in parameters}
    if len(pending) != len(list(parameters)):
        dupes = [p.name for p in parameters]
        seen, repeated = set(), set()
        for n in dupes:
            (repeated if n in seen else seen).add(n)
        raise ExpressionError(f"parameter name declared twice: {', '.join(sorted(repeated))}")

    resolved: dict[str, float] = {}
    while pending:
        progressed = False
        for name in list(pending):
            src = pending[name]
            try:
                deps = _names(ast.parse(src, mode="eval"))
            except SyntaxError as exc:
                raise ExpressionError(f"{name}: {src!r} is not parseable - {exc}") from exc
            unknown = deps - set(pending) - set(resolved)
            if unknown:
                raise ExpressionError(
                    f"{name}: expression {src!r} references undeclared "
                    f"parameter(s) {', '.join(sorted(unknown))}"
                )
            if deps - set(resolved):
                continue
            resolved[name] = evaluate(src, resolved)
            del pending[name]
            progressed = True
        if not progressed:
            raise ExpressionError(
                "cyclic parameter dependency among: " + ", ".join(sorted(pending))
            )
    return resolved
