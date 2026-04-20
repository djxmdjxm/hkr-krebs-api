# Licensed under the MIT License.
# Copyright (c) 2025 Nataliya Didukh, Ihor Zhvanko.
# See the LICENSE file in the project root for full license text.

from sqlalchemy import Column, Integer, Date, ForeignKey, TIMESTAMP, JSON, func

from .base import Base
from .utils import db_enum
from .mixins import ReprMixin
from .enums.systemic_therapy_intent_type import SystemicTherapyIntentType
from .enums.systemic_therapy_type import SystemicTherapyType
from .enums.surgery_relation_type import SurgeryRelationType
from .enums.date_accuracy_type import DateAccuracyType


class TumorSystemicTherapy(ReprMixin, Base):
  __tablename__ = "tumor_systemic_therapy"

  id = Column(Integer, primary_key=True)
  tumor_report_id = Column(Integer, ForeignKey("tumor_report.id"), nullable=False)

  start_date = Column(Date, nullable=False, comment='SYST:Datum_Beginn_SYST')
  start_date_accuracy = Column(db_enum(DateAccuracyType), nullable=True, comment='SYST:Datum_Beginn_SYST:Datumsgenauigkeit')
  duration_days = Column(Integer, nullable=True, comment='SYST:Anzahl_Tage_SYST_Dauer')
  intent = Column(db_enum(SystemicTherapyIntentType), nullable=False, comment='SYST:Intention')
  surgery_relation = Column(db_enum(SurgeryRelationType), nullable=True, comment='SYST:Stellung_OP')
  type = Column(db_enum(SystemicTherapyType), nullable=False, comment='SYST:Therapieart')
  protocol = Column(JSON, nullable=True, comment='SYST:Protokoll') # { name: string } | { code: string; version: string; }
  drugs = Column(JSON, nullable=False, comment='SYST:Menge_Substanz:Substanz') # [{ name: string; } | { code: string; version: string; }, ...]

  created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
  updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

  # - oBDS -> SYST
  # is_systemic_therapy_start = Column(Boolean, nullable=False, comment='Meldeanlass:True=behandlungsbeginn:False=behandlungsende')
  # end_reason = Column(Enum(SystemicTherapyEndReason), nullable=True, comment='Ende_Grund')
  # side_effect_grade = Column(Enum(SideEffectSeverityType), nullable=True, comment='Nebenwirkung:Grad_maximal2_oder_unbekannt')
  # side_effects = Column(JSON, nullable=True, comment='Nebenwirkung:Menge_Nebenwirkung') # [{ type_lable: string; type_meddra_code: string; grade: SideEffectSeverityType; version: CTCAEVersionType }, ...]
