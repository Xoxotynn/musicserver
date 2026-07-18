from __future__ import annotations

from syncworker.config import Config
from syncworker.filesystem.data.client.filesystem_client import FilesystemClient
from syncworker.filesystem.data.repository.filesystem_data_repository import FilesystemDataRepository
from syncworker.navidrome.data.client.navidrome_client import NavidromeClient
from syncworker.navidrome.data.repository.navidrome_data_repository import NavidromeDataRepository
from syncworker.navidrome.domain.usecase.clear_navidrome_likes_usecase import ClearNavidromeLikesUseCase
from syncworker.navidrome.domain.usecase.scan_navidrome_usecase import ScanNavidromeUseCase
from syncworker.soundcloud.data.client.soundcloud_client import SoundCloudClient
from syncworker.soundcloud.data.repository.soundcloud_data_repository import SoundCloudDataRepository
from syncworker.soundcloud.domain.usecase.download_soundcloud_tracks_usecase import DownloadSoundCloudTracksUseCase
from syncworker.sync.domain.scenario.full_sync_scenario import FullSyncScenario
from syncworker.sync.domain.usecase.build_music_library_usecase import BuildMusicLibraryUseCase
from syncworker.sync.domain.usecase.remove_unliked_tracks_usecase import RemoveUnlikedTracksUseCase
from syncworker.sync.domain.usecase.sync_liked_tracks_usecase import SyncLikedTracksUseCase
from syncworker.sync.domain.usecase.sync_playlists_usecase import SyncPlaylistsUseCase


def create_full_sync_scenario(config: Config) -> FullSyncScenario:
    soundcloud_repository = SoundCloudDataRepository(
        url=config.soundcloud_url,
        client=SoundCloudClient(),
    )
    navidrome_repository = NavidromeDataRepository(
        client=NavidromeClient(
            base_url=config.navidrome_base_url,
            user=config.navidrome_user,
            password=config.navidrome_password,
        )
    )
    filesystem_repository = FilesystemDataRepository(
        music_dir=config.music_dir,
        playlists_dir=config.playlists_dir,
        archive_file=config.archive_file,
        client=FilesystemClient(),
    )

    clear_likes_usecase = ClearNavidromeLikesUseCase(navidrome_repository)

    return FullSyncScenario(
        download_soundcloud_tracks_usecase=DownloadSoundCloudTracksUseCase(
            soundcloud_repository=soundcloud_repository,
            music_dir=config.music_dir,
            archive_file=config.archive_file,
        ),
        scan_navidrome_usecase=ScanNavidromeUseCase(navidrome_repository),
        build_music_library_usecase=BuildMusicLibraryUseCase(
            soundcloud_repository=soundcloud_repository,
            navidrome_repository=navidrome_repository,
        ),
        remove_unliked_tracks_usecase=RemoveUnlikedTracksUseCase(filesystem_repository),
        sync_liked_tracks_usecase=SyncLikedTracksUseCase(
            navidrome_repository=navidrome_repository,
            clear_likes_usecase=clear_likes_usecase,
        ),
        sync_playlists_usecase=SyncPlaylistsUseCase(filesystem_repository),
    )
