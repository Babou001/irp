C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker ps -a
CONTAINER ID   IMAGE             COMMAND                  CREATED       STATUS       PORTS     NAMES
69908734c676   prom/prometheus   "/bin/prometheus --c…"   2 hours ago   Up 2 hours             k8s_prometheus_prometheus-558f9d6497-7k8m9_default_690ae938-2df3-4850-a0e5-d1998750ba20_2
bf96676d19f9   grafana/grafana   "/run.sh"                2 hours ago   Up 2 hours             k8s_grafana_grafana-6957bcf98-rddk6_default_93f4d09e-5cd4-44e5-9c59-8851f618b512_2
aec28ea0f4bc   3081609656b3      "uvicorn src.api:app…"   2 hours ago   Up 2 hours             k8s_iris-api_iris-classifier-85b7874df6-jts9c_default_f4d3c6b4-07ad-4bc9-b3c9-79ea96528e46_2
2666af9a7533   3081609656b3      "uvicorn src.api:app…"   2 hours ago   Up 2 hours             k8s_iris-api_iris-classifier-85b7874df6-vr9bw_default_94fa7f2a-b300-4576-9bea-ee850b36e4ec_2
225f5b0476fc   3081609656b3      "uvicorn src.api:app…"   2 hours ago   Up 2 hours             k8s_iris-api_iris-classifier-85b7874df6-wxpk8_default_e3678b81-6b41-4fe1-8447-faf0da9f94ce_2

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker logs rag-fastapi --tail 100
Error response from daemon: No such container: rag-fastapi

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker logs milvus-standalone --tail 50  
Error response from daemon: No such container: milvus-standalone

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>curl http://localhost:8000/             
curl: (7) Failed to connect to localhost port 8000 after 2248 ms: Could not connect to server

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>curl http://localhost:8501  
curl: (7) Failed to connect to localhost port 8501 after 2228 ms: Could not connect to server

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>