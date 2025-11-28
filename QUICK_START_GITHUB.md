# 🚀 Quick Start - Déploiement depuis GitHub

Guide rapide pour cloner le projet depuis GitHub et le déployer.

---

## 📋 Prérequis

- Docker + Docker Compose installés
- 25+ GB d'espace disque libre
- Accès à Hugging Face pour télécharger les modèles

---

## 🔧 Étape 1 : Cloner le Repository

```bash
git clone <URL_DU_REPO_GITHUB>
cd version_using_milvus
```

---

## 📦 Étape 2 : Télécharger les Modèles ML

**IMPORTANT** : Les modèles ne sont PAS inclus dans Git (trop volumineux).

### Option A - Via Python (Automatique, recommandé)

```bash
# Installer huggingface-hub
pip install huggingface-hub

# Télécharger le modèle d'embeddings
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/all-mpnet-base-v2', local_dir='./models/all-mpnet-base-v2')"

# Télécharger le modèle LLM
huggingface-cli download bartowski/Llama-3.2-3B-Instruct-GGUF \
    Llama-3.2-3B-Instruct-Q5_K_L.gguf \
    --local-dir ./models \
    --local-dir-use-symlinks False
```

### Option B - Manuellement

Voir les instructions détaillées dans [MODELS_README.md](MODELS_README.md).

### Vérification

```bash
ls -lh models/
# Doit afficher :
# - all-mpnet-base-v2/ (dossier ~420 MB)
# - Llama-3.2-3B-Instruct-Q5_K_L.gguf (fichier ~2.3 GB)
```

---

## 🐳 Étape 3 : Déploiement

### Mode 1 : Développement (Rapide pour tester)

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Démarrer tous les services
docker-compose up --build -d

# Attendre ~2 minutes que tout démarre
docker-compose logs -f fastapi
```

**Accès** : http://localhost:8501

---

### Mode 2 : Production (Recommandé pour serveur)

```bash
# 1. Builder l'image avec modèles embarqués
./scripts/build-production-image.sh --export

# 2. Copier le fichier d'environnement
cp .env.example .env

# 3. Démarrer
docker-compose -f docker-compose.prod.yml up -d

# 4. Vérifier
curl http://localhost:8000/
```

**Accès** :
- Interface : http://localhost:8501
- API : http://localhost:8000
- Grafana : http://localhost:3000 (admin/admin123)

---

## ✅ Vérification du Déploiement

### 1. Vérifier les containers

```bash
docker-compose ps
# Tous les services doivent être "Up" et "healthy"
```

### 2. Tester l'API

```bash
# Health check
curl http://localhost:8000/

# Test de retrieval
curl -X POST http://localhost:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### 3. Tester l'interface

Ouvrir http://localhost:8501 dans un navigateur et :
1. Aller sur "📄 Documents"
2. Uploader un PDF de test
3. Aller sur "💬 Chatbot"
4. Poser une question

---

## 📊 Services Disponibles

| Service | URL | Authentification |
|---------|-----|------------------|
| **Streamlit UI** | http://localhost:8501 | - |
| **FastAPI** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **Grafana** | http://localhost:3000 | admin/admin123 |
| **Prometheus** | http://localhost:9090 | - |

---

## 🛠️ Opérations Courantes

### Arrêter les services
```bash
docker-compose down
```

### Voir les logs
```bash
docker-compose logs -f fastapi
docker-compose logs -f streamlit
```

### Redémarrer
```bash
docker-compose restart
```

### Ajouter des documents
```bash
# Via l'interface (recommandé)
# Aller sur http://localhost:8501 → "📄 Documents" → Upload

# Via CLI
cp nouveaux_docs/*.pdf data/
docker-compose exec fastapi python preprocess.py add_doc
```

---

## 🐛 Troubleshooting

### Les containers ne démarrent pas
```bash
# Vérifier les logs
docker logs rag-fastapi --tail 100

# Vérifier l'espace disque
df -h
docker system df

# Nettoyer si nécessaire
docker system prune -af
```

### Les modèles ne se chargent pas
```bash
# Vérifier que les modèles sont présents
ls -lh models/

# Vérifier dans le container
docker exec rag-fastapi ls -lh /app/models/
```

### Erreur "file locking" sur macOS
```bash
# Utiliser le mode production au lieu du mode dev
docker-compose down
./scripts/build-production-image.sh
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📚 Documentation Complète

- **[README_DEPLOYMENT.md](README_DEPLOYMENT.md)** - Guide complet de déploiement
- **[docs/AIRGAPPED.md](docs/AIRGAPPED.md)** - Déploiement air-gapped
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Guide rapide
- **[MODELS_README.md](MODELS_README.md)** - Téléchargement des modèles
- **[LIVRAISON.md](LIVRAISON.md)** - Note de livraison

---

## 💡 Conseils pour un Déploiement Réussi

1. **Espace disque** : Assurez-vous d'avoir au moins 25 GB libres
2. **Mémoire RAM** : 8 GB minimum recommandé
3. **Première requête** : La première requête au chatbot prendra ~30 secondes (chargement des modèles)
4. **Monitoring** : Utiliser Grafana pour surveiller les performances
5. **Sauvegardes** : Sauvegarder régulièrement les volumes Milvus et Redis

---

## ❓ Support

En cas de problème :
1. Consulter les logs : `docker logs rag-fastapi`
2. Vérifier la documentation dans `docs/`
3. Vérifier les health checks : `docker ps`
4. Consulter Grafana : http://localhost:3000

---

**Version** : 1.0 (Milvus Migration)
**Date** : 2025-11-27
**Statut** : Production Ready ✅
