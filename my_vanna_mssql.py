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

vn = MyVanna(
    config={
        "model": os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        "path": os.getenv("CHROMADB_PATH", "/data/chromadb"),
    }
)

vn.connect_to_mssql(odbc_conn_str='DRIVER={ODBC Driver 17 for SQL Server};SERVER=myserver;DATABASE=mydatabase;UID=myuser;PWD=mypassword') # You can use the ODBC connection string here
