#!/usr/bin/env python3
"""
WS2814 (RGBW) LED Strip Simulator with Tkinter GUI
Provides REST API with visual Tkinter display
"""

import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk
import math

# Configuration
LED_COUNT = 60
DEFAULT_FPS = 30
API_PORT = 8080

class LEDStrip:
    """Simulates a WS2814 RGBW LED strip"""
    
    def __init__(self, count=60):
        self.count = count
        self.pixels = [[0, 0, 0, 0] for _ in range(count)]  # RGBW
        self.brightness = 1.0
        self.lock = threading.Lock()
        self.update_callback = None
    
    def set_update_callback(self, callback):
        """Set callback for when pixels change"""
        self.update_callback = callback
    
    def set_pixel(self, index, r, g, b, w):
        """Set a single pixel color (RGBW)"""
        if 0 <= index < self.count:
            with self.lock:
                self.pixels[index] = [
                    int(r * self.brightness),
                    int(g * self.brightness),
                    int(b * self.brightness),
                    int(w * self.brightness)
                ]
            if self.update_callback:
                self.update_callback()
    
    def set_all(self, r, g, b, w):
        """Set all pixels to the same color"""
        with self.lock:
            for i in range(self.count):
                self.pixels[i] = [
                    int(r * self.brightness),
                    int(g * self.brightness),
                    int(b * self.brightness),
                    int(w * self.brightness)
                ]
        if self.update_callback:
            self.update_callback()
    
    def get_pixels(self):
        """Get current pixel data"""
        with self.lock:
            return [p[:] for p in self.pixels]
    
    def clear(self):
        """Turn off all LEDs"""
        self.set_all(0, 0, 0, 0)


