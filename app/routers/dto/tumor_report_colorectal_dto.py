from datetime import datetime

from pydantic import BaseModel

from ...krebs_db.enums.ras_mutation_type import RasMutationType


class TumorReportColorectalDto(BaseModel):
    tumor_report_id: int
    ras_mutation: RasMutationType | None = None
    rectum_distance_anocutaneous_line_cm: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
