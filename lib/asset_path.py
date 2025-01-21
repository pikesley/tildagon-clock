# https://tildagon.badge.emfcamp.org/tildagon-apps/reference/ctx/#adding-images
import os

apps = os.listdir("/apps")
path = ""
for a in apps:
    if a == "pikesley_tildagon_clock":
        path = "/apps/" + a
        ASSET_PATH = path + "/assets/"
    else:
        ASSET_PATH = "apps/clock/"
