from __future__ import annotations

from pathlib import Path

from syncworker.soundcloud.data.client.soundcloud_client import SoundCloudClient
from syncworker.soundcloud.data.models.soundcloud_models import SoundCloudEntry
from syncworker.soundcloud.domain.models.soundcloud_models import (
    SoundCloudDownloadResult,
    SoundCloudLibrary,
    SoundCloudPlaylist,
    SoundCloudTrack,
)
from syncworker.soundcloud.domain.repository.soundcloud_repository import SoundCloudRepository


class SoundCloudDataRepository(SoundCloudRepository):
    def __init__(self, url: str, client: SoundCloudClient):
        self.url = url
        self.client = client

    def download_tracks(self, music_dir: Path, archive_file: Path) -> SoundCloudDownloadResult:
        music_dir.mkdir(parents=True, exist_ok=True)
        archive_file.parent.mkdir(parents=True, exist_ok=True)

        exit_code = self.client.download(
            url=self.url,
            music_dir=music_dir,
            archive_file=archive_file,
        )

        return SoundCloudDownloadResult(exit_code=exit_code)

    def get_library(self) -> SoundCloudLibrary:
        root = self.client.extract_flat(self.url)

        liked_tracks: list[SoundCloudTrack] = []
        playlists: list[SoundCloudPlaylist] = []

        for entry in root.entries:
            item_id = self._required_str(entry, "id")
            title = self._required_str(entry, "title")
            url = self._required_str(entry, "url")

            if self._is_playlist(url):
                playlists.append(
                    SoundCloudPlaylist(
                        id=item_id,
                        url=url,
                        title=title,
                        tracks=self._get_playlist_tracks(url),
                    )
                )
                continue

            liked_tracks.append(SoundCloudTrack(id=item_id, url=url, title=title))

        return SoundCloudLibrary(liked_tracks=tuple(liked_tracks), playlists=tuple(playlists))

    def _get_playlist_tracks(self, playlist_url: str) -> tuple[SoundCloudTrack, ...]:
        playlist = self.client.extract_flat(playlist_url)
        return tuple(
            SoundCloudTrack(
                id=entry.id,
                url=entry.url,
                title=entry.title,
            )
            for entry in playlist.entries
            if entry.id is not None and entry.url is not None and entry.title is not None
        )

    @staticmethod
    def _is_playlist(url: str) -> bool:
        return "/sets/" in url

    @staticmethod
    def _required_str(entry: SoundCloudEntry, field: str) -> str:
        value = getattr(entry, field)
        if value is None:
            raise RuntimeError(f"SoundCloud entry has no {field}: {entry}")

        return value
