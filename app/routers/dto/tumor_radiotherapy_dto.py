from datetime import datetime

from pydantic import BaseModel

from ...krebs_db.enums.radiotherapy_intent_type import RadiotherapyIntentType
from ...krebs_db.enums.surgery_relation_type import SurgeryRelationType


class TumorRadiotherapyDto(BaseModel):
    tumor_report_id: int
    intent: RadiotherapyIntentType | None = None
    surgery_relation: SurgeryRelationType | None = None
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