class AnimationEngine:
    """Manages animation playback"""
    
    def __init__(self, strip):
        self.strip = strip
        self.animations = {}
        self.current_animation = None
        self.playing = False
        self.thread = None
        self.speed = 1.0
        self.frame_index = 0
        
        # Add some default animations
        self._add_default_animations()
    
    def _add_default_animations(self):
        """Add built-in animations"""
        self.animations['off'] = {
            'id': 'off',
            'name': 'Off',
            'description': 'All LEDs off',
            'type': 'solid',
            'color': [0, 0, 0, 0]
        }
        
        self.animations['warm-white'] = {
            'id': 'warm-white',
            'name': 'Warm White',
            'description': 'Soft warm white glow',
            'type': 'solid',
            'color': [255, 200, 150, 200]
        }
        
        self.animations['cool-white'] = {
            'id': 'cool-white',
            'name': 'Cool White',
            'description': 'Bright cool white',
            'type': 'solid',
            'color': [200, 220, 255, 255]
        }
        
        self.animations['rainbow'] = {
            'id': 'rainbow',
            'name': 'Rainbow Cycle',
            'description': 'Smooth rainbow animation',
            'type': 'rainbow',
            'speed': 1.0
        }
        
        self.animations['chase-red'] = {
            'id': 'chase-red',
            'name': 'Red Chase',
            'description': 'Red light chasing down the strip',
            'type': 'chase',
            'color': [255, 0, 0, 0],
            'background': [0, 0, 0, 0],
            'length': 5,
            'speed': 2.0
        }
    
    def add_animation(self, anim_id, animation_data):
        """Add or update an animation"""
        animation_data['id'] = anim_id
        self.animations[anim_id] = animation_data
        return True
    
    def delete_animation(self, anim_id):
        """Remove an animation"""
        if anim_id in self.animations:
            del self.animations[anim_id]
            return True
        return False
    
    def start_animation(self, anim_id):
        """Start playing an animation"""
        if anim_id not in self.animations:
            return False
        
        self.stop_animation()
        self.current_animation = anim_id
        self.frame_index = 0
        self.playing = True
        
        self.thread = threading.Thread(target=self._animation_loop, daemon=True)
        self.thread.start()
        return True
    
    def stop_animation(self):
        """Stop current animation"""
        self.playing = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.current_animation = None
    
    def _animation_loop(self):
        """Main animation rendering loop"""
        while self.playing and self.current_animation:
            anim = self.animations.get(self.current_animation)
            if not anim:
                break
            
            anim_type = anim.get('type', 'solid')
            
            if anim_type == 'solid':
                self._render_solid(anim)
                time.sleep(0.1)
            
            elif anim_type == 'frames':
                self._render_frames(anim)
            
            elif anim_type == 'rainbow':
                self._render_rainbow(anim)
            
            elif anim_type == 'chase':
                self._render_chase(anim)
            
            else:
                time.sleep(0.1)
    
    def _render_solid(self, anim):
        """Render a solid color"""
        color = anim.get('color', [0, 0, 0, 0])
        self.strip.set_all(*color)
    
    def _render_frames(self, anim):
        """Render frame-based animation"""
        frames = anim.get('frames', [])
        if not frames:
            return
        
        fps = anim.get('fps', DEFAULT_FPS)
        loop = anim.get('loop', True)
        
        if self.frame_index >= len(frames):
            if loop:
                self.frame_index = 0
            else:
                self.playing = False
                return
        
        frame = frames[self.frame_index]
        for i, color in enumerate(frame):
            if i < self.strip.count:
                self.strip.set_pixel(i, *color)
        
        self.frame_index += 1
        time.sleep(1.0 / (fps * self.speed))
    
    def _render_rainbow(self, anim):
        """Render rainbow effect"""
        speed = anim.get('speed', 1.0) * self.speed
        t = time.time() * speed
        
        for i in range(self.strip.count):
            hue = (i / self.strip.count + t * 0.1) % 1.0
            r, g, b = self._hsv_to_rgb(hue, 1.0, 1.0)
            self.strip.set_pixel(i, r, g, b, 0)
        
        time.sleep(1.0 / DEFAULT_FPS)
    
    def _render_chase(self, anim):
        """Render chase effect"""
        color = anim.get('color', [255, 0, 0, 0])
        bg = anim.get('background', [0, 0, 0, 0])
        length = anim.get('length', 5)
        speed = anim.get('speed', 1.0) * self.speed
        
        # Fill background
        self.strip.set_all(*bg)
        
        # Calculate chase position
        t = time.time() * speed
        position = int(t * 10) % (self.strip.count + length)
        
        # Draw chase
        for i in range(length):
            pos = (position - i) % self.strip.count
            self.strip.set_pixel(pos, *color)
        
        time.sleep(1.0 / DEFAULT_FPS)
    
    @staticmethod
    def _hsv_to_rgb(h, s, v):
        """Convert HSV to RGB"""
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        
        if i == 0: return int(v*255), int(t*255), int(p*255)
        if i == 1: return int(q*255), int(v*255), int(p*255)
        if i == 2: return int(p*255), int(v*255), int(t*255)
        if i == 3: return int(p*255), int(q*255), int(v*255)
        if i == 4: return int(t*255), int(p*255), int(v*255)
        if i == 5: return int(v*255), int(p*255), int(q*255)
    
    def get_status(self):
        """Get current playback status"""
        return {
            'playing': self.playing,
            'current_animation': self.current_animation,
            'speed': self.speed,
            'brightness': self.strip.brightness
        }


