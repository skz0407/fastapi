import os

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable

from models import Base

# データベースエンジンの作成
DATABASE = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE)

# CREATE TABLE ステートメントを生成してファイルに保存
with open("create_tables.sql", "w") as f:
    for table in Base.metadata.sorted_tables:
        create_table_sql = str(CreateTable(table).compile(engine))
        f.write(f"{create_table_sql};\n")
        f.write("\n")
