# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_report_colorectal import TumorReportColorectal
from .dto.tumor_report_colorectal_dto import TumorReportColorectalDto

logger = getLogger("tumor_report_colorectal")

router = APIRouter(
    prefix="/tumor_report_colorectal",
    tags=["tumor_report_colorectal"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorReportColorectalDto])
async def get_tumor_report_colorectal():
    with Session() as session:
        query = select(TumorReportColorectal)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s tumor_report_colorectal records", len(records))

        return [TumorReportColorectalDto.model_validate(record) for record in records]
