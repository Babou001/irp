# reset_collection.py
from pymilvus import connections, utility
import paths

COLL = getattr(paths, "MILVUS_COLLECTION", "rag_docs")

# Connexion (prend URI si défini, sinon host/port)
uri = getattr(paths, "MILVUS_URI", None)
if uri:
    connections.connect(alias="default", uri=uri)
else:
    host = getattr(paths, "MILVUS_HOST", "127.0.0.1")
    port = str(getattr(paths, "MILVUS_PORT", "19530"))
    connections.connect(alias="default", uri=f"http://{host}:{port}")

if utility.has_collection(COLL):
    utility.drop_collection(COLL)
    print(f"Dropped collection: {COLL}")
else:
    print(f"Collection not found: {COLL}")
