from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence
import numpy as np

from .io import read_image

@dataclass
class ImageRegistry:
    folder: Path
    mapping: dict[str, str]
    _images: dict[str, np.ndarray] = field(default_factory=dict, init=False)
    missing: list[str] = field(default_factory=list, init=False)
    _loaded: bool = field(default=False, init=False)

    def _load(self, key: str, filename: str) -> None:
        path = self.folder / filename
        if not path.exists():
            self.missing.append(filename)
            return
        self._images[key] = read_image(path)

    def load(self) -> "ImageRegistry":
        if self._loaded:
            return self
        for key, filename in self.mapping.items():
            self._load(key, filename)
        self._loaded = True
        return self

    def __contains__(self, key: str) -> bool:
        return key in self._images

    def __getitem__(self, key: str) -> np.ndarray:
        return self._images[key]

    def has_all(self, keys: Sequence[str]) -> bool:
        return all(k in self._images for k in keys)