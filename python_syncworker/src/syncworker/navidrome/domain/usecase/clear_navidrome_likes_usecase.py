from __future__ import annotations

from syncworker.navidrome.domain.repository.navidrome_repository import NavidromeRepository


class ClearNavidromeLikesUseCase:
    def __init__(self, navidrome_repository: NavidromeRepository):
        self.navidrome_repository = navidrome_repository

    def execute(self) -> None:
        starred = self.navidrome_repository.get_starred()
        self.navidrome_repository.unstar(starred.song_ids)
