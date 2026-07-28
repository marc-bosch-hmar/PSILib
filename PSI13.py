from .Codigos_PSI import SEPTI2D, SURGI2R, ORPROC, INFECID


def PSI13(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI13'):
    """
    This function computes the Patient Safety Indicator 13, postoperative
    sepsis.

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

    # Elective surgical discharges with more than 18 years with
    # any ORPROC procedure
    # TODO: Elective surgical discharges
    proc_abd = df[p_cols].isin(ORPROC).sum(1)
    psi_denom = df.eval('(' + age_col + '>=18) & (@proc_abd > 0)')

    #
    # Denominator exclusion
    #

    # Principal diagnosis or secondary POA with SEPTI2D
    # TODO: POA
    psi_denom.loc[df[d_cols[0]].isin(SEPTI2D)] = False
    # Principal diagnosis or secondary POA with INFECID
    # TODO: POA
    psi_denom.loc[df[d_cols[0]].isin(INFECID)] = False
    # TODO: Secondary diagnoses with accidental puncture POA
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(cdm_col +' == "14"')] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any secondary SEPTI2D diagnosis
    psi_num = df[d_cols[1:]].isin(SEPTI2D).any(1)

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
