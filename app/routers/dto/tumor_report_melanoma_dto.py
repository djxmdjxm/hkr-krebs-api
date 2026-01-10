from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TumorReportMelanomaDto(BaseModel):
    tumor_report_id: int
    tumor_thickness_mm: Decimal | None = None
    ldh: Decimal | None = None
    ulceration: bool | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
