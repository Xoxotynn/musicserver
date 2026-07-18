from __future__ import annotations

from syncworker.filesystem.domain.repository.filesystem_repository import FilesystemRepository
from syncworker.sync.domain.models.library_models import MusicLibrary


class SyncPlaylistsUseCase:
    def __init__(self, filesystem_repository: FilesystemRepository):
        self.filesystem_repository = filesystem_repository

    def execute(self, library: MusicLibrary) -> None:
        self.filesystem_repository.delete_m3u_playlists()

        for playlist in library.playlists:
            self.filesystem_repository.write_m3u_playlist(
                title=playlist.title,
                track_paths=tuple(track.navidrome_path for track in playlist.tracks),
            )
