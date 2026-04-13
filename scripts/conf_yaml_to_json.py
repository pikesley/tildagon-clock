import gzip
import json
from pathlib import Path

import yaml

try:
    source = yaml.safe_load(Path("conf.yaml").read_text(encoding="utf-8"))
    Path("conf.json").write_text(json.dumps(source, indent=2, sort_keys=True))

    Path("conf.json.gz").write_bytes(
        gzip.compress(
            json.dumps(source, separators=(",", ":")).encode("utf-8"), mtime=0
        )
    )

except FileNotFoundError:
    pass
