#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Testing Pizza Review Cache System${NC}"
echo "================================="

# Function to make a pizza query
make_query() {
    echo -e "\n${GREEN}Making query:${NC} $1"
    curl -X POST "http://localhost:8000/ask-pizza" \
         -H "Content-Type: application/json" \
         -d "{\"question\": \"$1\"}"
    echo -e "\n"
}

# Function to get cache stats
get_stats() {
    echo -e "\n${GREEN}Getting cache statistics:${NC}"
    curl -X POST "http://localhost:8000/cache-stats" \
         -H "Content-Type: application/json" \
         -d "{\"hours\": 24}"
    echo -e "\n"
}

# Initial cache stats
get_stats

# Test 1: Make a new query
echo "Test 1: Making a new query (should be a cache miss)"
make_query "best pizza in tel aviv"
get_stats

# Test 2: Repeat the same query
echo "Test 2: Repeating the same query (should be a cache hit)"
make_query "best pizza in tel aviv"
get_stats

# Test 3: Similar query
echo "Test 3: Making a similar query (should be a cache hit due to semantic similarity)"
make_query "where can I find good pizza in tlv"
get_stats

# Test 4: Different query
echo "Test 4: Making a different query (should be a cache miss)"
make_query "pizza places in jerusalem with great crust"
get_stats

# Test 5: Similar to Test 4
echo "Test 5: Similar to previous query (should be a cache hit)"
make_query "best pizza crust in jerusalem"
get_stats

echo -e "\n${BLUE}Test sequence completed!${NC}" 