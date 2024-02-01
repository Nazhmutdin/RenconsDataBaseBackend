import typing as t
from datetime import date


class WelderCertificationModel(t.TypedDict):
    kleymo: str
    certification_id: str
    job_title: str
    certification_number: str
    certification_date: date
    expiration_date: date
    expiration_date_fact: date
    insert: str
    certification_type: str
    company: str
    gtd: list[str]
    method: str
    details_type: list[str]
    joint_type: list[str]
    groups_materials_for_welding: list[str]
    welding_materials: str
    details_thikness_from: float
    details_thikness_before: float
    outer_diameter_from: float
    outer_diameter_before: float
    welding_position: str
    connection_type: str
    rod_diameter_from: float
    rod_diameter_before: float
    rod_axis_position: str
    weld_type: str
    joint_layer: str
    sdr: str
    automation_level: str
    details_diameter_from: float
    details_diameter_before: float
    welding_equipment: str
