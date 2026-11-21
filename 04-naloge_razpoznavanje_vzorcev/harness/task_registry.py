from pathlib import Path
from typing import Callable
import numpy as np

from naloge_razpoznavanje_vzorcev import (
    pripravi_razpoznavalnik, nalozi_razpoznavalnik, napovej_razred,
    prikazi_augmentiran_vzorec, nalozi_augmentiranega_razpoznavalnika,
    vizualiziraj_utezi,
    matrika_zmede, vrednoti_razpoznavo,
    detektiraj_okna,
    pripravi_detektor, nalozi_detektor, detektiraj,
    pripravi_resnet18_detektor, nalozi_resnet18_detektor,
    odpravi_duplikate,
    ujemanje_detekcij, vrednoti_detekcije,
    pripravi_detektor_okvirjev, nalozi_detektor_okvirjev
)

from .task import Task
from .task_report import PADDING

BASE = Path(__file__).resolve().parent.parent
INPUT_FOLDER  = BASE / "input-images"

INPUT_IMAGES = {
    # TODO
}

TASKS: list[Task] = [
    # TODO
]