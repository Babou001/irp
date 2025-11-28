C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>dir .env
 Volume in drive C is Windows
 Volume Serial Number is AC97-4896

 Directory of C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp

File Not Found

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>copy .env.example .env
        1 file(s) copied.

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker-compose -f docker-compose.prod.yml up -d
[+] Running 40/40
 ✔ etcd Pulled                                                                                                                                                                                                         52.3s 
 ✔ redis Pulled                                                                                                                                                                                                        33.5s 
 ✔ minio Pulled                                                                                                                                                                                                        49.4s 
 ✔ milvus Pulled                                                                                                                                                                                                       94.1s 
[+] Running 14/15
 ✔ Network irp_rag-network       Created                                                                                                                                                                                0.2s 
 ✔ Volume "irp_redis_data"       Created                                                                                                                                                                                0.0s 
 ✔ Volume "irp_prometheus_data"  Created                                                                                                                                                                                0.0s 
 ✔ Volume "irp_grafana_data"     Created                                                                                                                                                                                0.0s 
 ✔ Volume "irp_etcd_data"        Created                                                                                                                                                                                0.0s 
 ✔ Volume "irp_minio_data"       Created                                                                                                                                                                                0.0s 
 ✔ Volume "irp_milvus_data"      Created                                                                                                                                                                                0.0s 
 - Container milvus-minio        Starting                                                                                                                                                                               2.8s 
 ✔ Container rag-prometheus      Started                                                                                                                                                                                2.7s 
 ✔ Container milvus-etcd         Started                                                                                                                                                                                2.7s 
 ✔ Container rag-redis           Started                                                                                                                                                                                2.7s 
 ✔ Container rag-grafana         Created                                                                                                                                                                                0.3s 
 ✔ Container milvus-standalone   Created                                                                                                                                                                                0.2s 
 ✔ Container rag-fastapi         Created                                                                                                                                                                                0.2s 
 ✔ Container rag-streamlit       Created                                                                                                                                                                                0.2s 
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:9000 -> 127.0.0.1:0: listen tcp 0.0.0.0:9000: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>