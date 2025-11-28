C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker build -f Dockerfile.prod -t rag-system:prod .
[+] Building 1.6s (22/22) FINISHED                                                                                                                                                                      docker:desktop-linux
 => [internal] load build definition from Dockerfile.prod                                                                                                                                                               0.0s
 => => transferring dockerfile: 3.50kB                                                                                                                                                                                  0.0s
 => WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)                                                                                                                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                                                                                     1.2s
 => [internal] load .dockerignore                                                                                                                                                                                       0.0s
 => => transferring context: 1.44kB                                                                                                                                                                                     0.0s
 => [internal] load build context                                                                                                                                                                                       0.1s
 => => transferring context: 9.68kB                                                                                                                                                                                     0.0s
 => [builder 1/6] FROM docker.io/library/python:3.11-slim@sha256:193fdd0bbcb3d2ae612bd6cc3548d2f7c78d65b549fcaa8af75624c47474444d                                                                                       0.0s
 => CACHED [stage-1  2/12] RUN apt-get update && apt-get install -y     libgomp1     curl     && rm -rf /var/lib/apt/lists/*                                                                                            0.0s
 => CACHED [builder 2/6] WORKDIR /app                                                                                                                                                                                   0.0s
 => CACHED [builder 3/6] RUN apt-get update && apt-get install -y     build-essential     wget     git     && rm -rf /var/lib/apt/lists/*                                                                               0.0s
 => CACHED [builder 4/6] COPY requirements.txt .                                                                                                                                                                        0.0s
 => CACHED [builder 5/6] RUN python -m venv /opt/venv                                                                                                                                                                   0.0s 
 => CACHED [builder 6/6] RUN pip install --no-cache-dir --upgrade pip setuptools wheel &&     pip install --no-cache-dir -r requirements.txt                                                                            0.0s 
 => CACHED [stage-1  3/12] COPY --from=builder /opt/venv /opt/venv                                                                                                                                                      0.0s 
 => CACHED [stage-1  4/12] RUN useradd -m -u 1000 appuser &&     mkdir -p /app/data /app/uploads /app/preprocessed_data &&     chown -R appuser:appuser /app                                                            0.0s 
 => CACHED [stage-1  5/12] WORKDIR /app                                                                                                                                                                                 0.0s 
 => CACHED [stage-1  6/12] COPY --chown=appuser:appuser *.py ./                                                                                                                                                         0.0s 
 => CACHED [stage-1  7/12] COPY --chown=appuser:appuser streamlit_pages/ ./streamlit_pages/                                                                                                                             0.0s 
 => CACHED [stage-1  8/12] COPY --chown=appuser:appuser .streamlit/ ./.streamlit/                                                                                                                                       0.0s 
 => CACHED [stage-1  9/12] COPY --chown=appuser:appuser requirements.txt ./                                                                                                                                             0.0s 
 => CACHED [stage-1 10/12] COPY --chown=appuser:appuser models/ ./models/                                                                                                                                               0.0s 
 => CACHED [stage-1 11/12] RUN ls -lh /app/models/ &&     echo "✅ Models successfully embedded in image"                                                                                                                0.0s
 => CACHED [stage-1 12/12] RUN mkdir -p /app/images /app/videos &&     chown -R appuser:appuser /app                                                                                                                    0.0s 
 => exporting to image                                                                                                                                                                                                  0.0s 
 => => exporting layers                                                                                                                                                                                                 0.0s 
 => => writing image sha256:c8551aaf5923766760784335d0d57cab7832ae830ae4c9f0c0ab350a32017c8a                                                                                                                            0.0s 
 => => naming to docker.io/library/rag-system:prod                                                                                                                                                                      0.0s 

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/gjhrw0xx4bka1mp0966xmfwkp

 1 warning found (use docker --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>copy .env.example .env
Overwrite .env? (Yes/No/All): yes
        1 file(s) copied.

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker-compose -f docker-compose.prod.yml up -d
[+] Running 8/8
 ✔ Container milvus-etcd        Healthy                                                                                                                                                                                 1.2s 
 ✔ Container rag-redis          Healthy                                                                                                                                                                                32.2s 
 ✔ Container rag-prometheus     Running                                                                                                                                                                                 0.0s 
 ✔ Container milvus-standalone  Healthy                                                                                                                                                                                37.2s 
 ✔ Container milvus-minio       Healthy                                                                                                                                                                                31.2s 
 ✔ Container rag-grafana        Started                                                                                                                                                                                 0.4s 
 ✔ Container rag-fastapi        Healthy                                                                                                                                                                                79.5s 
 ✔ Container rag-streamlit      Started                                                                                                                                                                                 0.6s 

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>timeout /t 120

Waiting for   0 seconds, press a key to continue ...

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker logs rag-fastapi
2025-11-28 13:13:32.824819: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025-11-28 13:13:39.045830: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 AVX512F AVX512_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2025-11-28 13:13:47.381806: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:56492 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:50626 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:50248 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:54198 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55644 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:38178 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:58776 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:51162 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:35758 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:46530 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:48056 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:57394 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:38058 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:35786 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:48752 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:56376 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60790 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:35150 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:39012 - "GET /metrics HTTP/1.1" 404 Not Found

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker logs rag-fastapi
2025-11-28 13:13:32.824819: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025-11-28 13:13:39.045830: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 AVX512F AVX512_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2025-11-28 13:13:47.381806: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:56492 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:50626 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:50248 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:54198 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55644 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:38178 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:58776 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:51162 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:35758 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:46530 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:48056 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:57394 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:38058 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:35786 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:48752 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:56376 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60790 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:35150 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:39012 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:44038 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:47970 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:46790 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.1:43850 - "GET /docs HTTP/1.1" 200 OK
INFO:     172.18.0.1:43850 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     172.18.0.2:57138 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:39516 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:36456 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:37008 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:45324 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:47798 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:39476 - "GET / HTTP/1.1" 200 OK
INFO:     172.18.0.2:55498 - "GET /metrics HTTP/1.1" 404 Not Found
INFO:     172.18.0.2:43444 - "GET /metrics HTTP/1.1" 404 Not Found

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker run --rm rag-system:prod ls -lh /app/models/
total 2.3G
-rwxr-xr-x 1 appuser appuser 2.3G Nov 28 11:15 Llama-3.2-3B-Instruct-Q5_K_L.gguf
dr-xr-xr-x 1 appuser appuser 4.0K Aug 12 07:52 all-mpnet-base-v2

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker ps
CONTAINER ID   IMAGE                                      COMMAND                  CREATED          STATUS                    PORTS                                              NAMES
7e90bf670e2d   minio/minio:RELEASE.2024-05-28T17-19-04Z   "/usr/bin/docker-ent…"   6 minutes ago    Up 6 minutes (healthy)    0.0.0.0:9002->9000/tcp, 0.0.0.0:9003->9001/tcp     milvus-minio
cb174b4e7442   rag-system:prod                            "streamlit run strea…"   10 minutes ago   Up 4 minutes (healthy)    8000/tcp, 0.0.0.0:8501->8501/tcp                   rag-streamlit
1d0a5f6a8d91   rag-system:prod                            "uvicorn fast_api_ap…"   10 minutes ago   Up 5 minutes (healthy)    0.0.0.0:8000->8000/tcp, 8501/tcp                   rag-fastapi
074d0f0b8f94   milvusdb/milvus:v2.4.11                    "/tini -- milvus run…"   10 minutes ago   Up 6 minutes (healthy)    0.0.0.0:9091->9091/tcp, 0.0.0.0:19530->19530/tcp   milvus-standalone
df81f632e16e   grafana/grafana:latest                     "/run.sh"                10 minutes ago   Up 6 minutes              0.0.0.0:3000->3000/tcp                             rag-grafana
a961f4d9c9d8   quay.io/coreos/etcd:v3.5.12                "/usr/local/bin/etcd"    10 minutes ago   Up 10 minutes (healthy)   2379-2380/tcp                                      milvus-etcd
45716c27f3aa   prom/prometheus:latest                     "/bin/prometheus --c…"   10 minutes ago   Up 10 minutes             0.0.0.0:9090->9090/tcp                             rag-prometheus
326cd68d9cf5   redis:7-alpine                             "docker-entrypoint.s…"   10 minutes ago   Up 10 minutes (healthy)   0.0.0.0:6379->6379/tcp                             rag-redis
69908734c676   prom/prometheus                            "/bin/prometheus --c…"   2 hours ago      Up 2 hours                                                                   k8s_prometheus_prometheus-558f9d6497-7k8m9_default_690ae938-2df3-4850-a0e5-d1998750ba20_2
bf96676d19f9   grafana/grafana                            "/run.sh"                2 hours ago      Up 2 hours                                                                   k8s_grafana_grafana-6957bcf98-rddk6_default_93f4d09e-5cd4-44e5-9c59-8851f618b512_2
aec28ea0f4bc   3081609656b3                               "uvicorn src.api:app…"   2 hours ago      Up 2 hours                                                                   k8s_iris-api_iris-classifier-85b7874df6-jts9c_default_f4d3c6b4-07ad-4bc9-b3c9-79ea96528e46_2
2666af9a7533   3081609656b3                               "uvicorn src.api:app…"   2 hours ago      Up 2 hours                                                                   k8s_iris-api_iris-classifier-85b7874df6-vr9bw_default_94fa7f2a-b300-4576-9bea-ee850b36e4ec_2
225f5b0476fc   3081609656b3                               "uvicorn src.api:app…"   2 hours ago      Up 2 hours                                                                   k8s_iris-api_iris-classifier-85b7874df6-wxpk8_default_e3678b81-6b41-4fe1-8447-faf0da9f94ce_2

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>

Erreur vu sur l'interface : 

http://localhost:8501/chatbot

ModuleNotFoundError: No module named 'streamlit_cookies_manager'

File "/app/streamlit_app.py", line 29, in <module>
    pg.run()
File "/opt/venv/lib/python3.11/site-packages/streamlit/navigation/page.py", line 303, in run
    exec(code, module.__dict__)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/app/streamlit_pages/chatbot.py", line 8, in <module>
    from streamlit_cookies_manager import EncryptedCookieManager




http://localhost:8501/document_mining


Erreur de connexion à l'API /retrieve : HTTPConnectionPool(host='127.0.0.1', port=8000): Max retries exceeded with url: /retrieve (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x782af82e4d10>: Failed to establish a new connection: [Errno 111] Connection refused'))