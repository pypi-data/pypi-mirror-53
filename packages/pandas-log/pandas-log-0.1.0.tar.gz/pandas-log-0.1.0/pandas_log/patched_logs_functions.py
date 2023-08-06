# Rows messages
REMOVED_NO_ROWS_MSG = "\t* No change in number of rows."
FILTERED_ROWS_MSG = "\t* Removed {rows_removed} rows ({rows_removed_pct}%), {rows_remaining} rows remaining."

# Cols messages
REMOVED_NO_COLS_MSG = "\t* Removed no columns."
FILTERED_COLS_MSG = "\t* Removed the following columns ({cols_removed}) now only have the following columns ({cols_remaining})."
ASSIGN_EXISTING_MSG = "\t* The columns {existing_cols} were reassigned."
ASSIGN_NEW_MSG = "\t* The columns {new_cols} were created."

# N/A messages
FILLNA_NO_NA_MSG = "\t* There are no nulls."
FILLNA_WITHH_NA_MSG = "\t* Filled {} with {}."

# Mege messages
JOIN_ROWS_MSG = "\t* Its a {how} join.\n\t* Number of rows changed, after join is {output_rows} rows."
JOIN_NEW_COLS_MSG = "\t* Added {num_new_columns} columns ({new_columns})."

# Pick messages
SAMPLE_MSG = "\t* Picked random sample of {output_rows} rows."
NLARGEST_MSG = "\t* Picked {n} largest rows by columns ({cols})."
NSMALLEST_MSG = "\t* Picked {n} smallest rows by columns ({cols})."
HEAD_MSG = "\t* Picked the first {} rows."
TAIL_MSG = "\t* Picked the last {} rows."

# Others
SORT_VALUES_MSG = "\t* Sorting by columns {by} in a {'ascending' if ascending else 'descending'} order."
SORT_INDEX_MSG = "\t* Sorting by index in a {'ascending' if ascending else 'descending'} order."
NOT_IMPLEMENTED_MSG = "\t*Log not implemented yet for this function."


# TODO general stats if not exists
# TODO implement  a lot more functionality like iloc, loc, ix , apply applymap pipe where  isin mask rolling, groupby, .rename   expanding explode
# TODO refactor this mess


def rows_removed(input_df, output_df):
    return len(input_df) - len(output_df)


def rows_removed_pct(input_df, output_df):
    return (rows_removed(input_df, output_df)) / len(input_df)


def rows_remaining(output_df):
    return len(output_df)


def cols_removed(input_df, output_df):
    return ",".join(set(input_df.columns) - set(output_df.columns))


def cols_remaining(output_df):
    return ",".join(set(output_df.columns))


def is_same_cols(input_df, output_df):
    return len(input_df.columns) == len(output_df.columns)


def columns_changed(df, cols):
    return set(df.columns).intersection(set(cols))


def columns_added(df, cols):
    return set(cols) - set(df.columns)


def is_same_rows(input_df, output_df):
    return len(input_df) == len(output_df)


def num_of_na(df):
    return df.isnull().values.sum()


def str_new_columns(input_df, output_df):
    return ",".join(set(output_df.columns) - set(input_df.columns))


def num_new_columns(input_df, output_df):
    return len(set(output_df.columns) - set(input_df.columns))


def log_drop(key, input_df, output_df, **kwargs):
    logs = []
    if is_same_cols(input_df, output_df):
        logs.append(REMOVED_NO_COLS_MSG)
    else:
        logs.append(
            FILTERED_COLS_MSG.format(
                cols_removed=cols_removed(input_df, output_df),
                cols_remaining=cols_remaining(output_df),
            )
        )
    if is_same_rows(input_df, output_df):
        logs.append(REMOVED_NO_ROWS_MSG)
    else:
        logs.append(
            FILTERED_ROWS_MSG.format(
                rows_removed=rows_removed(input_df, output_df),
                rows_removed_pct=rows_removed_pct(input_df, output_df),
                rows_remaining=rows_remaining(output_df),
            )
        )
    return "\n".join(logs)


