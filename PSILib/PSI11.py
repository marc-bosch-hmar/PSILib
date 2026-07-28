from .Codigos_PSI import ACURF2D, PR9672P, PR9671P, PR9604P, SURGI2R
from .Codigos_PSI import ORPROC, ACURF3D, TRACHIP, NEUROMD, NUCRANP
from .Codigos_PSI import PRESOPP, LUNGCIP, DGNEUID, LUNGTRANSP


def PSI11(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI11'):
    """
    This function computes the Patient Safety Indicator 11, Postoperative
    respiratory failure.

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

    # Elective surgical discharges SURGI2R for patients ages 18 years
    # and older, with any ORPROC procedure
    expr = f"({age_col}>= 18) | ("
    if "==" in elective:
        expr += elective + ')'
    else:
        expr += elective + ' == 1)'

    psi_denom = df.eval(expr)
    psi_denom = psi_denom & df[ms_col].isin(SURGI2R)
    psi_denom = psi_denom & df[p_cols].isin(ORPROC).any(1)

    #
    # Denominator exclusion
    #

    # Principal diagnosis of ACURF3D (or secondary POA)
    # TODO: POA
    psi_denom.loc[df[d_cols[0]].isin(ACURF3D)] = False
    # The only ORPROC is TRACHIP
    orproc_trac = list(set(ORPROC).intersection(set(TRACHIP)))
    orproc_trac_sum = df[p_cols].isin(orproc_trac).sum(1)
    psi_denom.loc[orproc_trac_sum == 1] = False
    # TODO: Where TRACHIP occurs before the first ORPROC
    # Any diagnoses of NEUROMD
    psi_denom.loc[df[d_cols].isin(NEUROMD).any(1)] = False
    # Any NUCRANP procedure
    psi_denom.loc[df[p_cols].isin(NUCRANP).any(1)] = False
    # Any PRESOPP procedure
    psi_denom.loc[df[p_cols].isin(PRESOPP).any(1)] = False
    # Any LUNGCIP procedure
    psi_denom.loc[df[p_cols].isin(LUNGCIP).any(1)] = False
    # Any diagnoses of DGNEUID
    psi_denom.loc[df[d_cols].isin(DGNEUID).any(1)] = False
    # Any LUNGTRANSP procedure
    psi_denom.loc[df[p_cols].isin(LUNGTRANSP).any(1)] = False
    # Diseases of respiratory system
    psi_denom.loc[df.eval(cdm_col + ' == "04"')] = False
    # Diseases of circulatory system
    psi_denom.loc[df.eval(cdm_col + ' == "05"')] = False
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(cdm_col + ' == "14"')] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with either:
    # Any secondary diagnosis for ACURF2D
    psi_num = df[d_cols[1:]].isin(ACURF2D).any(1)
    # Any secondary procedure for PR9672P that occurs zero or more days after
    # the first major ORPROC
    # TODO: Zero or more days after the first ORPROC
    # psi_num.loc[df[p_cols[1:]].isin(PR9672P).any(1)] = True
    # Any secondary procedure for PR9671P that occurs two or more days after
    # the first major ORPROC
    # TODO: Two or more days after the first ORPROC
    # psi_num.loc[df[p_cols[1:]].isin(PR9671P).any(1)] = True
    # Any secondary procedure for PR9604P that occurs one or more days after
    # the first major ORPROC
    # TODO: One or more days after the first ORPROC
    # psi_num.loc[df[p_cols[1:]].isin(PR9604P).any(1)] = True

    df[psi_name] = 1*(psi_num & psi_denom)

    return df
