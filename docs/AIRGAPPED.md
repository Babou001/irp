# 🔒 Air-Gapped Deployment Guide

**Guide de déploiement pour environnements restreints sans accès Internet**

---

## 📋 Vue d'ensemble

Ce guide explique comment déployer le système RAG dans un environnement **air-gapped** (sans Internet), typique des infrastructures d'entreprise avec des restrictions de sécurité strictes.

### ✅ Avantages du mode production

- **100% autonome** - Aucune dépendance externe
- **Aucun téléchargement** - Tous les modèles sont embarqués
- **Confidentiel** - Pas de fuite de données vers l'extérieur
- **Reproductible** - Version exacte des modèles figée
- **Portable** - Un seul fichier `.tar` à transférer

---

## 🎯 Prérequis

### Sur la machine de build (avec Internet)

- Docker installé
- 10+ GB d'espace disque libre
- Le code source du projet
- Les modèles téléchargés :
  - `models/all-mpnet-base-v2/` (embeddings)
  - `models/Llama-3.2-3B-Instruct-Q5_K_L.gguf` (LLM)

### Sur le serveur de production (sans Internet)

- Docker + Docker Compose installés
- 15+ GB d'espace disque libre
- Accès root ou permissions Docker

---

## 🚀 Étape 1 : Build de l'image (sur machine avec Internet)

### 1.1 Vérification des modèles

```bash
cd /path/to/version_using_milvus

# Vérifier la présence des modèles
ls -lh models/
# Doit afficher :
# - all-mpnet-base-v2/       (dossier ~420 MB)
# - Llama-3.2-3B-Instruct-Q5_K_L.gguf (~2.3 GB)
```

### 1.2 Build de l'image production

```bash
# Build l'image avec modèles embarqués
./scripts/build-production-image.sh

# OU avec export automatique vers fichier .tar
./scripts/build-production-image.sh --export
```

Le script va :
1. ✅ Vérifier tous les prérequis
2. 🔨 Builder l'image Docker (~6-7 GB)
3. 📦 (Optionnel) Exporter vers `rag-system-prod.tar`

**Durée estimée** : 5-10 minutes selon votre machine

### 1.3 Export manuel (si nécessaire)

```bash
# Exporter l'image vers un fichier
docker save rag-system:prod -o rag-system-prod.tar

# Vérifier la taille
ls -lh rag-system-prod.tar
# ~6-7 GB
```

---

## 📦 Étape 2 : Transfert vers le serveur de production

### Option A : Transfert réseau (SCP/SFTP)

```bash
# Via SCP
scp rag-system-prod.tar user@production-server:/tmp/

# Via rsync (avec reprise en cas d'erreur)
rsync -avz --progress rag-system-prod.tar user@production-server:/tmp/
```

### Option B : Support physique (USB/DVD)

1. Copier `rag-system-prod.tar` sur clé USB
2. Transférer physiquement vers le serveur
3. Copier depuis la clé vers `/tmp/`

### Option C : Autres fichiers nécessaires

En plus de l'image Docker, transférer aussi :

```bash
# Créer une archive avec les fichiers de configuration
tar czf rag-config.tar.gz \
    docker-compose.prod.yml \
    .env.example \
    monitoring/ \
    data/ \
    docs/

# Transférer vers le serveur
scp rag-config.tar.gz user@production-server:/opt/rag-system/
```

---

## 🔧 Étape 3 : Déploiement sur le serveur de production

### 3.1 Connexion au serveur

```bash
ssh user@production-server
cd /opt/rag-system  # Ou votre répertoire de déploiement
```

### 3.2 Chargement de l'image Docker

```bash
# Charger l'image depuis le fichier .tar
docker load -i /tmp/rag-system-prod.tar

# Vérifier que l'image est chargée
docker images | grep rag-system
# Doit afficher : rag-system   prod   ...   6.5GB   ...
```

### 3.3 Extraction de la configuration

```bash
# Extraire les fichiers de config
tar xzf rag-config.tar.gz

# Structure attendue :
# /opt/rag-system/
# ├── docker-compose.prod.yml
# ├── .env
# ├── monitoring/
# ├── data/          # PDFs initiaux
# └── docs/
```

### 3.4 Configuration

```bash
# Copier et éditer le fichier d'environnement
cp .env.example .env

# Éditer si nécessaire (optionnel, valeurs par défaut OK)
nano .env
```

Exemple `.env` :

```bash
# Configuration Milvus
MILVUS_HOST=milvus-standalone
MILVUS_PORT=19530
MILVUS_COLLECTION=rag_docs

# Configuration Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Pas besoin de configurer les modèles - ils sont dans l'image !
```

### 3.5 Démarrage des services

```bash
# Démarrer tous les containers
docker-compose -f docker-compose.prod.yml up -d

# Suivre les logs en temps réel
docker-compose -f docker-compose.prod.yml logs -f
```

### 3.6 Vérification du déploiement

