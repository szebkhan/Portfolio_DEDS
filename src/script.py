import sqlite3
import pandas as pd
import warnings
import numpy as np
from settings import settings, logger
warnings.simplefilter('ignore')

import sqlite3
sales_conn = sqlite3.connect("/Users/shahzeb/Documents/CODE/PYTHON/project/data/raw/go_sales_train.sqlite")
sales_conn

def script():

    sales = pd.read_sql("SELECT * FROM product", sales_conn)

    country = pd.read_sql("SELECT * FROM country", sales_conn)

    retailer = pd.read_sql("SELECT * FROM retailer_site", sales_conn)

    returned = pd.read_sql("SELECT * FROM returned_item", sales_conn)

    branch = pd.read_sql("SELECT * FROM sales_branch", sales_conn)

    order = pd.read_sql("SELECT * FROM order_details", sales_conn)

    staff = pd.read_sql("SELECT * FROM sales_staff", sales_conn)

    order_header = pd.read_sql("SELECT * FROM order_header", sales_conn)

    details = pd.read_sql("SELECT * FROM order_details", sales_conn)

    salesSHOW = pd.read_sql("SELECT * FROM country WHERE COUNTRY_CODE = 1", sales_conn)

    product_type = pd.read_sql("SELECT * FROM product_type", sales_conn)

    reason = pd.read_sql("SELECT * FROM return_reason", sales_conn)

    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"

    pd.read_sql(sql_query, sales_conn)

    production_under_100_over_50: bool = ((sales["PRODUCTION_COST"] > 50) & (sales["PRODUCTION_COST"] < 100))

    filtered_sales_nodf = sales.loc[(production_under_100_over_50), ["PRODUCT_NUMBER", "PRODUCTION_COST"]]
    filtered_sales = pd.DataFrame(filtered_sales_nodf)
    filtered_sales.to_excel("data/processed/filtered_sales.xlsx", index=False)

    production_under_20_or_over_60_margin: bool = ((sales["MARGIN"] > 0.60) | (sales["MARGIN"] < 0.20))
    filtered_products_nodf = sales.loc[(production_under_20_or_over_60_margin), ["PRODUCT_NUMBER", "MARGIN"]]
    filtered_products = pd.DataFrame(filtered_products_nodf)
    filtered_products.to_excel("data/processed/filtered_products.xlsx", index=False)
    
    is_currency_francs = country["CURRENCY_NAME"] == "francs"
    country_with_francs = pd.DataFrame(country.loc[(is_currency_francs), :])
    country_with_francs.to_excel("data/processed/filtered_products.xlsx", index=False)
    

    production_over_50_margin: bool = sales["MARGIN"] > 0.50


    product_type_count = pd.DataFrame(sales.loc[(production_over_50_margin), ["INTRODUCTION_DATE"]].drop_duplicates("INTRODUCTION_DATE"))
    product_type_count.to_excel("data/processed/product_type_count.xlsx", index=False)

    is_region_empty = (branch["REGION"].notnull() & branch["ADDRESS2"].notnull())

    overview = branch.loc[is_region_empty, ["ADDRESS1", "CITY"]]
    overview.to_excel("data/processed/overview.xlsx", index=False)

    is_currency_dollars = ((country["CURRENCY_NAME"] == "dollars") | (country["CURRENCY_NAME"] == "new dollar"))


    country.loc[(is_currency_dollars), "COUNTRY"].sort_values()

    filter = ((retailer["POSTAL_ZONE"].astype(str).str[0] == "D") & (retailer["ADDRESS2"].notna()))

    retailer.loc[(filter), ["ADDRESS1", "ADDRESS2", "CITY"]]

    returns = returned["RETURN_QUANTITY"].sum()

    print(returns)

    regions = branch["REGION"].drop_duplicates().count()

    print(regions)

    min = sales["MARGIN"].min()
    max = sales["MARGIN"].max()

    sum = sales["MARGIN"].sum()
    count = sales["MARGIN"].count()

    avg = sum / count

    min_max_avg = {
        "min": min,
        "max": max,
        "avg": avg
    }

    min_max_avg_df = pd.Series(min_max_avg)

    retailers_no_address2 = retailer["ADDRESS2"].isna().sum()

    print(retailers_no_address2)

    avg_cost = order.loc[order["UNIT_SALE_PRICE"] < order["UNIT_PRICE"], "UNIT_COST"].mean()

    print(avg_cost)

    staff.groupby("POSITION_EN", as_index = False)["SALES_STAFF_CODE"].count()

    phones = staff.groupby("WORK_PHONE", as_index = False)["SALES_STAFF_CODE"].count()

    phones = phones[phones["SALES_STAFF_CODE"] > 4]


    retailer_country = pd.merge(retailer, country, left_on= 'COUNTRY_CODE', right_on='COUNTRY_CODE', how="left")

    is_country_nl = retailer_country["COUNTRY"] == "Netherlands"

    retailer_country.loc[(is_country_nl), ["ADDRESS1", "CITY"]]

    product_product_type = pd.merge(sales, product_type, left_on= 'PRODUCT_TYPE_CODE', right_on='PRODUCT_TYPE_CODE', how="left")

    product_is_eyewear = product_product_type["PRODUCT_TYPE_EN"] == "Eyewear"

    product_product_type = product_product_type.loc[(product_is_eyewear), "PRODUCT_NAME"]

    order_header_staff = pd.merge(order_header, staff, left_on= 'SALES_STAFF_CODE', right_on = 'SALES_STAFF_CODE', how="right")

    order_header_staff_retailer = pd.merge(order_header_staff, retailer, left_on= "RETAILER_SITE_CODE", right_on= "RETAILER_SITE_CODE", how="inner")

    is_staff_bm = order_header_staff_retailer["POSITION_EN"] == "Branch Manager"

    order_header_staff_retailer.loc[(is_staff_bm), ["ADDRESS1", "FIRST_NAME", "LAST_NAME"]].drop_duplicates()

    is_manager = order_header_staff["POSITION_EN"].str.contains("Manager")


    order_header_staff
    order_header_staff.loc[(is_manager), ["POSITION_EN", "ORDER_DATE"]].drop_duplicates()

    details_product = pd.merge(details, sales, left_on="PRODUCT_NUMBER", right_on="PRODUCT_NUMBER", how="inner")
    details_product_producttype = pd.merge(details_product, product_type, left_on="PRODUCT_TYPE_CODE", right_on="PRODUCT_TYPE_CODE", how="inner")

    is_bought_inbulkof_750 = details_product_producttype["QUANTITY"] > 750

    details_product_producttype.loc[(is_bought_inbulkof_750), ["PRODUCT_NAME", "PRODUCT_TYPE_EN"]].drop_duplicates("PRODUCT_NAME")

    product_details = pd.merge(sales, details, left_on="PRODUCT_NUMBER", right_on="PRODUCT_NUMBER", how="inner")

    is_sale_40p = ((product_details["UNIT_PRICE"] - product_details["UNIT_SALE_PRICE"]) / product_details["UNIT_PRICE"]) > 0.4

    pd.DataFrame(product_details.loc[(is_sale_40p), "PRODUCT_NAME"].drop_duplicates())

    returned_reason = pd.merge(returned, reason, left_on="RETURN_REASON_CODE", right_on="RETURN_REASON_CODE", how="inner")

    returned_reason_detail = pd.merge(returned_reason, details, left_on= "ORDER_DETAIL_CODE", right_on="ORDER_DETAIL_CODE", how="inner")

    return_perc = (returned_reason_detail["RETURN_QUANTITY"] / returned_reason_detail["QUANTITY"]) > 0.9

    pd.DataFrame(returned_reason_detail.loc[(return_perc), ["RETURN_DESCRIPTION_EN"]].drop_duplicates())

    product_producttype = pd.merge(product_type, sales, on="PRODUCT_TYPE_CODE", how="inner")

    product_producttype.groupby("PRODUCT_TYPE_EN", as_index= False)["PRODUCT_NUMBER"].count()

    country_retailer = pd.merge(country, retailer, on="COUNTRY_CODE", how="inner")

    country_retailer.groupby("COUNTRY", as_index= False)["RETAILER_SITE_CODE"].count()

    is_cooking_gear = details_product_producttype["PRODUCT_TYPE_EN"] == "Cooking Gear"

    cooking_gear = details_product_producttype.loc[(is_cooking_gear), ["PRODUCT_NAME", "PRODUCT_TYPE_EN", "QUANTITY"]]

    cooking_gear.groupby(["PRODUCT_NAME", "PRODUCT_TYPE_EN"], as_index= False)["QUANTITY"].agg({"QUANTITY" : "sum", "AVERAGE_PRICE" : "mean"})

    country_branch = pd.merge(country, branch, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")
    country_branch_retailer = pd.merge(country_branch, retailer, left_on="COUNTRY_CODE", right_on="COUNTRY_CODE")

    country_branch_retailer = country_branch_retailer.groupby(["COUNTRY", "CITY_x"], as_index=False)["RETAILER_CODE"].count()
    country_branch_retailer = country_branch_retailer.rename(columns={
        "CITY_x" : "SALES_MAN",
        "RETAILER_CODE" : "CUSTOMER"
    })
    country_branch_retailer

    not_in_sales = []

    staff_names_pd = pd.DataFrame()

    for index, row in staff.iterrows():
        if row["SALES_STAFF_CODE"] not in order_header["SALES_STAFF_CODE"].values:
            not_in_sales.append(row)

    staff_names_no_sales = pd.DataFrame(not_in_sales)

    staff_names_no_sales.loc[:, ["FIRST_NAME", "LAST_NAME"]]

    avg_margin = sales["MARGIN"].mean()

    lower_than_avg_products = []

    for index, row in sales.iterrows():
        margin = sales.at[index, "MARGIN"]

        if (margin < avg_margin):
            lower_than_avg_products.append(row)

    lower_than_avg = pd.DataFrame(lower_than_avg_products)

    list_for_avg_count = [
        int (lower_than_avg["MARGIN"].count()),
        float (lower_than_avg["MARGIN"].mean())
    ]

    pd.DataFrame(list_for_avg_count)


    returned_details = pd.merge(returned, details, on = "ORDER_DETAIL_CODE", how = "right")

    returned_details_products = pd.merge(returned_details, sales, on = "PRODUCT_NUMBER", how = "inner")

    is_unitprice_higher500 = ((returned_details_products["UNIT_PRICE"] > 500) & (returned_details_products["RETURN_CODE"].isna()))

    expensive_products = returned_details_products.loc[(is_unitprice_higher500), ["PRODUCT_NAME"]].drop_duplicates()

    staff_dupe = staff

    for index, row in staff_dupe.iterrows():
        current_function = staff_dupe.at[index, "POSITION_EN"]

        if "Manager" in current_function:
            staff_dupe.at[index, "IS_MANAGER"] = "YES"
        else:
            staff_dupe.at[index, "IS_MANAGER"] = "NO"

    staff_dupe.loc[:, ["LAST_NAME", "IS_MANAGER"]]

    from datetime import date
    date.today().year

    from datetime import datetime

    date_str = '16-8-2013'
    date_format = '%d-%m-%Y'
    date_obj = datetime.strptime(date_str, date_format)

    date_obj.year

    from datetime import date
    from datetime import datetime

    staff_dupe2 = staff

    now = date.today().year

    for index, row in staff_dupe2.iterrows():
        date_str = staff_dupe2.at[index, "DATE_HIRED"]
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_str, date_format)

        date_diff = now - date_obj.year

        if (date_diff < 25):
            staff_dupe2.at[index, "SHORT_IN_SERVICE"] = "short_in_service"
        else:
            staff_dupe2.at[index, "SHORT_IN_SERVICE"] = ""

        if (date_diff >= 12) :
            staff_dupe2.at[index, "LONG_IN_SERVICE"] = "long_in_service"
        else:
            staff_dupe2.at[index, "LONG_IN_SERVICE"] = ""

    staff_dupe2.loc[:, ["SALES_STAFF_CODE", "SHORT_IN_SERVICE", "LONG_IN_SERVICE"]]