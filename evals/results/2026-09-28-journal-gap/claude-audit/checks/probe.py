import json
from pathlib import Path
import sys
limit=json.loads(Path("settings.json").read_text())["batch_limit"]
if limit == 4:
    print("Synthetic staging fixture: batch_limit=4; queue overflow; exit 7. No production check.")
    sys.exit(7)
print(f"Synthetic staging fixture: batch_limit={limit}; passed; exit 0. No production check.")
