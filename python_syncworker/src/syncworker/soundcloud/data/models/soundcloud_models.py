from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SoundCloudEntry:
    id: str | None
    url: str | None
    title: str | None


@dataclass(frozen=True)
class SoundCloudExtractResult:
    entries: tuple[SoundCloudEntry, ...]
