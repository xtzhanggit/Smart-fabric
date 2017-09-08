import pymysql

def get():
    """
    读取数据库信息
    """
    conn = pymysql.connect(host='119.29.241.15', port=3306 ,user='root', passwd='acehjl057', db='iot', charset='utf8mb4')
    cursor = conn.cursor()

    ## 获取id行
    sql_id = "select id from accounts"
    cursor.execute(sql_id)
    result_id = cursor.fetchall()

    ## 获取password行
    sql_password = "select password from accounts"
    cursor.execute(sql_password)
    result_password = cursor.fetchall()
    cursor.close()
    conn.close()
    return result_id, result_password



if __name__ == "__main__":
    result_id, result_password = get()
    print(result_id, result_password)

