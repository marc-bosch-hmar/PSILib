from .PSI2 import PSI2
from .PSI3 import PSI3
from .PSI4 import PSI4
from .PSI5 import PSI5
from .PSI6 import PSI6
from .PSI7 import PSI7
from .PSI8 import PSI8
from .PSI9 import PSI9
from .PSI10 import PSI10
from .PSI11 import PSI11
from .PSI12 import PSI12
from .PSI13 import PSI13
from .PSI14 import PSI14
from .PSI15 import PSI15
from .PSI16 import PSI16
from .PSI17 import PSI17
from .PSI18 import PSI18
from .PSI19 import PSI19
from .PSI20 import PSI20
from .PSI21 import PSI21
from .PSI22 import PSI22


def PSI(df, d_cols, p_cols, death, elective, acute, ms_col, cdm_col, los_col,
        age_col, prefix="PSI"):
    """
    This function computes all the defined Patient Safety Indicators.

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
        - prefix (String): Prefix to the names of all PSI columns.

    Returns: DataFrame with all the PSI computed. Also the number of PSI per
             discharge and if the discharges have any PSI present.
    """

    N_PSI = 22

    for i in range(2, N_PSI + 1):
        i_name = str(i).zfill(2)
        df = eval(
            (f"PSI{i}("
             f'df=df, d_cols={d_cols}, p_cols={p_cols}, death="{death}", '
             f'elective="{elective}", acute="{acute}", ms_col="{ms_col}", '
             f'cdm_col="{cdm_col}", los_col="{los_col}", age_col="{age_col}", '
             f'psi_name="{prefix}{i_name}")'))

    psi_cols = [f"{prefix}{str(i).zfill(2)}" for i in range(2, N_PSI + 1)]
    df[f"{prefix}_Any"] = 1*(df[psi_cols].any(1))
    df[f"{prefix}_Num"] = df[psi_cols].sum(1)

    return df
