# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_follow_up import TumorFollowUp
from .dto.tumor_follow_up_dto import TumorFollowUpDto

logger = getLogger("tumor_follow_up")

router = APIRouter(
    prefix="/tumor_follow_up",
    tags=["tumor_follow_up"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorFollowUpDto])
async def get_tumor_follow_up():
    with Session() as session:
        query = select(TumorFollowUp)
        result = session.execute(query)

        records = result.scalars().all()

        logger.info("Fetched %s tumor_follow_up records", len(records))

        return [TumorFollowUpDto.model_validate(record) for record in records]
