# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_report_melanoma import TumorReportMelanoma
from .dto.tumor_report_melanoma_dto import TumorReportMelanomaDto

logger = getLogger("tumor_report_melanoma")

router = APIRouter(
    prefix="/tumor_report_melanoma",
    tags=["tumor_report_melanoma"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorReportMelanomaDto])
async def get_tumor_report_melanoma():
    with Session() as session:
        query = select(TumorReportMelanoma)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s tumor_report_melanoma records", len(records))

        return [TumorReportMelanomaDto.model_validate(record) for record in records]
