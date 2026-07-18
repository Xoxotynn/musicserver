from __future__ import annotations

from pathlib import Path
from typing import Protocol

from syncworker.soundcloud.domain.models.soundcloud_models import SoundCloudDownloadResult, SoundCloudLibrary


class SoundCloudRepository(Protocol):
    def download_tracks(self, music_dir: Path, archive_file: Path) -> SoundCloudDownloadResult:
        ...

    def get_library(self) -> SoundCloudLibrary:
        ...
