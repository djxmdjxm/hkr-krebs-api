# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_report_prostate import TumorReportProstate
from .dto.tumor_report_prostate_dto import TumorReportProstateDto

logger = getLogger("tumor_report_prostate")

router = APIRouter(
    prefix="/tumor_report_prostate",
    tags=["tumor_report_prostate"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorReportProstateDto])
async def get_tumor_report_prostate():
    with Session() as session:
        query = select(TumorReportProstate)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s tumor_report_prostate records", len(records))

        return [TumorReportProstateDto.model_validate(record) for record in records]
