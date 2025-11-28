#!/bin/bash

echo "=========================================="
echo "  Test des Services Déployés"
echo "=========================================="
echo ""

# Fonction pour tester un endpoint
function test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}

    echo -n "Testing $name... "

    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null)

    if [ "$response" = "$expected_code" ]; then
        echo "✅ OK (HTTP $response)"
        return 0
    else
        echo "❌ FAILED (HTTP $response, expected $expected_code)"
        return 1
    fi
}

# Attendre que les services démarrent
echo "⏳ Attente du démarrage des services (30 secondes)..."
sleep 30

echo ""
echo "🔍 Test des endpoints..."
echo ""

# Test FastAPI
test_endpoint "FastAPI Root" "http://localhost:8000/"

# Test FastAPI Docs
test_endpoint "FastAPI Docs" "http://localhost:8000/docs"

# Test Streamlit (retourne 403 sans cookies, c'est normal)
test_endpoint "Streamlit" "http://localhost:8501/_stcore/health"

# Test Prometheus
test_endpoint "Prometheus" "http://localhost:9090/-/healthy"

# Test Grafana
test_endpoint "Grafana" "http://localhost:3000/api/health"

# Test MinIO
test_endpoint "MinIO" "http://localhost:9000/minio/health/live"

echo ""
echo "🔍 Vérification de l'état des containers..."
docker-compose ps

echo ""
echo "🔍 Test de connexion Redis..."
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: OK"
else
    echo "❌ Redis: FAILED"
fi

echo ""
echo "🔍 Test de connexion Milvus..."
if curl -s http://localhost:9091/healthz | grep -q "OK" 2>/dev/null; then
    echo "✅ Milvus: OK"
else
    echo "❌ Milvus: Vérifier les logs (docker-compose logs milvus)"
fi

echo ""
echo "=========================================="
echo "  Test terminé"
echo "=========================================="
echo ""
echo "Accès aux services:"
echo "  📱 Streamlit:  http://localhost:8501"
echo "  🔌 FastAPI:    http://localhost:8000/docs"
echo "  📊 Grafana:    http://localhost:3000 (admin/admin123)"
echo ""
echo "Pour voir les logs:"
echo "  docker-compose logs -f"
echo ""
