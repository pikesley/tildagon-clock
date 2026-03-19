import json

from .asset_path import asset_path


def conf(app_file, target_file="conf.json"):
    """Get `conf`."""
    ass_path = asset_path(app_file.split("/")[1])
    with open(ass_path + target_file) as j:  # noqa: PTH123
        return json.loads(j.read())
