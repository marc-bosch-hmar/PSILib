from .Codigos_PSI import LIVEBND, LIVEB2D, PRETEID, BIRTHID, OSTEOID


def PSI17(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI17'):
    """
    This function computes the Patient Safety Indicator 17, birth trauma or
    injury to neonate.

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

    # All Newborns defined as Appendix M
    # Neonate with either:
    # - Any LIVEBND diagnoses
    # TODO: - Admission type of newborn and age in days equals zero without
    #       any LIVEB2D diagnoses
    # TODO: - Admission type of newborn with point of origin for born inside
    #       this hospital
    # Neonate:
    # TODO: - Age in days at admission between zero an 28 days.
    # - Age in days missing and age in years equals zero and either:
    #   TODO: - Admission type newborn
    #   Any diagnosis for LIVEBND
    # We just use the definition of Neonate
    neonate = df[d_cols].isin(LIVEBND).any(1)
    psi_denom = df.eval('(' + age_col + '< 0.2) & @neonate')

    #
    # Denominator exclusion
    #

    # Any PRETEID diagnoses
    psi_denom.loc[df[d_cols].isin(PRETEID).any(1)] = False
    # Any OSTEOID diagnoses
    psi_denom.loc[df[d_cols].isin(OSTEOID).any(1)] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any BIRTHID diagnoses
    psi_num = df[d_cols].isin(BIRTHID).any(1)

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
