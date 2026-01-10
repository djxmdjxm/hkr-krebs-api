from datetime import date, datetime
from typing import Any

from pydantic import BaseModel

from ...krebs_db.enums.surgery_intent_type import SurgeryIntentType
from ...krebs_db.enums.residual_status_type import ResidualStatusType
from ...krebs_db.enums.date_accuracy_type import DateAccuracyType


class TumorSurgeryDto(BaseModel):
    tumor_report_id: int
    intent: SurgeryIntentType
    date: date
    date_accuracy: DateAccuracyType | None = None
    operations: list[dict[str, Any]]
    local_residual_status: ResidualStatusType | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
