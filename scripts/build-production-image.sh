#!/bin/bash
# =============================================================================
# build-production-image.sh - Build production Docker image with embedded models
# =============================================================================
# This script builds a self-contained Docker image for air-gapped deployment.
#
# What it does:
#   1. Verifies all required models are present
#   2. Builds Docker image with models embedded (~6-7 GB)
#   3. Tags the image as rag-system:prod
#   4. Optionally exports to .tar file for transfer
#
# Usage:
#   ./scripts/build-production-image.sh              # Build only
#   ./scripts/build-production-image.sh --export     # Build + export to tar
#   ./scripts/build-production-image.sh --help       # Show help
#
# Requirements:
#   - Docker installed
#   - ~10 GB free disk space
#   - models/ directory with:
#     * all-mpnet-base-v2/
#     * Llama-3.2-3B-Instruct-Q5_K_L.gguf
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="rag-system"
IMAGE_TAG="prod"
EXPORT_FILE="rag-system-prod.tar"

# Change to project root
cd "$(dirname "$0")/.."

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

show_help() {
    cat << EOF
Build Production Docker Image with Embedded Models

Usage: $0 [OPTIONS]

Options:
    --export        Export image to ${EXPORT_FILE} after building
    --no-cache      Build without using Docker cache
    --tag TAG       Use custom tag (default: ${IMAGE_TAG})
    --help          Show this help message

Examples:
    $0                      # Build image
    $0 --export             # Build and export
    $0 --tag v1.0 --export  # Build with custom tag and export

The resulting image will be:
    - Size: ~6-7 GB
    - Name: ${IMAGE_NAME}:${IMAGE_TAG}
    - Self-contained (no internet required for deployment)

EOF
    exit 0
}

# =============================================================================
# Pre-flight Checks
# =============================================================================

check_requirements() {
    print_header "Pre-flight Checks"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker found: $(docker --version)"

    # Check disk space (need ~10GB)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        AVAILABLE_GB=$(df -g . | tail -1 | awk '{print $4}')
    else
        AVAILABLE_GB=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
    fi

    if [ "$AVAILABLE_GB" -lt 10 ]; then
        print_warning "Low disk space: ${AVAILABLE_GB}GB available (10GB+ recommended)"
    else
        print_success "Disk space: ${AVAILABLE_GB}GB available"
    fi

    # Check models directory
    if [ ! -d "models" ]; then
        print_error "models/ directory not found"
        exit 1
    fi
    print_success "models/ directory found"

    # Check embedding model
    if [ ! -d "models/all-mpnet-base-v2" ]; then
        print_error "Embedding model not found: models/all-mpnet-base-v2/"
        print_info "Download from: https://huggingface.co/sentence-transformers/all-mpnet-base-v2"
        exit 1
    fi
    print_success "Embedding model found: all-mpnet-base-v2"

    # Check LLM model
    if [ ! -f "models/Llama-3.2-3B-Instruct-Q5_K_L.gguf" ]; then
        print_error "LLM model not found: models/Llama-3.2-3B-Instruct-Q5_K_L.gguf"
        print_info "Expected path: models/Llama-3.2-3B-Instruct-Q5_K_L.gguf"
        exit 1
    fi
    MODEL_SIZE=$(du -h "models/Llama-3.2-3B-Instruct-Q5_K_L.gguf" | cut -f1)
    print_success "LLM model found: Llama-3.2-3B-Instruct-Q5_K_L.gguf ($MODEL_SIZE)"

    # Check Dockerfile.prod
    if [ ! -f "Dockerfile.prod" ]; then
        print_error "Dockerfile.prod not found"
        exit 1
    fi
    print_success "Dockerfile.prod found"

    echo ""
}

# =============================================================================
# Build Image
# =============================================================================

build_image() {
    print_header "Building Production Image"

    print_info "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
    print_info "This may take 5-10 minutes on first build..."
    echo ""

    # Use production .dockerignore if available
    if [ -f ".dockerignore.prod" ]; then
        cp .dockerignore .dockerignore.bak 2>/dev/null || true
        cp .dockerignore.prod .dockerignore
        print_info "Using .dockerignore.prod"
    fi

    # Build command
    BUILD_CMD="docker build -f Dockerfile.prod -t ${IMAGE_NAME}:${IMAGE_TAG}"

    if [ "$NO_CACHE" = true ]; then
        BUILD_CMD="$BUILD_CMD --no-cache"
        print_info "Cache disabled"
    fi

    BUILD_CMD="$BUILD_CMD ."

    # Execute build
    if $BUILD_CMD; then
        print_success "Image built successfully!"
    else
        print_error "Build failed"
        # Restore original .dockerignore
        [ -f ".dockerignore.bak" ] && mv .dockerignore.bak .dockerignore
        exit 1
    fi

    # Restore original .dockerignore
    if [ -f ".dockerignore.bak" ]; then
        mv .dockerignore.bak .dockerignore
    fi

    echo ""

    # Show image info
    print_info "Image details:"
    docker images "${IMAGE_NAME}:${IMAGE_TAG}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    echo ""
}

# =============================================================================
# Export Image
# =============================================================================

export_image() {
    print_header "Exporting Image"

    print_info "Exporting to: ${EXPORT_FILE}"
    print_info "This may take several minutes..."

    if docker save "${IMAGE_NAME}:${IMAGE_TAG}" -o "${EXPORT_FILE}"; then
        FILE_SIZE=$(du -h "${EXPORT_FILE}" | cut -f1)
        print_success "Image exported: ${EXPORT_FILE} (${FILE_SIZE})"
        echo ""
        print_info "Transfer this file to your production server:"
        echo "   scp ${EXPORT_FILE} user@server:/path/to/destination/"
        echo ""
        print_info "On the server, load the image with:"
        echo "   docker load -i ${EXPORT_FILE}"
        echo ""
    else
        print_error "Export failed"
        exit 1
    fi
}

# =============================================================================
# Main
# =============================================================================

main() {
    # Parse arguments
    EXPORT=false
    NO_CACHE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --export)
                EXPORT=true
                shift
                ;;
            --no-cache)
                NO_CACHE=true
                shift
                ;;
            --tag)
                IMAGE_TAG="$2"
                shift 2
                ;;
            --help)
                show_help
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done

    # Run build process
    check_requirements
    build_image

    if [ "$EXPORT" = true ]; then
        export_image
    fi

    # Final instructions
    print_header "Build Complete!"
    print_success "Image ready: ${IMAGE_NAME}:${IMAGE_TAG}"
    echo ""
    print_info "Next steps:"
    echo "   1. Deploy locally:"
    echo "      docker-compose -f docker-compose.prod.yml up -d"
    echo ""
    if [ "$EXPORT" = false ]; then
        echo "   2. Export for transfer (optional):"
        echo "      $0 --export"
        echo ""
    fi
    print_info "Documentation: docs/DEPLOYMENT.md"
    echo ""
}

# Run main function
main "$@"
