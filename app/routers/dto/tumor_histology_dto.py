from datetime import datetime
from typing import Any

from pydantic import BaseModel

from ...krebs_db.enums.histology_grading_type import HistologyGradingType


class TumorHistologyDto(BaseModel):
    tumor_report_id: int
    morphology_icd: dict[str, Any]
    grading: HistologyGradingType
    lymph_nodes_examined: int | None = None
    lymph_nodes_affected: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
