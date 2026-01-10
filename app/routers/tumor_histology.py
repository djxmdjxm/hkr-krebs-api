# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter
from sqlalchemy import select

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.tumor_histology import TumorHistology
from .dto.tumor_histology_dto import TumorHistologyDto

logger = getLogger("tumor_histology")

router = APIRouter(
    prefix="/tumor_histology",
    tags=["tumor_histology"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)


@router.get("", response_model=list[TumorHistologyDto])
async def get_tumor_histologies():
    with Session() as session:
        query = select(TumorHistology)
        result = session.execute(query)

        histologies = result.scalars().all()

        logger.info("Fetched %s tumor histologies", len(histologies))

        return [TumorHistologyDto.model_validate(histology) for histology in histologies]
