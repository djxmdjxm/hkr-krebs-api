# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_surgery import TumorSurgery
from .dto.tumor_surgery_dto import TumorSurgeryDto

logger = getLogger("tumor_surgery")

router = APIRouter(
    prefix="/tumor_surgery",
    tags=["tumor_surgery"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorSurgeryDto])
async def get_tumor_surgeries():
    with Session() as session:
        query = select(TumorSurgery)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s tumor_surgery records", len(records))

        return [TumorSurgeryDto.model_validate(record) for record in records]
