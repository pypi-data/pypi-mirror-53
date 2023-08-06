import sys
import re

args = sys.argv
total = 0
passed = 0
failed = 0

try:
    for arg in args[1:]:
        # ress = re.search("^.*\*([0-9]+)\*.*\*([0-9]+).*\*([0-9]+)", str(arg))
        # ress = re.search(".*([0-9]+).*([0-9]+).*([0-9]+).*", str(arg))
        # total += int(ress.group(1))
        # passed += int(ress.group(2))
        # failed += int(ress.group(3))
        restab = re.findall(r'\d+', str(arg))
        total += int(restab[0])
        passed += int(restab[1])
        failed += int(restab[2])

except Exception:
    pass


print("Summary | total: *{}* | passed: *{}* | failed: *{}* | passrate: *{}%*".format(total, passed, failed, int(passed/total*100)))