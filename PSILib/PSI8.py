from .Codigos_PSI import HIPFXID, MEDIC2R, SURGI2R, ORPROC, SEIZUID
from .Codigos_PSI import SYNCOID, STROKID, COMAID, CARDIID, POISOID
from .Codigos_PSI import TRAUMID, DELIRID, ANOXIID, METACID, LYMPHID
from .Codigos_PSI import BONEMID


def PSI8(df, d_cols, p_cols, death, elective, acute,
         ms_col, cdm_col, los_col, age_col, psi_name='PSI8'):
    """
    This function computes the Patient Safety Indicator 8, in hospital fall
    with hip fracture.

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

    # Medical and surgical discharges with more than 18 years in a medical or
    # quirurgical DRG (MEDIC2R, SURGI2R), with any ORPROC procedure
    # TODO: Medical and surgical drg
    or_proc = df[p_cols].isin(ORPROC).any(1)
    psi_denom = df.eval('(' + age_col + '>=18) & @or_proc')

    #
    # Denominator exclusion
    #

    # Any principal diagnosis or secondary POA for HIPFXID
    # TODO: POA
    psi_denom.loc[df[d_cols[0]].isin(HIPFXID)] = False
    # A principal diagnosis for SEIZUID, SYNCOID, STROKID, COMAID,
    # CARDIID, POISOID, TRAUMID, DELIRID, ANOXIID
    tmp_list = SEIZUID + SYNCOID + STROKID + COMAID + CARDIID + POISOID + \
        TRAUMID + DELIRID + ANOXIID
    psi_denom.loc[df[d_cols[0]].isin(tmp_list)] = False
    # Any diagnosis for METACID, LYMPHID, BONEMID
    psi_denom.loc[df[d_cols].isin(METACID + LYMPHID + BONEMID).any(1)] = False
    # Pregnancy, childbirth and puerperium
    psi_denom.loc[df.eval(cdm_col + ' == "14"')] = False
    # TODO: Missings

    #
    # Numerator
    #

    # Discharges among cases meeting inclusion and exclusion rules for the
    # denominator with any secondary HIPFXID diagnosis
    psi_num = df[d_cols[1:]].isin(HIPFXID).any(1)

    df.eval(psi_name + ' = 1.0*(@psi_num & @psi_denom)', inplace=True)
    return
