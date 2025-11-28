# 🚀 Guide de Déploiement Rapide - Système RAG IDEMIA

**Version Dockerisée avec Milvus | Prêt pour déploiement air-gapped**

---

## ⚡ Démarrage Rapide

### Pour un test local rapide

```bash
# Démarrer tous les services
docker-compose up --build -d

# Accéder à l'interface
open http://localhost:8501
```

### Pour un déploiement production (Recommandé)

```bash
# 1. Builder l'image avec modèles embarqués
./scripts/build-production-image.sh --export

# 2. Déployer
docker-compose -f docker-compose.prod.yml up -d

# 3. Accéder
open http://localhost:8501
```

---

## 📁 Structure du Projet

```
version_using_milvus/
├── fast_api_app.py          # API Backend (avec lazy loading)
├── streamlit_app.py         # Interface utilisateur
├── retriever.py             # Retrieval avec Milvus
├── generator.py             # Génération avec Llama
├── preprocess.py            # Preprocessing et indexation
│
├── models/                  # Modèles ML (embarqués en prod)
│   ├── all-mpnet-base-v2/   # Embeddings (768 dim)
│   └── Llama-3.2-3B-*.gguf  # LLM quantifié
│
├── data/                    # Corpus PDF initial
├── docker-compose.yml       # Config dev (volumes)
├── docker-compose.prod.yml  # Config prod (models embarqués)
├── Dockerfile               # Image dev
├── Dockerfile.prod          # Image prod
│
├── docs/                    # Documentation complète
│   ├── DEPLOYMENT.md        # Guide déploiement
│   ├── AIRGAPPED.md         # Guide air-gapped
│   ├── QUICKSTART.md        # Démarrage rapide
│   └── HANDOVER.md          # Transfert de projet
│
└── scripts/                 # Scripts automatisés
    ├── build-production-image.sh
    ├── start.sh
    └── stop.sh
```

---

## 🎯 Deux Modes de Déploiement

### 1. Mode Développement (`docker-compose.yml`)

**Avantages :**
- ✅ Rebuild rapide
- ✅ Modèles en volumes (modifiables)
- ✅ Parfait pour développement

**Inconvénients :**
- ⚠️ Problèmes de file locking possibles sur macOS
- ⚠️ Nécessite accès aux modèles locaux

**Usage :**
```bash
docker-compose up --build -d
```

### 2. Mode Production (`docker-compose.prod.yml`) ⭐ **RECOMMANDÉ**

**Avantages :**
- ✅ **Modèles embarqués dans l'image**
- ✅ **100% autonome - fonctionne sans Internet**
- ✅ **Pas de file locking issues**
- ✅ **Portable - un fichier .tar à transférer**
- ✅ **Air-gapped ready**

**Inconvénients :**
- ⚠️ Image plus lourde (~6-7 GB)
- ⚠️ Rebuild plus long (une seule fois)

**Usage :**
```bash
# Build
./scripts/build-production-image.sh --export

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🏢 Déploiement pour l'Entreprise (Air-Gapped)

### Scénario : Transfert vers serveur sans Internet

**Sur la machine avec Internet :**

```bash
# 1. Builder l'image complète
./scripts/build-production-image.sh --export
# Génère : rag-system-prod.tar (~6.5 GB)

# 2. Préparer les fichiers de config
tar czf rag-config.tar.gz \
    docker-compose.prod.yml \
    .env.example \
    monitoring/ \
    data/
```

**Transférer vers le serveur :**

```bash
# Via réseau
scp rag-system-prod.tar user@server:/tmp/
scp rag-config.tar.gz user@server:/opt/rag-system/

# OU via clé USB physique
```

**Sur le serveur de production :**

```bash
# 1. Charger l'image
docker load -i /tmp/rag-system-prod.tar

# 2. Extraire la config
cd /opt/rag-system
tar xzf rag-config.tar.gz

# 3. Démarrer
docker-compose -f docker-compose.prod.yml up -d

# 4. Vérifier
curl http://localhost:8000/
# {"message":"FastAPI is running!"}
```

**📘 Guide détaillé** : [docs/AIRGAPPED.md](docs/AIRGAPPED.md)

---

## 🔧 Opérations Courantes

### Ajouter des documents

```bash
# Via l'interface (recommandé)
open http://localhost:8501
# Aller sur "📄 Documents" → Uploader PDF

