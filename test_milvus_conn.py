from pymilvus import connections, utility
import os
for v in ("http_proxy","https_proxy","HTTP_PROXY","HTTPS_PROXY","ALL_PROXY","all_proxy"):
    os.environ.pop(v, None)

connections.connect(host="127.0.0.1", port=19530, alias="default", timeout=5)
print("connected ok")
print("server version:", utility.get_server_version())
print("collections:", utility.list_collections())
