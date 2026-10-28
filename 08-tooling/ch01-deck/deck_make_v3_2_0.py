"""Makes SEN0401_Ch01_Introduction_3e_v3_2_0.pptx from v3_1_0 (never edited): every package part is copied byte for byte (same order, same compression) except docProps/core.xml,
whose cp:version becomes 3.2.0. The chart values come from the new recording examples_out_v3_1_0.json (_charts). Usage: python3 -B deck_make_v3_2_0.py OLD NEW"""
__version__ = "3.2.0"
import sys, zipfile
old, new = sys.argv[1:3]
zi = zipfile.ZipFile(old)
with zipfile.ZipFile(new, "w") as zo:
    for info in zi.infolist():
        data = zi.read(info.filename)
        if info.filename == "docProps/core.xml":
            assert data.count(b"<cp:version>3.1.0</cp:version>") == 1
            data = data.replace(b"<cp:version>3.1.0</cp:version>", b"<cp:version>3.2.0</cp:version>")
        zo.writestr(info, data, compress_type=info.compress_type)
print("wrote", new)
