Azure sql done easy


if __name__=="__main__":
    creds=["#####@#####sqlserver","#####","#####_team","#####sqlserver.database.windows.net"]
    table="#####_item_attrs_temp"
    if True and "read":
        sql="select TOP(10) * from {}".format(table)
        print(sql_df(sql,*creds))
    if True and "write":
        df=pd.DataFrame([{"Artykul":"101-404-451",}])
        print(df_sql(df,table,*creds))
    if True and "query":
        query("delete from {}".format(table),*creds)
        if True and "insert":
        cnxn,c=connect(*creds)
        insert(c,table,{"Artykul":"101-404-451","Brand":"Huawei"},commit=True)
        insert(c,table,{"Artykul":"101-404-451","Brand":"Apple"},commit=True,replace="Artykul")
