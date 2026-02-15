# WS2814 RGBW LED Strip Control API Documentation

## Overview

This API controls a WS2814 RGBW LED strip with 60 addressable LEDs. It provides endpoints for managing animations, controlling playback, and adjusting display parameters.

**Base URL:** `http://localhost:8080`

**Color Format:** RGBW - 4-byte arrays `[R, G, B, W]` where each value is 0-255

## Quick Start

```bash
# List available animations
curl http://localhost:8080/animations

# Start rainbow animation
curl -X POST http://localhost:8080/playback/start \
  -H "Content-Type: application/json" \
  -d '{"animation_id": "rainbow"}'

# Set brightness to 50%
curl -X PUT http://localhost:8080/playback/brightness \
  -H "Content-Type: application/json" \
  -d '{"brightness": 0.5}'
```

---

## API Endpoints

### Animation Management

#### GET /animations
List all available animations.

**Response:**
```json
{
  "animations": [
    {
      "id": "rainbow",
      "name": "Rainbow Cycle",
      "description": "Smooth rainbow animation",
      "type": "rainbow",
      "speed": 1.0
    },
    ...
  ]
}
```

#### GET /animations/{id}
Get details of a specific animation.

**Parameters:**
- `id` (path): Animation identifier

**Response:**
```json
{
  "id": "warm-white",
  "name": "Warm White",
  "description": "Soft warm white glow",
  "type": "solid",
  "color": [255, 200, 150, 200]
}
```

#### POST /animations
Create a new animation.

**Request Body:**
```json
{
  "id": "my-animation",
  "name": "My Animation",
  "description": "Description here",
  "type": "solid",
  "color": [R, G, B, W]
}
```

**Response:**
```json
{
  "success": true,
  "id": "my-animation"
}
```

#### PUT /animations/{id}
Update an existing animation.

**Parameters:**
- `id` (path): Animation identifier

**Request Body:** Same as POST /animations

**Response:**
```json
{
  "success": true,
  "id": "my-animation"
}
```

#### DELETE /animations/{id}
Delete an animation.

**Parameters:**
- `id` (path): Animation identifier

**Response:**
```json
{
  "success": true
}
```

---

### Playback Control

#### POST /playback/start
Start playing an animation.

**Request Body:**
```json
{
  "animation_id": "rainbow"
}
```

**Response:**
```json
{
  "success": true,
  "animation_id": "rainbow"
}
```

#### POST /playback/stop
Stop the current animation.

**Response:**
```json
{
  "success": true
}
```

#### GET /playback/status
Get current playback status.

**Response:**
```json
{
  "playing": true,
  "current_animation": "rainbow",
  "speed": 1.0,
  "brightness": 0.5
}
```

#### PUT /playback/speed
Set playback speed multiplier.

**Request Body:**
```json
{
  "speed": 2.0
}
```

**Valid range:** 0.1 to 5.0

**Response:**
```json
{
  "success": true,
  "speed": 2.0
}
```

#### PUT /playback/brightness
Set global brightness.

**Request Body:**
```json
{
  "brightness": 0.5
}
```

**Valid range:** 0.0 to 1.0 (0% to 100%)

**Response:**
```json
{
  "success": true,
  "brightness": 0.5
}
```

---

### System Information

#### GET /status
Get system status.

**Response:**
```json
{
  "led_count": 60,
  "brightness": 1.0,
  "playback": {
    "playing": true,
    "current_animation": "rainbow",
    "speed": 1.0,
    "brightness": 1.0
  },
  "animation_count": 5
}
```

#### GET /capabilities
Get system capabilities.

**Response:**
```json
{
  "led_count": 60,
  "color_format": "RGBW",
  "supported_types": ["solid", "frames", "rainbow", "chase"],
  "max_fps": 60,
  "features": ["brightness_control", "speed_control", "custom_animations"]
}
```

#### GET /pixels
Get current RGBW values for all LEDs.

**Response:**
```json
{
  "pixels": [
    [255, 200, 150, 200],
    [255, 200, 150, 200],
    ...
  ],
  "count": 60
}
```

---

## Animation Types

### 1. Solid Color
Static color applied to all LEDs.

```json
{
  "id": "my-color",
  "name": "My Color",
  "description": "Description",
  "type": "solid",
  "color": [255, 128, 0, 50]
}
```

**Fields:**
- `color` (array): RGBW values [0-255, 0-255, 0-255, 0-255]

### 2. Frame-based Animation
Sequence of frames for custom animations.

```json
{
  "id": "my-animation",
  "name": "My Animation",
  "description": "Description",
  "type": "frames",
  "fps": 30,
  "loop": true,
  "frames": [
    [
      [255, 0, 0, 0],
      [0, 255, 0, 0],
      [0, 0, 255, 0],
      ...
    ],
    [
      [200, 0, 0, 0],
      [0, 200, 0, 0],
      [0, 0, 200, 0],
      ...
    ]
  ]
}
```

**Fields:**
- `fps` (number): Frame rate (1-60)
- `loop` (boolean): Whether to loop the animation
- `frames` (array): Array of frames, each frame is an array of 60 RGBW colors

### 3. Rainbow (Procedural)
Smooth rainbow cycle effect.

```json
{
  "id": "rainbow",
  "name": "Rainbow Cycle",
  "description": "Smooth rainbow animation",
  "type": "rainbow",
  "speed": 1.0
}
```

**Fields:**
- `speed` (number): Animation speed multiplier

### 4. Chase (Procedural)
Moving light chase effect.

```json
{
  "id": "chase",
  "name": "Chase Effect",
  "description": "Light chase animation",
  "type": "chase",
  "color": [255, 0, 0, 0],
  "background": [0, 0, 0, 10],
  "length": 5,
  "speed": 2.0
}
```

