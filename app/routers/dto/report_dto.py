from pydantic import BaseModel

from ...main_db.enums.report_type import ReportType

class ReportDto(BaseModel):
    type: ReportType
    file: str  # base64-encoded string