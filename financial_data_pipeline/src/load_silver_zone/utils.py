import re
import sh
import os
import pandas as pd


silver_zone = pd.read_csv(os.path.dirname(os.path.abspath(__file__))+"/silver_zone.csv")

def get_hdfs_files(directory: str):
    output = sh.hdfs('dfs', '-ls', directory).split('\n')
    files = []
    for line in output:
        match = re.search(f'({re.escape(directory)}.*$)', line)
        if match:
            files.append(match.group(0))

    return files

def get_table_name(file):
    return os.path.basename(file).split('.')[0]

def get_table_columns(table_name, with_datatype=False):
    if with_datatype:
        return silver_zone[(silver_zone['table_name'] == table_name)][['ordinal_position', 'new_column_name', 'data_type']
                                                                      ].sort_values('ordinal_position', axis=0)[['new_column_name', 'data_type']].values.tolist()
    return silver_zone[(silver_zone['table_name'] == table_name)][['ordinal_position', 'new_column_name']].sort_values('ordinal_position', axis=0)['new_column_name'].to_list()

def get_view_columns(table_name):
    return silver_zone[(silver_zone['table_name'] == table_name)][['ordinal_position', 'column_name']].sort_values('ordinal_position', axis=0)['column_name'].to_list()

def get_pk_columns(table_name):
    return silver_zone[(silver_zone['table_name'] == table_name) & (silver_zone['is_pk'] == True)][['column_name', 'new_column_name']].values.tolist()

def get_create_table_query(DATABASE_NAME, table_name):
    table_columns = get_table_columns(table_name, with_datatype=True)
    
    columns = []
    for col, dtype in table_columns:
        columns.append(f"{col} {dtype}")
    columns=",".join(columns)

    query = f"""
            create table if not exists {DATABASE_NAME}.{table_name}(
                {columns}
            )
            """
    return query