from __future__ import annotations

from typing import Protocol

from syncworker.navidrome.domain.models.navidrome_models import NavidromeSong, ScanStatus, StarredItems


class NavidromeRepository(Protocol):
    def start_scan(self) -> None:
        ...

    def get_scan_status(self) -> ScanStatus:
        ...

    def get_starred(self) -> StarredItems:
        ...

    def find_song_by_soundcloud_id(self, soundcloud_id: str) -> NavidromeSong | None:
        ...

    def find_songs_by_soundcloud_ids(self, soundcloud_ids: tuple[str, ...]) -> tuple[NavidromeSong, ...]:
        ...

    def star(self, item_id: str) -> None:
        ...

    def unstar(self, item_ids: tuple[str, ...]) -> None:
        ...
