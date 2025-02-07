from pathlib import Path

snake_name = Path.cwd().stem
camel_name = "".join(x.capitalize() for x in snake_name.lower().split("_"))
all_files = Path().glob("**/*")

for entry in all_files:
    if entry.is_file() and not str(entry).startswith(".git"):
        print(str(entry))
        lines = entry.read_text(encoding="utf-8").split("\n")
        fixed_lines = []

        fixed_lines = [
            line.replace("Skellington", camel_name).replace("skellington", snake_name)
            for line in lines
        ]

        entry.write_text("\n".join(fixed_lines))
