from typing import Any
import numpy as np

PADDING = " " * 5
SEPARATOR = "=" * 128

def _stats(el) -> str:
    return f"shape={el.shape}, dtype={el.dtype}, min={el.min():.3f}, max={el.max():.3f}"

def report(result: Any, name: str = "Izhod") -> None:
    if isinstance(result, (list, tuple)):
        print(f"{PADDING}• {name}: {type(result).__name__}[{len(result)}]")
        for i, el in enumerate(result):
            print(f"{PADDING}[{str(i).zfill(2)}] {_stats(el)}")
    elif isinstance(result, np.ndarray):
        print(f"{PADDING}• {name}: {_stats(result)}")
    else:
        print(f"{PADDING}• {name}: {type(result).__name__} = {result}")

def title(n: int, name: str, images: str) -> None:
    print(f"\n[{str(n).zfill(2)}] {name} | slika: {images}")