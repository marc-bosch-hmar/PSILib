def PSI20(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI20'):
    """
    This function computes our custom PSI: Infection and Inflammatory Reaction
    Due to Prosthetic Device, Other Complications Due to Internal Joint
    Prosthesis (Euro DRG project).

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
        'T8450XA',
        'T8450XD',
        'T8450XS',
        'T8451XA',
        'T8451XD',
        'T8451XS',
        'T8452XA',
        'T8452XD',
        'T8452XS',
        'T8453XA',
        'T8453XD',
        'T8453XS',
        'T8454XA',
        'T8454XD',
        'T8454XS',
        'T8459XA',
        'T8459XD',
        'T8459XS',
        'T8460XA',
        'T8460XD',
        'T8460XS',
        'T84610A',
        'T84610D',
        'T84610S',
        'T84611A',
        'T84611D',
        'T84611S',
        'T84612A',
        'T84612D',
        'T84612S',
        'T84613A',
        'T84613D',
        'T84613S',
        'T84614A',
        'T84614D',
        'T84614S',
        'T84615A',
        'T84615D',
        'T84615S',
        'T84619A',
        'T84619D',
        'T84619S',
        'T84620A',
        'T84620D',
        'T84620S',
        'T84621A',
        'T84621D',
        'T84621S',
        'T84622A',
        'T84622D',
        'T84622S',
        'T84623A',
        'T84623D',
        'T84623S',
        'T84624A',
        'T84624D',
        'T84624S',
        'T84625A',
        'T84625D',
        'T84625S',
        'T84629A',
        'T84629D',
        'T84629S',
        'T8463XA',
        'T8463XD',
        'T8463XS',
        'T8469XA',
        'T8469XD',
        'T8469XS',
        'T847XXA',
        'T847XXD',
        'T847XXS',
        'T8481XA',
        'T8481XD',
        'T8481XS',
        'T8482XA',
        'T8482XD',
        'T8482XS',
        'T8483XA',
        'T8483XD',
        'T8483XS',
        'T8484XA',
        'T8484XD',
        'T8484XS',
        'T8485XA',
        'T8485XD',
        'T8485XS',
        'T8486XA',
        'T8486XD',
        'T8486XS',
        'T8489XA',
        'T8489XD',
        'T8489XS',
        'T849XXA',
        'T849XXD',
        'T849XXS'
        ]


    # Codes present in secondary diagnoses in medical records
    sec_diag = d_cols[1:]
    psi_num = df[sec_diag].isin(CODES).any(1)

    df[psi_name] = 1*psi_num

    return df
