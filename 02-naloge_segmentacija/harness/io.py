from __future__ import annotations
from pathlib import Path
import numpy as np
import numpy.typing as npt

def read_image(path: Path) -> npt.NDArray[np.float32]:
    """Read an image as float32 RGB in [0, 1]. Raises FileNotFoundError."""
    if not path.exists():
        raise FileNotFoundError(f"Manjka slika: {path}")
    try:
        from PIL import Image
        img = Image.open(path).convert("RGB")
        return np.asarray(img, dtype=np.float32) / 255.0
    except ImportError:
        import imageio.v3 as iio
        arr = iio.imread(path)
        if arr.ndim == 2:
            arr = np.stack([arr] * 3, axis=-1)
        return arr[:, :, :3].astype(np.float32) / 255.0


def _to_u8(img: npt.NDArray[np.generic]) -> npt.NDArray[np.uint8]:
    arr = np.asarray(img)
    if not np.issubdtype(arr.dtype, np.uint8):
        arr = (np.clip(arr.astype(np.float32), 0.0, 1.0) * 255.0).round().astype(np.uint8)
    if arr.ndim == 2:
        arr = np.stack([arr] * 3, axis=-1)
    elif arr.ndim == 3 and arr.shape[2] == 1:
        arr = np.repeat(arr, 3, axis=2)
    return arr.astype(np.uint8)


def to_gray_u8(barvna: npt.NDArray[np.float32]) -> npt.NDArray[np.uint8]:
    return np.asarray(barvna.mean(axis=2) * 255.0, dtype=np.uint8)

def to_gray_f32(barvna: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    return np.asarray(barvna.mean(axis=2), dtype=np.float32)


def _write(path: Path, arr: npt.NDArray[np.uint8]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image
        Image.fromarray(arr).save(path)
    except ImportError:
        import imageio.v3 as iio
        iio.imwrite(path, arr)


def write_image(path: Path, img: npt.NDArray[np.generic], *, verify: bool = True) -> None:
    arr = _to_u8(img)
    _write(path, arr)
    if verify:
        reread = read_image(path)
        np.testing.assert_array_equal(
            np.asarray((reread * 255.0).round(), dtype=np.uint8), arr,
            err_msg=f"[ERROR] Round-trip FAIL: {path}",
        )


def write_image_list(base: Path, imgs: list[npt.NDArray[np.float32]]) -> list[Path]:
    if not imgs:
        return []
    width = max(1, len(str(len(imgs))))
    paths = []
    for i, img in enumerate(imgs):
        p = base.with_name(f"{base.stem}-{str(i + 1).zfill(width)}.png")
        write_image(p, img)
        paths.append(p)
    return paths
