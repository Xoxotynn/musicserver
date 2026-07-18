from __future__ import annotations

from syncworker.navidrome.domain.usecase.scan_navidrome_usecase import ScanNavidromeUseCase
from syncworker.soundcloud.domain.usecase.download_soundcloud_tracks_usecase import DownloadSoundCloudTracksUseCase
from syncworker.sync.domain.usecase.build_music_library_usecase import BuildMusicLibraryUseCase
from syncworker.sync.domain.usecase.remove_unliked_tracks_usecase import RemoveUnlikedTracksUseCase
from syncworker.sync.domain.usecase.sync_liked_tracks_usecase import SyncLikedTracksUseCase
from syncworker.sync.domain.usecase.sync_playlists_usecase import SyncPlaylistsUseCase


class FullSyncScenario:
    def __init__(
        self,
        download_soundcloud_tracks_usecase: DownloadSoundCloudTracksUseCase,
        scan_navidrome_usecase: ScanNavidromeUseCase,
        build_music_library_usecase: BuildMusicLibraryUseCase,
        remove_unliked_tracks_usecase: RemoveUnlikedTracksUseCase,
        sync_liked_tracks_usecase: SyncLikedTracksUseCase,
        sync_playlists_usecase: SyncPlaylistsUseCase,
    ):
        self.download_soundcloud_tracks_usecase = download_soundcloud_tracks_usecase
        self.scan_navidrome_usecase = scan_navidrome_usecase
        self.build_music_library_usecase = build_music_library_usecase
        self.remove_unliked_tracks_usecase = remove_unliked_tracks_usecase
        self.sync_liked_tracks_usecase = sync_liked_tracks_usecase
        self.sync_playlists_usecase = sync_playlists_usecase

    def execute(self) -> None:
        self.download_soundcloud_tracks_usecase.execute()

        self.scan_navidrome_usecase.execute()

        library = self.build_music_library_usecase.execute()
        self.remove_unliked_tracks_usecase.execute(library)

        self.scan_navidrome_usecase.execute()

        self.sync_liked_tracks_usecase.execute(library)
        self.sync_playlists_usecase.execute(library)

        self.scan_navidrome_usecase.execute()
