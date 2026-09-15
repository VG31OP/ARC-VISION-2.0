"""Run recording maintainer and cleanup."""

import logging
from multiprocessing.synchronize import Event as MpEvent

from arcvision.config import ArcVisionConfig
from arcvision.const import PROCESS_PRIORITY_MED
from arcvision.review.maintainer import ReviewSegmentMaintainer
from arcvision.util.process import ArcVisionProcess

logger = logging.getLogger(__name__)


class ReviewProcess(ArcVisionProcess):
    def __init__(self, config: ArcVisionConfig, stop_event: MpEvent) -> None:
        super().__init__(
            stop_event,
            PROCESS_PRIORITY_MED,
            name="arcvision.review_segment_manager",
            daemon=True,
        )
        self.config = config

    def run(self) -> None:
        self.pre_run_setup(self.config.logger)
        maintainer = ReviewSegmentMaintainer(
            self.config,
            self.stop_event,
        )
        maintainer.start()
