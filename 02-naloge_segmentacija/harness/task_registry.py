from pathlib import Path
from typing import Callable
import numpy as np

from naloge_segmentacija import (
    binarna_segmentacija,
    segmentiraj_rumeno_barvo,
    pobarvaj_sivinsko,
    odvzem_ozadja,
    stevilo_regij,
    sredisca_regij,
    izrezi_regije,
    detekcija_4_kotnikov,
    detekcija_4_kotnikov_adaptivno,
    pripravi_filter_plus, detekcija_plus,
)

from .io import to_gray_f32, read_image
from .task import Task
from .task_report import PADDING

BASE = Path(__file__).resolve().parent.parent
INPUT_FOLDER  = BASE / "input-images"
OUTPUT_FOLDER = BASE / "output-images"

INPUT_IMAGES = {
    "image-1": "input-image-1.png", # krog (sivinska)
    "image-2": "input-image-2.png", # svinčniki (barvna)
    "image-3": "input-image-3.png", # objekti / 4-kotniki (sivinska)
    "image-4": "input-image-4.png", # + in x simboli (sivinska)
}

def out(name: str) -> Path:
    return OUTPUT_FOLDER / name

PLUS_CENTERS = [(39, 98), (40, 176), (133, 191), (148, 53)] # (y, x)
X_CENTERS    = [(52, 38), (70, 214), (206, 154), (188, 41)] # (y, x)
PLUS_FILTER = pripravi_filter_plus(
    slika=to_gray_f32(read_image(INPUT_FOLDER / INPUT_IMAGES["image-4"])),
    sredisca_plus=PLUS_CENTERS,
    sredisca_x=X_CENTERS,
    velikost_okna=15
)

def _report_scalar(label: str) -> Callable[[int], None]:
    def _inner(value: int) -> None:
        print(f"{PADDING}  • {label}: {value}")
    return _inner

def _report_coords(label: str, max_rows: int = 50) -> Callable[[np.ndarray], None]:
    def _inner(pts: np.ndarray) -> None:
        max_rows_digits: int = len(str(len(pts) - 1))
        pts = pts[np.lexsort((pts[:, 1], pts[:, 0]))]
        print(f"{PADDING}  • {label}: {len(pts)}")
        for i, (y, x) in enumerate(pts[:max_rows]):
            print(f"{PADDING}    [{i:>{max_rows_digits}}] x={x}, y={y}")
        if len(pts) > max_rows:
            print(f"{PADDING}    ... ({len(pts) - max_rows} več)")
    return _inner

def _report_polys(label: str) -> Callable[[list[np.ndarray]], None]:
    def _inner(polys: list[np.ndarray]) -> None:
        print(f"{PADDING}  • {label}: {len(polys)}")
        for i, p in enumerate(polys):
            coords = ", ".join(f"({y},{x})" for y, x in p)
            print(f"{PADDING}    [{i}] {coords}")
    return _inner


TASKS: list[Task] = [
    # Task Category: Input Image 1
    Task(
        1, "binarna_segmentacija", ["image-1"],
        binarna_segmentacija,
        lambda r: (to_gray_f32(r["image-1"]),),
        [out("output-image-01.png")],
    ),

    # Task Category: Input Image 2
    Task(
        2, "segmentiraj_rumeno_barvo", ["image-2"],
        segmentiraj_rumeno_barvo,
        lambda r: (r["image-2"],),
        [out("output-image-02.png")],
        report_label="bool maska",
    ),
    Task(
        3, "pobarvaj_sivinsko", ["image-2"],
        pobarvaj_sivinsko,
        lambda r: (r["image-2"], segmentiraj_rumeno_barvo(r["image-2"])),
        [out("output-image-03.png")],
    ),

    # Task Category: Input Image 3
    Task(
        4, "odvzem_ozadja", ["image-3"],
        odvzem_ozadja,
        lambda r: (to_gray_f32(r["image-3"]), ),
        [out("output-image-04.png")],
        report_label="bool maska",
    ),
    Task(
        5, "stevilo_regij", ["image-3"],
        stevilo_regij,
        lambda r: (odvzem_ozadja(to_gray_f32(r["image-3"])), 128.0),
        outputs=(),
        annotate=_report_scalar("število regij (≥128px)"),
    ),
    Task(
        6, "sredisca_regij", ["image-3"],
        sredisca_regij,
        lambda r: (odvzem_ozadja(to_gray_f32(r["image-3"])), ),
        outputs=(),
        annotate=_report_coords("središča regij"),
    ),
    Task(
        7, "izrezi_regije", ["image-3"],
        izrezi_regije,
        lambda r: (
            to_gray_f32(r["image-3"]),
            odvzem_ozadja(to_gray_f32(r["image-3"]))
        ),
        [out("output-image-07.png")],   # -> output-image-07-01.png, ...
    ),
    Task(
        8, "detekcija_4_kotnikov", ["image-3"],
        detekcija_4_kotnikov,
        lambda r: (to_gray_f32(r["image-3"]),),
        outputs=(),
        annotate=_report_polys("4-kotniki"),
    ),
    Task(
        9, "detekcija_4_kotnikov_adaptivno", ["image-3"],
        detekcija_4_kotnikov_adaptivno,
        lambda r: (to_gray_f32(r["image-3"]),),
        outputs=(),
        annotate=_report_polys("4-kotniki (adaptivno)"),
    ),

    # Task Category: Input Image 4
    Task(
        10, "detekcija_plus", ["image-4"],
        detekcija_plus,
        lambda r: (to_gray_f32(r["image-4"]), PLUS_FILTER, 2, 48),
        outputs=(),
        annotate=_report_coords("lokalni maksimumi"),
    ),
]