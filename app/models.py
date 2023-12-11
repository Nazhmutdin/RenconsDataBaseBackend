from sqlalchemy import String, Column, Date, ForeignKey, Float, ARRAY, SMALLINT
from sqlalchemy.orm import Mapped, relationship

from app.db_engine import BaseModel


class WelderModel(BaseModel):
    __tablename__ = "welder_table"

    kleymo = Column(String(4), primary_key=True)
    name = Column(String(), nullable=True)
    birthday = Column(Date(), nullable=True)
    sicil_number = Column(String(), nullable=True)
    passport_id = Column(String(), nullable=True)
    sicil_number = Column(String(), nullable=True)
    nation = Column(String(), nullable=True)
    status = Column(SMALLINT)
    certifications: Mapped[list["WelderCertificationModel"]] = relationship(back_populates="welder")
    ndts: Mapped[list["WelderNDTModel"]] = relationship(back_populates="welder")


class WelderNDTModel(BaseModel):
    __tablename__ = "welder_ndt_table"
    
    kleymo = Column(String(4), ForeignKey("welder_table.kleymo"))
    comp = Column(String(), nullable=True)
    subcon = Column(String(), nullable=True)
    project = Column(String(), nullable=True)
    latest_welding_date = Column(Date(), nullable=True)
    total_weld_1 = Column(Float(), nullable=True)
    total_ndt_1 = Column(Float(), nullable=True)
    total_accepted_1 = Column(Float(), nullable=True)
    total_repair_1 = Column(Float(), nullable=True)
    repair_status_1 = Column(Float(), nullable=True)
    total_weld_2 = Column(Float(), nullable=True)
    total_ndt_2 = Column(Float(), nullable=True)
    total_accepted_2 = Column(Float(), nullable=True)
    total_repair_2 = Column(Float(), nullable=True)
    repair_status_2 = Column(Float(), nullable=True)
    total_weld_3 = Column(Float(), nullable=True)
    total_ndt_3 = Column(Float(), nullable=True)
    total_accepted_3 = Column(Float(), nullable=True)
    total_repair_3 = Column(Float(), nullable=True)
    repair_status_3 = Column(Float(), nullable=True)
    ndt_id = Column(String(), primary_key=True)
    welder: Mapped[WelderModel] = relationship(back_populates="welder")


class WelderCertificationModel(BaseModel):
    __tablename__ = "welder_certification_table"

    kleymo = Column(String(4), ForeignKey("welder_table.kleymo"))
    certification_id = Column(String(), primary_key=True)
    job_title = Column(String(), nullable=True)
    certification_number = Column(String())
    certification_date = Column(Date())
    expiration_date = Column(Date())
    expiration_date_fact = Column(Date())
    insert = Column(String(), nullable=True)
    certification_type = Column(String(), nullable=True)
    company = Column(String(), nullable=True)
    gtd = Column(ARRAY(String), nullable=True)
    method = Column(String(), nullable=True)
    details_type = Column(ARRAY(String), nullable=True)
    joint_type = Column(ARRAY(String), nullable=True)
    groups_materials_for_welding = Column(ARRAY(String), nullable=True)
    welding_materials = Column(String(), nullable=True)
    details_thikness_from = Column(Float(), nullable=True)
    details_thikness_before = Column(Float(), nullable=True)
    outer_diameter_from = Column(Float(), nullable=True)
    outer_diameter_before = Column(Float(), nullable=True)
    welding_position = Column(String(), nullable=True)
    connection_type = Column(String(), nullable=True)
    rod_diameter_from = Column(Float(), nullable=True)
    rod_diameter_before = Column(Float(), nullable=True)
    rod_axis_position = Column(String(), nullable=True)
    weld_type = Column(String(), nullable=True)
    joint_layer = Column(String(), nullable=True)
    sdr = Column(String(), nullable=True)
    automation_level = Column(String(), nullable=True)
    details_diameter_from = Column(Float(), nullable=True)
    details_diameter_before = Column(Float(), nullable=True)
    welding_equipment = Column(String(), nullable=True)
    welder: Mapped[WelderModel] = relationship(back_populates="welder")
