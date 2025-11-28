# Déploiement Docker - Application RAG IDEMIA

## Vue d'ensemble

Cette application RAG (Retrieval-Augmented Generation) est complètement dockerisée pour un déploiement facile et reproductible. Elle comprend :

- **FastAPI** : Backend API REST
- **Streamlit** : Interface utilisateur web
- **Milvus** : Base de données vectorielle pour le RAG
- **Redis** : Cache et historique des conversations
- **Prometheus** : Collecte de métriques
- **Grafana** : Visualisation et dashboards

## 🎯 Deux modes de déploiement

Ce projet supporte **deux modes de déploiement** selon vos besoins :

### Mode Développement (`docker-compose.yml`)
- ✅ Modèles montés en volumes (changements à chaud)
- ✅ Rebuild rapide
- ✅ Parfait pour tester et développer
- ⚠️ Peut avoir des problèmes de file locking sur macOS
- **Usage** : `docker-compose up`

### Mode Production (`docker-compose.prod.yml`)
- ✅ **Modèles embarqués dans l'image** Docker
- ✅ **100% autonome** - aucune dépendance externe
- ✅ **Air-gapped ready** - fonctionne sans Internet
- ✅ Pas de problèmes de file locking
- ✅ Parfait pour environnements d'entreprise restreints
- ⚠️ Image plus lourde (~6-7 GB)
- **Usage** : Voir section "Déploiement Production" ci-dessous

**🔒 Pour un déploiement air-gapped**, consultez [AIRGAPPED.md](AIRGAPPED.md)

## Prérequis

### Logiciels requis
- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Au moins 8 GB de RAM disponible
- 20 GB d'espace disque libre

### Fichiers requis
Avant de déployer, assurez-vous que ces dossiers/fichiers existent :

```
version_using_milvus/
├── models/
│   ├── Llama-3.2-3B-Instruct-Q4_K_L.gguf  # Modèle de génération
│   └── all-mpnet-base-v2/                  # Modèle d'embedding
├── data/                                    # Corpus de documents PDF
├── uploads/                                 # Dossier pour uploads temporaires
└── images/                                  # Ressources images
```

## Installation rapide

### 1. Cloner/Préparer le projet

```bash
cd /path/to/version_using_milvus
```

### 2. Vérifier la structure des dossiers

```bash
# Créer les dossiers manquants si nécessaire
mkdir -p data uploads preprocessed_data images videos
```

### 3. Configuration (optionnel)

Copier le fichier `.env.example` en `.env` et ajuster si nécessaire :

```bash
cp .env.example .env
```

Les valeurs par défaut fonctionnent pour un déploiement local.

### 4. Lancer l'application

```bash
# Build et démarrage de tous les services
docker-compose up --build -d

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f fastapi
docker-compose logs -f streamlit
```

### 5. Vérifier le déploiement

Attendre environ 2-3 minutes que tous les services démarrent. Vérifier l'état :

```bash
docker-compose ps
```

Tous les services doivent être en état `healthy` ou `running`.

---

## 🏢 Déploiement Production (Recommandé pour l'entreprise)

### Pourquoi le mode production ?

- ✅ **Modèles embarqués** - Pas besoin de monter `/models` en volume
- ✅ **Pas de problèmes de file locking** - Fonctionne sur macOS/Linux/Windows
- ✅ **Air-gapped ready** - Déploiement sans Internet possible
- ✅ **Portable** - Une seule image `.tar` à transférer

### Étape 1 : Build de l'image production

```bash
# Build l'image avec modèles embarqués (~6-7 GB)
./scripts/build-production-image.sh

# OU avec export automatique vers fichier .tar
./scripts/build-production-image.sh --export
```

Le script va automatiquement :
1. Vérifier que les modèles sont présents
2. Builder l'image Docker avec modèles inclus
3. (Optionnel) Exporter vers `rag-system-prod.tar`

**Durée** : 5-10 minutes

