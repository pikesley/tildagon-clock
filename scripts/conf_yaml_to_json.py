import json
from pathlib import Path

import yaml

try:
    source = yaml.safe_load(Path("conf.yaml").read_text(encoding="utf-8"))
    Path("conf.json").write_text(json.dumps(source, indent=2, sort_keys=True))

except FileNotFoundError:
    pass