class LEDVisualizer:
    """Tkinter GUI for visualizing LED strip"""
    
    def __init__(self, strip):
        self.strip = strip
        self.root = tk.Tk()
        self.root.title("WS2814 RGBW LED Simulator")
        self.root.configure(bg='#1a1a1a')
        
        # Set up the strip to notify us of updates
        self.strip.set_update_callback(self.schedule_update)
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(padx=20, pady=20)
        
        # Title
        title = tk.Label(
            main_frame,
            text="WS2814 RGBW LED Strip Simulator",
            font=('Arial', 18, 'bold'),
            bg='#1a1a1a',
            fg='#4CAF50'
        )
        title.pack(pady=(0, 10))
        
        # Info label
        info = tk.Label(
            main_frame,
            text=f"60 RGBW LEDs | API: http://localhost:{API_PORT}",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#888888'
        )
        info.pack(pady=(0, 20))
        
        # LED strip frame
        led_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RIDGE, bd=2)
        led_frame.pack(pady=10)
        
        # Create LED "pixels" as colored labels in a grid
        self.led_widgets = []
        rows = 6
        cols = 10
        
        for row in range(rows):
            for col in range(cols):
                led_index = row * cols + col
                led = tk.Label(
                    led_frame,
                    text='',
                    width=4,
                    height=2,
                    bg='#000000',
                    relief=tk.RAISED,
                    bd=1
                )
                led.grid(row=row, column=col, padx=2, pady=2)
                self.led_widgets.append(led)
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RIDGE, bd=2)
        status_frame.pack(pady=10, fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Stopped",
            font=('Arial', 12),
            bg='#2a2a2a',
            fg='#ffffff',
            pady=10
        )
        self.status_label.pack()
        
        # Start update loop
        self.update_pending = False
        self.update_display()
        
        # Update status periodically
        self.update_status()
    
    def schedule_update(self):
        """Schedule a display update (called from strip when pixels change)"""
        if not self.update_pending:
            self.update_pending = True
    
    def update_display(self):
        """Update the LED display"""
        pixels = self.strip.get_pixels()
        
        for i, (led_widget, color) in enumerate(zip(self.led_widgets, pixels)):
            r, g, b, w = color
            # Combine RGB with white channel
            r = min(255, r + w)
            g = min(255, g + w)
            b = min(255, b + w)
            
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            led_widget.configure(bg=hex_color)
        
        self.update_pending = False
        
        # Schedule next update
        self.root.after(50, self.update_display)  # 20 FPS for display
    
    def update_status(self):
        """Update status label"""
        status = engine.get_status()
        
        if status['playing']:
            text = f"Status: Playing '{status['current_animation']}' | "
            text += f"Speed: {status['speed']:.1f}x | "
            text += f"Brightness: {int(status['brightness'] * 100)}%"
        else:
            text = "Status: Stopped"
        
        self.status_label.configure(text=text)
        
        # Schedule next status update
        self.root.after(500, self.update_status)
    
    def run(self):
        """Run the Tkinter main loop"""
        self.root.mainloop()


class LEDAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the LED API"""
    
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _send_json(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_error(self, message, status=400):
        self._send_json({'error': message}, status)
    
    def _read_json(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        return json.loads(body) if body else {}
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        # GET / - Simple info page
        if path == '/':
            self._set_headers(content_type='text/plain')
            info = f"""WS2814 RGBW LED Simulator API
API Port: {API_PORT}
LED Count: {LED_COUNT}
Color Format: RGBW (4 bytes per pixel)

Available Endpoints:
  GET  /animations          - List all animations
  GET  /animations/{{id}}     - Get specific animation
  POST /animations          - Create new animation
  PUT  /animations/{{id}}     - Update animation
  DEL  /animations/{{id}}     - Delete animation
  
  POST /playback/start      - Start animation
  POST /playback/stop       - Stop animation
  GET  /playback/status     - Get playback status
  PUT  /playback/speed      - Set playback speed
  PUT  /playback/brightness - Set brightness
  
  GET  /status              - System status
  GET  /capabilities        - System capabilities
  GET  /pixels              - Current pixel state

Example:
  curl -X POST http://localhost:{API_PORT}/playback/start \\
    -H "Content-Type: application/json" \\
    -d '{{"animation_id": "rainbow"}}'
