C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker build -f Dockerfile.prod -t rag-system:prod .
[+] Building 1012.5s (12/22)                                                                                                                                                                            docker:desktop-linux
 => [internal] load build definition from Dockerfile.prod                                                                                                                                                               0.0s
 => => transferring dockerfile: 3.44kB                                                                                                                                                                                  0.0s 
 => WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)                                                                                                                                         0.0s 
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                                                                                     1.0s 
 => [internal] load .dockerignore                                                                                                                                                                                       0.0s
 => => transferring context: 1.44kB                                                                                                                                                                                     0.0s 
 => CACHED [builder 1/7] FROM docker.io/library/python:3.11-slim@sha256:193fdd0bbcb3d2ae612bd6cc3548d2f7c78d65b549fcaa8af75624c47474444d                                                                                0.0s 
 => [internal] load build context                                                                                                                                                                                     400.8s 
 => => transferring context: 9.85GB                                                                                                                                                                                   400.7s 
 => CACHED [builder 2/7] WORKDIR /app                                                                                                                                                                                   0.0s 
 => [stage-1  2/12] RUN apt-get update && apt-get install -y     libgomp1     curl     && rm -rf /var/lib/apt/lists/*                                                                                                  31.0s 
 => [builder 3/7] RUN apt-get update && apt-get install -y     build-essential     wget     git     && rm -rf /var/lib/apt/lists/*                                                                                    148.3s 
 => [builder 4/7] COPY requirements.txt .                                                                                                                                                                               0.4s
 => [builder 5/7] RUN python -m venv /opt/venv                                                                                                                                                                          5.6s
 => [builder 6/7] RUN pip install --no-cache-dir --upgrade pip setuptools wheel &&     pip install --no-cache-dir -r requirements.txt                                                                                 598.3s
 => ERROR [builder 7/7] RUN python -m spacy download en_core_web_lg                                                                                                                                                     6.1s
------
 > [builder 7/7] RUN python -m spacy download en_core_web_lg:
4.813 Traceback (most recent call last):
4.813   File "/opt/venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 464, in _make_request
4.814     self._validate_conn(conn)
4.814   File "/opt/venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 1093, in _validate_conn
4.814     conn.connect()
4.814   File "/opt/venv/lib/python3.11/site-packages/urllib3/connection.py", line 790, in connect
4.815     sock_and_verified = _ssl_wrap_socket_and_match_hostname(
4.815                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.815   File "/opt/venv/lib/python3.11/site-packages/urllib3/connection.py", line 969, in _ssl_wrap_socket_and_match_hostname
4.816     ssl_sock = ssl_wrap_socket(
4.816                ^^^^^^^^^^^^^^^^
4.816   File "/opt/venv/lib/python3.11/site-packages/urllib3/util/ssl_.py", line 480, in ssl_wrap_socket
4.817     ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls, server_hostname)
4.817                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.817   File "/opt/venv/lib/python3.11/site-packages/urllib3/util/ssl_.py", line 524, in _ssl_wrap_socket_impl
4.817     return ssl_context.wrap_socket(sock, server_hostname=server_hostname)
4.817            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.817   File "/usr/local/lib/python3.11/ssl.py", line 517, in wrap_socket
4.818     return self.sslsocket_class._create(
4.818            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.818   File "/usr/local/lib/python3.11/ssl.py", line 1104, in _create
4.818     self.do_handshake()
4.818   File "/usr/local/lib/python3.11/ssl.py", line 1382, in do_handshake
4.819     self._sslobj.do_handshake()
4.819 ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1016)
4.819
4.819 During handling of the above exception, another exception occurred:
4.819
4.819 Traceback (most recent call last):
4.819   File "/opt/venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 787, in urlopen
4.819     response = self._make_request(
4.819                ^^^^^^^^^^^^^^^^^^^
4.819   File "/opt/venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 488, in _make_request
4.819     raise new_e
4.819 urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1016)
4.819
4.819 The above exception was the direct cause of the following exception:
4.819
4.819 Traceback (most recent call last):
4.819   File "/opt/venv/lib/python3.11/site-packages/requests/adapters.py", line 644, in send
4.820     resp = conn.urlopen(
4.820            ^^^^^^^^^^^^^
4.820   File "/opt/venv/lib/python3.11/site-packages/urllib3/connectionpool.py", line 841, in urlopen
4.821     retries = retries.increment(
4.821               ^^^^^^^^^^^^^^^^^^
4.821   File "/opt/venv/lib/python3.11/site-packages/urllib3/util/retry.py", line 519, in increment
4.821     raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
4.821     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.821 urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='raw.githubusercontent.com', port=443): Max retries exceeded with url: /explosion/spacy-models/master/compatibility.json (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1016)')))
4.821
4.821 During handling of the above exception, another exception occurred:
4.821
4.821 Traceback (most recent call last):
4.822   File "<frozen runpy>", line 198, in _run_module_as_main
4.822   File "<frozen runpy>", line 88, in _run_code
4.822   File "/opt/venv/lib/python3.11/site-packages/spacy/__main__.py", line 4, in <module>
4.822     setup_cli()
4.822   File "/opt/venv/lib/python3.11/site-packages/spacy/cli/_util.py", line 87, in setup_cli
4.822     command(prog_name=COMMAND)
4.822   File "/opt/venv/lib/python3.11/site-packages/click/core.py", line 1485, in __call__
4.823     return self.main(*args, **kwargs)
4.823            ^^^^^^^^^^^^^^^^^^^^^^^^^^
4.823   File "/opt/venv/lib/python3.11/site-packages/typer/core.py", line 803, in main
4.824     return _main(
4.824            ^^^^^^
4.824   File "/opt/venv/lib/python3.11/site-packages/typer/core.py", line 192, in _main
4.824     rv = self.invoke(ctx)
4.824          ^^^^^^^^^^^^^^^^
4.824   File "/opt/venv/lib/python3.11/site-packages/click/core.py", line 1873, in invoke
4.825     return _process_result(sub_ctx.command.invoke(sub_ctx))
4.825                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.825   File "/opt/venv/lib/python3.11/site-packages/click/core.py", line 1269, in invoke
4.825     return ctx.invoke(self.callback, **ctx.params)
4.825            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.825   File "/opt/venv/lib/python3.11/site-packages/click/core.py", line 824, in invoke
4.825     return callback(*args, **kwargs)
4.825            ^^^^^^^^^^^^^^^^^^^^^^^^^
4.825   File "/opt/venv/lib/python3.11/site-packages/typer/main.py", line 691, in wrapper
4.827     return callback(**use_params)
4.827            ^^^^^^^^^^^^^^^^^^^^^^
4.827   File "/opt/venv/lib/python3.11/site-packages/spacy/cli/download.py", line 45, in download_cli
4.827     download(model, direct, sdist, url, *ctx.args)
4.827   File "/opt/venv/lib/python3.11/site-packages/spacy/cli/download.py", line 87, in download
4.827     compatibility = get_compatibility()
4.827                     ^^^^^^^^^^^^^^^^^^^
4.827   File "/opt/venv/lib/python3.11/site-packages/spacy/cli/download.py", line 132, in get_compatibility
4.827     r = requests.get(about.__compatibility__)
4.827         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.827   File "/opt/venv/lib/python3.11/site-packages/requests/api.py", line 73, in get
4.828     return request("get", url, params=params, **kwargs)
4.828            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.828   File "/opt/venv/lib/python3.11/site-packages/requests/api.py", line 59, in request
4.828     return session.request(method=method, url=url, **kwargs)
4.828            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.828   File "/opt/venv/lib/python3.11/site-packages/requests/sessions.py", line 589, in request
4.829     resp = self.send(prep, **send_kwargs)
4.829            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.829   File "/opt/venv/lib/python3.11/site-packages/requests/sessions.py", line 703, in send
4.832     r = adapter.send(request, **kwargs)
4.832         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4.832   File "/opt/venv/lib/python3.11/site-packages/requests/adapters.py", line 675, in send
4.832     raise SSLError(e, request=request)
4.832 requests.exceptions.SSLError: HTTPSConnectionPool(host='raw.githubusercontent.com', port=443): Max retries exceeded with url: /explosion/spacy-models/master/compatibility.json (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1016)')))
------

 1 warning found (use docker --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 14)
Dockerfile.prod:38
--------------------
  36 |
  37 |     # Download spaCy model
  38 | >>> RUN python -m spacy download en_core_web_lg
  39 |
  40 |     # =============================================================================
--------------------
ERROR: failed to solve: process "/bin/sh -c python -m spacy download en_core_web_lg" did not complete successfully: exit code: 1

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/1rhqlx8m44cb6v98owntm2fj3
