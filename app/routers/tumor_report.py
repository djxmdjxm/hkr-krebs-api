# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_report import TumorReport
from .dto.tumor_report_dto import TumorReportDto

logger = getLogger('tumor_report')

router = APIRouter(
    prefix="/tumor_report",
    tags=["tumor_report"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorReportDto])
async def get_tumor_reports():
    with Session() as session:
        query = select(TumorReport)
        result = session.execute(query)

        reports = result.scalars().all()

        logger.info("Fetched %s tumor reports", len(reports))

        return [TumorReportDto.model_validate(report) for report in reports]
