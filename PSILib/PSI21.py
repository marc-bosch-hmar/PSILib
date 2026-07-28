def PSI21(df, d_cols, p_cols, death, elective, acute,
          ms_col, cdm_col, los_col, age_col, psi_name='PSI21'):
    """
    This function computes our custom PSI: Urinary Tract Infection
    (Euro DRG project).

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
        'N3000',
        'N3001',
        'N3010',
        'N3011',
        'N3020',
        'N3021',
        'N3030',
        'N3031',
        'N3040',
        'N3041',
        'N3080',
        'N3081',
        'N3090',
        'N3091',
        'N390',  # In theory the most used code (Albert Anglès)
        'O2300',
        'O2301',
        'O2302',
        'O2303',
        'O2310',
        'O2311',
        'O2312',
        'O2313',
        'O2320',
        'O2321',
        'O2322',
        'O2323',
        'O2330',
        'O2331',
        'O2332',
        'O2333',
        'O2340',
        'O2341',
        'O2342',
        'O2343',
        'O23511',
        'O23512',
        'O23513',
        'O23519',
        'O23521',
        'O23522',
        'O23523',
        'O23529',
        'O23591',
        'O23592',
        'O23593',
        'O23599',
        'O2390',
        'O2391',
        'O2392',
        'O2393',
        'O8620',
        'O8621',
        'O8622',
        'O8629'
    ]


    # Codes present in secondary diagnoses in medical records
    sec_diag = d_cols[1:]
    psi_num = df[sec_diag].isin(CODES).any(1)

    df[psi_name] = 1*psi_num

    return df
