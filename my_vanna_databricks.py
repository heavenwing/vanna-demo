import os
import pandas as pd
from vanna.openai import OpenAI_Chat
from openai import AzureOpenAI
from vanna.chromadb import ChromaDB_VectorStore
from vanna.exceptions import DependencyError, ImproperlyConfigured, ValidationError

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

    def connect_to_databricks(
        self, hostname: str, http_path: str, access_token: str, **kwargs
    ):
        """
        Connect to a Databricks database. This is just a helper function to set [`vn.run_sql`][vanna.base.base.VannaBase.run_sql]

        Args:
            hostname (str): The hostname of the Databricks workspace.
            http_path (str): The HTTP path to the Databricks SQL endpoint.
            access_token (str): The access token for authentication.

        Returns:
            None
        """
        try:
            from databricks import sql
        except ImportError:
            raise DependencyError(
                "You need to install required dependencies to execute this method,"
                " run command: pip install databricks-sql-connector"
            )

        
        connection = sql.connect(
            server_hostname=hostname,
            http_path=http_path,
            access_token=access_token
        )

        def run_sql_mssql(sql: str):
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()
                return pd.DataFrame(data, columns=columns)

        self.dialect = "T-SQL / Databricks SQL"
        self.run_sql = run_sql_mssql
        self.run_sql_is_set = True


vn = MyVanna(
    config={
        "model": os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        "path": os.getenv("CHROMADB_PATH", "/data/chromadb"),
    }
)

vn.connect_to_databricks(
    hostname=os.getenv("DATABRICKS_HOSTNAME"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_ACCESS_TOKEN"),
)

training_data = vn.get_training_data()
if training_data.empty is False:
    print("Training data loaded successfully.")
else:
    print("No training data found.")
    ddl="""
CREATE TABLE sales_data_2025 (
    date DATE,
    region VARCHAR(100),
    dealer VARCHAR(100),
    retailer VARCHAR(100),
    store VARCHAR(100),
    product VARCHAR(100),
    sku VARCHAR(100),
    units_sold BIGINT,
    revenue DOUBLE
);
"""
    vn.train(ddl=ddl)
