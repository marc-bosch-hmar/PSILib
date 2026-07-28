def PSI22(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI22'):
    """
    This function computes our custom PSI: Wound Infection (Euro DRG project).

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

    CODES = [
        'T814XXA',
        'T814XXD',
        'T814XXS'
    ]

    # Codes present in secondary diagnoses in medical records
    sec_diag = d_cols[1:]
    psi_num = df[sec_diag].isin(CODES).any(1)

    df[psi_name] = 1*psi_num

    return df
