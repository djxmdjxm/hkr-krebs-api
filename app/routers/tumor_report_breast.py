# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_report_breast import TumorReportBreast
from .dto.tumor_report_breast_dto import TumorReportBreastDto

logger = getLogger("tumor_report_breast")

router = APIRouter(
    prefix="/tumor_report_breast",
    tags=["tumor_report_breast"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorReportBreastDto])
async def get_tumor_report_breast():
    with Session() as session:
        query = select(TumorReportBreast)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s tumor_report_breast records", len(records))

        return [TumorReportBreastDto.model_validate(record) for record in records]
