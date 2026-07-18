from __future__ import annotations

from syncworker.filesystem.domain.repository.filesystem_repository import FilesystemRepository
from syncworker.sync.domain.models.library_models import MusicLibrary


class RemoveUnlikedTracksUseCase:
    def __init__(self, filesystem_repository: FilesystemRepository):
        self.filesystem_repository = filesystem_repository

    def execute(self, library: MusicLibrary) -> None:
        actual_soundcloud_ids = {track.soundcloud_id for track in library.all_tracks}

        archive_entry_ids = {entry.item_id for entry in self.filesystem_repository.read_archive()}
        self.filesystem_repository.remove_archive_entries(archive_entry_ids - actual_soundcloud_ids)

        for track in self.filesystem_repository.list_tracks():
            if track.soundcloud_id not in actual_soundcloud_ids:
                self.filesystem_repository.delete_track(track)
