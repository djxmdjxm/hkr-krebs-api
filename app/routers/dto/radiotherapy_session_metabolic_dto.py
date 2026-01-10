from datetime import datetime

from pydantic import BaseModel

from ...krebs_db.enums.radionuclide_therapy_type import RadionuclideTherapyType


class RadiotherapySessionMetabolicDto(BaseModel):
    radiotherapy_session_id: int
    type: RadionuclideTherapyType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
