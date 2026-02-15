# WS2814 RGBW LED Simulator (Tkinter Version)

A Python-based simulator with Tkinter GUI for testing LED control APIs before deploying to Raspberry Pi hardware.

## Features

- **Tkinter GUI** - Visual display of 60 LEDs in a 6x10 grid
- **Full REST API** - Complete HTTP API for LED control
- **RGBW Support** - 4-byte color format for WS2814 LEDs
- **Built-in Animations** - Solid colors, rainbow, chase effects
- **Custom Animations** - Upload your own frame-based or parametric animations
- **Real-time Updates** - LEDs update immediately when API calls are made
- **Status Display** - Shows current animation, speed, and brightness
- **No Browser Required** - Pure Tkinter GUI, HTTP API returns plain text/JSON only

## Quick Start

1. Run the simulator:

   ```bash
   python3 led_simulator_tkinter.py
   ```

2. A Tkinter window will open showing the LED strip
3. Use curl to control the LEDs via the API

## What You'll See

- **Tkinter Window**: Shows 60 colored boxes representing each LED
- **Status Bar**: Displays current animation, playback speed, and brightness
- **Console Output**: Shows API requests and responses

## API Usage

The API is identical to the previous version but now only returns JSON or plain text (no HTML).

### Quick Test

```bash
# Start rainbow animation
curl -X POST http://localhost:8080/playback/start \
  -H "Content-Type: application/json" \
  -d '{"animation_id": "rainbow"}'

# Watch the LEDs change in the Tkinter window!
```

### List Available Animations

```bash
curl http://localhost:8080/animations
```

Response:

```json
{
  "animations": [
    {
      "id": "off",
      "name": "Off",
      "description": "All LEDs off",
      "type": "solid",
      "color": [0, 0, 0, 0]
    },
    {
      "id": "warm-white",
      "name": "Warm White",
      "description": "Soft warm white glow",
      "type": "solid",
      "color": [255, 200, 150, 200]
    },
    ...
  ]
}
```

### Create Custom Animation

```bash
# Create a purple glow
curl -X POST http://localhost:8080/animations \
  -H "Content-Type: application/json" \
  -d '{
    "id": "purple",
    "name": "Purple Glow",
    "description": "Purple with white accent",
    "type": "solid",
    "color": [128, 0, 128, 50]
  }'

# Play it
curl -X POST http://localhost:8080/playback/start \
  -H "Content-Type: application/json" \
  -d '{"animation_id": "purple"}'
```

### Create a simple two-frame blink

```bash
curl -X POST http://localhost:8080/animations \
  -H "Content-Type: application/json" \
  -d '{
    "id": "blink",
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

# Play it
curl -X POST http://localhost:8080/playback/start \
  -H "Content-Type: application/json" \
  -d '{"animation_id": "blink"}'
```

### Control Brightness

```bash
# Set to 50%
curl -X PUT http://localhost:8080/playback/brightness \
  -H "Content-Type: application/json" \
  -d '{"brightness": 0.5}'
```

### Control Speed

```bash
# Double speed
curl -X PUT http://localhost:8080/playback/speed \
  -H "Content-Type: application/json" \
  -d '{"speed": 2.0}'
```

### Stop Animation

```bash
curl -X POST http://localhost:8080/playback/stop
```

## API Endpoints

### Animation Management

- `GET /animations` - List all animations
- `GET /animations/{id}` - Get specific animation details
- `POST /animations` - Create new animation
- `PUT /animations/{id}` - Update existing animation
- `DELETE /animations/{id}` - Delete animation

### Playback Control

- `POST /playback/start` - Start animation (body: `{"animation_id": "rainbow"}`)
- `POST /playback/stop` - Stop current animation
- `GET /playback/status` - Get current playback state
- `PUT /playback/speed` - Set playback speed (body: `{"speed": 1.5}`)
- `PUT /playback/brightness` - Set brightness (body: `{"brightness": 0.8}`)

### System Information

- `GET /status` - System status and LED count
- `GET /capabilities` - Supported features and animation types
- `GET /pixels` - Current RGBW values for all pixels
- `GET /` - API information (plain text)

