import pandas as pd
from .Codigos_PSI import RECLOIP, ABWALLCD, ABDOMIPOPEN, ABDOMIPOTHER, IMMUNID


def PSI14(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI14'):
    """
    This function computes the Patient Safety Indicator 14, postoperative
    wound dehiscence.

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

    # Discharges for patients ages 18 years and older, with any procedure for
    # ABDOMIPOPEN or ABDOMIPOTHER
    proc = df[p_cols].isin(ABDOMIPOPEN + ABDOMIPOTHER).any(1)
    psi_denom = df.eval('(' + age_col + '>=18) & @proc')

    #
    # Denominator exclusion
    #

    # TODO: Procedure for abdominal wall reclosure RECLOIP
    #       on or before the day of the first ABDOMIPOPEN and the day of
    #       the first ABDOMIPOTHER
    # Diagnosis or procedures for IMMUNID
    psi_denom.loc[df[d_cols + p_cols].isin(IMMUNID).any(1)] = False
    # TODO: Diagnosis POA of ABWALLCD.
    # Length of Stay less than two days
    psi_denom.loc[df.eval(los_col +'<2')] = False
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(cdm_col +' == "14"')] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any RECLOIP procedure and any ABWALLCD diagnosis
    tmp = df[p_cols].isin(RECLOIP).any(1)
    psi_num = df[d_cols].isin(ABWALLCD).any(1)
    psi_num = pd.eval('tmp & psi_num')

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