**Fields:**
- `color` (array): Chase light color RGBW
- `background` (array): Background color RGBW
- `length` (number): Number of LEDs in the chase
- `speed` (number): Animation speed multiplier

---

## Built-in Animations

The following animations are available by default:

| ID | Name | Type | Description |
|---|---|---|---|
| `off` | Off | solid | All LEDs off |
| `warm-white` | Warm White | solid | Soft warm white glow |
| `cool-white` | Cool White | solid | Bright cool white |
| `rainbow` | Rainbow Cycle | rainbow | Smooth rainbow animation |
| `chase-red` | Red Chase | chase | Red light chasing effect |

---

## Color Format: RGBW

All colors use 4-byte RGBW format: `[R, G, B, W]`

**Examples:**
- `[255, 0, 0, 0]` - Pure red
- `[0, 255, 0, 0]` - Pure green
- `[0, 0, 255, 0]` - Pure blue
- `[0, 0, 0, 255]` - Pure white
- `[255, 200, 100, 150]` - Warm amber-white
- `[128, 0, 128, 50]` - Purple with white accent

**Note:** The white channel is additive - it adds brightness to the RGB channels in the hardware.

---

## Common Workflows

### Create and Play Custom Color

```bash
# 1. Create animation
curl -X POST http://localhost:8080/animations \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ocean-blue",
    "name": "Ocean Blue",
    "description": "Deep ocean blue",
    "type": "solid",
    "color": [0, 100, 200, 30]
  }'

# 2. Play it
curl -X POST http://localhost:8080/playback/start \
  -H "Content-Type: application/json" \
  -d '{"animation_id": "ocean-blue"}'
```

### Adjust Playback Parameters

```bash
# Set brightness to 70%
curl -X PUT http://localhost:8080/playback/brightness \
  -H "Content-Type: application/json" \
  -d '{"brightness": 0.7}'

# Speed up 2x
curl -X PUT http://localhost:8080/playback/speed \
  -H "Content-Type: application/json" \
  -d '{"speed": 2.0}'
```

### Create Chase Animation

```bash
curl -X POST http://localhost:8080/animations \
  -H "Content-Type: application/json" \
  -d '{
    "id": "blue-chase",
    "name": "Blue Chase",
    "description": "Blue light chase with dim white background",
    "type": "chase",
    "color": [0, 100, 255, 0],
    "background": [0, 0, 0, 20],
    "length": 8,
    "speed": 1.5
  }'

curl -X POST http://localhost:8080/playback/start \
  -H "Content-Type: application/json" \
  -d '{"animation_id": "blue-chase"}'
```

### Simple Two-Frame Blink

```bash
curl -X POST http://localhost:8080/animations \
  -H "Content-Type: application/json" \
  -d '{
    "id": "red-blink",
    "name": "Red Blink",
    "type": "frames",
    "fps": 2,
    "loop": true,
    "frames": [
      [
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0],
        [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0], [255,0,0,0]
      ],
      [
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0],
        [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]
      ]
    ]
  }'
```

---

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `201` - Created (new animation)
- `400` - Bad Request (invalid JSON, missing required fields)
- `404` - Not Found (animation doesn't exist)

Error response format:
```json
{
  "error": "Error message description"
}
```

---

## Notes

- **LED Count:** Currently fixed at 60 LEDs (indices 0-59)
- **Thread Safety:** All operations are thread-safe
- **Performance:** Frame-based animations should stay under 60 FPS for smooth operation
- **Storage:** Animations are stored in memory; custom animations persist only during runtime
- **Concurrency:** Only one animation can play at a time; starting a new animation stops the current one

---

## Python Example

```python
import requests
import json

BASE_URL = "http://localhost:8080"

# Create custom animation
animation = {
    "id": "sunset",
    "name": "Sunset",
    "description": "Orange and red sunset colors",
    "type": "solid",
    "color": [255, 100, 0, 50]
}

response = requests.post(
    f"{BASE_URL}/animations",
    headers={"Content-Type": "application/json"},
    json=animation
)
print(f"Created: {response.json()}")

# Start the animation
response = requests.post(
    f"{BASE_URL}/playback/start",
    headers={"Content-Type": "application/json"},
    json={"animation_id": "sunset"}
)
print(f"Started: {response.json()}")

# Adjust brightness
response = requests.put(
    f"{BASE_URL}/playback/brightness",
    headers={"Content-Type": "application/json"},
    json={"brightness": 0.6}
)
print(f"Brightness: {response.json()}")

# Check status
response = requests.get(f"{BASE_URL}/playback/status")
print(f"Status: {response.json()}")
```

---

## JavaScript Example

```javascript
const BASE_URL = 'http://localhost:8080';

// Create animation
async function createAnimation() {
  const animation = {
    id: 'sunset',
    name: 'Sunset',
    description: 'Orange and red sunset colors',
    type: 'solid',
    color: [255, 100, 0, 50]
  };
  
  const response = await fetch(`${BASE_URL}/animations`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(animation)
  });
  
  return response.json();
}

// Start animation
async function startAnimation(id) {
  const response = await fetch(`${BASE_URL}/playback/start`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({animation_id: id})
  });
  
  return response.json();
}

// Set brightness
async function setBrightness(level) {
  const response = await fetch(`${BASE_URL}/playback/brightness`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({brightness: level})
  });
  
  return response.json();
}

// Usage
await createAnimation();
await startAnimation('sunset');
await setBrightness(0.6);
```

---

## Support

For issues or questions about this API, refer to the implementation documentation or contact the system administrator.
