from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FilesystemPath:
    path: Path
    is_file: bool
    is_dir: bool
