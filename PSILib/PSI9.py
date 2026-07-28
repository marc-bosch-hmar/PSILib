import pandas as pd
from .Codigos_PSI import POHMRI2D, HEMOTH2P, SURGI2R, ORPROC, COAGDID


def PSI9(df, d_cols, p_cols, death, elective, acute,
         ms_col, cdm_col, los_col, age_col, psi_name='PSI09'):
    """
    This function computes the Patient Safety Indicator 9, perioperative
    hemorrhage or hematoma.

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

    # Surgical discharges SURGI2R for patients ages 18 years and older,
    # with any ORPROC procedure
    psi_denom = df.eval(f"{age_col} >= 18")
    psi_denom = psi_denom & df[ms_col].isin(SURGI2R)
    psi_denom = psi_denom & df[p_cols].isin(ORPROC).any(1)

    #
    # Denominator exclusion
    #

    # Principal diagnosis of POHMRI2D
    psi_denom.loc[df[d_cols[0]].isin(POHMRI2D)] = False
    # TODO: Secondary diagnoses POHMRI2D POA

    # The only ORPROC is for treatment of HEMOTH2P and with any secondary
    # diagnoses for POHMRI2D
    orproc_hemo = list(set(ORPROC).intersection(set(HEMOTH2P)))
    or_proc = df[p_cols].isin(orproc_hemo).sum(1)
    poh_diag = df[d_cols[1:]].isin(POHMRI2D).any(1)
    psi_denom.loc[(or_proc == 1) & poh_diag] = False

    # TODO: Treatment of POHMRI2D occurs one day or more before the first
    # HEMOTH2P and with any secondary diagnoses for POHMRI2D
    # With any diagnosis for COAGDID
    psi_denom.loc[df[d_cols].isin(COAGDID).any(1)] = False
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(f"{cdm_col}  == '14'")] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any secondary diagnoses POHMRI2D and any HEMOTH2P
    # procedure
    tmp = df[d_cols[1:]].isin(POHMRI2D).any(1)
    psi_num = df[p_cols].isin(HEMOTH2P).any(1)
    psi_num = pd.eval('tmp & psi_num')

    df[psi_name] = 1*(psi_num & psi_denom)

    return df
