# https://tildagon.badge.emfcamp.org/tildagon-apps/reference/ctx/#adding-images
import os


def asset_path(app_name):
    """Determine asset_path."""
    try:
        apps = os.listdir("/apps")
    except FileNotFoundError:
        apps = []
    ass_path = ""

    if f"pikesley_tildagon_{app_name}" in apps:
        ass_path = f"/apps/pikesley_tildagon_{app_name}/"

    if app_name in apps:
        ass_path = f"apps/{app_name}/"

    return ass_path