def log_dropna(input_df, output_df, **kwargs):
    logs = []
    if is_same_cols(input_df, output_df):
        logs.append(REMOVED_NO_COLS_MSG)
    else:
        logs.append(
            FILTERED_COLS_MSG.format(
                cols_removed=cols_removed(input_df, output_df),
                cols_remaining=cols_remaining(output_df),
            )
        )
    if is_same_rows(input_df, output_df):
        logs.append(REMOVED_NO_ROWS_MSG)
    else:
        logs.append(
            FILTERED_ROWS_MSG.format(
                rows_removed=rows_removed(input_df, output_df),
                rows_removed_pct=rows_removed_pct(input_df, output_df),
                rows_remaining=rows_remaining(output_df),
            )
        )
    return "\n".join(logs)


def log_assign(input_df, original_kwargs, **kwargs):
    logs = []
    cols = original_kwargs.keys()
    if columns_changed(input_df, cols):
        logs.append(
            ASSIGN_EXISTING_MSG.format(
                existing_cols=",".join(columns_changed(input_df, cols))
            )
        )
    if columns_added(input_df, cols):
        logs.append(
            ASSIGN_NEW_MSG.format(
                new_cols=",".join(columns_added(input_df, cols))
            )
        )
    return "\n".join(logs)


def log_query(expr, output_df, input_df, **kwargs):
    if is_same_rows(input_df, output_df):
        return REMOVED_NO_ROWS_MSG
    else:
        return FILTERED_ROWS_MSG.format(
            rows_removed=rows_removed(input_df, output_df),
            rows_removed_pct=rows_removed_pct(input_df, output_df),
            rows_remaining=rows_remaining(output_df),
        )


def log_reset_index(**kwargs):
    return ""


def log_sort_index(ascending, **kwargs):
    return SORT_INDEX_MSG.format(ascending)


def log_sort_values(by, ascending, **kwargs):
    return SORT_VALUES_MSG.format(by, ascending)


def log_tail(n, **kwargs):
    return TAIL_MSG.format(n)


def log_head(n, **kwargs):
    return HEAD_MSG.format(n)


def log_merge(input_df, other_df, output_df, how, **kwargs):
    logs = []
    if is_same_rows(input_df, output_df):
        logs.append(REMOVED_NO_ROWS_MSG)
    else:
        logs.append(JOIN_ROWS_MSG.format(how=how, output_rows=len(output_df)))
    if not is_same_cols(input_df, output_df):
        logs.append(
            JOIN_NEW_COLS_MSG.format(
                num_new_columns=num_new_columns(input_df, other_df),
                new_columns=str_new_columns(input_df, other_df),
            )
        )
    return "\n".join(logs)


def log_join(input_df, other_df, output_df, how, **kwargs):
    logs = []
    if is_same_rows(input_df, output_df):
        logs.append(REMOVED_NO_ROWS_MSG)
    else:
        logs.append(JOIN_ROWS_MSG.format(how=how, output_rows=len(output_df)))
    if not is_same_cols(input_df, output_df):
        logs.append(
            JOIN_NEW_COLS_MSG.format(
                num_new_columns=num_new_columns(input_df, other_df),
                new_columns=str_new_columns(input_df, other_df),
            )
        )
    return logs


def log_fillna(filled_with, input_df, output_df, **kwargs):
    if num_of_na(input_df) == num_of_na(output_df):
        return FILLNA_NO_NA_MSG
    else:
        return FILLNA_WITHH_NA_MSG.format(num_of_na(input_df), filled_with)


def log_sample(output_df, **kwargs):
    return SAMPLE_MSG.format(output_rows=len(output_df))


def log_nlargest(n, columns, **kwargs):
    return NLARGEST_MSG.format(n=n, cols=columns)


def log_nsmallest(n, columns, **kwargs):
    return NSMALLEST_MSG.format(n=n, cols=columns)


if __name__ == "__main__":
    pass
