# 🤖 Instructions Claude - Résolution Problèmes

**Dernière mise à jour** : 2025-11-28 13:25

---

## ❌ PROBLÈME ACTUEL : Image Docker Supprimée + Firewall Bloque Rebuild

### Diagnostic
```cmd
docker images | findstr rag-system
REM → Aucun résultat (image supprimée avec les containers)

docker-compose -f docker-compose.prod.yml up -d
REM → Error: pull access denied for rag-system (image n'existe ni localement ni sur Docker Hub)
```

### Situation
1. **Image `rag-system:prod` supprimée** lors du nettoyage Docker
2. **Firewall bloque rebuild** : `Unable to connect to deb.debian.org:http`
3. **Impossible de démarrer** sans rebuilder l'image

### 🎯 Solutions Disponibles

**OPTION 1 - Hotspot Mobile (RECOMMANDÉ)** ⭐

Le firewall bloque seulement le réseau entreprise. Utilisez le hotspot de votre téléphone :

```cmd
cd C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp

REM Étape 1 : Connecter votre PC au hotspot de votre téléphone

REM Étape 2 : Vérifier que les modèles sont présents
dir models
REM Doit afficher : all-mpnet-base-v2\ et Llama-3.2-3B-Instruct-Q5_K_L.gguf

REM Étape 3 : Switcher les .dockerignore (pour inclure models/)
ren .dockerignore .dockerignore.dev
ren .dockerignore.prod .dockerignore

REM Étape 4 : Builder l'image (prend 10-15 min)
docker build -f Dockerfile.prod -t rag-system:prod .

REM Étape 5 : Restaurer les .dockerignore
ren .dockerignore .dockerignore.prod
ren .dockerignore.dev .dockerignore

REM Étape 6 : Créer .env
copy .env.example .env

REM Étape 7 : Démarrer tous les services
docker-compose -f docker-compose.prod.yml up -d

REM Étape 8 : Attendre 2 minutes
timeout /t 120

REM Étape 9 : Tester
start http://localhost:8501
```

---

**OPTION 2 - Builder sur PC Personnel et Transférer**

Si vous avez accès à votre PC personnel sans restrictions réseau :

**Sur PC personnel** :
```cmd
REM 1. Cloner le repo
git clone https://github.com/Babou001/irp.git
cd irp

REM 2. Télécharger les modèles (voir MODELS_README.md)
pip install huggingface-hub

REM Modèle embeddings
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/all-mpnet-base-v2', local_dir='./models/all-mpnet-base-v2')"

REM Modèle LLM
huggingface-cli download bartowski/Llama-3.2-3B-Instruct-GGUF Llama-3.2-3B-Instruct-Q5_K_L.gguf --local-dir ./models --local-dir-use-symlinks False

REM 3. Switcher .dockerignore
ren .dockerignore .dockerignore.dev
ren .dockerignore.prod .dockerignore

REM 4. Builder l'image
docker build -f Dockerfile.prod -t rag-system:prod .

REM 5. Exporter l'image (fichier ~6-7 GB)
docker save rag-system:prod -o rag-system-prod.tar

REM 6. Copier rag-system-prod.tar sur clé USB
```

**Sur PC entreprise** :
```cmd
cd C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp

REM 1. Copier le fichier .tar depuis la clé USB
REM 2. Importer l'image (prend 2-3 min)
docker load -i rag-system-prod.tar

REM 3. Vérifier
docker images | findstr rag-system

REM 4. Démarrer
copy .env.example .env
docker-compose -f docker-compose.prod.yml up -d
timeout /t 120
start http://localhost:8501
```

---

### 🔄 Solutions Alternatives (Moins Recommandées)

**Option A - Build sur Réseau Personnel** :
- Connecter le PC à un réseau sans restrictions (hotspot mobile)
- Lancer le build

**Option B - Image Pré-Construite** :
- Builder l'image sur un PC personnel
- Exporter : `docker save rag-system:prod -o rag-system.tar`
- Transférer via clé USB
- Importer : `docker load -i rag-system.tar`

**Option C - Proxy Entreprise** (si disponible) :
```dockerfile
# Ajouter avant apt-get dans Dockerfile.prod
ENV HTTP_PROXY=http://proxy-entreprise:port
ENV HTTPS_PROXY=http://proxy-entreprise:port
```

---

## ✅ Problème Résolu : Variables d'Environnement Redis Manquantes

### Erreur (résolue)
```
redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:6379. Connection refused.
```

### Cause
Les variables d'environnement `REDIS_HOST` et `REDIS_PORT` n'étaient pas définies pour le service Streamlit dans docker-compose.prod.yml

### Solution Appliquée
Variables ajoutées dans docker-compose.prod.yml (lignes 146-147). **Pas besoin de rebuild**, juste redémarrer les containers.

---

## ✅ Problème Résolu : Docker Build Échoue (models/ not found)

### Erreur (résolue)
```
ERROR: failed to solve: failed to compute cache key: failed to calculate checksum of ref: "/models": not found
```

### Solution Appliquée : Switcher les .dockerignore

**Commandes Windows CMD** :
```cmd
cd C:\Users\elhadsey\OneDrive - myidemia\Bureau\irp

REM Étape 1 : Renommer temporairement les .dockerignore
ren .dockerignore .dockerignore.dev
ren .dockerignore.prod .dockerignore

REM Étape 2 : Builder l'image production
docker build -f Dockerfile.prod -t rag-system:prod .

REM Étape 3 : Restaurer les .dockerignore après le build
ren .dockerignore .dockerignore.prod
ren .dockerignore.dev .dockerignore
```

