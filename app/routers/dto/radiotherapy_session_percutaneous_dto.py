from datetime import datetime

from pydantic import BaseModel

from ...krebs_db.enums.chemoradio_type import ChemoradioType


class RadiotherapySessionPercutaneousDto(BaseModel):
    radiotherapy_session_id: int
    chemoradio: ChemoradioType | None = None
    stereotactic: bool
    respiratory_gated: bool
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
