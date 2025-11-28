# 🚀 Aide-Mémoire des Commandes - Application RAG

## Démarrage Rapide

```bash
# Vérifier l'environnement
./check_deployment.sh

# Démarrer tous les services
./start.sh

# Tester les services
./test_services.sh

# Arrêter tous les services
./stop.sh
```

---

## Gestion des Services

### Démarrage/Arrêt

```bash
# Démarrer tous les services
docker-compose up -d

# Arrêter tous les services
docker-compose down

# Redémarrer tous les services
docker-compose restart

# Redémarrer un service spécifique
docker-compose restart fastapi
docker-compose restart streamlit
docker-compose restart milvus
docker-compose restart redis
```

### État des Services

```bash
# Voir l'état de tous les containers
docker-compose ps

# Voir l'utilisation des ressources en temps réel
docker stats

# Vérifier les health checks
docker inspect --format='{{.State.Health.Status}}' rag-fastapi
docker inspect --format='{{.State.Health.Status}}' milvus-standalone
```

---

## Logs et Debugging

### Voir les Logs

```bash
# Tous les services (temps réel)
docker-compose logs -f

# Service spécifique
docker-compose logs -f fastapi
docker-compose logs -f streamlit
docker-compose logs -f milvus
docker-compose logs -f redis

# Dernières 100 lignes
docker-compose logs --tail=100

# Depuis une heure
docker-compose logs --since 1h

# Exporter les logs
docker-compose logs > application.log
```

### Accès Shell

```bash
# Entrer dans le container FastAPI
docker-compose exec fastapi bash

# Entrer dans le container Streamlit
docker-compose exec streamlit bash

# Entrer dans Redis
docker-compose exec redis redis-cli

# Accès root (si nécessaire)
docker-compose exec -u root fastapi bash
```

---

## Gestion des Documents

### Indexation

```bash
# Indexer tous les documents du dossier data/
docker-compose exec fastapi python preprocess.py preprocess

# Ajouter de nouveaux documents depuis uploads/
docker-compose exec fastapi python preprocess.py add_doc

# Tester la connexion Milvus
docker-compose exec fastapi python test_milvus_conn.py

# Reset de la collection (ATTENTION: perte de données)
docker-compose exec fastapi python reset_collection.py
```

### Upload de Documents

```bash
# Copier des PDFs dans le dossier data
cp mes_documents/*.pdf data/

# Ou dans uploads pour traitement automatique
cp mes_documents/*.pdf uploads/

# Puis indexer
docker-compose exec fastapi python preprocess.py add_doc
```

---

## Monitoring et Métriques

### Accès aux Dashboards

```bash
# Ouvrir Grafana
open http://localhost:3000  # macOS
# ou
xdg-open http://localhost:3000  # Linux
# Login: admin / admin123

# Ouvrir Prometheus
open http://localhost:9090

# API Swagger
open http://localhost:8000/docs
```

### Requêtes Prometheus

```bash
# Depuis le terminal
curl http://localhost:9090/api/v1/query?query=up

# Temps de réponse moyen
curl 'http://localhost:9090/api/v1/query?query=rate(http_request_duration_seconds_sum[5m])/rate(http_request_duration_seconds_count[5m])'
```

---

## Redis - Cache et Historique

### Commandes Redis

```bash
# Connexion Redis
docker-compose exec redis redis-cli

# Dans redis-cli:
PING                              # Test connexion
INFO                              # Informations serveur
DBSIZE                            # Nombre de clés
KEYS chat_history:*               # Lister les sessions
GET chat_history:session123       # Voir une session
FLUSHDB                           # Vider la DB (ATTENTION!)
BGSAVE                            # Backup

# Depuis le terminal
docker-compose exec redis redis-cli INFO
docker-compose exec redis redis-cli DBSIZE
docker-compose exec redis redis-cli KEYS "chat_history:*"
```

### Backup Redis

```bash
# Créer un backup
docker-compose exec redis redis-cli BGSAVE

# Copier le backup
docker cp rag-redis:/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb

# Restaurer (arrêter Redis d'abord)
docker-compose stop redis
docker cp ./redis_backup.rdb rag-redis:/data/dump.rdb
docker-compose start redis
```

---

## Milvus - Base Vectorielle

### Commandes Milvus

```bash
# Vérifier la santé
curl http://localhost:9091/healthz

# Statistiques via Python
docker-compose exec fastapi python -c "
from pymilvus import Collection, connections
connections.connect(host='milvus-standalone', port='19530')
col = Collection('rag_docs')
print(f'Entités: {col.num_entities}')
"
```

---

## Backup et Restauration

### Backup Complet

