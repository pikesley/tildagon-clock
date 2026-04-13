import os
from pathlib import Path


class PushManager:
    """Manage pushing."""

    def __init__(self, app, app_root=".", includes="includes"):
        """Construct."""
        self.app = app
        self.app_root = Path(app_root)

        self.includes = (
            Path(app_root, includes).read_text(encoding="utf-8").strip().split("\n")
        )

        self.find_files()
        self.find_dirs()

        self.get_mkdir_commands()
        self.get_cp_dir_commands()
        self.get_cp_file_commands()

    def find_files(self):
        """Find files."""
        self.files = sorted(
            [entry for entry in self.includes if Path(self.app_root, entry).is_file()]
        )

    def find_dirs(self):
        """Find dirs that we must create and maybe push."""
        self.dirs_to_make = []
        self.dirs_to_push = []

        for entry in self.includes:
            if Path(self.app_root, entry).is_dir():
                self.dirs_to_make.append(entry)
                self.dirs_to_push.append((entry, str(Path(entry).parent)))

            if "/" in entry:
                x = Path(entry).parent
                while str(x) != ".":
                    if str(x) not in self.dirs_to_make:
                        self.dirs_to_make.append(str(x))
                    x = x.parent

        self.dirs_to_make.sort()
        self.dirs_to_push.sort()

    def get_mkdir_commands(self):
        """Assemble commands."""
        self.mkdir_commands = [mkdir("/", self.app)] + [
            mkdir(entry, self.app) for entry in self.dirs_to_make
        ]

    def get_cp_dir_commands(self):
        """Assemble commands."""
        self.cp_dir_commands = []
        for directory, parent in self.dirs_to_push:
            trail = parent
            if parent == ".":
                trail = ""

            self.cp_dir_commands.append(
                f"python -m mpremote fs cp -r {directory} :/apps/{self.app}/{trail}"
            )

    def get_cp_file_commands(self):
        """Assemble commands."""
        self.cp_file_commands = [cp_file(entry, self.app) for entry in self.files]

    def push(self):
        """Push."""
        commands = self.mkdir_commands + self.cp_dir_commands + self.cp_file_commands
        for command in commands:
            print(command)
            os.system(command)  # noqa: S605


def mkdir(entry, app):
    """Generate an `mpremote mkdir` command."""
    if entry.endswith("/"):
        entry = entry[:-1]

    sep = "/"
    if entry == "":
        sep = ""

    return f"python -m mpremote fs mkdir :/apps/{app}{sep}{entry}"


def cp_file(entry, app):
    """Generate an `mpremote fs cp` command."""
    return f"python -m mpremote fs cp {entry} :/apps/{app}/{entry}"


def cp_dir(entry, app):
    """Recursively copy a dir."""
    if entry:
        return f"python -m mpremote fs cp -r {entry}/* :/apps/{app}/{entry}/*"
    return ""


if __name__ == "__main__":
    import sys

    includes = "includes"
    if len(sys.argv) > 1:
        includes = sys.argv[1]

    inc = Path(includes)
    if not inc.exists():
        print(f"`{includes}` needs to exist")
        sys.exit(1)

    if Path("includes").stat().st_size == 0:
        print(f"`{includes}` needs be populated")
        sys.exit(1)

    app = Path(__file__).parent.parent.stem
    pm = PushManager(app, includes=includes)
    pm.push()
