# https://tildagon.badge.emfcamp.org/tildagon-apps/reference/ctx/#adding-images
import os

apps = os.listdir("/apps")
path = ""
ASSET_PATH = "apps/clock/"

if "pikesley_tildagon_clock" in apps:
    ASSET_PATH = "/apps/pikesley_tildagon_clock/"

if "clock" in apps:
    ASSET_PATH = "apps/clock/"
