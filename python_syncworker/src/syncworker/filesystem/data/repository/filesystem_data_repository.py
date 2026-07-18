from __future__ import annotations

import re
from pathlib import Path

from syncworker.filesystem.data.client.filesystem_client import FilesystemClient
from syncworker.filesystem.domain.models.filesystem_models import ArchiveEntry, LocalTrack
from syncworker.filesystem.domain.repository.filesystem_repository import FilesystemRepository


SOUNDCLOUD_ID_PATTERN = re.compile(r"\[(?P<id>\d+)]")
INVALID_PLAYLIST_FILENAME_CHARS = str.maketrans("", "", '/\\?%*:|"<>')


class FilesystemDataRepository(FilesystemRepository):
    def __init__(self, music_dir: Path, playlists_dir: Path, archive_file: Path, client: FilesystemClient):
        self.music_dir = music_dir
        self.playlists_dir = playlists_dir
        self.archive_file = archive_file
        self.client = client

    def list_tracks(self) -> tuple[LocalTrack, ...]:
        tracks: list[LocalTrack] = []

        for entry in self.client.list_dir(self.music_dir):
            if not entry.is_file:
                continue

            track_id = self._extract_soundcloud_id(entry.path.name)
            if track_id is None:
                continue

            tracks.append(LocalTrack(soundcloud_id=track_id, path=entry.path))

        return tuple(tracks)

    def read_archive(self) -> tuple[ArchiveEntry, ...]:
        if not self.client.exists(self.archive_file):
            return ()

        entries: list[ArchiveEntry] = []
        for raw_line in self.client.read_lines(self.archive_file):
            entry = self._parse_archive_line(raw_line)
            if entry is not None:
                entries.append(entry)

        return tuple(entries)

    def remove_archive_entries(self, item_ids: set[str]) -> None:
        if not item_ids or not self.client.exists(self.archive_file):
            return

        removable_ids = {entry.item_id for entry in self.read_archive() if entry.item_id in item_ids}
        if not removable_ids:
            return

        lines: list[str] = []
        for raw_line in self.client.read_lines(self.archive_file, keepends=True):
            entry = self._parse_archive_line(raw_line)
            if entry is not None and entry.item_id in removable_ids:
                continue

            lines.append(raw_line)

        self.client.write_text(self.archive_file, "".join(lines))

    def delete_m3u_playlists(self) -> None:
        for entry in self.client.list_dir(self.playlists_dir):
            if entry.is_dir:
                self.client.delete_tree(entry.path)
                continue

            self.client.delete_file(entry.path)

    def write_m3u_playlist(self, title: str, track_paths: tuple[str, ...]) -> Path:
        self.client.ensure_dir(self.playlists_dir)
        playlist_file = self.playlists_dir / f"{self.sanitize_playlist_filename(title)}.m3u"
        lines = ["#EXTM3U"]
        lines.extend(f"../{track_path}" for track_path in track_paths)
        self.client.write_text(playlist_file, "\n".join(lines) + "\n")
        return playlist_file

    def delete_track(self, track: LocalTrack) -> None:
        self.client.delete_file(track.path, missing_ok=True)

    @staticmethod
    def sanitize_playlist_filename(title: str) -> str:
        clean_title = title.translate(INVALID_PLAYLIST_FILENAME_CHARS).lstrip(".-").strip()
        return clean_title or "unnamed_playlist"

    @staticmethod
    def _extract_soundcloud_id(filename: str) -> str | None:
        match = SOUNDCLOUD_ID_PATTERN.search(filename)
        if match is None:
            return None

        return match.group("id")

    @staticmethod
    def _parse_archive_line(raw_line: str) -> ArchiveEntry | None:
        line = raw_line.strip()
        if not line:
            return None

        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            return None

        return ArchiveEntry(extractor=parts[0], item_id=parts[1], raw=line)
