# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.radiotherapy_session import RadiotherapySession
from .dto.radiotherapy_session_dto import RadiotherapySessionDto

logger = getLogger("radiotherapy_session")

router = APIRouter(
    prefix="/radiotherapy_session",
    tags=["radiotherapy_session"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[RadiotherapySessionDto])
async def get_radiotherapy_sessions():
    with Session() as session:
        query = select(RadiotherapySession)
        result = session.execute(query)

        sessions = result.scalars().all()

        logger.info("Fetched %s radiotherapy_session records", len(sessions))

        return [RadiotherapySessionDto.model_validate(session) for session in sessions]
