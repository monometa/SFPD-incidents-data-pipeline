import pyarrow.compute as pc

def cast_column_datetime_2_timestamp(table, column_name, column_pos):
    new_datetime = pc.strptime(
        table.column(column_name), format="%Y/%m/%d %H:%M:%S %p", unit="s"
    )
    table = table.set_column(column_pos, column_name, new_datetime)
    return table