```bash
# Vérifier l'état des containers
docker-compose -f docker-compose.prod.yml ps

# Doit afficher 7 containers "healthy" :
# - milvus-etcd
# - milvus-minio
# - milvus-standalone
# - rag-redis
# - rag-fastapi          ← Service principal
# - rag-streamlit        ← Interface utilisateur
# - rag-prometheus
# - rag-grafana

# Test de l'API
curl http://localhost:8000/
# Réponse attendue : {"message":"FastAPI is running!"}

# Test de l'interface web
curl http://localhost:8501/_stcore/health
# Réponse attendue : {"status":"ok"}
```

---

## 🌐 Étape 4 : Accès aux interfaces

### URLs d'accès

| Service | URL | Authentification |
|---------|-----|------------------|
| **Streamlit UI** | http://server-ip:8501 | Aucune |
| **API FastAPI** | http://server-ip:8000 | Aucune |
| **API Docs** | http://server-ip:8000/docs | Aucune |
| **Grafana** | http://server-ip:3000 | admin / admin123 |
| **Prometheus** | http://server-ip:9090 | Aucune |
| **MinIO** | http://server-ip:9001 | minioadmin / minioadmin |

### Test de l'interface

1. Ouvrir http://server-ip:8501 dans un navigateur
2. Naviguer vers **"📄 Documents"**
3. Uploader un PDF de test
4. Aller sur **"💬 Chatbot"**
5. Poser une question sur le document

---

## 📊 Étape 5 : Indexation initiale des documents

### 5.1 Copier les PDFs

```bash
# Copier vos documents PDF dans le dossier data/
cp /path/to/pdfs/*.pdf /opt/rag-system/data/
```

### 5.2 Indexation

**Méthode 1 : Via l'interface Streamlit**
- Aller sur http://server-ip:8501
- Page "📄 Documents"
- Uploader les PDFs un par un

**Méthode 2 : Via script Python**

```bash
# Accéder au container FastAPI
docker exec -it rag-fastapi bash

# Lancer le preprocessing
python preprocess.py preprocess

# Sortir du container
exit
```

**Durée** : ~2-5 minutes par PDF selon la taille

### 5.3 Vérification

```bash
# Vérifier que les documents sont indexés
docker exec rag-fastapi python -c "
from retriever import load_vectorstore
from langchain_huggingface import HuggingFaceEmbeddings
import paths

emb = HuggingFaceEmbeddings(model_name=paths.bert_model_path)
vs = load_vectorstore(emb)
print(f'Documents indexés : {vs._collection.num_entities}')
"
```

---

## 🔧 Opérations courantes

### Arrêter les services

```bash
docker-compose -f docker-compose.prod.yml stop
```

### Redémarrer les services

```bash
docker-compose -f docker-compose.prod.yml restart
```

### Voir les logs

```bash
# Tous les services
docker-compose -f docker-compose.prod.yml logs -f

# Service spécifique
docker logs rag-fastapi -f
docker logs rag-streamlit -f
```

### Sauvegarder les données

```bash
# Sauvegarder les volumes Docker
docker run --rm \
  -v rag_milvus_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/milvus-backup-$(date +%Y%m%d).tar.gz /data

# Sauvegarder Redis
docker exec rag-redis redis-cli SAVE
docker cp rag-redis:/data/dump.rdb ./backups/redis-backup-$(date +%Y%m%d).rdb
```

### Mise à jour du système

```bash
# 1. Transférer la nouvelle image
scp rag-system-prod-v2.tar user@server:/tmp/

# 2. Sur le serveur
docker load -i /tmp/rag-system-prod-v2.tar

# 3. Redémarrer avec la nouvelle image
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🐛 Troubleshooting

### Container ne démarre pas

```bash
# Vérifier les logs d'erreur
docker logs rag-fastapi --tail 100

# Vérifier les ressources
docker stats

# Vérifier les volumes
docker volume ls
docker volume inspect rag_milvus_data
```

### Erreur "Out of memory"

```bash
# Augmenter les limites dans docker-compose.prod.yml
# Sous le service fastapi :
deploy:
  resources:
    limits:
      memory: 8G
    reservations:
      memory: 4G
```

### Performances lentes

```bash
# Vérifier les métriques dans Grafana
# http://server-ip:3000

# Vérifier l'utilisation CPU/RAM
docker stats

# Optimiser Milvus (dans docker-compose.prod.yml)
# Augmenter le cache :
environment:
  MILVUS_CACHE_SIZE: 4096  # En MB
```

### Ré-initialiser complètement

```bash
# ATTENTION : Supprime toutes les données !
docker-compose -f docker-compose.prod.yml down -v
docker volume prune -f
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📚 Documentation complémentaire

- [DEPLOYMENT.md](DEPLOYMENT.md) - Guide de déploiement général
- [QUICKSTART.md](QUICKSTART.md) - Guide de démarrage rapide
- [HANDOVER.md](HANDOVER.md) - Documentation de transfert de projet

---

## 🆘 Support

En cas de problème :

1. **Consulter les logs** : `docker logs rag-fastapi`
2. **Vérifier la documentation** : dossier `docs/`
3. **Vérifier les health checks** : `docker ps`
4. **Consulter Grafana** : http://localhost:3000

---

**Version du document** : 1.0
**Dernière mise à jour** : 2025-11-27
**Compatibilité** : Docker 20.10+, Docker Compose 2.0+
