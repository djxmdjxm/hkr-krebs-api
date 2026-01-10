from datetime import date, datetime

from pydantic import BaseModel

from ...krebs_db.enums.target_region_version import TargetRegionVersion
from ...krebs_db.enums.laterality_type import LateralityType
from ...krebs_db.enums.date_accuracy_type import DateAccuracyType


class RadiotherapySessionDto(BaseModel):
    tumor_radiotherapy_id: int
    start_date: date
    start_date_accuracy: DateAccuracyType | None = None
    duration_days: int | None = None
    target_area: TargetRegionVersion | None = None
    laterality: LateralityType | None = None
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
