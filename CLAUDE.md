# 🤖 Instructions Claude - Résolution Problèmes

**Dernière mise à jour** : 2025-11-28 13:05

---

## ❌ Problème Actuel : Docker Build Échoue

### Erreur
```
ERROR: failed to solve: failed to compute cache key: failed to calculate checksum of ref: "/models": not found
```

### Cause
Le `.dockerignore` exclut le dossier `models/` → Docker ne voit pas les modèles lors du build production.

### Solution : Switcher les .dockerignore

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
