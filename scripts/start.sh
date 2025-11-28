#!/bin/bash

# Se placer dans le dossier racine du projet (parent du dossier scripts)
cd "$(dirname "$0")/.." || exit 1

echo "=========================================="
echo "  RAG Application - Démarrage Docker"
echo "=========================================="
echo ""
echo "📁 Répertoire de travail: $(pwd)"
echo ""

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Installez Docker Desktop d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé."
    exit 1
fi

echo "✅ Docker et Docker Compose sont installés"
echo ""

# Vérifier que les dossiers requis existent
echo "🔍 Vérification des dossiers..."
mkdir -p data uploads preprocessed_data images videos

if [ ! -d "models/all-mpnet-base-v2" ]; then
    echo "⚠️  ATTENTION: Le modèle d'embedding 'models/all-mpnet-base-v2' n'existe pas"
    echo "   Assurez-vous qu'il est présent avant de continuer"
fi

if [ ! -f "models/Llama-3.2-3B-Instruct-Q4_K_L.gguf" ]; then
    echo "⚠️  ATTENTION: Le modèle de génération 'Llama-3.2-3B-Instruct-Q4_K_L.gguf' n'existe pas"
    echo "   Assurez-vous qu'il est présent avant de continuer"
fi

echo ""
echo "📦 Arrêt des conteneurs existants (si présents)..."
docker-compose down

echo ""
echo "🏗️  Construction des images Docker (cela peut prendre 5-10 minutes)..."
docker-compose build

echo ""
echo "🚀 Démarrage des services..."
docker-compose up -d

echo ""
echo "⏳ Attente du démarrage des services (60 secondes)..."
sleep 60

echo ""
echo "🔍 Vérification de l'état des services..."
docker-compose ps

echo ""
echo "=========================================="
echo "  ✅ Déploiement terminé!"
echo "=========================================="
echo ""
echo "Accès aux services:"
echo "  📱 Streamlit:  http://localhost:8501"
echo "  🔌 FastAPI:    http://localhost:8000"
echo "  📊 Grafana:    http://localhost:3000 (admin/admin123)"
echo "  📈 Prometheus: http://localhost:9090"
echo ""
echo "Commandes utiles:"
echo "  Voir les logs:        docker-compose logs -f"
echo "  Arrêter:              docker-compose down"
echo "  Redémarrer:           docker-compose restart"
echo ""
echo "Pour plus d'informations, consultez DEPLOYMENT.md"
echo ""
