import psycopg2
import psycopg2.extras


class Dal:

    def __init__(self, connection_string):
        self.connection = psycopg2.connect(connection_string)

    def copy_to_table(self, table_name, file_path, has_header, is_csv_format, delimiter, empty_string, black_columns_list='', table_schema='public',
                      encoding='utf8'):
        cursor = self.connection.cursor()
        columns_list = self._generate_columns_list(black_columns_list, table_name, table_schema)
        sql = _generate_copy_command(columns_list, delimiter, encoding, has_header, is_csv_format, empty_string, table_name, table_schema)
        print("Executing copy command", sql)
        with open(file_path) as file:
            cursor.copy_expert(sql, file)
        file.close()
        self.commit()
        print(f"Loaded {str(cursor.rowcount)} rows to table", table_name)
        return cursor.rowcount

    def execute_query(self, sql_script, parameters=None):
        cursor = self.connection.cursor()
        print(f"About to run the following query: {sql_script} parameters:", parameters)
        cursor.execute(sql_script, parameters)
        self.commit()
        return cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.commit()
        self.connection.close()
        print("Database connection was closed")

    def _generate_columns_list(self, black_columns_list, table_name, table_schema):
        if black_columns_list:
            print(f"Getting columns list for table '{table_schema}.{table_name}', black list columns {black_columns_list}")
            query = """select column_name from information_schema.columns 
                        where table_schema = %s 
                        and table_name = %s 
                        and column_name not in (%s)"""
            results = self.execute_query(query, (table_schema, table_name, black_columns_list))
            return [row[0] for row in results]
        else:
            return None

    def execute_file(self, file_path, parameters=None):
        with open(file_path, "r") as file:
            sql = file.read()
        file.close()
        self.execute_cmd(sql, parameters)

    def execute_cmd(self, sql_script, parameters=None):
        print(f"About to run the following sql: {sql_script} parameters:", parameters)
        self.connection.cursor().execute(sql_script, parameters)
        self.commit()

    def switch_tables(self, schema_name, source_table_name, destination_table_name, archive_suffix):
        query = f"""drop table if exists {schema_name}.{destination_table_name}_{archive_suffix}; 
                    alter table if exists {schema_name}.{destination_table_name} rename to {destination_table_name}_{archive_suffix}; 
                    alter table if exists {schema_name}.{source_table_name} rename to {destination_table_name};"""
        self.execute_cmd(query)


def _generate_header_csv_option(has_header, is_csv_format):
    if has_header:
        return "csv header"
    elif is_csv_format:
        return "csv"
    else:
        return ""


def _generate_copy_command(columns_list, delimiter, encoding, has_header, is_csv_format, empty_string,
                           table_name, table_schema):
    copy_encoding = f"encoding '{encoding}'" if encoding else ""
    null_as = f"null as '{empty_string}'" if empty_string else ""
    copy_header = _generate_header_csv_option(has_header, is_csv_format)
    copy_columns_list = f'({",".join(columns_list)})' if columns_list else ""
    sql = f"""copy {table_schema}.{table_name} {copy_columns_list}
            from stdin with  delimiter '{delimiter}' {copy_header} {copy_encoding} {null_as} ;"""
    return sql
