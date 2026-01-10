# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_radiotherapy import TumorRadiotherapy
from .dto.tumor_radiotherapy_dto import TumorRadiotherapyDto

logger = getLogger("tumor_radiotherapy")

router = APIRouter(
    prefix="/tumor_radiotherapy",
    tags=["tumor_radiotherapy"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorRadiotherapyDto])
async def get_tumor_radiotherapy():
    with Session() as session:
        query = select(TumorRadiotherapy)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s tumor_radiotherapy records", len(records))

        return [TumorRadiotherapyDto.model_validate(record) for record in records]