"""
            self.wfile.write(info.encode())
        
        # GET /animations - List all animations
        elif path == '/animations':
            animations = list(engine.animations.values())
            self._send_json({'animations': animations})
        
        # GET /animations/{id} - Get specific animation
        elif path.startswith('/animations/'):
            anim_id = path.split('/')[-1]
            if anim_id in engine.animations:
                self._send_json(engine.animations[anim_id])
            else:
                self._send_error('Animation not found', 404)
        
        # GET /playback/status - Get playback status
        elif path == '/playback/status':
            status = engine.get_status()
            self._send_json(status)
        
        # GET /status - System status
        elif path == '/status':
            self._send_json({
                'led_count': strip.count,
                'brightness': strip.brightness,
                'playback': engine.get_status(),
                'animation_count': len(engine.animations)
            })
        
        # GET /capabilities - System capabilities
        elif path == '/capabilities':
            self._send_json({
                'led_count': strip.count,
                'color_format': 'RGBW',
                'supported_types': ['solid', 'frames', 'rainbow', 'chase'],
                'max_fps': 60,
                'features': ['brightness_control', 'speed_control', 'custom_animations']
            })
        
        # GET /pixels - Current pixel state
        elif path == '/pixels':
            self._send_json({
                'pixels': strip.get_pixels(),
                'count': strip.count
            })
        
        else:
            self._send_error('Not found', 404)
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        try:
            data = self._read_json()
        except json.JSONDecodeError:
            self._send_error('Invalid JSON')
            return
        
        # POST /animations - Create new animation
        if path == '/animations':
            anim_id = data.get('id')
            if not anim_id:
                self._send_error('Missing animation id')
                return
            
            engine.add_animation(anim_id, data)
            self._send_json({'success': True, 'id': anim_id}, 201)
        
        # POST /playback/start - Start animation
        elif path == '/playback/start':
            anim_id = data.get('animation_id')
            if not anim_id:
                self._send_error('Missing animation_id')
                return
            
            if engine.start_animation(anim_id):
                self._send_json({'success': True, 'animation_id': anim_id})
            else:
                self._send_error('Animation not found', 404)
        
        # POST /playback/stop - Stop animation
        elif path == '/playback/stop':
            engine.stop_animation()
            self._send_json({'success': True})
        
        else:
            self._send_error('Not found', 404)
    
    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        try:
            data = self._read_json()
        except json.JSONDecodeError:
            self._send_error('Invalid JSON')
            return
        
        # PUT /animations/{id} - Update animation
        if path.startswith('/animations/'):
            anim_id = path.split('/')[-1]
            engine.add_animation(anim_id, data)
            self._send_json({'success': True, 'id': anim_id})
        
        # PUT /playback/speed - Set speed
        elif path == '/playback/speed':
            speed = data.get('speed', 1.0)
            engine.speed = max(0.1, min(5.0, speed))
            self._send_json({'success': True, 'speed': engine.speed})
        
        # PUT /playback/brightness - Set brightness
        elif path == '/playback/brightness':
            brightness = data.get('brightness', 1.0)
            strip.brightness = max(0.0, min(1.0, brightness))
            self._send_json({'success': True, 'brightness': strip.brightness})
        
        else:
            self._send_error('Not found', 404)
    
    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        # DELETE /animations/{id} - Delete animation
        if path.startswith('/animations/'):
            anim_id = path.split('/')[-1]
            if engine.delete_animation(anim_id):
                self._send_json({'success': True})
            else:
                self._send_error('Animation not found', 404)
        else:
            self._send_error('Not found', 404)
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[API] {format % args}")


# Global instances
strip = LEDStrip(LED_COUNT)
engine = AnimationEngine(strip)


def run_api_server():
    """Run the HTTP API server in a separate thread"""
    server_address = ('', API_PORT)
    httpd = HTTPServer(server_address, LEDAPIHandler)
    print(f"[API] Server started on http://localhost:{API_PORT}")
    httpd.serve_forever()


def main():
    """Main entry point"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║           WS2814 RGBW LED Simulator with Tkinter          ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print(f"║  API Server:    http://localhost:{API_PORT}                     ║")
    print(f"║  LED Count:     {LED_COUNT}                                      ║")
    print("║  Color Format:  RGBW (4 bytes per pixel)                   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print("Starting API server...")
    
    # Start API server in background thread
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()
    
    print("Starting Tkinter GUI...")
    
    # Run Tkinter GUI in main thread
    visualizer = LEDVisualizer(strip)
    visualizer.run()


if __name__ == '__main__':
    main()
