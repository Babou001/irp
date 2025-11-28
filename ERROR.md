C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker images | findstr rag-system

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>docker-compose -f docker-compose.prod.yml up -d
[+] Running 6/6
 ✘ streamlit Error pull access denied for rag-system, repository does not exist or may require 'docker login': denied: requested access to the resource is denied                                                                        1.7s 
 ✘ redis Error     pull access denied for rag-system, repository does not exist or may require 'docker login': denied: requested access to the resource is denied                                                                        1.7s 
 ✘ minio Error     pull access denied for rag-system, repository does not exist or may require 'docker login': denied: requested access to the resource is denied                                                                        1.7s 
 ✘ etcd Error      pull access denied for rag-system, repository does not exist or may require 'docker login': denied: requested access to the resource is denied                                                                        1.7s 
 ✘ fastapi Error   pull access denied for rag-system, repository does not exist or may require 'docker login': denied: requested access to the resource is denied                                                                        1.7s 
 ✘ milvus Error    pull access denied for rag-system, repository does not exist or may require 'docker login': denied: requested access to the resource is denied                                                                        1.7s 
Error response from daemon: pull access denied for rag-system, repository does not exist or may require 'docker login': denied: requested access to the resource is denied

C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp>