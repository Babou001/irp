# 🚀 Guide de Démarrage Rapide

## Démarrage en 3 étapes

### 1. Préparer l'environnement

```bash
# Vérifier que Docker est installé et en cours d'exécution
docker --version
docker-compose --version

# S'assurer que les modèles sont présents
ls models/Llama-3.2-3B-Instruct-Q4_K_L.gguf
ls models/all-mpnet-base-v2/
```

### 2. Lancer l'application

```bash
# Option A : Utiliser le script de démarrage (recommandé)
../scripts/start.sh

# Option B : Commande manuelle
docker-compose up --build -d
```

### 3. Accéder à l'interface

Ouvrir votre navigateur : **http://localhost:8501**

---

## Vérification rapide

```bash
# Voir l'état de tous les services
docker-compose ps

# Voir les logs en temps réel
docker-compose logs -f

# Tester l'API
curl http://localhost:8000/
```

---

## Premiers pas

1. **Interface Streamlit** (http://localhost:8501)
   - Page "Documents" : Uploader des PDFs
   - Page "Chatbot" : Poser des questions
   - Page "Dashboard" : Voir les statistiques

2. **Monitoring** (http://localhost:3000)
   - Login : `admin` / `admin123`
   - Dashboard pré-configuré disponible

---

## Commandes essentielles

```bash
# Arrêter l'application
../scripts/stop.sh
# ou
docker-compose down

# Redémarrer un service
docker-compose restart fastapi

# Voir les logs d'un service spécifique
docker-compose logs -f streamlit

# Accéder au shell d'un container
docker-compose exec fastapi bash
```

---

## Indexer vos documents

### Via l'interface web (recommandé)
1. Aller sur http://localhost:8501
2. Page "Documents"
3. Uploader vos PDFs

### Via la ligne de commande
```bash
# Copier vos PDFs dans le dossier data/
cp mes_documents/*.pdf data/

# Lancer l'indexation
docker-compose exec fastapi python preprocess.py preprocess
```

---

## Troubleshooting

### ❌ Les services ne démarrent pas
```bash
# Vérifier les logs
docker-compose logs

# Nettoyer et redémarrer
docker-compose down -v
docker-compose up --build
```

### ❌ "Out of memory"
- Augmenter la RAM allouée à Docker Desktop (minimum 8GB)
- Paramètres → Resources → Memory

### ❌ "Port already in use"
```bash
# Trouver le processus qui utilise le port
lsof -i :8501  # ou :8000, :6379, etc.

# Arrêter le processus ou changer le port dans docker-compose.yml
```

---

## 📖 Documentation complète

Pour plus de détails, consultez [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## Support

- Logs : `docker-compose logs -f`
- État des services : `docker-compose ps`
- Docs API : http://localhost:8000/docs
