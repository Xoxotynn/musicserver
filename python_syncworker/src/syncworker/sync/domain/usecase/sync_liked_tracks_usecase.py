from __future__ import annotations

from syncworker.navidrome.domain.repository.navidrome_repository import NavidromeRepository
from syncworker.navidrome.domain.usecase.clear_navidrome_likes_usecase import ClearNavidromeLikesUseCase
from syncworker.sync.domain.models.library_models import MusicLibrary


class SyncLikedTracksUseCase:
    def __init__(
        self,
        navidrome_repository: NavidromeRepository,
        clear_likes_usecase: ClearNavidromeLikesUseCase,
    ):
        self.navidrome_repository = navidrome_repository
        self.clear_likes_usecase = clear_likes_usecase

    def execute(self, library: MusicLibrary) -> None:
        self.clear_likes_usecase.execute()

        for track in library.liked_tracks:
            self.navidrome_repository.star(track.navidrome_id)
