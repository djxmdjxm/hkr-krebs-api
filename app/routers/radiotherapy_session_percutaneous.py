# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.radiotherapy_session_percutaneous import RadiotherapySessionPercutaneous
from .dto.radiotherapy_session_percutaneous_dto import RadiotherapySessionPercutaneousDto

logger = getLogger("radiotherapy_session_percutaneous")

router = APIRouter(
    prefix="/radiotherapy_session_percutaneous",
    tags=["radiotherapy_session_percutaneous"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[RadiotherapySessionPercutaneousDto])
async def get_radiotherapy_session_percutaneous():
    with Session() as session:
        query = select(RadiotherapySessionPercutaneous)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s radiotherapy_session_percutaneous records", len(records))

        return [RadiotherapySessionPercutaneousDto.model_validate(record) for record in records]
