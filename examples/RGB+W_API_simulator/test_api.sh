#!/bin/bash
# Test script for WS2814 LED API
# Run this after starting the simulator to test various API endpoints

API_URL="http://localhost:8080"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           WS2814 LED API Test Suite                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function test_endpoint {
    echo -e "${BLUE}Testing: $1${NC}"
    echo -e "${YELLOW}Command: $2${NC}"
    eval $2
    echo ""
    echo "---"
    echo ""
    sleep 1
}

# Test 1: Get system status
test_endpoint "System Status" \
    "curl -s $API_URL/status | jq"

# Test 2: Get capabilities
test_endpoint "System Capabilities" \
    "curl -s $API_URL/capabilities | jq"

# Test 3: List all animations
test_endpoint "List Animations" \
    "curl -s $API_URL/animations | jq"

# Test 4: Start rainbow animation
test_endpoint "Start Rainbow Animation" \
    "curl -s -X POST $API_URL/playback/start \
        -H 'Content-Type: application/json' \
        -d '{\"animation_id\": \"rainbow\"}' | jq"

sleep 3

# Test 5: Check playback status
test_endpoint "Playback Status" \
    "curl -s $API_URL/playback/status | jq"

# Test 6: Set brightness to 50%
test_endpoint "Set Brightness to 50%" \
    "curl -s -X PUT $API_URL/playback/brightness \
        -H 'Content-Type: application/json' \
        -d '{\"brightness\": 0.5}' | jq"

sleep 2

# Test 7: Set speed to 2x
test_endpoint "Set Speed to 2x" \
    "curl -s -X PUT $API_URL/playback/speed \
        -H 'Content-Type: application/json' \
        -d '{\"speed\": 2.0}' | jq"

sleep 3

# Test 8: Create custom solid color (purple with white)
test_endpoint "Create Custom Purple Animation" \
    "curl -s -X POST $API_URL/animations \
        -H 'Content-Type: application/json' \
        -d '{
            \"id\": \"purple-glow\",
            \"name\": \"Purple Glow\",
            \"description\": \"Purple with white accent\",
            \"type\": \"solid\",
            \"color\": [128, 0, 128, 50]
        }' | jq"

# Test 9: Switch to purple animation
test_endpoint "Play Purple Animation" \
    "curl -s -X POST $API_URL/playback/start \
        -H 'Content-Type: application/json' \
        -d '{\"animation_id\": \"purple-glow\"}' | jq"

sleep 3

# Test 10: Create a chase animation
test_endpoint "Create Blue Chase Animation" \
    "curl -s -X POST $API_URL/animations \
        -H 'Content-Type: application/json' \
        -d '{
            \"id\": \"blue-chase\",
            \"name\": \"Blue Chase\",
            \"description\": \"Blue light chasing with white background\",
            \"type\": \"chase\",
            \"color\": [0, 100, 255, 0],
            \"background\": [0, 0, 0, 20],
            \"length\": 8,
            \"speed\": 1.5
        }' | jq"

# Test 11: Play blue chase
test_endpoint "Play Blue Chase" \
    "curl -s -X POST $API_URL/playback/start \
        -H 'Content-Type: application/json' \
        -d '{\"animation_id\": \"blue-chase\"}' | jq"

sleep 4

# Test 12: Get specific animation details
test_endpoint "Get Blue Chase Details" \
    "curl -s $API_URL/animations/blue-chase | jq"

# Test 13: Reset brightness to 100%
test_endpoint "Reset Brightness to 100%" \
    "curl -s -X PUT $API_URL/playback/brightness \
        -H 'Content-Type: application/json' \
        -d '{\"brightness\": 1.0}' | jq"

# Test 14: Start warm white
test_endpoint "Switch to Warm White" \
    "curl -s -X POST $API_URL/playback/start \
        -H 'Content-Type: application/json' \
        -d '{\"animation_id\": \"warm-white\"}' | jq"

sleep 2

# Test 15: Get current pixel data
test_endpoint "Get Current Pixel Data (first 5 LEDs)" \
    "curl -s $API_URL/pixels | jq '.pixels[:5]'"

# Test 16: Stop playback
test_endpoint "Stop Playback" \
    "curl -s -X POST $API_URL/playback/stop | jq"

# Test 17: Delete custom animation
test_endpoint "Delete Purple Animation" \
    "curl -s -X DELETE $API_URL/animations/purple-glow | jq"

# Test 18: Verify deletion
test_endpoint "Verify Purple Deleted" \
    "curl -s $API_URL/animations | jq '.animations | map(.id)'"

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  Test Suite Complete                       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "All tests completed!"
