from pydantic import Field

from arcvision.const import DEFAULT_DB_PATH

from .base import ArcVisionBaseModel

__all__ = ["DatabaseConfig"]


class DatabaseConfig(ArcVisionBaseModel):
    path: str = Field(
        default=DEFAULT_DB_PATH,
        title="Database path",
        description="Filesystem path where the Frigate SQLite database file will be stored.",
    )  # noqa: F821
