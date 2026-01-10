from datetime import date, datetime
from typing import Any

from pydantic import BaseModel

from ...krebs_db.enums.systemic_therapy_intent_type import SystemicTherapyIntentType
from ...krebs_db.enums.systemic_therapy_type import SystemicTherapyType
from ...krebs_db.enums.surgery_relation_type import SurgeryRelationType
from ...krebs_db.enums.date_accuracy_type import DateAccuracyType


class TumorSystemicTherapyDto(BaseModel):
    tumor_report_id: int
    start_date: date
    start_date_accuracy: DateAccuracyType | None = None
    duration_days: int | None = None
    intent: SystemicTherapyIntentType
    surgery_relation: SurgeryRelationType
    type: SystemicTherapyType
    protocol: dict[str, Any] | None = None
    drugs: list[dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
