from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LinkIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    expires_in_days: int | None = Field(
        default=None, ge=1, le=365
    )


class LinkOut(BaseModel):
    code: str
    short_url: str
    url: str
    expires_at: datetime | None


class Stats(BaseModel):
    code: str
    url: str
    clicks: int
    pending: int
