from datetime import date, datetime
from typing import Any

from pydantic import BaseModel

from ...krebs_db.enums.gender_type import GenderType
from ...krebs_db.enums.date_accuracy_type import DateAccuracyType
from ...krebs_db.enums.register_type import RegisterType


class PatientReportDto(BaseModel):
    patient_id: str
    gender: GenderType
    date_of_birth: date
    date_of_birth_accuracy: DateAccuracyType | None = None
    is_deceased: bool
    vital_status_date: date | None = None
    vital_status_date_accuracy: DateAccuracyType | None = None
    death_causes: list[dict[str, Any]] | None = None
    register: RegisterType
    reported_at: date
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True