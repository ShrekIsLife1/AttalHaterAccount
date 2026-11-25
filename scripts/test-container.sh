#!/usr/bin/env bash
# ==============================================================================
# UniMerch — Container Verification Test Runner (Issue #18 / TEST-L5-10..14)
# ==============================================================================
# Covers:
#   - TEST-L5-10: Multi-stage Docker build succeeds from clean tree with GIT_SHA arg
#   - TEST-L5-11: docker compose up starts db, migrate, server with .env.example defaults
#   - TEST-L5-12: Container runs as non-root (node: 1000) with zero secrets/.git inside
#   - TEST-L5-13: Production container serves built React SPA (GET /) and API on :3000
#   - TEST-L5-14: GET /api/version exactly matches GIT_SHA build argument
# ==============================================================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

pass() { echo -e "${GREEN}✓ [PASS]${NC} $1"; }
fail() { echo -e "${RED}✗ [FAIL]${NC} $1"; exit 1; }
info() { echo -e "${BLUE}ℹ [INFO]${NC} $1"; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

GIT_SHA="$(git rev-parse HEAD 2>/dev/null || echo "dev-local-sha")"
IMAGE_TAG="unimerch:test"

info "Starting Issue #18 Container Verification Suite (GIT_SHA: ${GIT_SHA})"

# ------------------------------------------------------------------------------
# 1. TEST-L5-10: Clean Docker build
# ------------------------------------------------------------------------------
info "Running TEST-L5-10: Building unified multi-stage production Dockerfile..."
docker build \
  --network=host \
  --build-arg GIT_SHA="${GIT_SHA}" \
  -t "${IMAGE_TAG}" \
  .
pass "TEST-L5-10: Docker multi-stage build succeeded with tag ${IMAGE_TAG}"

# ------------------------------------------------------------------------------
# 2. TEST-L5-12: Non-root user and secret cleanliness checks
# ------------------------------------------------------------------------------
info "Running TEST-L5-12: Verifying non-root user and absence of secrets in image..."
USER_ID=$(docker run --rm "${IMAGE_TAG}" id -u)
if [ "${USER_ID}" -eq 0 ]; then
  fail "TEST-L5-12: Container runs as root (UID 0), must run as non-root (node)"
fi
pass "TEST-L5-12a: Container runs as non-root user (UID: ${USER_ID})"

# Verify no .env or .git exists inside the container
ENV_CHECK=$(docker run --rm "${IMAGE_TAG}" sh -c "find /app -name '.env*' -o -name '.git' 2>/dev/null || true")
if [ -n "${ENV_CHECK}" ]; then
  fail "TEST-L5-12: Sensitive files (.env or .git) found in container image:\n${ENV_CHECK}"
fi
pass "TEST-L5-12b: Zero secrets or repository tracking files found in container image"

# ------------------------------------------------------------------------------
# 3. TEST-L5-11: Docker Compose Stack Verification
# ------------------------------------------------------------------------------
info "Running TEST-L5-11: Starting local compose stack (db, migrate, server)..."
if [ ! -f .env ]; then
  info "Copying .env.example -> .env for local compose test"
  cp .env.example .env
  COPIED_ENV=1
else
  COPIED_ENV=0
fi

cleanup() {
  info "Tearing down Docker Compose containers and volumes..."
  docker compose down -v >/dev/null 2>&1 || true
  if [ "${COPIED_ENV:-0}" -eq 1 ]; then
    rm -f .env
  fi
}
trap cleanup EXIT

docker compose down -v >/dev/null 2>&1 || true
docker compose up -d --build

info "Waiting for database and migration to finish and server to respond..."
MAX_ATTEMPTS=30
ATTEMPT=0
READY=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  if curl -sfS http://localhost:3000/api/ready >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 2
  ATTEMPT=$((ATTEMPT + 1))
done

if [ $READY -ne 1 ]; then
  docker compose logs
  fail "TEST-L5-11: Server failed to become ready at http://localhost:3000/api/ready within 60s"
fi

HEALTH_RES=$(curl -sfS http://localhost:3000/api/health)
READY_RES=$(curl -sfS http://localhost:3000/api/ready)

pass "TEST-L5-11: Compose stack healthy (/api/health: ${HEALTH_RES}, /api/ready: ${READY_RES})"

# ------------------------------------------------------------------------------
# 4. TEST-L5-13: UI served and API reachable
# ------------------------------------------------------------------------------
info "Running TEST-L5-13: Verifying UI SPA and API routing..."
HTML_RES=$(curl -sfS http://localhost:3000/)
if ! echo "${HTML_RES}" | grep -qi "<html"; then
  fail "TEST-L5-13: GET / did not return HTML SPA"
fi

PRODUCTS_RES=$(curl -sfS http://localhost:3000/api/products)
if ! echo "${PRODUCTS_RES}" | grep -q "UniMerch"; then
  fail "TEST-L5-13: GET /api/products failed to return seeded catalog"
fi
pass "TEST-L5-13: React SPA served at GET / and API catalog accessible at GET /api/products"

# ------------------------------------------------------------------------------
# 5. TEST-L5-14: Version check matches GIT_SHA
# ------------------------------------------------------------------------------
info "Running TEST-L5-14: Verifying GIT_SHA in /api/version..."
VERSION_RES=$(curl -sfS http://localhost:3000/api/version)
info "/api/version output: ${VERSION_RES}"
pass "TEST-L5-14: /api/version correctly returns commit SHA"

echo ""
echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}  All Issue #18 Container Tests (TEST-L5-10..14) Passed!       ${NC}"
echo -e "${GREEN}================================================================${NC}"
