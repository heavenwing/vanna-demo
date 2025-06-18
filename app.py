
from vanna.flask import VannaFlaskApp
from my_vanna_sqlite import vn

app = VannaFlaskApp(vn, allow_llm_to_see_data=True)
app.run()
