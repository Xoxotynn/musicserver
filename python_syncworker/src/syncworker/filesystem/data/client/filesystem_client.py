from __future__ import annotations

import shutil
from pathlib import Path

from syncworker.filesystem.data.models.filesystem_models import FilesystemPath


class FilesystemClient:
    def list_dir(self, directory: Path) -> tuple[FilesystemPath, ...]:
        if not directory.exists():
            return ()

        return tuple(
            FilesystemPath(
                path=path,
                is_file=path.is_file(),
                is_dir=path.is_dir(),
            )
            for path in directory.iterdir()
        )

    @staticmethod
    def exists(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def ensure_dir(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def read_lines(path: Path, keepends: bool = False) -> tuple[str, ...]:
        return tuple(path.read_text(encoding="utf-8").splitlines(keepends=keepends))

    @staticmethod
    def write_text(path: Path, text: str) -> None:
        path.write_text(text, encoding="utf-8")

    @staticmethod
    def delete_file(path: Path, missing_ok: bool = False) -> None:
        path.unlink(missing_ok=missing_ok)

    @staticmethod
    def delete_tree(path: Path) -> None:
        shutil.rmtree(path)
