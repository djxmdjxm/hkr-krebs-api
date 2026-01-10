# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.



from typing import Any, List

from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import aliased

from ..common.logging import getLogger
from ..krebs_db import Session
from ..krebs_db.patient_report import PatientReport
from ..krebs_db.tumor_report import TumorReport
from ..krebs_db.tnm import TNM
from ..krebs_db.tumor_histology import TumorHistology
from ..krebs_db.tumor_report_breast import TumorReportBreast
from ..krebs_db.tumor_report_colorectal import TumorReportColorectal
from ..krebs_db.tumor_report_melanoma import TumorReportMelanoma
from ..krebs_db.tumor_report_prostate import TumorReportProstate
from ..krebs_db.tumor_radiotherapy import TumorRadiotherapy
from ..krebs_db.radiotherapy_session import RadiotherapySession
from ..krebs_db.radiotherapy_session_percutaneous import RadiotherapySessionPercutaneous
from ..krebs_db.radiotherapy_session_brachytherapy import RadiotherapySessionBrachytherapy
from ..krebs_db.radiotherapy_session_metabolic import RadiotherapySessionMetabolic
from ..krebs_db.tumor_follow_up import TumorFollowUp
from ..krebs_db.tumor_surgery import TumorSurgery
from ..krebs_db.tumor_systemic_therapy import TumorSystemicTherapy
from .dto.patient_report_dto import PatientReportDto

logger = getLogger('report')

router = APIRouter(
    prefix="/patient_report",
    tags=["patient_report"],
    dependencies=[],
    responses={
        404: {"description": "Not found"}
    },
)

@router.get("", response_model=list[PatientReportDto])
async def get_patient_report():
    with Session() as session:
        query = select(PatientReport)
        result = session.execute(query)

        reports = result.scalars().all()

        return [PatientReportDto.model_validate(report) for report in reports]


