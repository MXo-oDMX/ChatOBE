"""
一些辅助类/方法
"""

import tiktoken
import config
import pymysql
from config import DATABASE_CONFIG

enc = tiktoken.encoding_for_model(config.MODEL)

def count_token(text):
    """计算text对应的token数"""
    tokens = enc.encode(text)
    return len(tokens)


def get_db_connection():
    """建立数据库连接"""
    conn = pymysql.connect(
        host=DATABASE_CONFIG["host"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        port=DATABASE_CONFIG["port"],
        charset=DATABASE_CONFIG["charset"],
        database=DATABASE_CONFIG["database"],
    )
    return conn


def query_database(sql):
    """执行sql语句并返回结果"""
    try:
        # 正常情况：执行sql并提交事务、返回结果
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
            conn.commit()
        return f"Success, get: {str(results)}"
    except Exception as e:
        # 出现异常：返回报错
        return f"Fail, error: {str(e)}"


def sql_in_text(text):
    """判断text中是否有sql语句"""
    return config.SQL_START in text and config.SQL_END in text


def extract_sql(text):
    """从text中提取sql语句"""
    start = text.find(config.SQL_START) + len(config.SQL_START)
    end = text.find(config.SQL_END)
    return text[start:end].strip()
