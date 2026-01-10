from datetime import date, datetime
from typing import Any

from pydantic import BaseModel

from ...krebs_db.enums.date_accuracy_type import DateAccuracyType
from ...krebs_db.enums.diagnostic_certainty_type import DiagnosticCertaintyType
from ...krebs_db.enums.laterality_type import LateralityType


class TumorReportDto(BaseModel):
    patient_report_id: int
    tumor_id: str
    diagnosis_date: date
    diagnosis_date_accuracy: DateAccuracyType
    incidence_location: str
    icd: dict[str, Any]
    topographie: dict[str, Any] | None = None
    diagnostic_certainty: DiagnosticCertaintyType
    c_tnm_id: int | None = None
    p_tnm_id: int | None = None
    distant_metastasis: list[dict[str, Any]] | None = None
    other_classification: list[dict[str, Any]] | None = None
    laterality: LateralityType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
