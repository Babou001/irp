C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker build -f Dockerfile.prod -t rag-system:prod .
[+] Building 382.1s (22/22) FINISHED                                                                                                                                                                    docker:desktop-linux
 => [internal] load build definition from Dockerfile.prod                                                                                                                                                               0.0s
 => => transferring dockerfile: 3.50kB                                                                                                                                                                                  0.0s 
 => WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)                                                                                                                                         0.0s 
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                                                                                     1.2s 
 => [internal] load .dockerignore                                                                                                                                                                                       0.0s
 => => transferring context: 1.44kB                                                                                                                                                                                     0.0s 
 => [builder 1/6] FROM docker.io/library/python:3.11-slim@sha256:193fdd0bbcb3d2ae612bd6cc3548d2f7c78d65b549fcaa8af75624c47474444d                                                                                       0.0s 
 => [internal] load build context                                                                                                                                                                                       0.1s 
 => => transferring context: 9.68kB                                                                                                                                                                                     0.0s 
 => CACHED [stage-1  2/12] RUN apt-get update && apt-get install -y     libgomp1     curl     && rm -rf /var/lib/apt/lists/*                                                                                            0.0s 
 => CACHED [builder 2/6] WORKDIR /app                                                                                                                                                                                   0.0s 
 => CACHED [builder 3/6] RUN apt-get update && apt-get install -y     build-essential     wget     git     && rm -rf /var/lib/apt/lists/*                                                                               0.0s 
 => CACHED [builder 4/6] COPY requirements.txt .                                                                                                                                                                        0.0ss
 => CACHED [builder 5/6] RUN python -m venv /opt/venv                                                                                                                                                                   0.0s 
 => CACHED [builder 6/6] RUN pip install --no-cache-dir --upgrade pip setuptools wheel &&     pip install --no-cache-dir -r requirements.txt                                                                            0.0ss
 => [stage-1  3/12] COPY --from=builder /opt/venv /opt/venv                                                                                                                                                            93.6ss
 => [stage-1  4/12] RUN useradd -m -u 1000 appuser &&     mkdir -p /app/data /app/uploads /app/preprocessed_data &&     chown -R appuser:appuser /app                                                                   1.0s
 => [stage-1  5/12] WORKDIR /app                                                                                                                                                                                        0.1s 
 => [stage-1  6/12] COPY --chown=appuser:appuser *.py ./                                                                                                                                                                0.5s 
 => [stage-1  7/12] COPY --chown=appuser:appuser streamlit_pages/ ./streamlit_pages/                                                                                                                                    0.8s 
 => [stage-1  8/12] COPY --chown=appuser:appuser .streamlit/ ./.streamlit/                                                                                                                                              0.0s 
 => [stage-1  9/12] COPY --chown=appuser:appuser requirements.txt ./                                                                                                                                                    0.0s 
 => [stage-1 10/12] COPY --chown=appuser:appuser models/ ./models/                                                                                                                                                     38.1s 
 => [stage-1 11/12] RUN ls -lh /app/models/ &&     echo "✅ Models successfully embedded in image"                                                                                                                       0.8s
 => [stage-1 12/12] RUN mkdir -p /app/images /app/videos &&     chown -R appuser:appuser /app                                                                                                                          36.5s 
 => exporting to image                                                                                                                                                                                                 93.6s 
 => => exporting layers                                                                                                                                                                                                93.5s 
 => => writing image sha256:c8551aaf5923766760784335d0d57cab7832ae830ae4c9f0c0ab350a32017c8a                                                                                                                            0.0s 
 => => naming to docker.io/library/rag-system:prod                                                                                                                                                                      0.0s 

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/dzg8zikv19k33k0zrcmjjz7h4

 1 warning found (use docker --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>