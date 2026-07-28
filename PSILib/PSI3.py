from .Codigos_PSI import DECUBVD, SURGI2R, MEDIC2R, BURNDX, EXFOLIATXD


def PSI3(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI3'):
    """
    This function computes the Patient Safety Indicator 3, Pressure Ulcer rate.

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

    # Surgical or medical discharges for patients ages 18 years and older
    # TODO: Surgical and medical discharges
    psi_denom = df.eval('(' + age_col + '>=18)')

    #
    # Denominator exclusion
    #

    # Length of Stay of less than 3 days
    psi_denom.loc[df.eval(los_col + '< 3')] = False
    # Principal diagnosis for DECUBVD
    psi_denom.loc[df[d_cols[0]].isin(DECUBVD)] = False
    # TODO: All secondary diagnosis for DECUBVD POA
    # Any BURNDX diagnoses
    psi_denom.loc[df[d_cols].isin(BURNDX).any(1)] = False
    # Any EXFOLIATXD diagnoses
    psi_denom.loc[df[d_cols].isin(EXFOLIATXD).any(1)] = False
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(cdm_col + ' == "14"')] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any secondary diagnosis DECUBVD
    psi_num = df[d_cols[1:]].isin(DECUBVD).any(1)

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
