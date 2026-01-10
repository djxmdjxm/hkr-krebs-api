from datetime import datetime

from pydantic import BaseModel

from ...krebs_db.enums.menopausal_status_type import MenopausalStatusType
from ...krebs_db.enums.receptor_status_type import ReceptorStatusType


class TumorReportBreastDto(BaseModel):
    tumor_report_id: int
    menopause_status_at_diagnosis: MenopausalStatusType | None = None
    estrogen_receptor_status: ReceptorStatusType | None = None
    progesterone_receptor_status: ReceptorStatusType | None = None
    her2neu_status: ReceptorStatusType | None = None
    tumor_size_mm_invasive: int | None = None
    tumor_size_mm_dcis: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
