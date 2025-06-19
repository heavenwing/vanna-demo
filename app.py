
from vanna.flask import VannaFlaskApp
from my_vanna_databricks import vn

app = VannaFlaskApp(vn, allow_llm_to_see_data=True)
app.run()
