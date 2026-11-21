# run_tests.py
"""Testna skripta za paket naloge_segmentacija."""

from __future__ import annotations
from harness.image_registry import ImageRegistry
from harness.task_registry  import TASKS, INPUT_FOLDER, INPUT_IMAGES
from harness.task_report    import SEPARATOR
import sys


def main() -> int:
    if not INPUT_FOLDER.is_dir():
        print(f"Mapa ne obstaja: {INPUT_FOLDER}", file=sys.stderr)
        print("Ustvari mapo 'input-images' in vanjo daj pričakovane slike.", file=sys.stderr)
        return 1

    print(SEPARATOR)
    print(f"Mapa vhodnih  slik: {INPUT_FOLDER}")
    print(SEPARATOR)

    reg = ImageRegistry(INPUT_FOLDER, INPUT_IMAGES).load()
    if reg.missing:
        print("\nManjkajoče slike:")
        for name in reg.missing:
            print(f"• {name}")
        print("\nNadaljujem samo z obstoječimi...\n")

    for task in TASKS:
        if task.can_run(reg):
            task.run(reg)
        else:
            missing = [k for k in task.input_keys if k not in reg]
            print(
                f"• preskočeno [{task.n:02d}] {task.name} "
                f"(manjka: {', '.join(missing)})"
            )

    print("\n" + SEPARATOR)
    print("Konec testov.")
    print(SEPARATOR)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())