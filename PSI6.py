from .Codigos_PSI import IATROID, SURGI2R, MEDIC2R, CTRAUMD
from .Codigos_PSI import PLEURAD, THORAIP, CARDSIP


def PSI6(df, d_cols, p_cols, death, elective, acute,
         ms_col, cdm_col, los_col, age_col, psi_name='PSI06'):
    """
    This function computes the Patient Safety Indicator 6, Iatrogenic
    pneumotorax.

    Parameters:
        - df (pandas DataFrame): A DataFrame with hospital discharges
        - d_cols (list): List of the names in which diagnosis are located
        - p_cols (list): List of the names in which procedures are located
        - death (String): Column in which an indicator of death is, or and
                          expression of type "<variable> == <value>" where
                          <variable> is the variable in which death is coded,
                          and <value> is the code value of death.
        - elective (String): Column in which an indicator of elective is, or
                             and expression of type "<variable> == <value>"
                             where <variable> is the variable in which
                             elective is coded, and <value> is the code
                             value of elective.
        - acute (String): Column in which an indicator of transfered to an
                          acute care facility is, or and expression of type
                          "<variable> == <value>" where <variable> is the
                          variable in which "transfered to an acute care
                          facility" is coded, and <value> is the code
                          value of "transfered to an acute care facility".
        - ms_col (String): Name of the column in which MS-DRG is
        - cdm_col (String): Name of the column in which MDC is located
        - los_col (String): Name of the column in which Length of Stay is
        - age_col (String): Name of the column in which age is located
        - psi_name (Optional, String):  Column name where PSI indicator
                                        is computed
    Returns: DataFrame with a new column indicating if the discharge has the PSI
    """

    #
    # Denominator inclusion
    #

    # Surgical SURGI2R and medical discharges MEDIC2R for patients ages 18
    # years and older
    psi_denom = df.eval(f"{age_col} >= 18")
    psi_denom = psi_denom & df[ms_col].isin(MEDIC2R + SURGI2R)

    #
    # Denominator exclusion
    #

    # Principal diagnosis code (or secondary POA) for IATROID.
    # TODO: Secondary POA
    psi_denom.loc[df[d_cols[0]].isin(IATROID)] = False
    # Any diagnosis for CTRAUMD
    psi_denom.loc[df[d_cols].isin(CTRAUMD).any(1)] = False
    # Any diagnosis for PLEURAD
    psi_denom.loc[df[d_cols].isin(PLEURAD).any(1)] = False
    # Any procedure for THORAIP
    psi_denom.loc[df[p_cols].isin(THORAIP).any(1)] = False
    # Any procedure for CARDSIP
    psi_denom.loc[df[p_cols].isin(CARDSIP).any(1)] = False
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(cdm_col + ' == "14"')] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any secondary diagnosis for IATROID
    psi_num = df[d_cols[1:]].isin(IATROID).any(1)

    df[psi_name] = 1*(psi_num & psi_denom)

    return df
