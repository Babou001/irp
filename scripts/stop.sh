#!/bin/bash

# Se placer dans le dossier racine du projet
cd "$(dirname "$0")/.." || exit 1

echo "=========================================="
echo "  RAG Application - Arrêt"
echo "=========================================="
echo ""
echo "📁 Répertoire de travail: $(pwd)"
echo ""

echo "🛑 Arrêt des services..."
docker-compose down

echo ""
echo "✅ Tous les services sont arrêtés"
echo ""
echo "💡 Pour supprimer également les volumes (données):"
echo "   docker-compose down -v"
echo ""
