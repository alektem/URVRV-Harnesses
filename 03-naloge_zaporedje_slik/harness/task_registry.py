from pathlib import Path
from typing import Callable
import numpy as np

from naloge_zaporedje_slik import (
    oceni_ozadje,
    segmentiraj_ospredje,
    DetektorGibanja,
    DetektorRegijGibanja,
    DetektorRegijGibanja,
    SledilecRegije,
    hitrost_gibanja,
    UsmerjenDetektorRegijGibanja,
    trajektorije_objektov,
    analiziraj_opticni_pretok
)

from .task import Task
from .task_report import PADDING

BASE = Path(__file__).resolve().parent.parent
INPUT_FOLDER  = BASE / "input-videos"

INPUT_VIDEOS = {
    # TODO
}

TASKS: list[Task] = [
    # TODO
]