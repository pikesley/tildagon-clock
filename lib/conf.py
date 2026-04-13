import gzip
import json

from .asset_path import ASSET_PATH

conf = json.loads(
    gzip.decompress(open(ASSET_PATH + "conf.json.gz", "rb").read()).decode()  # noqa: PTH123, SIM115
)
