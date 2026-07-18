from __future__ import annotations

from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL  # type: ignore[import-untyped]

from syncworker.soundcloud.data.models.soundcloud_models import SoundCloudEntry, SoundCloudExtractResult


class SoundCloudClient:
    def download(self, url: str, music_dir: Path, archive_file: Path) -> int:
        options = {
            "ignoreerrors": True,
            "download_archive": str(archive_file),
            "format": "bestaudio/best",
            "outtmpl": str(music_dir / "[%(id)s] %(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredquality": "0",
                },
                {"key": "FFmpegMetadata"},
                {"key": "EmbedThumbnail"},
            ],
            "writethumbnail": True,
        }

        with YoutubeDL(options) as ydl:
            return ydl.download([url])

    def extract_flat(self, url: str) -> SoundCloudExtractResult:
        with YoutubeDL({"extract_flat": True, "quiet": True, "no_warnings": True}) as ydl:
            result = ydl.extract_info(url, download=False)

        if not isinstance(result, dict):
            raise RuntimeError(f"Invalid SoundCloud response for url: {url}")

        return SoundCloudExtractResult(entries=self._entries(result))

    @staticmethod
    def _entries(result: dict[str, Any]) -> tuple[SoundCloudEntry, ...]:
        entries = result.get("entries") or []
        if not isinstance(entries, list):
            return ()

        return tuple(
            SoundCloudEntry(
                id=SoundCloudClient._optional_str(entry.get("id")),
                url=SoundCloudClient._optional_str(entry.get("url")),
                title=SoundCloudClient._optional_str(entry.get("title")),
            )
            for entry in entries
            if isinstance(entry, dict)
        )

    @staticmethod
    def _optional_str(value: Any) -> str | None:
        if value is None:
            return None

        return str(value)
