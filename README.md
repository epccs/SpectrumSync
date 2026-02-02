# SpectrumSync Projects

Why? "Spectrum" for RGB+W channels that output a range of color, "Sync" for the synced chaining across lights (think NeoPixels but higher power).

Meme vibe: "Sync your pixel spectrum to animate your GlowForge".

## Folder Structure and Names

```text
docs/                            # how to power and chain boards
hardware/                        # Top-level folder for all PCB designs and KiCad/Eagle files
├── drivers/                     # e.g., 20W RGB+W driver
├── led-boards/                  # e.g., IMS star board with Cree XLamp XN-P Color LED
├── controllers/                 # e.g., control-point board with ports for data and power
│
firmware/                        # e.g., embedded software for the control-point board
examples/                        # e.g., "4-port loop tutorial"
```

- /docs - For system level documentation: schematics, and guides (e.g., how to power and chain boards).
- /hardware - Top-level folder for all PCB designs and KiCad/Eagle files. Subfolders below for categorization.
- - /drivers - For the initial 20W RGB+W driver (2in x 1in FR4) and future driver variants.
- - /led-boards - For the IMS star board with Cree XLamp XN-P Color LED, plus future IMS additions.
- - /controllers - For the control-point board (with ports for WS2814 data/power looping) and future controllers.
- /firmware - For embedded code (e.g., embedded software for the control-point board).
- /examples - For demo projects, assembly instructions, or chained setups (e.g., "4-port loop tutorial").

## Open Hardware Licensing Recommendations

<https://gemini.google.com/share/2dea24fdcb34>