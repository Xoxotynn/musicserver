from __future__ import annotations

import time

from syncworker.navidrome.domain.repository.navidrome_repository import NavidromeRepository


class ScanNavidromeUseCase:
    def __init__(
        self,
        navidrome_repository: NavidromeRepository,
        poll_interval_seconds: float = 1,
    ):
        self.navidrome_repository = navidrome_repository
        self.poll_interval_seconds = poll_interval_seconds

    def execute(self) -> None:
        self.navidrome_repository.start_scan()

        while self.navidrome_repository.get_scan_status().scanning:
            time.sleep(self.poll_interval_seconds)
