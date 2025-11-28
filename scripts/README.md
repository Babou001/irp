# 🛠️ Scripts Utilitaires

Collection de scripts pour faciliter le déploiement et la gestion de l'application.

## 📜 Scripts Disponibles

### [start.sh](start.sh)
**Démarrage automatique de l'application**

```bash
./start.sh
```

- Vérifie que Docker est installé
- Crée les dossiers nécessaires
- Vérifie la présence des modèles
- Build les images Docker
- Démarre tous les services
- Affiche les URLs d'accès

**Durée estimée :** 5-10 minutes (première fois)

---

### [stop.sh](stop.sh)
**Arrêt propre de l'application**

```bash
./stop.sh
```

- Arrête tous les containers
- Préserve les données (volumes)

---

### [check_deployment.sh](check_deployment.sh)
**Vérification complète de l'environnement**

```bash
./check_deployment.sh
```

**Vérifie :**
- ✅ Installation Docker & Docker Compose
- ✅ Espace disque disponible
- ✅ Présence des modèles ML
- ✅ Structure des dossiers
- ✅ Fichiers de configuration
- ✅ Disponibilité des ports
- ✅ Configuration monitoring

**15+ vérifications automatiques**

---

### [test_services.sh](test_services.sh)
**Tests automatiques post-déploiement**

```bash
./test_services.sh
```

**Teste :**
- FastAPI (root + docs)
- Streamlit (health check)
- Prometheus (healthy)
- Grafana (API health)
- MinIO (health)
- Redis (PING)
- Milvus (healthz)

**Durée :** ~1 minute

---

## 🎯 Workflow Recommandé

### Premier Déploiement

```bash
# 1. Vérifier l'environnement
./check_deployment.sh

# 2. Démarrer l'application
./start.sh

# 3. Tester les services
./test_services.sh
```

### Utilisation Quotidienne

```bash
# Démarrer
./start.sh

# Arrêter
./stop.sh
```

### Dépannage

```bash
# Vérifier l'environnement
./check_deployment.sh

# Voir les logs
docker-compose logs -f

# Tester les services
./test_services.sh
```

---

## 📝 Notes

- Tous les scripts sont exécutables (`chmod +x`)
- Conçus pour être lancés depuis la racine du projet
- Compatible macOS et Linux
- Sortie colorée et informative

---

Retour à la [documentation](../docs/) | [README principal](../README.md)
