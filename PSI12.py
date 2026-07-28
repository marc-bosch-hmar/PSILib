import pandas as pd
from .Codigos_PSI import DEEPVIB, PULMOID, SURGI2R, ORPROC, VENACIP
from .Codigos_PSI import NEURTRAD, ECMOP, THROMP


def PSI12(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI12'):
    """
    This function computes the Patient Safety Indicator 12, perioperative
    pulmonary embolism or deep vein thrombosis.

    Parameters:
        - df (pandas DataFrame): A DataFrame with hospital discharges
        - d_cols (list): List of the names in which diagnosis are located
        - p_cols (list): List of the names in which procedures are located
        - death (String): Column in with an indicator of death is, or and
                          expression of type "<variable> == <value>" where
                          <variable> is the variable in which death is coded,
                          and <value> is the code value of death.
        - elective (String): Column in with an indicator of elective is, or
                             and expression of type "<variable> == <value>"
                             where <variable> is the variable in which
                             elective is coded, and <value> is the code
                             value of elective.
        - acute (String): Column in with an indicator of transfered to an
                          acute care facility is, or and expression of type
                          "<variable> == <value>" where <variable> is the
                          variable in which "transfered to an acute care
                          facility" is coded, and <value> is the code
                          value of "transfered to an acute care facility".
        - ms_col (String): Name of the column in which MS-DRG is
        - cdm_col (String): Name of the column in wich MDC is located
        - los_col (String): Name of the column in which Length of Stay is
        - age_col (String): Name of the column in with age is located
        - psi_name (Optional, String):  Column name where PSI indicator
                                        is computed
    Returns: None
    """

    #
    # Denominator inclusion
    #

    # Surgical discharges SURGI2R for patients ages 18 years and
    # older, with any ORPROC procedure
    op_proc = df[p_cols].isin(ORPROC).sum(1)
    psi_denom = df.eval('(' + age_col + '>=18) & (@op_proc >= 1)')

    #
    # Denominator exclusion
    #

    # Principal diagnosis (or secondary POA) for DEEPVIB
    # TODO: POA
    psi_denom.loc[df[d_cols[0]].isin(DEEPVIB)] = False
    # Principal diagnosis (or secondary POA) for PULMOID
    # TODO: POA
    psi_denom.loc[df[d_cols[0]].isin(PULMOID)] = False
    # TODO: VENACIP procedure before or on the same day as the first
    # ORPROC
    # The only ORPROC is VENACIP
    vena_proc = df[p_cols].isin(VENACIP).sum(1)
    psi_denom.loc[pd.eval('op_proc == vena_proc')] = False
    # TODO: NEURTRAD diagnoses POA
    # Any ECMOP procedure
    psi_denom.loc[df[p_cols].isin(ECMOP).any(1)] = False
    # TODO: THROMP procedure occurs before or on the same day
    # as the first ORPROC
    # The only ORPROC is THROMP
    th_proc = df[p_cols].isin(THROMP).sum(1)
    psi_denom.loc[pd.eval('th_proc == op_proc')] = False
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(cdm_col + ' == "14"')] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with secondary diagnosis DEEPVIB or PULMOID
    psi_num = df[d_cols[1:]].isin(DEEPVIB + PULMOID).any(1)

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
