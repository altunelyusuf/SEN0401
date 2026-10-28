#!/usr/bin/env python3
"""Chapter 5 deck v3.3.0 (a NEW tool file). The deck v3.2.0 is read, never written. The slides, notes, charts, pictures and links of v3.2.0 were correct; the defect was the
recording (examples_out_v1_1_0.json) and the chart value sources, repaired by examples_v1_2_0.py and examples_out_v1_2_0.json. So v3.3.0 is v3.2.0 with one change: the title in
the document properties names v3.3.0. Usage: deck_derive_v3_3_0.py"""
__version__ = "3.3.0"
import os
from pptx import Presentation
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_2_0.pptx")
DST = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_3_0.pptx")
p = Presentation(SRC)
p.core_properties.title = p.core_properties.title.replace("v3.2.0", "v3.3.0")
p.save(DST)
print("written", DST)
