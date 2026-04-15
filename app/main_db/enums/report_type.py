import enum

class ReportType(enum.Enum):
  # HKR delivers XML in oBDS_RKI format (tumor-centric, ZfKD standard).
  # This value is sent by the frontend as the 'type' field in the multipart upload
  # and stored in the main DB to identify which processor handles the import.
  # Version updated from 3.0.0.8a_RKI to 3.0.4_RKI in April 2024 (new schema from HKR).
  XML_oBDS_3_0_4_RKI = 'XML:oBDS_3.0.4_RKI'