# Via CLI
cp nouveaux_docs/*.pdf uploads/
docker-compose exec fastapi python preprocess.py add_doc
```

### Monitoring

```bash
# Grafana (dashboards)
open http://localhost:3000
# admin / admin123

# Prometheus (métriques)
open http://localhost:9090

# Logs
docker-compose logs -f fastapi
docker-compose logs -f streamlit
```

### Sauvegarder

```bash
# Sauvegarder Milvus
docker run --rm \
  -v rag_milvus_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/milvus-$(date +%Y%m%d).tar.gz /data

# Sauvegarder Redis
docker exec rag-redis redis-cli SAVE
docker cp rag-redis:/data/dump.rdb backups/redis-$(date +%Y%m%d).rdb
```

### Arrêter/Redémarrer

```bash
# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Tout supprimer (ATTENTION: perte de données!)
docker-compose down -v
```

---

## 📊 Services et Ports

| Service | Port | URL | Authentification |
|---------|------|-----|------------------|
| **Streamlit UI** | 8501 | http://localhost:8501 | - |
| **FastAPI** | 8000 | http://localhost:8000 | - |
| **API Docs** | 8000 | http://localhost:8000/docs | - |
| **Grafana** | 3000 | http://localhost:3000 | admin/admin123 |
| **Prometheus** | 9090 | http://localhost:9090 | - |
| **Milvus** | 19530 | - | - |
| **Redis** | 6379 | - | - |
| **MinIO Console** | 9001 | http://localhost:9001 | minioadmin/minioadmin |

---

## 🛠️ Troubleshooting

### FastAPI ne démarre pas

```bash
# Vérifier les logs
docker logs rag-fastapi --tail 100

# Vérifier que Milvus est healthy
docker ps | grep milvus

# Redémarrer
docker-compose restart fastapi
```

### Problème de file locking (macOS)

**Solution** : Utiliser le mode production au lieu du mode dev

```bash
# Au lieu de :
docker-compose up

# Utiliser :
./scripts/build-production-image.sh
docker-compose -f docker-compose.prod.yml up -d
```

### Modèle Llama ne charge pas

```bash
# Vérifier le modèle dans le container
docker exec rag-fastapi ls -lh /app/models/

# Doit afficher Llama-3.2-3B-Instruct-Q5_K_L.gguf
```

---

## 📚 Documentation Complète

- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guide de déploiement complet
- **[AIRGAPPED.md](docs/AIRGAPPED.md)** - Déploiement air-gapped détaillé
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Démarrage rapide
- **[HANDOVER.md](docs/HANDOVER.md)** - Transfert de projet
- **[NEXT_STEPS.md](docs/NEXT_STEPS.md)** - Améliorations futures

---

## 🎓 Architecture Technique

### Stack Technologique

- **Backend** : FastAPI (async, queue-based)
- **Frontend** : Streamlit (multi-page app)
- **Vector DB** : Milvus 2.4.11 (HNSW index, COSINE)
- **Cache** : Redis 7 (chat history, metrics)
- **Embeddings** : all-mpnet-base-v2 (768 dim)
- **LLM** : Llama 3.2 3B Q5 (quantized, local)
- **Monitoring** : Prometheus + Grafana

### Fonctionnalités Clés

- ✅ **Lazy Loading** - Modèles chargés à la première requête (pas au boot)
- ✅ **Deduplication** - Retourne documents uniques (pas chunks dupliqués)
- ✅ **Source Citations** - Métadonnées PDF automatiques
- ✅ **Streaming Responses** - Génération mot par mot
- ✅ **Feedback System** - Thumbs up/down avec persistence
- ✅ **Multi-User Sessions** - Historique isolé par session
- ✅ **Metrics & Monitoring** - Dashboards Grafana pré-configurés

---

## 📞 Support

En cas de problème :

1. **Consulter les logs** : `docker logs rag-fastapi`
2. **Vérifier la santé** : `docker ps`
3. **Lire la doc** : Dossier `docs/`
4. **Vérifier Grafana** : http://localhost:3000

---

**Version** : 1.0 (Milvus Migration)
**Date** : 2025-11-27
**Auteur** : Projet IDEMIA RAG
**Statut** : Production Ready ✅
