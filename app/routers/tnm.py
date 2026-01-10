# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tnm import TNM
from .dto.tnm_dto import TnmDto

logger = getLogger("tnm")

router = APIRouter(
    prefix="/tnm",
    tags=["tnm"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TnmDto])
async def get_tnm():
    with Session() as session:
        records = session.execute(select(TNM)).scalars().all()

        dtos = [TnmDto.model_validate(record) for record in records]

        logger.info("Fetched %s TNM records", len(dtos))

        return dtos
