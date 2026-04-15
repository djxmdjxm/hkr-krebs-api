# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

import os
import uuid

from fastapi import APIRouter, UploadFile, File, Form
from sqlalchemy import select

from ..main_db import Session, ReportImport
from ..main_db.enums.report_import_status import ReportImportStatus
from ..main_db.enums.report_type import ReportType
from ..import_queue import trigger_report_import

from ..common.logging import getLogger

logger = getLogger('report')

# Directory where uploaded XML files are stored temporarily until the import-worker
# processes them. Mounted as a shared Docker volume between krebs-api and import-worker.
UPLOAD_DIR = '/data/uploads'

router = APIRouter(
    prefix='/report',
    tags=['report'],
    dependencies=[],
    responses={
        404: {'description': 'Not found'}
    },
)

@router.post('')
async def upload_report(
    type: ReportType = Form(...),   # XML format/version, e.g. XML:oBDS_3.0.0.8a_RKI
    file: UploadFile = File(...)    # the XML file as multipart upload
):
    # Generate a unique ID for this import job — used as filename on the shared volume
    file_uid = str(uuid.uuid4())
    file_path = f'{UPLOAD_DIR}/{file_uid}.xml'

    # Ensure upload directory exists (volume may not have been written to yet)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Write file chunk-by-chunk to avoid loading 100+ MB into RAM at once.
    # Hamburg alone sends >100 MB per delivery — await file.read() would OOM.
    with open(file_path, 'wb') as f:
        while chunk := await file.read(1024 * 1024):  # 1 MB per chunk
            f.write(chunk)

    logger.info(f'file written to {file_path}')

    with Session() as session:
        report_import = ReportImport(
            status          = ReportImportStatus.Created,
            type            = type,
            file            = file_path,   # store path, not base64 content
            additional_info = None
        )
        session.add(report_import)
        session.commit()

        await trigger_report_import(report_import.uid)

        return {'uid': report_import.uid}


@router.get('/{uid}')
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
