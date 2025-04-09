import pandas as pd
import pyodbc
from datetime import datetime


def script():
    go_sales_conn = sqlite3.connect("../../../data/raw/go_sales_volledig.sqlite")
    go_crm_conn = sqlite3.connect("../../../data/raw/go_crm_volledig.sqlite")
    go_staff_conn = sqlite3.connect("../../../data/raw/go_staff_volledig.sqlite")


    DB = {"servername": r"localhost,1433", "database": "sdm", "username": "sa", "password": "iDTyjZx7dRL4"}

    sdm = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB['servername']};"
        f"DATABASE={DB['database']};"
        f"UID={DB['username']};"
        f"PWD={DB['password']}"
    )

    def create_dataframes_sql(connection, db_type):
        dictionary : dict = {}
        query : str = ""
        key : str = ""

        if (db_type == "sqlite"):
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            key = "name"
        elif (db_type == "ssms"):
            query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
            key = "TABLE_NAME"

        table_names = pd.read_sql(query, connection)

        for table in table_names[key].tolist():
            dictionary[table] = pd.read_sql(f"SELECT * FROM {table}", connection)

        return dictionary

    go_sales_tables = create_dataframes_sql(go_sales_conn, "sqlite")
    go_crm_tables = create_dataframes_sql(go_crm_conn, "sqlite")
    go_staff_tables = create_dataframes_sql(go_staff_conn, "sqlite")

    sdm_current = create_dataframes_sql(sdm, "ssms")

    go_sdm_tables = go_sales_tables | go_crm_tables | go_staff_tables # Alle drie mergen in 1 Dictionary met alle DataFrames

    # DataFrames met ontbrekende/verkeerd genoemde rows updaten:
    go_sdm_tables["country"]["LANGUAGE"] = go_sales_tables["country"]["LANGUAGE"]

    go_sdm_tables["country"]["CURRENCY_NAME"] = go_sales_tables["country"]["CURRENCY_NAME"]

    go_sdm_tables["country"] = go_sdm_tables["country"].rename(columns={'COUNTRY_EN': 'COUNTRY'})

    go_sdm_tables["product_line"] = go_sales_tables["product_line"]

    try:
        go_sdm_tables["retailer_headquarters"].drop('POSTAL_ZONE', axis=1, inplace=True)
    except KeyError:
        print("Removal of Postal Zone in tables has already been complete.")

    def merge_and_remove_duplicates(sdm_current, sdm_new):
        merged_dfs = {}
        for table in sdm_new:
            if table in sdm_current:
                combined = pd.concat([sdm_current[table], sdm_new[table]], ignore_index=True)
                new_rows_only = combined.drop_duplicates()
            else:
                new_rows_only = sdm_new[table]
            merged_dfs[table] = new_rows_only
        return merged_dfs

    sdm_new = merge_and_remove_duplicates(sdm_current, go_sdm_tables)

    # Dictionary in goede volgorde zetten (om inserts goed te laten werken):
    dict_order = [
        'sales_territory', 
        'country', 
        'order_method', 
        'retailer_site', 
        'sales_branch', 
        'sales_staff', 
        'retailer_contact', 
        'order_header', 
        'product_line', 
        'product_type', 
        'product', 
        'order_details', 
        'return_reason', 
        'returned_item', 
        'course', 
        'satisfaction_type', 
        'satisfaction', 
        'training',
        'age_group',
        'retailer_segment',
        'retailer_headquarters',
        'retailer_type',
        'retailer'
        'sales_demographic',
        'inventory_levels',
        'forecast'
    ]

    sdm_new = {k: sdm_new[k] for k in dict_order if k in sdm_new}

    export_cursor = sdm.cursor()

    for table_name, df in sdm_new.items():
        try:
            for index, row in df.iterrows():
                columns = df.columns.tolist()

                values = []
                for col in columns:
                    value = row[col]

                    if pd.isna(value):
                        values.append("NULL")

                    elif isinstance(value, str):
                        values.append(f"'{value.replace("'", "''")}'")

                    else:
                        values.append(str(value))

                column_names = ", ".join(columns)
                value_string = ", ".join(values)
                query = f"INSERT INTO {table_name} ({column_names}) VALUES ({value_string})"

                export_cursor.execute(query)
        except pyodbc.Error as e:
            print(f"Error in table: {table_name}")
            print(f"Query: {query}")
            print(f"Error message: {e}")
            print("-" * 80)

    sdm.commit()
    export_cursor.close()

    DB_SDM = {"servername": r"localhost,1433", "database": "sdm", "username": "sa", "password": "iDTyjZx7dRL4"}
    DB_DWH = {"servername": r"localhost,1433", "database": "dwh", "username": "sa", "password": "iDTyjZx7dRL4"}


    import_conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SDM['servername']};"
        f"DATABASE={DB_SDM['database']};"
        f"UID={DB_SDM['username']};"
        f"PWD={DB_SDM['password']}"
    )

    export_conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_DWH['servername']};"
        f"DATABASE={DB_DWH['database']};"
        f"UID={DB_DWH['username']};"
        f"PWD={DB_DWH['password']}"
    )

    def create_dataframes_sql(connection):
        dictionary : dict = {}
        query : str = ""
        key : str = ""

        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
        key = "TABLE_NAME"

        table_names = pd.read_sql(query, connection)

        for table in table_names[key].tolist():
            dictionary[table] = pd.read_sql(f"SELECT * FROM {table}", connection)

        return dictionary

    sdm = create_dataframes_sql(import_conn)

    print(list(sdm.keys()))

    order_details = sdm["order_details"]
    order_details = pd.merge(order_details, sdm["order_header"], left_on="ORDER_NUMBER", how="inner", right_on="ORDER_NUMBER")
    order_details = pd.merge(order_details, sdm["order_method"], left_on="ORDER_METHOD_CODE", how="inner", right_on="ORDER_METHOD_CODE")
    order_details = pd.merge(order_details, sdm["returned_item"], left_on="ORDER_DETAIL_CODE", how="inner", right_on="ORDER_DETAIL_CODE")
    order_details = order_details.drop(columns=["ORDER_NUMBER", "RETURN_CODE", "ORDER_METHOD_CODE"])
    order_details["REVENUE"] = order_details["UNIT_SALE_PRICE"] * order_details["QUANTITY"]
    order_details["TOTAL_COST"] = order_details["UNIT_COST"] * order_details["QUANTITY"]


    product = sdm["product"]
    product = pd.merge(product, sdm["product_type"], left_on="PRODUCT_TYPE_CODE", how="inner", right_on="PRODUCT_TYPE_CODE")
    product = pd.merge(product, sdm["product_line"], left_on="PRODUCT_LINE_CODE", how="inner", right_on="PRODUCT_LINE_CODE")
    product = product.drop(columns=["PRODUCT_TYPE_CODE", "PRODUCT_LINE_CODE"])
    current_year = datetime.now().year
    product["PRODUCT_AGE"] = current_year - (pd.to_datetime(product["INTRODUCTION_DATE"]).dt.year)

    retailer_site = sdm["retailer_site"]
    retailer_site = pd.merge(retailer_site, sdm["country"], left_on="COUNTRY_CODE", how="inner", right_on="COUNTRY_CODE")
    retailer_site = retailer_site.drop(columns=["RETAILER_CODE", "COUNTRY_CODE", "FLAG_IMAGE", "SALES_TERRITORY_CODE"])

    sales_staff = sdm["sales_staff"]
    sales_staff["FULL_NAME"] = sales_staff["FIRST_NAME"] + " " + sales_staff["LAST_NAME"]
    sales_staff = sales_staff.drop(columns=["FIRST_NAME", "LAST_NAME", "WORK_PHONE", "FAX", "EMAIL"])
    sales_staff["YEARS_OF_EXPERIENCE"] = current_year - (pd.to_datetime(sales_staff["DATE_HIRED"]).dt.year)
    sales_staff

    dwh_dict = {
        "sales_staff": sales_staff,
        "retailer_site": retailer_site,
        "product": product,
        "inventory_levels": sdm["inventory_levels"],
        "order_details": order_details
    }

    export_cursor = export_conn.cursor()

    for table_name, df in dwh_dict.items():
        try:
            for index, row in df.iterrows():
                columns = df.columns.tolist()

                values = []
                for col in columns:
                    value = row[col]

                    if pd.isna(value):
                        values.append("NULL")

                    elif isinstance(value, str):
                        values.append(f"'{value.replace("'", "''")}'")

                    else:
                        values.append(str(value))

                column_names = ", ".join(columns)
                value_string = ", ".join(values)
                query = f"INSERT INTO {table_name} ({column_names}) VALUES ({value_string})"

                export_cursor.execute(query)
        except pyodbc.Error as e:
            print(f"Error in table: {table_name}")
            print(f"Query: {query}")
            print(f"Error message: {e}")
            print("-" * 80)

    export_conn.commit()
    export_cursor.close()
