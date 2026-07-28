from .Codigos_PSI import PHYSIDB, DIALYIP, SURGI2R, ORPROC, DIALY2P
import pandas as pd
from .Codigos_PSI import CARDIID, CARDRID, SHOCKID, CRENLFD, URINARYOBSID
from .Codigos_PSI import SOLKIDD, PNEPHREP


def PSI10(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI10'):
    """
    This function computes the Patient Safety Indicator 10, postoperative
    acute kidney injury requiring dialysis.

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
    expr = f"({age_col}>= 18) & ("
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

    # Principal diagnosis of PHYSIDB
    psi_denom.loc[df[d_cols[0]].isin(PHYSIDB)] = False
    # TODO: Secondary diagnoses PHYSIDB POA
    # TODO: Any DIALYIP that occurs before or on the same day as
    # the first ORPROC
    # TODO: Any DIALY2P that occurs before or on the same day as
    # the first ORPROC
    # Principal diagnosis of CARDIID
    psi_denom.loc[df[d_cols[0]].isin(CARDIID)] = False
    # Principal diagnosis of CARDRID
    psi_denom.loc[df[d_cols[0]].isin(CARDRID)] = False
    # TODO: Secondary diagnoses CARDRID POA
    # Principal diagnosis of SHOCKID
    psi_denom.loc[df[d_cols[0]].isin(SHOCKID)] = False
    # TODO: Secondary diagnoses SHOCKID POA
    # Principal diagnosis of CRENLFD
    psi_denom.loc[df[d_cols[0]].isin(CRENLFD)] = False
    # TODO: Secondary diagnoses CRENLFD POA
    # Principal diagnosis of URINARYOBSID
    psi_denom.loc[df[d_cols[0]].isin(URINARYOBSID)] = False
    # SOLKIDD POA and any PNEPHREP procedure
    # TODO: SOLKIDD POA
    # psi_denom.loc[df[p_cols].isin(PNEPHREP).any(1)] = False
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(f"{cdm_col}  == '14'")] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any secondary diagnoses PHYSIDB and any DIALYIP
    # procedure
    tmp = df[d_cols[1:]].isin(PHYSIDB).any(1)
    psi_num = df[p_cols].isin(DIALYIP).any(1)
    psi_num = pd.eval('tmp & psi_num')

    df[psi_name] = 1*(psi_num & psi_denom)

    return df