```bash
# Backup volumes Docker
docker run --rm \
  -v version_using_milvus_milvus_data:/milvus \
  -v version_using_milvus_redis_data:/redis \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup_$(date +%Y%m%d_%H%M%S).tar.gz /milvus /redis

# Backup Redis seul
docker-compose exec redis redis-cli BGSAVE
docker cp rag-redis:/data/dump.rdb ./redis_backup.rdb

# Backup des documents
tar czf documents_backup_$(date +%Y%m%d).tar.gz data/
```

### Restauration

```bash
# Restaurer depuis un backup
docker-compose down
tar xzf backup_20251126_120000.tar.gz -C /
docker-compose up -d
```

---

## Build et Images

### Reconstruire les Images

```bash
# Build sans cache
docker-compose build --no-cache

# Build un service spécifique
docker-compose build fastapi

# Pull des images officielles
docker-compose pull

# Rebuild et redémarrer
docker-compose up -d --build
```

### Nettoyage Docker

```bash
# Nettoyer les images inutilisées
docker image prune -a

# Nettoyer tout (ATTENTION!)
docker system prune -a --volumes

# Voir l'espace utilisé
docker system df
```

---

## Tests et Validation

### Tests Unitaires

```bash
# Lancer les tests pytest
docker-compose exec fastapi pytest

# Tests spécifiques
docker-compose exec fastapi pytest unit_test.py -v

# Avec coverage
docker-compose exec fastapi pytest --cov=. --cov-report=html
```

### Tests API

```bash
# Test endpoint root
curl http://localhost:8000/

# Test chat (remplacer USER_INPUT et SESSION_ID)
curl -X POST "http://localhost:8000/chat?user_input=Bonjour&session_id=test123"

# Test upload PDF
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"

# Test retrieve
curl -X POST "http://localhost:8000/retrieve" \
  -H "Content-Type: application/json" \
  -d '{"query": "test search"}'
```

---

## Troubleshooting

### Problèmes de Démarrage

```bash
# Voir les erreurs
docker-compose logs --tail=50

# Vérifier les ports
lsof -i :8000
lsof -i :8501
lsof -i :19530

# Tuer un processus bloquant
kill -9 <PID>

# Restart complet
docker-compose down -v  # ATTENTION: supprime les données
docker-compose up -d --build
```

### Problèmes de Performance

```bash
# Voir l'utilisation des ressources
docker stats

# Augmenter la mémoire Redis
# Éditer docker-compose.yml: --maxmemory 1gb

# Augmenter workers FastAPI
# Éditer docker-compose.yml: --workers 4

# Redémarrer après modification
docker-compose up -d --force-recreate fastapi
```

### Problèmes de Connexion

```bash
# Test Milvus
docker-compose exec fastapi python test_milvus_conn.py

# Test Redis
docker-compose exec fastapi python -c "import redis_db; redis_db.create_redis_client().ping()"

# Vérifier le réseau
docker network inspect version_using_milvus_rag-network

# Ping entre containers
docker-compose exec fastapi ping milvus-standalone
docker-compose exec fastapi ping rag-redis
```

---

## Maintenance Régulière

### Quotidienne

```bash
# Vérifier l'état
docker-compose ps

# Voir l'utilisation
docker stats --no-stream
```

### Hebdomadaire

```bash
# Backup des données
./backup.sh  # (créer ce script avec les commandes backup ci-dessus)

# Vérifier les logs pour erreurs
docker-compose logs --since 7d | grep -i error

# Nettoyer les logs Docker
docker system prune
```

### Mensuelle

```bash
# Mise à jour des images
docker-compose pull
docker-compose up -d

# Vérifier l'espace disque
df -h
docker system df

# Optimiser Redis
docker-compose exec redis redis-cli BGREWRITEAOF
```

---

## Variables d'Environnement

### Afficher la Configuration

```bash
# Voir les variables d'environnement d'un container
docker-compose exec fastapi env | grep MILVUS
docker-compose exec fastapi env | grep REDIS

# Modifier les variables (éditer .env puis):
docker-compose up -d --force-recreate
```

---

## Liens Rapides

```bash
# Interface Streamlit
http://localhost:8501

# API FastAPI
http://localhost:8000

# Documentation API
http://localhost:8000/docs

# Grafana
http://localhost:3000 (admin/admin123)

# Prometheus
http://localhost:9090

# MinIO Console
http://localhost:9001 (minioadmin/minioadmin)
```

---

## Commandes d'Urgence

```bash
# Tout arrêter immédiatement
docker-compose kill

# Redémarrage d'urgence
docker-compose down && docker-compose up -d

# Voir ce qui consomme (si freeze)
docker stats --no-stream

# Logs d'erreur uniquement
docker-compose logs | grep -i "error\|exception\|failed"
```

---

**💡 Astuce:** Ajoutez ces alias dans votre `~/.bashrc` ou `~/.zshrc`:

```bash
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'
alias dclogs='docker-compose logs -f'
alias dcps='docker-compose ps'
alias dcrestart='docker-compose restart'
```

---

**Dernière mise à jour:** 26 Novembre 2025
