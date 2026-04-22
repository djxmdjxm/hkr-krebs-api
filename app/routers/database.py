import os
import glob

from fastapi import APIRouter
from sqlalchemy import text, delete

from ..main_db import Session, ReportImport
from ..krebs_db import Session as KrebsSession

from ..common.logging import getLogger

logger = getLogger('database')

UPLOAD_DIR = '/data/uploads'

router = APIRouter(
    prefix='/database',
    tags=['database'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/reset')
async def reset_database():
    logger.info('Database reset requested')

    # 1. Truncate all krebs data — CASCADE removes all dependent child rows
    with KrebsSession() as session:
        session.execute(text('TRUNCATE TABLE patient_report CASCADE'))
        session.commit()

    # 2. Clear import history in main_db
    with Session() as session:
        session.execute(delete(ReportImport))
        session.commit()

    # 3. Delete uploaded XML files from shared volume
    removed = 0
    for f in glob.glob(f'{UPLOAD_DIR}/*.xml'):
        try:
            os.remove(f)
            removed += 1
        except OSError:
            pass

    logger.info(f'Database reset complete — {removed} XML files removed')
    return {'status': 'ok'}
