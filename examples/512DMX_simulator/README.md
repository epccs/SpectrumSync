# Simulator for DMX512

A desktop visualizer for a 512-channel DMX universe, built with [Clay](https://github.com/nicbarker/clay) (an immediate-mode C UI layout library) rendered via [raylib](https://www.raylib.com/). It's a starting point for prototyping DMX controller UIs before wiring them up to real hardware.

## Features

- Renders all 512 DMX channels as a 32x16 grid of cells, colored by value
- A demo chase animation drives the channel values so the grid is alive out of the box
- Click a cell to select a channel and see its number/value in the header

## Quick Start

### 1. Install build tools (Ubuntu 24.04)

Clay is a single header file (vendored in `vendor/clay/`), and raylib is fetched and built from source by CMake, so the only system packages needed are the compiler, CMake, and raylib's windowing/GL dependencies:

```bash
sudo apt update
sudo apt install -y build-essential cmake libgl1-mesa-dev libx11-dev \
  libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev libwayland-dev libxkbcommon-dev
```

### 2. Build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j"$(nproc)"
```

The first configure step clones and builds raylib (via CMake `FetchContent`), so it takes a few minutes; later builds are fast.

### 3. Run

```bash
./build/dmx512_simulator
```

## Layout

- `src/main.c` — application entry point and Clay layout for the channel grid
- `vendor/clay/` — vendored copy of `clay.h` and its raylib renderer, pulled from the upstream [Clay repo](https://github.com/nicbarker/clay)
- `CMakeLists.txt` — build configuration; fetches raylib 5.5 via CMake `FetchContent`
