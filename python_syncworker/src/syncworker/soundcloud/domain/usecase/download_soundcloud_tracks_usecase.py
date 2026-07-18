from __future__ import annotations

from pathlib import Path

from syncworker.soundcloud.domain.models.soundcloud_models import SoundCloudDownloadResult
from syncworker.soundcloud.domain.repository.soundcloud_repository import SoundCloudRepository


class DownloadSoundCloudTracksUseCase:
    def __init__(
        self,
        soundcloud_repository: SoundCloudRepository,
        music_dir: Path,
        archive_file: Path,
    ):
        self.soundcloud_repository = soundcloud_repository
        self.music_dir = music_dir
        self.archive_file = archive_file

    def execute(self) -> SoundCloudDownloadResult:
        return self.soundcloud_repository.download_tracks(
            music_dir=self.music_dir,
            archive_file=self.archive_file,
        )
