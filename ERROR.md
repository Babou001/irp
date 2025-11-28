
http://localhost:8501/chatbot

redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:6379. Connection refused.

File "/app/streamlit_app.py", line 29, in <module>
    pg.run()
File "/opt/venv/lib/python3.11/site-packages/streamlit/navigation/page.py", line 303, in run
    exec(code, module.__dict__)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/app/streamlit_pages/chatbot.py", line 130, in <module>
    redis_client.sadd(f"users:{date_str}", session_id)
File "/opt/venv/lib/python3.11/site-packages/redis/commands/core.py", line 3512, in sadd
    return self.execute_command("SADD", name, *values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/opt/venv/lib/python3.11/site-packages/redis/client.py", line 657, in execute_command
    return self._execute_command(*args, **options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/opt/venv/lib/python3.11/site-packages/redis/client.py", line 663, in _execute_command
    conn = self.connection or pool.get_connection()
                              ^^^^^^^^^^^^^^^^^^^^^
File "/opt/venv/lib/python3.11/site-packages/redis/utils.py", line 196, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
File "/opt/venv/lib/python3.11/site-packages/redis/connection.py", line 2603, in get_connection
    connection.connect()
File "/opt/venv/lib/python3.11/site-packages/redis/connection.py", line 846, in connect
    self.connect_check_health(check_health=True)
File "/opt/venv/lib/python3.11/site-packages/redis/connection.py", line 863, in connect_check_health
    raise ConnectionError(self._error_message(e))



http://localhost:8501/document_mining


Erreur de connexion à l'API /retrieve : HTTPConnectionPool(host='rag-fastapi', port=8000): Max retries exceeded with url: /retrieve (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x773b16aee590>: Failed to resolve 'rag-fastapi' ([Errno -3] Temporary failure in name resolution)"))