from datetime import datetime

from pydantic import BaseModel

from ...krebs_db.enums.brachytherapy_type import BrachytherapyType
from ...krebs_db.enums.brachytherapy_dose_rate_type import BrachytherapyDoseRateType


class RadiotherapySessionBrachytherapyDto(BaseModel):
    radiotherapy_session_id: int
    type: BrachytherapyType
    dose_rate: BrachytherapyDoseRateType | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
