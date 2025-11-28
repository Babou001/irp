# 📋 Document de Passation - Application RAG IDEMIA

## 📌 Informations Générales

**Projet :** Application RAG (Retrieval-Augmented Generation)
**Développeur :** [Votre Nom]
**Période :** [Dates de l'alternance]
**Date de passation :** [Date]
**Version :** 1.0 - Production Ready

---

## 🎯 Résumé Exécutif

Cette application RAG permet d'interroger intelligemment une base documentaire PDF en utilisant :
- **Milvus** pour la recherche vectorielle
- **Llama 3.2** pour la génération de réponses
- **FastAPI** pour l'API backend
- **Streamlit** pour l'interface utilisateur
- **Redis** pour le cache et l'historique
- **Prometheus + Grafana** pour le monitoring

**État actuel :** ✅ **Prêt pour le déploiement** - Entièrement dockerisé et documenté.

---

## 📦 Contenu Livré

### 1. Application Principale
```
├── fast_api_app.py          # API REST backend
├── streamlit_app.py         # Interface utilisateur
├── retriever.py             # Système de recherche Milvus
├── generator.py             # Génération de réponses LLM
├── preprocess.py            # Indexation des documents
├── redis_db.py              # Gestion cache/historique
└── paths.py                 # Configuration des chemins
```

### 2. Infrastructure Docker
```
├── Dockerfile               # Image de l'application
├── docker-compose.yml       # Orchestration complète
├── .dockerignore           # Optimisation du build
├── .env.example            # Variables d'environnement
└── requirements.txt        # Dépendances Python (VÉRIFIÉ ✅)
```

### 3. Monitoring
```
monitoring/
├── prometheus.yml                           # Configuration métriques
└── grafana/
    └── provisioning/
        ├── datasources/prometheus.yml       # Source de données
        └── dashboards/
            ├── dashboards.yml               # Config dashboards
            └── json/rag-overview.json       # Dashboard pré-configuré
```

### 4. Documentation
```
├── DEPLOYMENT.md           # Guide de déploiement complet (⭐ IMPORTANT)
├── QUICKSTART.md          # Démarrage en 3 étapes
├── HANDOVER.md           # Ce document
├── README.md             # Documentation projet
└── Support.md            # Support technique
```

### 5. Scripts Utilitaires
```
├── start.sh                # 🚀 Démarrage automatique
├── stop.sh                 # 🛑 Arrêt propre
└── check_deployment.sh     # ✅ Vérification pré-déploiement
```

---

## 🚀 Déploiement - Guide Rapide

### Prérequis Serveur
- **OS :** Linux (Ubuntu 20.04+ recommandé) ou Windows Server avec Docker
- **RAM :** Minimum 8 GB (16 GB recommandé)
- **CPU :** 4 cores minimum (8 cores recommandé)
- **Disque :** 50 GB minimum (SSD recommandé)
- **Docker :** Version 20.10+
- **Docker Compose :** Version 2.0+

### Installation en 4 Étapes

```bash
# 1. Transférer le projet sur le serveur
scp -r version_using_milvus user@serveur:/opt/

# 2. Se connecter au serveur
ssh user@serveur

# 3. Aller dans le dossier
cd /opt/version_using_milvus

# 4. Vérifier et lancer
./check_deployment.sh    # Vérification
./start.sh               # Démarrage
```

**C'est tout ! L'application sera accessible sur :**
- Interface : http://serveur:8501
- API : http://serveur:8000
- Monitoring : http://serveur:3000

---

## 📊 Architecture Déployée

```
┌─────────────────────────────────────────────────┐
│            Serveur Docker Host                  │
│                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │Streamlit │───▶│ FastAPI  │───▶│  Milvus  │ │
│  │  :8501   │    │  :8000   │    │  :19530  │ │
│  └──────────┘    └──────────┘    └──────────┘ │
│                        │               │        │
│                        ├──────────────▶┤        │
│                        │          ┌────▼─────┐  │
│                        └─────────▶│  Redis   │  │
│                                   │  :6379   │  │
│                                   └──────────┘  │
│                                                 │
│  ┌───────────┐         ┌──────────┐            │
│  │Prometheus │────────▶│ Grafana  │            │
│  │  :9090    │         │  :3000   │            │
│  └───────────┘         └──────────┘            │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Configuration Importante

### Variables d'Environnement (`.env`)

Les valeurs par défaut fonctionnent, mais vous pouvez personnaliser :

```env
# Connexions internes (NE PAS CHANGER pour Docker)
MILVUS_HOST=milvus-standalone
REDIS_HOST=rag-redis

# Sécurité - À CHANGER en production
GF_SECURITY_ADMIN_PASSWORD=admin123    # ⚠️ Changez ce mot de passe !

# Performance
CHUNK_SIZE=1200          # Taille des chunks de texte
CHUNK_OVERLAP=150        # Chevauchement entre chunks
MAX_PDF_MB=25           # Taille max des uploads
```

### Ports Exposés

| Service | Port | Accès |
|---------|------|-------|
| Streamlit | 8501 | Public (utilisateurs) |
| FastAPI | 8000 | Public (API) |
| Grafana | 3000 | Interne (monitoring) |
| Prometheus | 9090 | Interne (métriques) |
| Milvus | 19530 | Interne |
| Redis | 6379 | Interne |

---

## 📈 Monitoring et Métriques

### Dashboards Grafana (http://serveur:3000)

**Login :** `admin` / `admin123` (à changer !)

**Métriques disponibles :**
1. **Performance**
   - Temps de réponse moyen
   - Requêtes/seconde
   - Latence des requêtes Milvus

2. **Utilisation**
   - Nombre de sessions actives
   - Documents uploadés
   - Taille de la base vectorielle

3. **Santé système**
   - Utilisation mémoire Redis
   - Taux d'erreurs API
   - État des services

### Alertes Pré-configurées
- ⚠️ Taux d'erreur API > 10%
- ⚠️ Temps de réponse > 5s
- ⚠️ Mémoire Redis > 90%

---

## 🔒 Sécurité - Points d'Attention

### ✅ Déjà Implémenté
- Utilisateur non-root dans les containers
- Validation des uploads PDF
- Limite de taille des fichiers (25 MB)
- Sanitization des noms de fichiers
- Isolation réseau Docker

### ⚠️ À Faire en Production
1. **Changer les mots de passe**
   ```env
   GF_SECURITY_ADMIN_PASSWORD=VotreMotDePasseFort!
   MINIO_ROOT_PASSWORD=AutreMotDePasseSecurise!
   ```

2. **Activer HTTPS** avec reverse proxy (nginx/traefik)

3. **Limiter l'accès réseau** (firewall)
   ```bash
   # Exemple: autoriser seulement votre réseau
   sudo ufw allow from 192.168.1.0/24 to any port 8501
   ```

4. **Authentification utilisateurs** (à implémenter si nécessaire)

---

## 🛠️ Maintenance

### Opérations Courantes

#### Voir les logs
```bash
docker-compose logs -f                    # Tous les services
docker-compose logs -f fastapi            # Service spécifique
docker-compose logs --tail=100 streamlit  # Dernières 100 lignes
```

#### Redémarrer un service
```bash
docker-compose restart fastapi
docker-compose restart streamlit
```

#### Ajouter des documents
```bash
# Option 1: Via l'interface web (recommandé)
# Aller sur http://serveur:8501 → Page Documents

# Option 2: Via ligne de commande
cp documents/*.pdf data/
docker-compose exec fastapi python preprocess.py preprocess
```

#### Backup des données
```bash
# Backup Milvus
docker run --rm -v version_using_milvus_milvus_data:/data \
  -v $(pwd):/backup alpine tar czf /backup/milvus_backup.tar.gz /data

# Backup Redis
docker-compose exec redis redis-cli BGSAVE
docker cp rag-redis:/data/dump.rdb ./redis_backup.rdb
```

### Mises à Jour

```bash
# 1. Pull les nouvelles images
docker-compose pull

# 2. Rebuild avec nouvelles dépendances
docker-compose build --no-cache

# 3. Redémarrer
docker-compose up -d
```

---

## 🐛 Problèmes Connus et Solutions

### Problème 1 : "Out of memory"
**Solution :** Augmenter la RAM de Docker ou du serveur
```bash
# Vérifier l'utilisation
docker stats

# Augmenter dans docker-compose.yml si nécessaire
```

### Problème 2 : Milvus ne démarre pas
**Solution :** Vérifier les dépendances (etcd, minio)
```bash
docker-compose logs etcd
docker-compose logs minio
docker-compose restart etcd minio milvus
```

### Problème 3 : Lenteur des recherches
**Solutions :**
- Augmenter `ef` dans retriever.py (search_params)
- Utiliser un SSD
- Réduire la taille du corpus

---

## 📞 Support

### Documentation Complète
- **DEPLOYMENT.md** - Guide détaillé de déploiement
- **QUICKSTART.md** - Démarrage rapide
- API Swagger - http://serveur:8000/docs

### Commandes de Diagnostic
```bash
# État des services
docker-compose ps

# Utilisation ressources
docker stats

# Test connexion Milvus
docker-compose exec fastapi python test_milvus_conn.py

# Logs détaillés
docker-compose logs -f --tail=200
```

### Contacts Techniques (à compléter)
- **DevOps :** [email@idemia.com]
- **Support IT :** [support@idemia.com]

---

## ✅ Checklist de Déploiement

### Avant le Déploiement
- [ ] Serveur provisionné (8GB+ RAM, 50GB+ disque)
- [ ] Docker et Docker Compose installés
- [ ] Ports 8501, 8000, 3000 disponibles
- [ ] Modèles ML présents dans `models/`
- [ ] Documents PDF dans `data/` (optionnel)

### Pendant le Déploiement
- [ ] Exécuter `./check_deployment.sh` avec succès
- [ ] Modifier `.env` (changer mots de passe)
- [ ] Exécuter `./start.sh`
- [ ] Vérifier que tous les services sont "healthy"
- [ ] Accéder à http://serveur:8501

### Après le Déploiement
- [ ] Tester l'upload d'un document
- [ ] Tester une requête chat
- [ ] Configurer Grafana
- [ ] Configurer les backups automatiques
- [ ] Configurer le firewall
- [ ] Documenter les accès pour l'équipe

---

## 📝 Notes Techniques

### Choix Techniques
- **Milvus** : Choisi pour performance et scalabilité (vs ChromaDB)
- **Docker** : Pour portabilité et reproductibilité
- **Llama 3.2** : Modèle local (pas de dépendance cloud)
- **Redis** : Cache rapide + persistence chat history

### Limitations Actuelles
- Modèle LLM local uniquement (pas d'API externe)
- Un seul worker FastAPI (à scaler si besoin)
- Pas d'authentification utilisateurs (à ajouter si nécessaire)

### Évolutions Possibles
1. **Next.js frontend** : Migration de Streamlit vers Next.js (planifiée)
2. **Multi-tenancy** : Support de plusieurs organisations
3. **API Keys** : Authentification API
4. **OCR** : Support des PDF scannés
5. **Langues** : Support multilingue


**Pour démarrer immédiatement :**
```bash
./check_deployment.sh && ./start.sh
```



---

**Document préparé par :** [Votre Nom]
**Date :** [Date]
**Contact :** [Votre Email]
