# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.radiotherapy_session_brachytherapy import RadiotherapySessionBrachytherapy
from .dto.radiotherapy_session_brachytherapy_dto import RadiotherapySessionBrachytherapyDto

logger = getLogger("radiotherapy_session_brachytherapy")

router = APIRouter(
    prefix="/radiotherapy_session_brachytherapy",
    tags=["radiotherapy_session_brachytherapy"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[RadiotherapySessionBrachytherapyDto])
async def get_radiotherapy_session_brachytherapy():
    with Session() as session:
        query = select(RadiotherapySessionBrachytherapy)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s radiotherapy_session_brachytherapy records", len(records))

        return [RadiotherapySessionBrachytherapyDto.model_validate(record) for record in records]