### Étape 2 : Déployer en mode production

```bash
# Démarrer avec la configuration production
docker-compose -f docker-compose.prod.yml up -d

# Suivre les logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Étape 3 : Vérification

```bash
# Vérifier l'état des services
docker-compose -f docker-compose.prod.yml ps

# Test rapide de l'API
curl http://localhost:8000/
# Réponse attendue : {"message":"FastAPI is running!"}
```

### Transfert vers un autre serveur

```bash
# 1. Export de l'image (si pas déjà fait)
docker save rag-system:prod -o rag-system-prod.tar

# 2. Transférer vers le serveur
scp rag-system-prod.tar user@server:/tmp/
scp docker-compose.prod.yml user@server:/opt/rag-system/

# 3. Sur le serveur, charger l'image
ssh user@server
cd /opt/rag-system
docker load -i /tmp/rag-system-prod.tar

# 4. Démarrer les services
docker-compose -f docker-compose.prod.yml up -d
```

**📘 Guide complet** : Pour un déploiement air-gapped détaillé, consultez [AIRGAPPED.md](AIRGAPPED.md)

---

## Accès aux services

| Service | URL | Identifiants |
|---------|-----|--------------|
| **Streamlit** (Interface principale) | http://localhost:8501 | - |
| **FastAPI** (API Backend) | http://localhost:8000 | - |
| **FastAPI Docs** (Swagger) | http://localhost:8000/docs | - |
| **Grafana** (Monitoring) | http://localhost:3000 | admin / admin123 |
| **Prometheus** | http://localhost:9090 | - |
| **MinIO Console** | http://localhost:9001 | minioadmin / minioadmin |

## Initialisation des données

### Première utilisation - Indexation des documents

Si tu as déjà des documents dans le dossier `data/`, ils seront automatiquement indexés au premier lancement du FastAPI.

Pour forcer une ré-indexation :

```bash
docker-compose exec fastapi python preprocess.py preprocess
```

### Ajouter de nouveaux documents

1. Via l'interface Streamlit (page Documents)
2. Via l'API FastAPI : `POST /upload`
3. Manuellement :
   ```bash
   # Copier les PDFs dans uploads/
   cp nouveaux_documents/*.pdf uploads/

   # Indexer
   docker-compose exec fastapi python preprocess.py add_doc
   ```

## Monitoring et Observabilité

### Grafana Dashboards

1. Ouvrir http://localhost:3000
2. Login : `admin` / `admin123`
3. Aller dans "Dashboards" → "RAG Monitoring" → "RAG Application Overview"

**Métriques disponibles :**
- Nombre de requêtes chat par seconde
- Temps de réponse moyen
- Taux d'upload de documents
- Taille de la collection Milvus
- Utilisation mémoire Redis
- Taux d'erreurs API
- Latence des requêtes Milvus

### Prometheus

Accéder aux métriques brutes : http://localhost:9090

Exemples de requêtes PromQL :
```
# Temps de réponse moyen
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# Nombre de vecteurs dans Milvus
milvus_collection_entities_count{collection_name="rag_docs"}
```

## Commandes utiles

### Gestion des services

```bash
# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes (ATTENTION : perte de données)
docker-compose down -v

# Redémarrer un service spécifique
docker-compose restart fastapi

# Voir l'utilisation des ressources
docker stats

# Reconstruire les images
docker-compose build --no-cache
```

### Debugging

```bash
# Entrer dans le container FastAPI
docker-compose exec fastapi bash

# Entrer dans le container Streamlit
docker-compose exec streamlit bash

# Vérifier la connexion à Milvus
docker-compose exec fastapi python test_milvus_conn.py

# Voir les logs en temps réel
docker-compose logs -f --tail=100
```

### Backup et Restauration

```bash
# Backup des données Milvus
docker run --rm -v version_using_milvus_milvus_data:/data -v $(pwd):/backup alpine tar czf /backup/milvus_backup.tar.gz /data

# Backup Redis
docker-compose exec redis redis-cli BGSAVE
docker cp rag-redis:/data/dump.rdb ./redis_backup.rdb

# Restauration Milvus
docker run --rm -v version_using_milvus_milvus_data:/data -v $(pwd):/backup alpine tar xzf /backup/milvus_backup.tar.gz -C /
```

## Scaling et Performance

### Ajuster les ressources

Modifier `docker-compose.yml` pour limiter/augmenter les ressources :

```yaml
fastapi:
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 4G
      reservations:
        cpus: '1.0'
        memory: 2G
```

### Augmenter le nombre de workers FastAPI

Dans `docker-compose.yml` :

```yaml
fastapi:
  command: uvicorn fast_api_app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Troubleshooting

### Problème : Les services ne démarrent pas

**Solution :**
```bash
# Vérifier les logs
docker-compose logs

# Vérifier l'espace disque
df -h

# Vérifier la mémoire
free -h

# Nettoyer Docker
docker system prune -a
```

### Problème : Milvus ne se connecte pas

**Solution :**
```bash
# Vérifier que Milvus est healthy
docker-compose ps milvus

# Vérifier les logs Milvus
docker-compose logs milvus

# Redémarrer Milvus et ses dépendances
docker-compose restart etcd minio milvus
```

### Problème : L'indexation échoue

**Solution :**
```bash
# Vérifier la structure des fichiers
ls -lh data/
ls -lh models/

# Tester la connexion Milvus
docker-compose exec fastapi python test_milvus_conn.py

# Reset de la collection (ATTENTION : perte de données)
docker-compose exec fastapi python reset_collection.py
```

### Problème : Performances lentes

**Solutions :**
1. Augmenter la RAM allouée à Docker
2. Réduire `CHUNK_SIZE` dans `.env`
3. Augmenter le cache Redis : `maxmemory 1gb`
4. Utiliser un SSD pour les volumes Docker

## Architecture réseau

```
┌─────────────────────────────────────────────────────────────┐
│                        rag-network                          │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │ Streamlit│───▶│ FastAPI  │───▶│  Milvus  │             │
│  │  :8501   │    │  :8000   │    │  :19530  │             │
│  └──────────┘    └──────────┘    └──────────┘             │
│                        │               │                    │
│                        │          ┌────▼─────┐             │
│                        ├─────────▶│  Redis   │             │
│                        │          │  :6379   │             │
│                        │          └──────────┘             │
│                        │                                    │
│                   ┌────▼──────┐     ┌──────────┐           │
│                   │Prometheus │────▶│ Grafana  │           │
│                   │  :9090    │     │  :3000   │           │
│                   └───────────┘     └──────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Sécurité

### Pour la production

1. **Changer les mots de passe par défaut** dans `.env` :
   - `GF_SECURITY_ADMIN_PASSWORD`
   - `MINIO_ROOT_PASSWORD`

2. **Utiliser HTTPS** avec un reverse proxy (nginx, traefik)

3. **Limiter l'accès réseau** :
   ```yaml
   services:
     prometheus:
       ports: []  # Retirer l'exposition publique
       expose:
         - "9090"
   ```

4. **Activer l'authentification** sur FastAPI

5. **Configurer les firewalls** du serveur

## Support

Pour toute question ou problème :
1. Vérifier les logs : `docker-compose logs -f`
2. Consulter ce README
3. Vérifier les issues GitHub du projet

## Maintenance

### Mises à jour

```bash
# Mettre à jour les images Docker
docker-compose pull

# Reconstruire avec les nouvelles dépendances
docker-compose up --build -d
```

### Nettoyage régulier

```bash
# Nettoyer les logs Docker
docker system prune -a --volumes

# Nettoyer les vieilles sessions Redis
docker-compose exec redis redis-cli FLUSHDB
```

---

**Version :** 1.0
**Date :** 2025-11
**Auteur :** IDEMIA RAG Project
