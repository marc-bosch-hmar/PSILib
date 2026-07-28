import pandas as pd
from .Codigos_PSI import OBTRAID, DELOCMD, VAGDELP, INSTRIP


def PSI18(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI18'):
    """
    This function computes the Patient Safety Indicator 18, obstetric trauma,
    vaginal delivery with instrument.

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

    # Any DELOCMD diagnosis with any VAGDELP procedure and any VAGDELP
    # procedure
    del_diag = df[d_cols].isin(DELOCMD).any(1)
    vag_proc = df[p_cols].isin(VAGDELP).any(1)
    ins_proc = df[p_cols].isin(INSTRIP).any(1)
    psi_denom = pd.eval('del_diag & vag_proc & ins_proc')

    #
    # Denominator exclusion
    #

    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any OBTRAID diagnosis
    psi_num = df[d_cols].isin(OBTRAID).any(1)

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
