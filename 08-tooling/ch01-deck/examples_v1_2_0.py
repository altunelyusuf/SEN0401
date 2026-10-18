"""Chapter 1 examples, version 1.2.0: examples_v1_1_0.py unchanged, plus one group that is not on a slide and exists only so that the Pizza Day chart has an executed source: the six plotted values are READ from
the story companion's PIZZA_VALUE (documented milestones, the last one fetched live on 2026-10-06), and the slide says that they are Recorded, not computed. Recorded again, under the interpreter now in use,
by sen0401_deck_examples_record_v1_0_0.py."""
__version__ = "1.2.0"
import os
from examples_v1_1_0 import *          # PRELUDE, EX, BLOCKS, EXPECT
from examples_v1_1_0 import EX as _EX
_TOOL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = dict(_EX)
EX["PizzaValueRecorded"] = [
    "import sys; sys.path.insert(0, %r); import sen0401_ch01_stories_v1_5_0 as ST" % _TOOL,
    "[(d, v) for d, v, _ in ST.PIZZA_VALUE]",
]
# the subsidy chart plots nine values (five real halvings, four projected); one executed line computes all nine, so that every plotted value has an executed source
EX["HalvingChartValues"] = ["[50 / 2 ** k for k in range(9)]"]
