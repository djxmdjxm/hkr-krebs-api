# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from fastapi import APIRouter

from sqlalchemy import select

from .dto import ReportDto
from ..main_db import Session, ReportImport
from ..main_db.enums.report_import_status import ReportImportStatus
from ..import_queue import trigger_report_import

from ..common.logging import getLogger

logger = getLogger('report')

router = APIRouter(
    prefix="/report",
    tags=["report"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)

@router.post("")
async def upload_report(data: ReportDto):
    with Session() as session:
        report_import = ReportImport(
            status          = ReportImportStatus.Created,
            type            = data.type,
            file            = data.file,
            additional_info = None
        )
        session.add(report_import)
        session.commit()

        await trigger_report_import(report_import.uid)

        return {"uid": report_import.uid}


@router.get("/{uid}")
async def get_report(uid: str):
    with Session() as session:
        query = select(
            ReportImport.uid,
            ReportImport.status,
            ReportImport.type,
            ReportImport.additional_info,
            ReportImport.updated_at,
            ReportImport.created_at,
        ).where(ReportImport.uid == uid)
        result = session.execute(query)
        
        entity = result.mappings().one_or_none()
        
        return entity
