#coding:utf-8

import ctypes


LENGTH = 50
DB_META_DB = "meta.db"
DATA_META_DB = "data_meta.db"

class MetaStruct(ctypes.Structure):
    # table 元数据
    _fields_ = [
        ("database", ctypes.c_char * LENGTH),
        ("table", ctypes.c_char * LENGTH),
        ("primary_key", ctypes.c_char * LENGTH),
        ("columns", ctypes.c_char * LENGTH),
        ("auto_pk_value", ctypes.c_int),
        ("offset", ctypes.c_int)
    ]

class DataMetaStruct(ctypes.Structure):
    # 相当于索引
    _fields_ = [
        ("database", ctypes.c_char * LENGTH),
        ("table", ctypes.c_char * LENGTH),
        ("primary_key", ctypes.c_char * LENGTH),
        ("primary_value", ctypes.c_int),
        # ("value_md5_hash", ctypes.c_char * LENGTH),
        ("offset", ctypes.c_int)
    ]

class BucketStruct(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_int),
        ("name", ctypes.c_char * 50),
        ("public", ctypes.c_bool)
    ]

def struct_to_bytes(struct_obj):
    # return ctypes.string_at(ctypes.addressof(struct_obj), ctypes.sizeof(struct_obj))
    return bytes(struct_obj)

def bytes_to_struct(struct, content):
    if not isinstance(struct, ctypes.Structure):
        return None
    return struct.from_buffer_copy(content)

def to_bytes(value):
    if isinstance(value, str):
        value = bytes(value, "utf8")
    if not isinstance(value, bytes):
        raise Exception("Type Error: bytes expect, but {} found, value = {}".format(type(value), value))
    return value

def add_bucket(name, public):
    pk_value = get_auto_pk_value(database="hista", table="bucket")
    print("pk_value = ", pk_value)
    bucket = BucketStruct()
    bucket.id     = pk_value
    bucket.name   = to_bytes(name)
    bucket.public = public
    # md5_hash = hashlib.md5(bucket_bytes).hexdigest()
    with open("hista.db", "ab+") as f:
        f.write(bytes(bucket))
    create_data_meta(database=b"hista", table=b"bucket", primary_key=b"id", primary_value=pk_value)


def find_bucket(name):
    bucket = None
    with open("hista.db", "rb") as f:
        content = f.read(ctypes.sizeof(BucketStruct))
        while content:
            bucket = BucketStruct.from_buffer_copy(content)
            if bucket.name == name:
                break
            content = f.read(ctypes.sizeof(BucketStruct))
    return bucket

def get_table_meta(database, table):
    table = to_bytes(table)
    database = to_bytes(database)
    meta = None
    with open(DB_META_DB, "rb") as f:
        content = f.read(ctypes.sizeof(MetaStruct))
        while content:
            meta = MetaStruct.from_buffer_copy(content)
            if meta.database == database and meta.table == table:
                break
            content = f.read(ctypes.sizeof(MetaStruct))
    return meta

def create_db_meta(database, table, primary_key, columns):
    table       = to_bytes(table)
    columns     = to_bytes(columns)
    database    = to_bytes(database)
    primary_key = to_bytes(primary_key)

    meta = MetaStruct()
    meta.database = database
    meta.table = table
    meta.primary_key = primary_key
    meta.columns = columns
    meta.auto_pk_value = 0
    with open(DB_META_DB, "ab+") as f:
        meta.offset = f.tell()
        f.write(bytes(meta))

def get_auto_pk_value(database, table):
    # get pk_value, then incr it.
    meta = get_table_meta(database, table)
    meta.auto_pk_value = meta.auto_pk_value + 1
    with open(DB_META_DB, "ab+") as f:
        print("offset = ", meta.offset)
        f.seek(meta.offset)
        f.write(bytes(meta))
    return meta.auto_pk_value

def create_data_meta(database, table, primary_key, primary_value):
    table = to_bytes(table)
    database = to_bytes(database)
    primary_key = to_bytes(primary_key)
    # primary_value = to_bytes(primary_value)

    data_meta = DataMetaStruct()
    data_meta.database = database
    data_meta.table = table
    data_meta.primary_key = primary_key
    data_meta.primary_value = primary_value
    with open(DATA_META_DB, "ab+") as f:
        data_meta.offset = f.tell()
        print("data meta offset = ", data_meta.offset)
        f.write(bytes(data_meta))

def get_data_meta(database, table, primary_key, primary_value):
    meta = None
    with open(DATA_META_DB, "rb") as f:
        content = f.read(ctypes.sizeof(DataMetaStruct))
        while content:
            meta = MetaStruct.from_buffer_copy(content)
            if meta.database == database and meta.table == table and meta.primary_key == primary_key and meta.primary_value == primary_value:
                break
            content = f.read(ctypes.sizeof(MetaStruct))
    return meta

def create_database(database):
    pass

def create_tables():
    create_db_meta(database="hista", table="bucket", primary_key="id", columns="")

if __name__ == "__main__":
    # create_tables()
    add_bucket(name="album3", public=1)
    bucket = find_bucket("album3")
    print("bucket id = ", bucket.id)
    print("bucket name = ", bucket.name)
    print("bucket public = ", bucket.public)
    