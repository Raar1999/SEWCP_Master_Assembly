"""aief_draw - generic 2D engineering-drawing vocabulary.

A drawing here is data: sheets of views, dimensions, notes and tables.
Two rules make it an *engineering* drawing layer rather than a picture
library:

1. **Every dimension carries provenance.** A `Dim` without a `source`
   (a governing specification anchor, a parameter-master name, an
   observed-geometry reference, or a recorded engineering decision) is
   refused at construction. The renderer emits a machine-readable
   provenance sidecar next to every sheet, so "every drawing dimension
   traces" is checkable, not asserted.

2. **No component knowledge.** The vocabulary is circles, bolt circles,
   sections, hatches, dimension types and note blocks. Part-specific
   content lives in drawing *definitions* that consume requirement
   packages and observed geometry, outside this package.

Renderers: SVG (canonical, diffable) and PDF (matplotlib, print form).
"""

from aief_draw.model import (
    Arc,
    Circle,
    Dim,
    Drawing,
    DrawError,
    Hatch,
    Line,
    Polyline,
    Sheet,
    Table,
    Text,
    View,
)

__all__ = [
    "Arc", "Circle", "Dim", "Drawing", "DrawError", "Hatch", "Line",
    "Polyline", "Sheet", "Table", "Text", "View",
]
