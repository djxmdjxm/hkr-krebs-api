from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from ...krebs_db.enums.gleason_score_result_type import GleasonScoreResultType
from ...krebs_db.enums.gleason_score_reason_type import GleasonScoreReasonType
from ...krebs_db.enums.date_accuracy_type import DateAccuracyType
from ...krebs_db.enums.gleason_grade_type import GleasonGradeType


class TumorReportProstateDto(BaseModel):
    tumor_report_id: int
    gleason_primary_grade: GleasonGradeType | None = None
    gleason_secondary_grade: GleasonGradeType | None = None
    gleason_score_result: GleasonScoreResultType | None = None
    gleason_score_reason: GleasonScoreReasonType | None = None
    psa: Decimal | None = None
    psa_date: date | None = None
    psa_date_accuracy: DateAccuracyType | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
