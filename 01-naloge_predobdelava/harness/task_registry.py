from pathlib import Path
import numpy as np

from naloge_predobdelava import (
    normaliziraj_sivine_uniformno, 
    transformiraj_z_lut, 
    razrez_slike_3_4,
    pretvorba_G_RB, 
    zmanjsaj_za_2, 
    povecaj_za_2, 
    odstrani_crte,
    filtriraj_piramido_slik, 
    isci_koticke, 
    isci_znak_A
)

from .io import to_gray_u8, to_gray_f32
from .task import Task
from .task_report import PADDING

BASE = Path(__file__).resolve().parent.parent
INPUT_FOLDER = BASE / "input-images"
OUTPUT_FOLDER = BASE / "output-images"

INPUT_IMAGES = {
    "shared": "input-image-1.png",
    "lines": "input-image-2.png",
    "pyramid-S": "input-image-3-S.png",
    "pyramid-M": "input-image-3-M.png",
    "pyramid-L": "input-image-3-L.png",
    "corners": "input-image-4.png",
    "character": "input-image-5.png",
}

def out(name: str) -> Path:
    return OUTPUT_FOLDER / name

LUT_INV = (255 - np.arange(256)).astype(np.uint8)
LUT_LIN = np.linspace(0.0, 1.0, 256, dtype=np.float32)
CORNER_LABELS = ("TL", "TR", "BR", "BL")

def _peak_report(response: np.ndarray) -> None:
    """Print the argmax location of each corner response map in an (H, W, 4) array."""
    for i, name in enumerate(CORNER_LABELS):
        ch = response[..., i]
        row, col = np.unravel_index(np.argmax(ch), ch.shape)
        print(
            f"{PADDING}  • {name}: peak pri (vrstica={row}, stolpec={col}), "
            f"vrednost={ch[row, col]:.3f}"
        )

TASKS: list[Task] = [
    # Task Category: Input Image "Shared"
    Task(
        1, "normaliziraj_sivine_uniformno", ["shared"],
        normaliziraj_sivine_uniformno,
        lambda r: (to_gray_u8(r["shared"]), 0.0, 1.0),
        [
            out("output-image-01.png")
        ]
    ),
    Task(
        2, "transformiraj_z_lut", ["shared"],
        transformiraj_z_lut,
        lambda r: (to_gray_u8(r["shared"]), LUT_INV),
        [
            out("output-image-02-inv.png")
        ],
        report_label="inverz (uint8)"
    ),
    Task(
        2, "transformiraj_z_lut", ["shared"],
        transformiraj_z_lut,
        lambda r: (to_gray_u8(r["shared"]), LUT_LIN),
        [
            out("output-image-02-lin.png")
        ],
        report_label="linearna (float32)"
    ),
    Task(
        3, "razrez_slike_3_4", ["shared"],
        razrez_slike_3_4,
        lambda r: (r["shared"],),
        [
            out("output-image-03.png")
        ]
    ),
    Task(
        4, "pretvorba_G_RB", ["shared"],
        pretvorba_G_RB, lambda r: (r["shared"],),
        [
            out("output-image-04.png")
        ]
    ),
    Task(
        5, "zmanjsaj_za_2", ["shared"],
        zmanjsaj_za_2, lambda r: (r["shared"],),
        [
            out("output-image-05.png")
        ]
    ),
    Task(
        6, "povecaj_za_2", ["shared"],
        povecaj_za_2, lambda r: (r["shared"],),
        [
            out("output-image-06.png")
        ]
    ),

    # Task Category: Input Image "Lines"
    Task(
        7, "odstrani_crte", ["lines"],
        odstrani_crte, lambda r: (to_gray_f32(r["lines"]),),
        [
            out("output-image-07-siva.png")
        ],
        report_label="float32 [siva]"
    ),

    # Task Category: Input Image "Lines"
    Task(
        7, "odstrani_crte", ["lines"],
        odstrani_crte, lambda r: (r["lines"],),
        [
            out("output-image-07-barvna.png")
        ],
        report_label="float32 [barvna]"
    ),

    # Task Category: Input Images "Pyramid"
    Task(
        8, "filtriraj_piramido_slik", ["pyramid-S", "pyramid-M", "pyramid-L"],
        filtriraj_piramido_slik, lambda r: (r["pyramid-S"], r["pyramid-M"], r["pyramid-L"]),
        [
            out("output-image-08-S.png"),
            out("output-image-08-M.png"),
            out("output-image-08-L.png")
        ]
    ),

    # Task Category: Input Image "Corners"
    Task(
        9, "isci_koticke", ["corners"],
        isci_koticke, lambda r: (to_gray_f32(r["corners"]),),
        [out(f"output-image-09-{c}.png") for c in CORNER_LABELS],
        split=lambda r: [r[..., i] for i in range(4)],
        annotate=_peak_report,
    ),

    # Task Category: Input Image "Character"
    Task(
        10, "isci_znak_A", ["character"],
        isci_znak_A, lambda r: (to_gray_f32(r["character"]),),
        [
            out("output-image-10.png")
        ]
    ),
]