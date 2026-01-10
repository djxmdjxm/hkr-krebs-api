# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.radiotherapy_session_metabolic import RadiotherapySessionMetabolic
from .dto.radiotherapy_session_metabolic_dto import RadiotherapySessionMetabolicDto

logger = getLogger("radiotherapy_session_metabolic")

router = APIRouter(
    prefix="/radiotherapy_session_metabolic",
    tags=["radiotherapy_session_metabolic"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[RadiotherapySessionMetabolicDto])
async def get_radiotherapy_session_metabolic():
    with Session() as session:
        query = select(RadiotherapySessionMetabolic)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s radiotherapy_session_metabolic records", len(records))

        return [RadiotherapySessionMetabolicDto.model_validate(record) for record in records]
