#coding:utf-8
import configparser

settings = configparser.ConfigParser()
settings.read("hista.conf")

ROLE = settings.get("main", "role").lower()

MYSQL_HOST = settings.get("db", "mysql_host")
MYSQL_PORT = settings.getint("db", "mysql_port")
MYSQL_USER = settings.get("db", "mysql_user")
MYSQL_PASSWORD = settings.get("db", "mysql_password")
REDIS_HOST = settings.get("db", "redis_host")
REDIS_PORT = settings.getint("db", "redis_port")

SERIAL_CACHE = "SERIALNUMBER:{}"
BUCKET_BASE_PATH = "/Users/gao/hista"

# MAX_SAVED_VERSION = 10  # 最多保存10个版本。0 表示保存所有版本。标记为 important 的对象不受此限制，会保存所有版本。

