"""Run the frozen source-native extraction contract on the preselected secondary panel."""
import runpy
from pathlib import Path
import sys

source = Path(__file__).resolve().parent / "R8_SOURCE_NATIVE_MECHANISM_AUDIT.py"
code = source.read_text(encoding='utf-8')
code = code.replace("IDS=['0180','0513','0526','1144','1765','2092','2497','2499','2505','2506']", "IDS=['0001','0003','0006','0009','0030','0031','0045','0054','0153','0154','0165','0179','0260','0261','0339','1160']")
code = code.replace("ARCH=ROOT/'R8_EXTERNAL_NR_SOURCE_ARCHIVE'", "ARCH=ROOT/'R8_SECONDARY_NR_SOURCE_ARCHIVE'")
code = code.replace("OUT=ROOT/'R8_DERIVED_SOURCE_NATIVE'", "OUT=ROOT/'R8_SECONDARY_DERIVED_SOURCE_NATIVE'")
ns={"__name__":"__main__"}
exec(compile(code, str(source), 'exec'), ns, ns)
