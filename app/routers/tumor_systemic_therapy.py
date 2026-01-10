# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_systemic_therapy import TumorSystemicTherapy
from .dto.tumor_systemic_therapy_dto import TumorSystemicTherapyDto

logger = getLogger("tumor_systemic_therapy")

router = APIRouter(
    prefix="/tumor_systemic_therapy",
    tags=["tumor_systemic_therapy"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorSystemicTherapyDto])
async def get_tumor_systemic_therapy():
    with Session() as session:
        query = select(TumorSystemicTherapy)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s tumor_systemic_therapy records", len(records))

        return [TumorSystemicTherapyDto.model_validate(record) for record in records]
