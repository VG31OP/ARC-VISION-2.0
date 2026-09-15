from pydantic import Field

from .base import ArcVisionBaseModel

__all__ = ["TlsConfig"]


class TlsConfig(ArcVisionBaseModel):
    enabled: bool = Field(
        default=True,
        title="Enable TLS",
        description="Enable TLS for Frigate's web UI and API on the configured TLS port.",
    )
