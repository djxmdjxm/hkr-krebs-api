from datetime import date, datetime
from typing import Any

from pydantic import BaseModel

from ...krebs_db.enums.overall_tumor_status_type import OverallTumorStatusType
from ...krebs_db.enums.local_tumor_status_type import LocalTumorStatusType
from ...krebs_db.enums.lymph_node_tumor_status_type import LymphNodeTumorStatusType
from ...krebs_db.enums.distant_metastasis_tumor_status_type import DistantMetastasisTumorStatusType


class TumorFollowUpDto(BaseModel):
    tumor_report_id: int
    tnm_id: int | None = None
    other_classification: list[dict[str, Any]] | None = None
    date: date
    date_accuracy: str
    overall_tumor_status: OverallTumorStatusType
    local_tumor_status: LocalTumorStatusType | None = None
    lymph_node_tumor_status: LymphNodeTumorStatusType | None = None
    distant_metastasis_tumor_status: DistantMetastasisTumorStatusType | None = None
    distant_metastasis: list[dict[str, Any]] | None = None
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
