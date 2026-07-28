from .Codigos_PSI import SURGI2R, ORPROC, FTR2DXB, FTR3DX, FTR4DX
import pandas as pd
from .Codigos_PSI import FTR5DX, FTR5PR, FTR6DX, FTR2DXB, OBEMBOL
from .Codigos_PSI import FTR3EXA, FTR3EXB, LUNGCIP, INFECID, TRAUMID
from .Codigos_PSI import HEMORID, GASTRID, FTR5EX, FTR6DX, FTR6GV
from .Codigos_PSI import FTR6QD, ALCHLSM, FTR6EX


def PSI4(df, d_cols, p_cols, death, elective, acute,
         ms_col, cdm_col, los_col, age_col, psi_name='PSI4'):
    """
    This function computes the Patient Safety Indicator 4, death rate among
    surgical inpatients with serious treatable conditions.

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

    # Surgical SURGI2R discharges for patients ages 18 through 89 years or
    # MDC 14 (pregnancy, childbirth and puerperium) with all of the following:
    # - Elective admission or
    #   TODO: any admission type in which the earliest ORPROC occurs within
    #         two days of admission.
    # - Inclusion criteria for STRATUM_SHOCK, STRATUM_SEPSIS,
    # STRATUM_PNEUMONIA, STRATUM_DVT OR STRATUM_GI_HEM
    # TODO: Surgical discharges
    expr = '(' + age_col + '>=18) & (' + age_col + '<=89)' + ' & ('
    if "==" in elective:
        expr += elective + ')'
    else:
        expr += elective + ' == 1)'
    cond1 = df.eval(expr)
    # STRATUM_DVT: Any secondary FTR2DXB diagnosis
    psi_denom = df[d_cols[1:]].isin(FTR2DXB).any(1)
    # STRATUM_PNEUMONIA: Any secondary FTR3DX diagnosis
    psi_denom.loc[df[d_cols[1:]].isin(FTR3DX).any(1)] = True
    # STRATUM_SEPSIS: Any secondary FTR4DX diagnosis
    psi_denom.loc[df[d_cols[1:]].isin(FTR4DX).any(1)] = True
    # STRATUM_SHOCK: Any secondary FTR5DX diagnosis or any FTR5PR procedure
    psi_denom.loc[df[d_cols[1:]].isin(FTR5DX).any(1)] = True
    psi_denom.loc[df[p_cols].isin(FTR5PR).any(1)] = True
    # STRATUM_GI_HEM: Any secondary FTR6DX diagnosis
    psi_denom.loc[df[d_cols[1:]].isin(FTR6DX).any(1)] = True

    psi_denom = pd.eval('cond1 & psi_denom')

    #
    # Denominator exclusion
    #

    # Transfered to an acute care facility
    if "==" in acute:
        expr = acute
    else:
        expr = acute + " == 1"
    psi_denom.loc[df.eval(expr)] = False
    # TODO: Admitted from hospice care
    # TODO: Missings
    # STRATUM_DVT: Principal diagnosis for FTR2DXB or OBEMBOL.
    psi_denom.loc[df[d_cols[0]].isin(FTR2DXB + OBEMBOL)] = False
    # STRATUM_PNEUMONIA: Principal diagnosis for FTR3DX or FTR3EXA
    psi_denom.loc[df[d_cols[0]].isin(FTR3DX + FTR3EXA)] = False
    # STRATUM_PNEUMONIA: Any diagnosis for FTR3EXB
    psi_denom.loc[df[d_cols].isin(FTR3EXB).any(1)] = False
    # STRATUM_PNEUMONIA: Any procedure for LUNGCIP
    psi_denom.loc[df[p_cols].isin(LUNGCIP).any(1)] = False
    # STRATUM_SEPSIS: Principal diagnosis for FTR4DX or INFECID
    psi_denom.loc[df[d_cols[0]].isin(FTR4DX + INFECID)] = False
    # STRATUM_SHOCK: Principal diagnosis for FTR5DX, TRAUMID, HEMORID, GASTRID
    #                or FTR5EX
    psi_denom.loc[df[d_cols[0]].isin(FTR5DX + TRAUMID + HEMORID +
                                     GASTRID + FTR5EX)] = False
    # STRATUM_SHOCK: MCD 4 or 5
    psi_denom.loc[df.eval(cdm_col + ' in ["04", "05"]')] = False
    # STRATUM_GI_HEM: Principal diagnosis for FTR6DX, TRAUMID, ALCHLSM, FTR6EX
    psi_denom.loc[df[d_cols[0]].isin(FTR6DX + TRAUMID + ALCHLSM +
                                     FTR6EX)] = False
    # STRATUM_GI_HEM: Secondary diagnoses for FTR6GV and principal diagnosis
    #                 for FTR6QD
    gv = df[d_cols[1:]].isin(FTR6GV).any(1)
    qd = df[d_cols[0]].isin(FTR6QD)
    psi_denom.loc[pd.eval('gv & qd')] = False
    # STRATUM_GI_HEM: MCD 6 or 7
    psi_denom.loc[df.eval(cdm_col + ' in ["06", "07"]')] = False

    #
    # Numerator
    #

    # Deaths
    if "==" in death:
        expr = death
    else:
        expr = death + ' == 1'

    psi_num = df.eval(expr)

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
