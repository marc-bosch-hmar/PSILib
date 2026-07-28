from .Codigos_PSI import SURGI2R, MEDIC2R, IDTMC3D, CANCEID, IMMUNID
from .Codigos_PSI import IMMUNIP


def PSI7(df, d_cols, p_cols, death, elective, acute,
         ms_col, cdm_col, los_col, age_col, psi_name='PSI7'):
    """
    This function computes the Patient Safety Indicator 7, central venous
    catheter-related blood stream infection.

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

    # Surgical and medical discharges with more than 18 years or MDC 14
    # TODO: Surgical and medical discharges
    psi_denom = df.eval('(' + age_col + '>=18) | (' + cdm_col + ' == "14")')

    #
    # Denominator exclusion
    #

    # Principal diagnosis for IDTMC3D
    psi_denom.loc[df[d_cols[0]].isin(IDTMC3D)] = False
    # TODO: Secondary diagnoses for IDTMC3D (todo because it is an inclusion
    # criteria for the numerator)
    # Length of Stay less than 2 days
    psi_denom.loc[df.eval(los_col + '<2')] = False
    # Any CANCEID diagnoses
    psi_denom.loc[df[d_cols].isin(CANCEID).any(1)] = False
    # Any IMMUNID diagnoses
    psi_denom.loc[df[d_cols].isin(IMMUNID).any(1)] = False
    # Any IMMUNIP procedures
    psi_denom.loc[df[p_cols].isin(IMMUNIP).any(1)] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any secondary IDTMC3D diagnosis
    psi_num = df[d_cols[1:]].isin(IDTMC3D).any(1)

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
