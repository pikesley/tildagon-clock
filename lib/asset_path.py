# https://tildagon.badge.emfcamp.org/tildagon-apps/reference/ctx/#adding-images
import os

apps = os.listdir("/apps")
path = ""
ASSET_PATH = "apps/clock/"

for a in apps:
    if a == "pikesley_tildagon_clock":
        print("found published-app-dir")
        path = "/apps/" + a
        ASSET_PATH = path + "/assets/"
