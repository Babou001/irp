#!/bin/bash

echo "=========================================="
echo "  Vérification de l'environnement"
echo "=========================================="
echo ""

EXIT_CODE=0

# Fonction pour afficher les erreurs
function error() {
    echo "❌ $1"
    EXIT_CODE=1
}

# Fonction pour afficher les succès
function success() {
    echo "✅ $1"
}

# Fonction pour afficher les avertissements
function warning() {
    echo "⚠️  $1"
}

# Vérifier Docker
echo "🔍 Vérification de Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    success "Docker installé: $DOCKER_VERSION"

    if docker ps &> /dev/null; then
        success "Docker daemon en cours d'exécution"
    else
        error "Docker daemon n'est pas en cours d'exécution. Lancez Docker Desktop."
    fi
else
    error "Docker n'est pas installé"
fi

# Vérifier Docker Compose
echo ""
echo "🔍 Vérification de Docker Compose..."
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    success "Docker Compose installé: $COMPOSE_VERSION"
else
    error "Docker Compose n'est pas installé"
fi

# Vérifier l'espace disque
echo ""
echo "🔍 Vérification de l'espace disque..."
AVAILABLE_SPACE=$(df -h . | awk 'NR==2 {print $4}')
echo "   Espace disponible: $AVAILABLE_SPACE"
if [ $(df . | awk 'NR==2 {print $4}') -lt 20000000 ]; then
    warning "Moins de 20GB d'espace disponible. Recommandé: 20GB+"
else
    success "Espace disque suffisant"
fi

# Vérifier la structure des dossiers
echo ""
echo "🔍 Vérification de la structure des dossiers..."
REQUIRED_DIRS=("data" "uploads" "models" "images")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        success "Dossier '$dir' présent"
    else
        warning "Dossier '$dir' manquant (sera créé automatiquement)"
        mkdir -p "$dir"
    fi
done

# Vérifier les modèles
echo ""
echo "🔍 Vérification des modèles..."

if [ -d "models/all-mpnet-base-v2" ]; then
    success "Modèle d'embedding 'all-mpnet-base-v2' présent"
else
    error "Modèle d'embedding 'models/all-mpnet-base-v2' manquant"
    echo "   Téléchargez-le depuis HuggingFace"
fi

if [ -f "models/Llama-3.2-3B-Instruct-Q4_K_L.gguf" ]; then
    MODEL_SIZE=$(du -h models/Llama-3.2-3B-Instruct-Q4_K_L.gguf | cut -f1)
    success "Modèle de génération présent (taille: $MODEL_SIZE)"
else
    warning "Modèle 'Llama-3.2-3B-Instruct-Q4_K_L.gguf' manquant"
    echo "   Utilisez le modèle défini dans paths.py ou ajoutez-le"
fi

# Vérifier les fichiers de configuration
echo ""
echo "🔍 Vérification des fichiers de configuration..."
CONFIG_FILES=("docker-compose.yml" "Dockerfile" "requirements.txt" ".dockerignore")
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        success "Fichier '$file' présent"
    else
        error "Fichier '$file' manquant"
    fi
done

# Vérifier les fichiers Python principaux
echo ""
echo "🔍 Vérification des fichiers Python..."
PYTHON_FILES=("fast_api_app.py" "streamlit_app.py" "retriever.py" "generator.py" "preprocess.py" "paths.py" "redis_db.py")
for file in "${PYTHON_FILES[@]}"; do
    if [ -f "$file" ]; then
        success "Fichier '$file' présent"
    else
        error "Fichier '$file' manquant"
    fi
done

# Vérifier les ports disponibles
echo ""
echo "🔍 Vérification des ports..."
PORTS=(8000 8501 19530 6379 9090 3000 9000 9001)
PORT_NAMES=("FastAPI" "Streamlit" "Milvus" "Redis" "Prometheus" "Grafana" "MinIO" "MinIO Console")
for i in "${!PORTS[@]}"; do
    PORT=${PORTS[$i]}
    NAME=${PORT_NAMES[$i]}
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        warning "Port $PORT ($NAME) est déjà utilisé"
    else
        success "Port $PORT ($NAME) disponible"
    fi
done

# Vérifier monitoring
echo ""
echo "🔍 Vérification de la configuration monitoring..."
if [ -f "monitoring/prometheus.yml" ]; then
    success "Configuration Prometheus présente"
else
    error "Configuration Prometheus manquante"
fi

if [ -d "monitoring/grafana/provisioning" ]; then
    success "Configuration Grafana présente"
else
    error "Configuration Grafana manquante"
fi

# Résumé
echo ""
echo "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "  ✅ Tous les prérequis sont satisfaits"
    echo "=========================================="
    echo ""
    echo "Vous pouvez maintenant lancer l'application:"
    echo "  ./start.sh"
    echo ""
else
    echo "  ⚠️  Des problèmes ont été détectés"
    echo "=========================================="
    echo ""
    echo "Corrigez les erreurs ci-dessus avant de continuer."
    echo ""
fi

exit $EXIT_CODE
