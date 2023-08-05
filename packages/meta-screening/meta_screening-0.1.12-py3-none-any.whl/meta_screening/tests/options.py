from edc_constants.constants import YES, BLACK, FEMALE, NOT_APPLICABLE, TBD, NO
from edc_utils.date import get_utcnow
from dateutil.relativedelta import relativedelta
from edc_reportable.units import MILLIMOLES_PER_LITER, MICROMOLES_PER_LITER

part_one_eligible_options = dict(
    report_datetime=get_utcnow(),
    hospital_identifier="111",
    initials="ZZ",
    gender=FEMALE,
    age_in_years=25,
    ethnicity=BLACK,
    hiv_pos=YES,
    art_six_months=YES,
    on_rx_stable=YES,
    lives_nearby=YES,
    staying_nearby=YES,
    pregnant=NOT_APPLICABLE,
    consent_ability=YES,
)


part_two_eligible_options = dict(
    part_two_report_datetime=get_utcnow(),
    acute_condition=NO,
    acute_metabolic_acidosis=NO,
    advised_to_fast=YES,
    alcoholism=NO,
    appt_datetime=get_utcnow() + relativedelta(days=1),
    congestive_heart_failure=NO,
    liver_disease=NO,
    metformin_sensitivity=NO,
    renal_function_condition=NO,
    tissue_hypoxia_condition=NO,
    urine_bhcg_performed=NO,
)

part_three_eligible_options = dict(
    part_three_report_datetime=get_utcnow(),
    weight=65,
    height=110,
    hba1c_performed=YES,
    hba1c=7.0,
    creatinine_performed=YES,
    creatinine=50,
    creatinine_units=MICROMOLES_PER_LITER,
    fasted=YES,
    fasted_duration_str="8h",
    fasting_glucose=7.0,
    fasting_glucose_datetime=get_utcnow(),
    ogtt_base_datetime=get_utcnow(),
    ogtt_two_hr=7.5,
    ogtt_two_hr_units=MILLIMOLES_PER_LITER,
    ogtt_two_hr_datetime=get_utcnow(),
)
