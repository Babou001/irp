# Application RAG IDEMIA - Version Dockerisée

## 🚀 Démarrage Rapide

```bash
# 1. Vérifier les prérequis
./scripts/check_deployment.sh

# 2. Lancer l'application
./scripts/start.sh

# 3. Accéder à l'interface
# http://localhost:8501
```

**Documentation complète :** [DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 📋 Vue d'ensemble

Application RAG (Retrieval-Augmented Generation) pour interroger intelligemment une base documentaire PDF.

### Architecture
- **FastAPI** : API REST backend
- **Streamlit** : Interface utilisateur multi-pages
- **Milvus** : Base de données vectorielle
- **Redis** : Cache et historique des conversations
- **Llama 3.2** : Génération de réponses
- **Prometheus + Grafana** : Monitoring

### ✅ Prêt pour la Production
- Entièrement dockerisé
- Monitoring intégré
- Scripts de déploiement automatisés
- Documentation complète

---

## 📦 Structure du Projet

```
├── README.md                # Ce fichier
├── docker-compose.yml       # Orchestration services
├── Dockerfile               # Image application
├── .env.example             # Template configuration
│
├── docs/                    # 📚 Documentation
│   ├── QUICKSTART.md
│   ├── DEPLOYMENT.md
│   ├── HANDOVER.md
│   ├── NEXT_STEPS.md
│   ├── COMMANDS_CHEATSHEET.md
│   └── SUMMARY.md
│
├── scripts/                 # 🛠️ Scripts utilitaires
│   ├── start.sh
│   ├── stop.sh
│   ├── check_deployment.sh
│   └── test_services.sh
│
├── streamlit_pages/         # Pages Streamlit
│   ├── home.py
│   ├── chatbot.py
│   ├── documents.py
│   ├── document_mining.py
│   └── dashboard.py
│
├── monitoring/              # Config Prometheus/Grafana
│
├── fast_api_app.py          # Backend API
├── streamlit_app.py         # Interface utilisateur
├── retriever.py             # Recherche vectorielle Milvus
├── generator.py             # Génération LLM
├── preprocess.py            # Indexation documents
└── redis_db.py              # Gestion cache
```

---

## 🎯 Fonctionnalités

### 1. Interface Multi-Pages Streamlit
- **Home** : Page d'accueil
- **Documents** : Upload et gestion des PDFs
- **Document Mining** : Recherche et visualisation des documents
- **Chatbot** : Conversation avec l'IA (multi-utilisateurs)
- **Dashboard** : Statistiques et métriques

### 2. Chatbot Multi-Utilisateurs
- Sessions isolées par utilisateur
- Historique persistant (Redis)
- File d'attente pour gérer la concurrence
- Partage d'instance du modèle LLM

### 3. Visualisation PDF Intégrée
- Affichage des PDFs dans l'interface
- Navigation dans les documents
- Pas besoin de téléchargement

### 4. Tests Unitaires
- Framework pytest
- Fichier `unit_test.py`

### 5. Monitoring Production
- Dashboards Grafana pré-configurés
- Métriques temps réel (Prometheus)
- Alertes automatiques

---

## 🛠️ Déploiement

### Prérequis
- Docker 20.10+
- Docker Compose 2.0+
- 8 GB RAM minimum
- 50 GB espace disque

### Installation

```bash
# Clone ou transfert du projet
cd version_using_milvus

# Vérification pré-déploiement
./scripts/check_deployment.sh

# Démarrage
./scripts/start.sh

# Test des services
./scripts/test_services.sh
```

### Accès aux Services

| Service | URL | Description |
|---------|-----|-------------|
| Streamlit | http://localhost:8501 | Interface utilisateur |
| FastAPI | http://localhost:8000 | API REST |
| API Docs | http://localhost:8000/docs | Documentation Swagger |
| Grafana | http://localhost:3000 | Dashboards (admin/admin123) |
| Prometheus | http://localhost:9090 | Métriques brutes |

---

## 📚 Documentation

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Démarrage en 3 étapes
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guide complet de déploiement
- **[HANDOVER.md](docs/HANDOVER.md)** - Document de passation
- **[NEXT_STEPS.md](docs/NEXT_STEPS.md)** - Prochaines étapes
- **[COMMANDS_CHEATSHEET.md](docs/COMMANDS_CHEATSHEET.md)** - Aide-mémoire commandes
- **[Support.md](Support.md)** - Support technique

---

## 🔧 Commandes Utiles

```bash
# Voir les logs
docker-compose logs -f

# Arrêter l'application
./scripts/stop.sh

# Redémarrer un service
docker-compose restart fastapi

# Indexer de nouveaux documents
docker-compose exec fastapi python preprocess.py add_doc

# Backup des données
docker-compose exec redis redis-cli BGSAVE
```

---

## 🐛 Troubleshooting

Consulter [DEPLOYMENT.md](docs/DEPLOYMENT.md) pour les problèmes courants et solutions.

```bash
# Vérifier l'état des services
docker-compose ps

# Voir les logs détaillés
docker-compose logs -f --tail=100

# Test connexion Milvus
docker-compose exec fastapi python test_milvus_conn.py
```

---

## 📊 Monitoring

Dashboard Grafana inclut :
- Temps de réponse moyen
- Nombre de requêtes/sec
- Utilisation mémoire Redis
- Taille collection Milvus
- Taux d'erreurs API
- Sessions actives

---

## 🔐 Sécurité

Pour la production :
1. Changer les mots de passe (`.env`)
2. Activer HTTPS (reverse proxy)
3. Configurer le firewall
4. Limiter l'accès réseau

---

## 📈 Version & Changelog

**Version actuelle :** 1.0 - Production Ready

### Nouvelles Fonctionnalités (v1.0)
- ✅ Dockerisation complète
- ✅ Monitoring Prometheus + Grafana
- ✅ Scripts de déploiement automatisés
- ✅ Documentation exhaustive
- ✅ Migration Milvus (vs ChromaDB)
- ✅ Support variables d'environnement

### Fonctionnalités Existantes
- ✅ Interface multi-pages Streamlit
- ✅ Chatbot multi-utilisateurs
- ✅ Visualisation PDF intégrée
- ✅ Tests unitaires (pytest)
- ✅ Cache Redis avec historique
- ✅ Worker pool FastAPI

---

## 👥 Contributeurs

Développé pendant l'alternance chez IDEMIA.

---

## 📞 Support

Pour toute question :
1. Consulter la documentation ([DEPLOYMENT.md](docs/DEPLOYMENT.md))
2. Vérifier les logs : `docker-compose logs -f`
3. Exécuter le check : `./scripts/check_deployment.sh`