#coding:utf-8
import configparser

settings = configparser.ConfigParser()
settings.read("hista.conf")

PORT = settings.getint("main", "port")
ROLE = settings.get("main", "role").lower()
DATA_PATH = settings.get("main", "data_path")

MYSQL_DB = settings.get("db", "mysql_db")
MYSQL_HOST = settings.get("db", "mysql_host")
MYSQL_PORT = settings.getint("db", "mysql_port")
MYSQL_USER = settings.get("db", "mysql_user")
MYSQL_PASSWORD = settings.get("db", "mysql_password")
REDIS_HOST = settings.get("db", "redis_host")
REDIS_PORT = settings.getint("db", "redis_port")

SERIAL_CACHE = "SERIALNUMBER:{}"


# MAX_SAVED_VERSION = 10  # 最多保存10个版本。0 表示保存所有版本。标记为 important 的对象不受此限制，会保存所有版本。