**Explication** :
- `.dockerignore` (actuel) : Exclut `models/` → Pour mode dev
- `.dockerignore.prod` : N'exclut PAS `models/` → Pour mode production
- Il faut utiliser `.dockerignore.prod` pendant le build pour que Docker copie les modèles dans l'image

---

## ✅ Après le Build Réussi

### Démarrer le système en production
```cmd
REM Copier le fichier d'environnement
copy .env.example .env

REM Démarrer tous les services
docker-compose -f docker-compose.prod.yml up -d

REM Attendre 2 minutes que tout démarre
timeout /t 120

REM Vérifier les logs
docker logs rag-fastapi

REM Tester l'API
curl http://localhost:8000/

REM Ouvrir l'interface
start http://localhost:8501
```

---

## 🔍 Vérifications

### Vérifier que les modèles sont dans l'image Docker
```cmd
docker run --rm rag-system:prod ls -lh /app/models/
```

**Résultat attendu** :
```
all-mpnet-base-v2/
Llama-3.2-3B-Instruct-Q5_K_L.gguf  (2.3 GB)
```

### Vérifier les containers actifs
```cmd
docker ps
```

**Containers attendus** :
- rag-fastapi
- rag-streamlit
- milvus-standalone
- milvus-etcd
- milvus-minio
- redis
- prometheus
- grafana

---

## 🐛 Debugging

### Si FastAPI ne démarre pas
```cmd
REM Voir les logs détaillés
docker logs rag-fastapi --tail 100

REM Vérifier si les modèles sont chargés
docker exec rag-fastapi ls -lh /app/models/
```

### Si Milvus ne connecte pas
```cmd
REM Vérifier Milvus
docker logs milvus-standalone --tail 50

REM Tester la connexion
docker exec rag-fastapi python test_milvus_conn.py
```

### Si manque d'espace disque
```cmd
REM Vérifier l'espace
docker system df

REM Nettoyer si nécessaire
docker system prune -af --volumes
```

---

## 📝 Historique des Problèmes Résolus

### ✅ Problème 1 : Modèles non téléchargés
**Solution** : Télécharger via Hugging Face avant le build (voir MODELS_README.md)

### ✅ Problème 2 : File locking macOS
**Solution** : Lazy loading implémenté dans fast_api_app.py

### ✅ Problème 3 : Connexion Milvus échoue
**Solution** : Utiliser URI au lieu de host/port dans retriever.py

### ✅ Problème 4 : Modèle Q4 vs Q5
**Solution** : Corriger paths.py pour utiliser Q5_K_L

### ✅ Problème 5 : .dockerignore exclut models/
**Solution** : Switcher entre .dockerignore et .dockerignore.prod pendant le build

### ✅ Problème 6 : Restrictions réseau entreprise (spaCy)
**Solution** : Supprimer `RUN python -m spacy download en_core_web_lg` du Dockerfile.prod (non utilisé)

### ✅ Problème 7 : Port 9000 déjà utilisé
**Solution** : Changer ports Minio dans docker-compose.prod.yml (9000→9002, 9001→9003)

### ✅ Problème 8 : streamlit-cookies-manager manquant
**Solution** : Ajouter `streamlit-cookies-manager` à requirements.txt

### ✅ Problème 9 : Streamlit ne peut pas joindre FastAPI
**Solution** : Utiliser variable d'environnement FASTAPI_URL avec nom du service Docker (rag-fastapi:8000)

### ✅ Problème 10 : Streamlit ne peut pas joindre Redis
**Solution** : Ajouter variables REDIS_HOST et REDIS_PORT dans docker-compose.prod.yml pour Streamlit

### ❌ Problème 11 : Docker Build Bloqué par Firewall (ACTUEL)
**Cause** : Firewall entreprise bloque deb.debian.org lors du `apt-get install`
**Aggravation** : Image `rag-system:prod` supprimée lors du nettoyage → Rebuild obligatoire
**Solutions recommandées** :
1. Build via hotspot mobile (plus rapide)
2. Build sur PC perso + export/import via clé USB (plus fiable)

---

## 🚀 Checklist Déploiement Final

- [ ] Modèles téléchargés (2.7 GB total)
- [ ] .dockerignore.prod utilisé pour le build
- [ ] Image rag-system:prod buildée avec succès
- [ ] .env créé depuis .env.example
- [ ] docker-compose.prod.yml up -d exécuté
- [ ] Tous les containers "healthy"
- [ ] API répond sur http://localhost:8000/
- [ ] Interface accessible sur http://localhost:8501
- [ ] Test upload PDF réussi
- [ ] Test chat avec retrieval réussi

---

## 📞 En Cas de Blocage

1. **Vérifier ERROR.md** : Le fichier contient les erreurs rencontrées
2. **Consulter les docs** :
   - [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md) - Démarrage rapide
   - [README_DEPLOYMENT.md](README_DEPLOYMENT.md) - Guide complet
   - [STATUS.md](STATUS.md) - Statut et limitations
3. **Logs Docker** : `docker logs <container_name>`
4. **Grafana** : http://localhost:3000 (admin/admin123)

---

**Bonne chance ! 🚀**