## Animation Types

### Solid Color

Static color applied to all LEDs:

```json
{
  "id": "my-color",
  "name": "My Color",
  "type": "solid",
  "color": [R, G, B, W]
}
```

### Frame-based

Sequence of frames for custom animations:

```json
{
  "id": "my-animation",
  "name": "My Animation",
  "type": "frames",
  "fps": 30,
  "loop": true,
  "frames": [
    [[R,G,B,W], [R,G,B,W], ...],  // Frame 1 (60 LEDs)
    [[R,G,B,W], [R,G,B,W], ...],  // Frame 2
    ...
  ]
}
```

### Rainbow (Procedural)

Smooth rainbow cycle:

```json
{
  "id": "rainbow",
  "name": "Rainbow",
  "type": "rainbow",
  "speed": 1.0
}
```

### Chase (Procedural)

Moving light chase effect:

```json
{
  "id": "chase",
  "name": "Chase",
  "type": "chase",
  "color": [255, 0, 0, 0],
  "background": [0, 0, 0, 10],
  "length": 5,
  "speed": 2.0
}
```

## RGBW Color Format

All colors use 4-byte RGBW format: `[R, G, B, W]`

- Each value: 0-255
- Example: `[255, 0, 0, 0]` = Pure red
- Example: `[0, 0, 0, 255]` = Pure white
- Example: `[255, 200, 100, 150]` = Warm amber-white

The white channel is **additive** in the visualization - it adds brightness to all RGB channels.

## Example Workflow

```bash
# 1. Check what animations are available
curl http://localhost:8080/animations

# 2. Start the rainbow
curl -X POST http://localhost:8080/playback/start \
  -H "Content-Type: application/json" \
  -d '{"animation_id": "rainbow"}'

# 3. Speed it up
curl -X PUT http://localhost:8080/playback/speed \
  -H "Content-Type: application/json" \
  -d '{"speed": 2.0}'

# 4. Dim it
curl -X PUT http://localhost:8080/playback/brightness \
  -H "Content-Type: application/json" \
  -d '{"brightness": 0.3}'

# 5. Create a custom blue
curl -X POST http://localhost:8080/animations \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ocean-blue",
    "name": "Ocean Blue",
    "type": "solid",
    "color": [0, 100, 200, 50]
  }'

# 6. Switch to it
curl -X POST http://localhost:8080/playback/start \
  -H "Content-Type: application/json" \
  -d '{"animation_id": "ocean-blue"}'

# 7. Stop
curl -X POST http://localhost:8080/playback/stop
```

## Running the Test Suite

You can use the provided test script:

```bash
./test_api.sh
```

This will run through various API operations while you watch the Tkinter window update in real-time.

## Differences from Browser Version

- **No HTML interface** - The HTTP server returns JSON/text only
- **Tkinter GUI** - Desktop window instead of browser visualization
- **Immediate updates** - No need to poll or refresh
- **Status bar** - Built into the Tkinter window
- **Same API** - All endpoints work identically

## Configuration

Edit these constants at the top of the script:

- `LED_COUNT = 60` - Number of LEDs
- `DEFAULT_FPS = 30` - Default animation frame rate
- `API_PORT = 8080` - HTTP API port

## Next Steps for Pi Deployment

Once tested, you can port this to your Raspberry Pi:

1. Keep the exact same API structure
2. Replace the `LEDStrip` class with actual `rpi_ws281x` library calls
3. Remove the Tkinter GUI (or keep it if you have a display on the Pi)
4. The AnimationEngine can stay largely the same

## Troubleshooting

**Tkinter not installed?**

```bash
sudo apt-get install python3-tk
```

**Port already in use?**

```bash
# Find and kill the process using port 8080
sudo lsof -i :8080
kill <PID>
```

**LEDs not updating?**
The Tkinter GUI updates every 50ms. If you're making rapid API calls, you should see smooth updates.

## License

Free to use for your LED projects!

## AI thread

[Claude](https://claude.ai/share/00dfdeb1-ada5-4725-b858-c2336605fd5b)