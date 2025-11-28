# 📦 Models Required

**IMPORTANT**: Les modèles ML ne sont PAS inclus dans le repository Git car ils sont trop volumineux (>2 GB). Vous devez les télécharger séparément.

## 📥 Modèles à Télécharger

### 1. Modèle d'Embeddings (all-mpnet-base-v2)

**Taille**: ~420 MB

**Méthode 1 - Via Hugging Face Hub** (Recommandé):
```bash
pip install huggingface-hub

# Télécharger le modèle
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/all-mpnet-base-v2', local_dir='./models/all-mpnet-base-v2')"
```

**Méthode 2 - Manuellement**:
1. Aller sur https://huggingface.co/sentence-transformers/all-mpnet-base-v2
2. Télécharger tous les fichiers dans `models/all-mpnet-base-v2/`

**Structure attendue**:
```
models/all-mpnet-base-v2/
├── config.json
├── pytorch_model.bin
├── tokenizer_config.json
├── vocab.txt
├── special_tokens_map.json
└── ... (autres fichiers)
```

---

### 2. Modèle LLM Llama 3.2 3B (Quantifié Q5)

**Taille**: ~2.3 GB

**Méthode 1 - Via Hugging Face** (Recommandé):
```bash
# Installer huggingface-cli
pip install huggingface-hub

# Télécharger le modèle
huggingface-cli download bartowski/Llama-3.2-3B-Instruct-GGUF \
    Llama-3.2-3B-Instruct-Q5_K_L.gguf \
    --local-dir ./models \
    --local-dir-use-symlinks False
```

**Méthode 2 - Manuellement**:
1. Aller sur https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF
2. Cliquer sur "Files and versions"
3. Télécharger `Llama-3.2-3B-Instruct-Q5_K_L.gguf`
4. Le placer dans `models/Llama-3.2-3B-Instruct-Q5_K_L.gguf`

**Structure attendue**:
```
models/
└── Llama-3.2-3B-Instruct-Q5_K_L.gguf  (2.3 GB)
```

---

## ✅ Vérification

Après téléchargement, vérifiez que vous avez cette structure :

```
version_using_milvus/
├── models/
│   ├── all-mpnet-base-v2/
│   │   ├── config.json
│   │   ├── pytorch_model.bin
│   │   └── ... (autres fichiers)
│   └── Llama-3.2-3B-Instruct-Q5_K_L.gguf
├── data/
├── fast_api_app.py
└── ... (autres fichiers)
```

Vérifier la taille des fichiers :
```bash
ls -lh models/all-mpnet-base-v2/
ls -lh models/Llama-3.2-3B-Instruct-Q5_K_L.gguf
```

---

## 🚀 Après le Téléchargement

Une fois les modèles téléchargés, vous pouvez :

### Mode Développement (avec volumes Docker) :
```bash
docker-compose up --build -d
```

### Mode Production (modèles embarqués dans l'image) :
```bash
./scripts/build-production-image.sh --export
docker-compose -f docker-compose.prod.yml up -d
```

---

## ⚠️ Notes Importantes

1. **Espace disque requis** :
   - Modèles : ~2.7 GB
   - Build Docker production : ~20-25 GB temporaires
   - Image finale : ~5-7 GB

2. **Confidentialité** :
   - Les modèles s'exécutent 100% en local
   - Aucune donnée n'est envoyée vers l'extérieur
   - Parfait pour environnements air-gapped

3. **Alternatives** :
   - Si `Llama-3.2-3B-Instruct-Q5_K_L.gguf` n'est pas disponible
   - Vous pouvez utiliser `Q4_K_L` (plus petit, moins performant)
   - Ou `Q6_K` (plus gros, plus performant)
   - Modifier `paths.py` ligne 17 si nécessaire

---

## 📚 Documentation

- Guide de déploiement complet : [README_DEPLOYMENT.md](README_DEPLOYMENT.md)
- Déploiement air-gapped : [docs/AIRGAPPED.md](docs/AIRGAPPED.md)
- Démarrage rapide : [docs/QUICKSTART.md](docs/QUICKSTART.md)