@router.get("/flat")
async def get_patient_report_flat() -> List[dict[str, Any]]:
    with Session() as session:
        c_tnm_alias = aliased(TNM)
        p_tnm_alias = aliased(TNM)
        follow_up_tnm_alias = aliased(TNM)

        query = (
            select(
                PatientReport.id.label("patient_report_id"),
                PatientReport.patient_id.label("patient_report_patient_id"),
                PatientReport.gender.label("patient_report_gender"),
                PatientReport.date_of_birth.label("patient_report_date_of_birth"),
                PatientReport.date_of_birth_accuracy.label("patient_report_date_of_birth_accuracy"),
                PatientReport.is_deceased.label("patient_report_is_deceased"),
                PatientReport.vital_status_date.label("patient_report_vital_status_date"),
                PatientReport.vital_status_date_accuracy.label("patient_report_vital_status_date_accuracy"),
                PatientReport.death_causes.label("patient_report_death_causes"),
                PatientReport.register.label("patient_report_register"),
                PatientReport.reported_at.label("patient_report_reported_at"),
                PatientReport.updated_at.label("patient_report_updated_at"),
                PatientReport.created_at.label("patient_report_created_at"),

                TumorReport.id.label("tumor_report_id"),
                TumorReport.tumor_id.label("tumor_report_tumor_id"),
                TumorReport.diagnosis_date.label("tumor_report_diagnosis_date"),
                TumorReport.diagnosis_date_accuracy.label("tumor_report_diagnosis_date_accuracy"),
                TumorReport.incidence_location.label("tumor_report_incidence_location"),
                TumorReport.icd.label("tumor_report_icd"),
                TumorReport.topographie.label("tumor_report_topographie"),
                TumorReport.diagnostic_certainty.label("tumor_report_diagnostic_certainty"),
                TumorReport.distant_metastasis.label("tumor_report_distant_metastasis"),
                TumorReport.other_classification.label("tumor_report_other_classification"),
                TumorReport.laterality.label("tumor_report_laterality"),
                TumorReport.created_at.label("tumor_report_created_at"),
                TumorReport.updated_at.label("tumor_report_updated_at"),

                c_tnm_alias.id.label("tumor_report_c_tnm_id"),
                c_tnm_alias.version.label("tumor_report_c_tnm_version"),
                c_tnm_alias.y_symbol.label("tumor_report_c_tnm_y_symbol"),
                c_tnm_alias.r_symbol.label("tumor_report_c_tnm_r_symbol"),
                c_tnm_alias.a_symbol.label("tumor_report_c_tnm_a_symbol"),
                c_tnm_alias.t_prefix.label("tumor_report_c_tnm_t_prefix"),
                c_tnm_alias.t.label("tumor_report_c_tnm_t"),
                c_tnm_alias.m_symbol.label("tumor_report_c_tnm_m_symbol"),
                c_tnm_alias.n_prefix.label("tumor_report_c_tnm_n_prefix"),
                c_tnm_alias.n.label("tumor_report_c_tnm_n"),
                c_tnm_alias.m_prefix.label("tumor_report_c_tnm_m_prefix"),
                c_tnm_alias.m.label("tumor_report_c_tnm_m"),
                c_tnm_alias.l.label("tumor_report_c_tnm_l"),
                c_tnm_alias.v.label("tumor_report_c_tnm_v"),
                c_tnm_alias.pn.label("tumor_report_c_tnm_pn"),
                c_tnm_alias.s.label("tumor_report_c_tnm_s"),
                c_tnm_alias.uicc_stage.label("tumor_report_c_tnm_uicc_stage"),
                c_tnm_alias.created_at.label("tumor_report_c_tnm_created_at"),
                c_tnm_alias.updated_at.label("tumor_report_c_tnm_updated_at"),

                p_tnm_alias.id.label("tumor_report_p_tnm_id"),
                p_tnm_alias.version.label("tumor_report_p_tnm_version"),
                p_tnm_alias.y_symbol.label("tumor_report_p_tnm_y_symbol"),
                p_tnm_alias.r_symbol.label("tumor_report_p_tnm_r_symbol"),
                p_tnm_alias.a_symbol.label("tumor_report_p_tnm_a_symbol"),
                p_tnm_alias.t_prefix.label("tumor_report_p_tnm_t_prefix"),
                p_tnm_alias.t.label("tumor_report_p_tnm_t"),
                p_tnm_alias.m_symbol.label("tumor_report_p_tnm_m_symbol"),
                p_tnm_alias.n_prefix.label("tumor_report_p_tnm_n_prefix"),
                p_tnm_alias.n.label("tumor_report_p_tnm_n"),
                p_tnm_alias.m_prefix.label("tumor_report_p_tnm_m_prefix"),
                p_tnm_alias.m.label("tumor_report_p_tnm_m"),
                p_tnm_alias.l.label("tumor_report_p_tnm_l"),
                p_tnm_alias.v.label("tumor_report_p_tnm_v"),
                p_tnm_alias.pn.label("tumor_report_p_tnm_pn"),
                p_tnm_alias.s.label("tumor_report_p_tnm_s"),
                p_tnm_alias.uicc_stage.label("tumor_report_p_tnm_uicc_stage"),
                p_tnm_alias.created_at.label("tumor_report_p_tnm_created_at"),
                p_tnm_alias.updated_at.label("tumor_report_p_tnm_updated_at"),

                TumorHistology.morphology_icd.label("tumor_histology_morphology_icd"),
                TumorHistology.grading.label("tumor_histology_grading"),
                TumorHistology.lymph_nodes_examined.label("tumor_histology_lymph_nodes_examined"),
                TumorHistology.lymph_nodes_affected.label("tumor_histology_lymph_nodes_affected"),
                TumorHistology.created_at.label("tumor_histology_created_at"),
                TumorHistology.updated_at.label("tumor_histology_updated_at"),

                TumorReportBreast.menopause_status_at_diagnosis.label("tumor_report_breast_menopause_status_at_diagnosis"),
                TumorReportBreast.estrogen_receptor_status.label("tumor_report_breast_estrogen_receptor_status"),
                TumorReportBreast.progesterone_receptor_status.label("tumor_report_breast_progesterone_receptor_status"),
                TumorReportBreast.her2neu_status.label("tumor_report_breast_her2neu_status"),
                TumorReportBreast.tumor_size_mm_invasive.label("tumor_report_breast_tumor_size_mm_invasive"),
                TumorReportBreast.tumor_size_mm_dcis.label("tumor_report_breast_tumor_size_mm_dcis"),
                TumorReportBreast.created_at.label("tumor_report_breast_created_at"),
                TumorReportBreast.updated_at.label("tumor_report_breast_updated_at"),

                TumorReportColorectal.ras_mutation.label("tumor_report_colorectal_ras_mutation"),
                TumorReportColorectal.rectum_distance_anocutaneous_line_cm.label("tumor_report_colorectal_rectum_distance_anocutaneous_line_cm"),
                TumorReportColorectal.created_at.label("tumor_report_colorectal_created_at"),
                TumorReportColorectal.updated_at.label("tumor_report_colorectal_updated_at"),

                TumorReportMelanoma.tumor_thickness_mm.label("tumor_report_melanoma_tumor_thickness_mm"),
                TumorReportMelanoma.ldh.label("tumor_report_melanoma_ldh"),
                TumorReportMelanoma.ulceration.label("tumor_report_melanoma_ulceration"),
                TumorReportMelanoma.created_at.label("tumor_report_melanoma_created_at"),
                TumorReportMelanoma.updated_at.label("tumor_report_melanoma_updated_at"),

                TumorReportProstate.gleason_primary_grade.label("tumor_report_prostate_gleason_primary_grade"),
                TumorReportProstate.gleason_secondary_grade.label("tumor_report_prostate_gleason_secondary_grade"),
                TumorReportProstate.gleason_score_result.label("tumor_report_prostate_gleason_score_result"),
                TumorReportProstate.gleason_score_reason.label("tumor_report_prostate_gleason_score_reason"),
                TumorReportProstate.psa.label("tumor_report_prostate_psa"),
                TumorReportProstate.psa_date.label("tumor_report_prostate_psa_date"),
                TumorReportProstate.psa_date_accuracy.label("tumor_report_prostate_psa_date_accuracy"),
                TumorReportProstate.created_at.label("tumor_report_prostate_created_at"),
                TumorReportProstate.updated_at.label("tumor_report_prostate_updated_at"),

                TumorRadiotherapy.id.label("tumor_radiotherapy_id"),
                TumorRadiotherapy.intent.label("tumor_radiotherapy_intent"),
                TumorRadiotherapy.surgery_relation.label("tumor_radiotherapy_surgery_relation"),
                TumorRadiotherapy.updated_at.label("tumor_radiotherapy_updated_at"),
                TumorRadiotherapy.created_at.label("tumor_radiotherapy_created_at"),

                RadiotherapySession.id.label("radiotherapy_session_id"),
                RadiotherapySession.start_date.label("radiotherapy_session_start_date"),
                RadiotherapySession.start_date_accuracy.label("radiotherapy_session_start_date_accuracy"),
                RadiotherapySession.duration_days.label("radiotherapy_session_duration_days"),
                RadiotherapySession.target_area.label("radiotherapy_session_target_area"),
                RadiotherapySession.laterality.label("radiotherapy_session_laterality"),
                RadiotherapySession.updated_at.label("radiotherapy_session_updated_at"),
                RadiotherapySession.created_at.label("radiotherapy_session_created_at"),

                RadiotherapySessionPercutaneous.chemoradio.label("radiotherapy_session_percutaneous_chemoradio"),
                RadiotherapySessionPercutaneous.stereotactic.label("radiotherapy_session_percutaneous_stereotactic"),
                RadiotherapySessionPercutaneous.respiratory_gated.label("radiotherapy_session_percutaneous_respiratory_gated"),
                RadiotherapySessionPercutaneous.updated_at.label("radiotherapy_session_percutaneous_updated_at"),
                RadiotherapySessionPercutaneous.created_at.label("radiotherapy_session_percutaneous_created_at"),

                RadiotherapySessionBrachytherapy.type.label("radiotherapy_session_brachytherapy_type"),
                RadiotherapySessionBrachytherapy.dose_rate.label("radiotherapy_session_brachytherapy_dose_rate"),
                RadiotherapySessionBrachytherapy.created_at.label("radiotherapy_session_brachytherapy_created_at"),
                RadiotherapySessionBrachytherapy.updated_at.label("radiotherapy_session_brachytherapy_updated_at"),

                RadiotherapySessionMetabolic.type.label("radiotherapy_session_metabolic_type"),
                RadiotherapySessionMetabolic.created_at.label("radiotherapy_session_metabolic_created_at"),
                RadiotherapySessionMetabolic.updated_at.label("radiotherapy_session_metabolic_updated_at"),

                TumorFollowUp.id.label("tumor_follow_up_id"),
                TumorFollowUp.other_classification.label("tumor_follow_up_other_classification"),
                TumorFollowUp.date.label("tumor_follow_up_date"),
                TumorFollowUp.date_accuracy.label("tumor_follow_up_date_accuracy"),
                TumorFollowUp.overall_tumor_status.label("tumor_follow_up_overall_tumor_status"),
                TumorFollowUp.local_tumor_status.label("tumor_follow_up_local_tumor_status"),
                TumorFollowUp.lymph_node_tumor_status.label("tumor_follow_up_lymph_node_tumor_status"),
                TumorFollowUp.distant_metastasis_tumor_status.label("tumor_follow_up_distant_metastasis_tumor_status"),
                TumorFollowUp.distant_metastasis.label("tumor_follow_up_distant_metastasis"),
                TumorFollowUp.updated_at.label("tumor_follow_up_updated_at"),
                TumorFollowUp.created_at.label("tumor_follow_up_created_at"),

                follow_up_tnm_alias.id.label("tumor_follow_up_tnm_id"),
                follow_up_tnm_alias.version.label("tumor_follow_up_tnm_version"),
                follow_up_tnm_alias.y_symbol.label("tumor_follow_up_tnm_y_symbol"),
                follow_up_tnm_alias.r_symbol.label("tumor_follow_up_tnm_r_symbol"),
                follow_up_tnm_alias.a_symbol.label("tumor_follow_up_tnm_a_symbol"),
                follow_up_tnm_alias.t_prefix.label("tumor_follow_up_tnm_t_prefix"),
                follow_up_tnm_alias.t.label("tumor_follow_up_tnm_t"),
                follow_up_tnm_alias.m_symbol.label("tumor_follow_up_tnm_m_symbol"),
                follow_up_tnm_alias.n_prefix.label("tumor_follow_up_tnm_n_prefix"),
                follow_up_tnm_alias.n.label("tumor_follow_up_tnm_n"),
                follow_up_tnm_alias.m_prefix.label("tumor_follow_up_tnm_m_prefix"),
                follow_up_tnm_alias.m.label("tumor_follow_up_tnm_m"),
                follow_up_tnm_alias.l.label("tumor_follow_up_tnm_l"),
                follow_up_tnm_alias.v.label("tumor_follow_up_tnm_v"),
                follow_up_tnm_alias.pn.label("tumor_follow_up_tnm_pn"),
                follow_up_tnm_alias.s.label("tumor_follow_up_tnm_s"),
                follow_up_tnm_alias.uicc_stage.label("tumor_follow_up_tnm_uicc_stage"),
                follow_up_tnm_alias.created_at.label("tumor_follow_up_tnm_created_at"),
                follow_up_tnm_alias.updated_at.label("tumor_follow_up_tnm_updated_at"),

                TumorSurgery.id.label("tumor_surgery_id"),
                TumorSurgery.intent.label("tumor_surgery_intent"),
                TumorSurgery.date.label("tumor_surgery_date"),
                TumorSurgery.date_accuracy.label("tumor_surgery_date_accuracy"),
                TumorSurgery.operations.label("tumor_surgery_operations"),
                TumorSurgery.local_residual_status.label("tumor_surgery_local_residual_status"),
                TumorSurgery.created_at.label("tumor_surgery_created_at"),
                TumorSurgery.updated_at.label("tumor_surgery_updated_at"),

                TumorSystemicTherapy.id.label("tumor_systemic_therapy_id"),
                TumorSystemicTherapy.start_date.label("tumor_systemic_therapy_start_date"),
                TumorSystemicTherapy.start_date_accuracy.label("tumor_systemic_therapy_start_date_accuracy"),
                TumorSystemicTherapy.duration_days.label("tumor_systemic_therapy_duration_days"),
                TumorSystemicTherapy.intent.label("tumor_systemic_therapy_intent"),
                TumorSystemicTherapy.surgery_relation.label("tumor_systemic_therapy_surgery_relation"),
                TumorSystemicTherapy.type.label("tumor_systemic_therapy_type"),
                TumorSystemicTherapy.protocol.label("tumor_systemic_therapy_protocol"),
                TumorSystemicTherapy.drugs.label("tumor_systemic_therapy_drugs"),
                TumorSystemicTherapy.created_at.label("tumor_systemic_therapy_created_at"),
                TumorSystemicTherapy.updated_at.label("tumor_systemic_therapy_updated_at"),
            )
            .outerjoin(TumorReport, TumorReport.patient_report_id == PatientReport.id)
            .outerjoin(c_tnm_alias, TumorReport.c_tnm_id == c_tnm_alias.id)
            .outerjoin(p_tnm_alias, TumorReport.p_tnm_id == p_tnm_alias.id)
            .outerjoin(TumorHistology, TumorHistology.tumor_report_id == TumorReport.id)
            .outerjoin(TumorReportBreast, TumorReportBreast.tumor_report_id == TumorReport.id)
            .outerjoin(TumorReportColorectal, TumorReportColorectal.tumor_report_id == TumorReport.id)
            .outerjoin(TumorReportMelanoma, TumorReportMelanoma.tumor_report_id == TumorReport.id)
            .outerjoin(TumorReportProstate, TumorReportProstate.tumor_report_id == TumorReport.id)
            .outerjoin(TumorRadiotherapy, TumorRadiotherapy.tumor_report_id == TumorReport.id)
            .outerjoin(RadiotherapySession, RadiotherapySession.tumor_radiotherapy_id == TumorRadiotherapy.id)
            .outerjoin(RadiotherapySessionPercutaneous, RadiotherapySessionPercutaneous.radiotherapy_session_id == RadiotherapySession.id)
            .outerjoin(RadiotherapySessionBrachytherapy, RadiotherapySessionBrachytherapy.radiotherapy_session_id == RadiotherapySession.id)
            .outerjoin(RadiotherapySessionMetabolic, RadiotherapySessionMetabolic.radiotherapy_session_id == RadiotherapySession.id)
            .outerjoin(TumorFollowUp, TumorFollowUp.tumor_report_id == TumorReport.id)
            .outerjoin(follow_up_tnm_alias, TumorFollowUp.tnm_id == follow_up_tnm_alias.id)
            .outerjoin(TumorSurgery, TumorSurgery.tumor_report_id == TumorReport.id)
            .outerjoin(TumorSystemicTherapy, TumorSystemicTherapy.tumor_report_id == TumorReport.id)
        )

        rows = session.execute(query).mappings().all()

        logger.info("Flattened patient report export rows: %s", len(rows))

        return [dict(row) for row in rows]
