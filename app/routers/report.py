# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

import os
import uuid

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from sqlalchemy import select, func

from ..main_db import Session, ReportImport
from ..main_db.enums.report_import_status import ReportImportStatus
from ..main_db.enums.report_type import ReportType
from ..import_queue import trigger_report_import
from ..krebs_db import Session as KrebsSession
from ..krebs_db.patient_report import PatientReport
from ..krebs_db.tumor_report import TumorReport

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


@router.get('/{uid}/summary')
async def get_report_summary(uid: str):
    # Resolve import timestamp from main_db to scope krebs_db queries to this batch.
    with Session() as session:
        row = session.execute(
            select(ReportImport.created_at).where(ReportImport.uid == uid)
        ).one_or_none()

    if row is None:
        raise HTTPException(status_code=404, detail='Report not found')

    import_created_at = row[0]

    with KrebsSession() as session:
        # One row per distinct patient_id — deduplicated basis for all patient stats.
        # GROUP BY patient_id, take earliest date_of_birth per patient.
        distinct_patients_q = (
            select(
                PatientReport.patient_id,
                func.min(PatientReport.date_of_birth).label('date_of_birth'),
            )
            .where(PatientReport.created_at >= import_created_at)
            .group_by(PatientReport.patient_id)
            .subquery()
        )

        # Patient count (distinct) + age stats via PostgreSQL percentile aggregate.
        age_expr = func.date_part(
            'year', func.age(func.now(), distinct_patients_q.c.date_of_birth)
        )
        stats = session.execute(
            select(
                func.count().label('patient_count'),
                func.percentile_cont(0.5).within_group(age_expr).label('median_age'),
                func.min(age_expr).label('min_age'),
                func.max(age_expr).label('max_age'),
            ).select_from(distinct_patients_q)
        ).one()

        # Distinct tumor_id (Fall-ID) count + diagnosis year range for this batch.
        tumor_stats = session.execute(
            select(
                func.count(func.distinct(TumorReport.tumor_id)).label('tumor_count'),
                func.min(func.extract('year', TumorReport.diagnosis_date)).label('min_year'),
                func.max(func.extract('year', TumorReport.diagnosis_date)).label('max_year'),
            ).join(PatientReport, TumorReport.patient_report_id == PatientReport.id)
            .where(PatientReport.created_at >= import_created_at)
        ).one()

    def _int(v):
        return int(v) if v is not None else None

    return {
        'patient_count':      _int(stats.patient_count),
        'median_age':         _int(stats.median_age),
        'min_age':            _int(stats.min_age),
        'max_age':            _int(stats.max_age),
        'tumor_count':        _int(tumor_stats.tumor_count),
        'min_diagnosis_year': _int(tumor_stats.min_year),
        'max_diagnosis_year': _int(tumor_stats.max_year),
    }
