from datetime import datetime

from pydantic import BaseModel

from ...krebs_db.enums.tnm_version_type import TnmVersionType
from ...krebs_db.enums.cpu_prefix_type import CpuPrefixType
from ...krebs_db.enums.tnm_lymphatic_invasion_type import TnmLymphaticInvasionType
from ...krebs_db.enums.tnm_venous_invasion_type import TnmVenousInvasionType
from ...krebs_db.enums.tnm_perineural_invasion_type import TnmPerineuralInvasionType
from ...krebs_db.enums.tnm_surgical_margin_type import TnmSurgicalMarginType
from ...krebs_db.enums.uicc_stage_type import UiccStageType


class TnmDto(BaseModel):
    version: TnmVersionType | None = None
    y_symbol: bool | None = None
    r_symbol: bool | None = None
    a_symbol: bool | None = None
    t_prefix: CpuPrefixType | None = None
    t: str | None = None
    m_symbol: str | None = None
    n_prefix: CpuPrefixType | None = None
    n: str | None = None
    m_prefix: CpuPrefixType | None = None
    m: str | None = None
    l: TnmLymphaticInvasionType | None = None
    v: TnmVenousInvasionType | None = None
    pn: TnmPerineuralInvasionType | None = None
    s: TnmSurgicalMarginType | None = None
    uicc_stage: UiccStageType | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
