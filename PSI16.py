from .Codigos_PSI import SURGI2R, MEDIC2R, TRANFID


def PSI16(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI16'):
    """
    This function computes the Patient Safety Indicator 16, transfusion
    reaction.

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

    # Códigos no específicos de reacción a la transfusión
    # (Albert Anglès)
    TRANS = TRANFID + \
        [
            "T80A0XA",
            "T80A10A",
            "T80A11A",
            "T80A19A",
            "T80A9XA"
        ]

    #
    # Numerator inclusion
    #

    # Surgical and medical discharges with more than 18 years or MDC 14
    # with any secondary TRANFID diagnosis
    psi_num = df[d_cols[1:]].isin(TRANS).any(1)

    string = (f"(({ms_col} in @SURGI2R) | ({ms_col} in @MEDIC2R)) & "
              f"(({age_col}>=18) | ({cdm_col} == '14')) &"
              "@psi_num")

    psi_num = df.eval(string)

    #
    # Numerator exclusion
    #

    # Principal diagnosis for TRANFID or secondary POA
    # TODO: POA
    psi_num.loc[df[d_cols[0]].isin(TRANS)] = False
    # TODO: Missings

    df[psi_name] = 1*(psi_num)

    return df
