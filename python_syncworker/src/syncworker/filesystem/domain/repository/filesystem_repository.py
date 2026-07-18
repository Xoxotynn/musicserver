from __future__ import annotations

from pathlib import Path
from typing import Protocol

from syncworker.filesystem.domain.models.filesystem_models import ArchiveEntry, LocalTrack


class FilesystemRepository(Protocol):
    def list_tracks(self) -> tuple[LocalTrack, ...]:
        ...

    def read_archive(self) -> tuple[ArchiveEntry, ...]:
        ...

    def remove_archive_entries(self, item_ids: set[str]) -> None:
        ...

    def delete_m3u_playlists(self) -> None:
        ...

    def write_m3u_playlist(self, title: str, track_paths: tuple[str, ...]) -> Path:
        ...

    def delete_track(self, track: LocalTrack) -> None:
        ...
