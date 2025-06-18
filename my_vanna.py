import os
from vanna.openai import OpenAI_Chat
from openai import AzureOpenAI
from vanna.chromadb import ChromaDB_VectorStore


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):

    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(
            self,
            client=AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            ),
            config=config,
        )  # Make sure to put your AzureOpenAI client here


def train(vn: MyVanna):
    ddl = """
-- 媒体类型表
CREATE TABLE media_types (
    MediaTypeId INTEGER PRIMARY KEY,
    Name NVARCHAR(120) NOT NULL
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 音乐类型表
CREATE TABLE genres (
    GenreId INTEGER PRIMARY KEY,
    Name NVARCHAR(120) NOT NULL
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 艺术家表
CREATE TABLE artists (
    ArtistId INTEGER PRIMARY KEY,
    Name NVARCHAR(120) NOT NULL
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 专辑表
CREATE TABLE albums (
    AlbumId INTEGER PRIMARY KEY,
    Title NVARCHAR(160) NOT NULL, -- 补充标准字段
    ArtistId INTEGER NOT NULL,
    FOREIGN KEY (ArtistId) REFERENCES artists(ArtistId)
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 曲目表（核心表）
CREATE TABLE tracks (
    TrackId INTEGER PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,
    AlbumId INTEGER,
    MediaTypeId INTEGER NOT NULL,
    GenreId INTEGER,
    Composer NVARCHAR(220),
    Milliseconds INTEGER NOT NULL,
    Bytes INTEGER,
    UnitPrice NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (AlbumId) REFERENCES albums(AlbumId),
    FOREIGN KEY (MediaTypeId) REFERENCES media_types(MediaTypeId),
    FOREIGN KEY (GenreId) REFERENCES genres(GenreId)
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 播放列表表
CREATE TABLE playlists (
    PlaylistId INTEGER PRIMARY KEY,
    Name NVARCHAR(120) NOT NULL
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 播放列表-曲目关联表
CREATE TABLE playlist_track (
    PlaylistId INTEGER NOT NULL,
    TrackId INTEGER NOT NULL,
    PRIMARY KEY (PlaylistId, TrackId),
    FOREIGN KEY (PlaylistId) REFERENCES playlists(PlaylistId),
    FOREIGN KEY (TrackId) REFERENCES tracks(TrackId)
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 员工表
CREATE TABLE employees (
    EmployeeId INTEGER PRIMARY KEY,
    LastName NVARCHAR(20) NOT NULL,
    FirstName NVARCHAR(20) NOT NULL,
    Title NVARCHAR(30),
    ReportsTo INTEGER,
    BirthDate DATETIME,
    HireDate DATETIME,
    Address NVARCHAR(70) NOT NULL,
    City NVARCHAR(40) NOT NULL,
    State NVARCHAR(40),
    Country NVARCHAR(40) NOT NULL,
    PostalCode NVARCHAR(10),
    Phone NVARCHAR(24),
    Fax NVARCHAR(24),
    Email NVARCHAR(60) NOT NULL,
    FOREIGN KEY (ReportsTo) REFERENCES employees(EmployeeId)
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 客户表
CREATE TABLE customers (
    CustomerId INTEGER PRIMARY KEY,
    FirstName NVARCHAR(40) NOT NULL,
    LastName NVARCHAR(20) NOT NULL,
    Company NVARCHAR(80), -- 补充常用字段
    Address NVARCHAR(70) NOT NULL,
    City NVARCHAR(40) NOT NULL,
    State NVARCHAR(40),
    Country NVARCHAR(40) NOT NULL,
    PostalCode NVARCHAR(10),
    Phone NVARCHAR(24),
    Fax NVARCHAR(24),
    Email NVARCHAR(60) NOT NULL,
    SupportRepId INTEGER,
    FOREIGN KEY (SupportRepId) REFERENCES employees(EmployeeId)
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 发票表
CREATE TABLE invoices (
    InvoiceId INTEGER PRIMARY KEY,
    CustomerId INTEGER NOT NULL,
    InvoiceDate DATETIME NOT NULL,
    BillingAddress NVARCHAR(70) NOT NULL,
    BillingCity NVARCHAR(40) NOT NULL,
    BillingState NVARCHAR(40),
    BillingCountry NVARCHAR(40) NOT NULL,
    BillingPostalCode NVARCHAR(10),
    Total NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (CustomerId) REFERENCES customers(CustomerId)
);
"""
    vn.train(ddl=ddl)

    ddl = """
-- 发票项表
CREATE TABLE invoice_items (
    InvoiceLineId INTEGER PRIMARY KEY,
    InvoiceId INTEGER NOT NULL,
    TrackId INTEGER NOT NULL,
    UnitPrice NUMERIC(10,2) NOT NULL,
    Quantity INTEGER NOT NULL,
    FOREIGN KEY (InvoiceId) REFERENCES invoices(InvoiceId),
    FOREIGN KEY (TrackId) REFERENCES tracks(TrackId)
);
"""
    vn.train(ddl=ddl)


vn = MyVanna(
    config={
        "model": os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        "path": os.getenv("CHROMADB_PATH", "/data/chromadb"),
    }
)

vn.connect_to_sqlite("chinook.db")

training_data = vn.get_training_data()
if training_data.empty is False:
    print("Training data loaded successfully.")
else:
    print("No training data found.")
    train(vn)
