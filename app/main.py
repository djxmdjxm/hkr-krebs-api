from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    database,
    report,
    patient_report,
    tumor_report,
    tnm,
    tumor_histology,
    tumor_report_breast,
    tumor_report_colorectal,
    tumor_report_melanoma,
    tumor_report_prostate,
    tumor_radiotherapy,
    radiotherapy_session,
    radiotherapy_session_percutaneous,
    radiotherapy_session_brachytherapy,
    radiotherapy_session_metabolic,
    tumor_follow_up,
    tumor_surgery,
    tumor_systemic_therapy,
)

app = FastAPI(
  redirect_slashes=False
)

ROUTERS = [
    database,
    report,
    patient_report,
    tumor_report,
    tnm,
    tumor_histology,
    tumor_report_breast,
    tumor_report_colorectal,
    tumor_report_melanoma,
    tumor_report_prostate,
    tumor_radiotherapy,
    radiotherapy_session,
    radiotherapy_session_percutaneous,
    radiotherapy_session_brachytherapy,
    radiotherapy_session_metabolic,
    tumor_follow_up,
    tumor_surgery,
    tumor_systemic_therapy,
]

for module in ROUTERS:
    app.include_router(module.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def root():
  return {"message": "Krebs API says MOIN!"}
