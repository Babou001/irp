C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>dir
 Volume in drive C is Windows
 Volume Serial Number is AC97-4896

 Directory of C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp

11/28/2025  01:01 PM    <DIR>          .
11/28/2025  11:43 AM    <DIR>          ..
11/28/2025  11:43 AM             1,105 .dockerignore
11/28/2025  11:43 AM             1,401 .dockerignore.prod
11/28/2025  11:43 AM               776 .env.example
11/28/2025  11:43 AM             2,261 .gitignore
11/28/2025  12:26 PM    <DIR>          .streamlit
11/28/2025  11:43 AM             6,338 docker-compose.prod.yml
11/28/2025  11:43 AM             5,561 docker-compose.yml
11/28/2025  11:43 AM             1,783 Dockerfile
11/28/2025  11:43 AM             3,398 Dockerfile.prod
11/28/2025  11:46 AM    <DIR>          docs
11/28/2025  01:01 PM             9,144 ERROR.md
11/28/2025  11:43 AM            12,676 fast_api_app.py
11/28/2025  11:43 AM             7,466 generator.py
11/28/2025  11:46 AM    <DIR>          images
11/28/2025  11:43 AM            10,104 LIVRAISON.md
11/28/2025  11:43 AM            84,448 main.ipynb
11/28/2025  11:43 AM             1,644 main.py
11/28/2025  12:16 PM    <DIR>          models
11/28/2025  11:43 AM             3,566 MODELS_README.md
11/28/2025  11:46 AM    <DIR>          monitoring
11/28/2025  11:43 AM             1,815 paths.py
11/28/2025  11:43 AM            18,473 preprocess.py
11/28/2025  11:46 AM    <DIR>          preprocessed_data
11/28/2025  11:43 AM            15,601 preprocess_reset.py
11/28/2025  12:40 PM             5,859 PUSH_TO_GITHUB.md
11/28/2025  11:43 AM             5,488 QUICK_START_GITHUB.md
11/28/2025  11:43 AM               783 rag.yaml
11/28/2025  11:43 AM             6,354 Readme.md
11/28/2025  11:43 AM             7,937 README_DEPLOYMENT.md
11/28/2025  11:43 AM             3,392 redis_db.py
11/28/2025  11:43 AM             3,270 REORGANIZATION.md
11/28/2025  11:43 AM               740 requirements.txt
11/28/2025  11:43 AM               648 reset_collection.py
11/28/2025  11:43 AM             7,190 retriever.py
11/28/2025  11:46 AM    <DIR>          scripts
11/28/2025  11:43 AM             7,050 STATUS.md
11/28/2025  11:43 AM             1,042 streamlit_app.py
11/28/2025  11:46 AM    <DIR>          streamlit_pages
11/28/2025  11:43 AM             8,282 Support.md
11/28/2025  11:43 AM               385 test_milvus_conn.py
11/28/2025  11:43 AM             1,128 test_retriever.py
11/28/2025  11:43 AM             1,553 unit_test.py
              34 File(s)        248,661 bytes
              10 Dir(s)  95,340,007,424 bytes free

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>
C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>
C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>dir models
 Volume in drive C is Windows
 Volume Serial Number is AC97-4896

 Directory of C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp\models

11/28/2025  12:16 PM    <DIR>          .
11/28/2025  01:01 PM    <DIR>          ..
08/12/2025  08:52 AM    <DIR>          all-mpnet-base-v2
11/28/2025  12:15 PM     2,417,576,480 Llama-3.2-3B-Instruct-Q5_K_L.gguf
               1 File(s)  2,417,576,480 bytes
               3 Dir(s)  95,340,298,240 bytes free

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker build -f Dockerfile.prod -t rag-system:prod .
[+] Building 1.2s (20/22)                                                                                                                                                                               docker:desktop-linux
 => [internal] load build definition from Dockerfile.prod                                                                                                                                                               0.0s
 => => transferring dockerfile: 3.44kB                                                                                                                                                                                  0.0s 
 => WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)                                                                                                                                         0.0s 
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                                                                                     0.6s 
 => [internal] load .dockerignore                                                                                                                                                                                       0.0s
 => => transferring context: 1.15kB                                                                                                                                                                                     0.0s 
 => [internal] load build context                                                                                                                                                                                       0.0s 
 => => transferring context: 758B                                                                                                                                                                                       0.0s 
 => CACHED [builder 1/7] FROM docker.io/library/python:3.11-slim@sha256:193fdd0bbcb3d2ae612bd6cc3548d2f7c78d65b549fcaa8af75624c47474444d                                                                                0.0s 
 => CACHED [builder 2/7] WORKDIR /app                                                                                                                                                                                   0.0s 
 => CANCELED [builder 3/7] RUN apt-get update && apt-get install -y     build-essential     wget     git     && rm -rf /var/lib/apt/lists/*                                                                             0.4s 
 => CANCELED [stage-1  2/12] RUN apt-get update && apt-get install -y     libgomp1     curl     && rm -rf /var/lib/apt/lists/*                                                                                          0.4s 
 => CACHED [builder 4/7] COPY requirements.txt .                                                                                                                                                                        0.0s
 => CACHED [builder 5/7] RUN python -m venv /opt/venv                                                                                                                                                                   0.0s 
 => CACHED [builder 6/7] RUN pip install --no-cache-dir --upgrade pip setuptools wheel &&     pip install --no-cache-dir -r requirements.txt                                                                            0.0s 
 => CACHED [builder 7/7] RUN python -m spacy download en_core_web_lg                                                                                                                                                    0.0s 
 => CACHED [stage-1  3/12] COPY --from=builder /opt/venv /opt/venv                                                                                                                                                      0.0s
 => CACHED [stage-1  4/12] RUN useradd -m -u 1000 appuser &&     mkdir -p /app/data /app/uploads /app/preprocessed_data &&     chown -R appuser:appuser /app                                                            0.0s 
 => CACHED [stage-1  5/12] WORKDIR /app                                                                                                                                                                                 0.0s 
 => CACHED [stage-1  6/12] COPY --chown=appuser:appuser *.py ./                                                                                                                                                         0.0s 
 => CACHED [stage-1  7/12] COPY --chown=appuser:appuser streamlit_pages/ ./streamlit_pages/                                                                                                                             0.0s 
 => CACHED [stage-1  8/12] COPY --chown=appuser:appuser .streamlit/ ./.streamlit/                                                                                                                                       0.0s 
 => CACHED [stage-1  9/12] COPY --chown=appuser:appuser requirements.txt ./                                                                                                                                             0.0s 
 => ERROR [stage-1 10/12] COPY --chown=appuser:appuser models/ ./models/                                                                                                                                                0.0s 
------
 > [stage-1 10/12] COPY --chown=appuser:appuser models/ ./models/:
------

 1 warning found (use docker --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)
Dockerfile.prod:77
--------------------
  75 |     # =============================================================================
  76 |     # This is what makes the image self-contained (but larger)
  77 | >>> COPY --chown=appuser:appuser models/ ./models/
  78 |
  79 |     # Verify models are present
--------------------
ERROR: failed to solve: failed to compute cache key: failed to calculate checksum of ref 5308fb2f-088c-4b1a-a635-9146a2e996e3::3vp4bpfcg26el95ooi9jbo8y3: "/models": not found

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/2nqoa5x6s2neclgfafeiv1lle

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>