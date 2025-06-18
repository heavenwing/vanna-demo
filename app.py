
from vanna.flask import VannaFlaskApp
from my_vanna import vn

app = VannaFlaskApp(vn, allow_llm_to_see_data=True)
app.run()
