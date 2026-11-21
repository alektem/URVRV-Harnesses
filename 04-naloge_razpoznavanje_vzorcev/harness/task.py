from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence
import numpy as np

from .image_registry import ImageRegistry
from .io import write_image, write_image_list
from .task_report import report, title

@dataclass
class Task:
    n: int
    name: str
    input_keys: Sequence[str]
    fn: Callable[..., Any]
    build_args: Callable[[ImageRegistry], tuple]
    outputs: Sequence[Path] = ()
    report_label: str = "Izhod"
    split: Callable[[Any], Sequence[np.ndarray]] | None = None
    annotate: Callable[[Any], None] | None = None

    def can_run(self, reg: ImageRegistry) -> bool:
        return reg.has_all(self.input_keys)

    def run(self, reg: ImageRegistry) -> Any:
        title(self.n, self.name, ", ".join(self.input_keys))
        result = self.fn(*self.build_args(reg))
        report(result, self.report_label)
        if self.annotate:
            self.annotate(result)
        self._persist(result)
        return result

    def _persist(self, result: Any) -> None:
        if not self.outputs:
            return
        if self.split is not None:
            arrays = self.split(result)
        elif isinstance(result, list):
            write_image_list(self.outputs[0], result)
            return
        elif isinstance(result, tuple):
            arrays = result
        else:
            arrays = [result]
        for path, arr in zip(self.outputs, arrays):
            write_image(path, arr)