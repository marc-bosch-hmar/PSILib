import pandas as pd
from .Codigos_PSI import TECHNI15D, ABDOMI15P


def PSI15(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI15'):
    """
    This function computes the Patient Safety Indicator 15, accidental
    puncture or laceration.

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

    # Medical and surgical discharges with more than 18 years with ABDOMI15P
    # TODO: Filter medical and surgical MS-DRG
    proc_abd = df[p_cols].isin(ABDOMI15P).sum(1)
    psi_denom = df.eval('(' + age_col + '>=18) & (@proc_abd > 0)')

    #
    # Denominator exclusion
    #

    # Principal diagnosis with accidental puncture
    psi_denom.loc[df[d_cols[0]].isin(TECHNI15D)] = False
    # TODO: Secondary diagnoses with accidental puncture POA
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(cdm_col +' == "14"')] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any secondary accidental puncture and a second
    # abdominopelvic procedure
    tmp1 = pd.eval('psi_denom & (proc_abd >= 2)')
    psi_num = df[d_cols[1:]].isin(TECHNI15D).any(1)
    psi_num = pd.eval('tmp1 & psi_num')

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
