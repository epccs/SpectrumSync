// 512-channel DMX universe visualizer, built as a starter for trying the Clay GUI library.
// Renders each of the 512 channels as a cell in a 32x16 grid, colored by value.
// A demo chase animation drives the values; click a cell to inspect its channel/value.

#define CLAY_IMPLEMENTATION
#include "clay.h"
#include "renderers/raylib/clay_renderer_raylib.c"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_CHANNELS 512
#define GRID_COLS 32
#define GRID_ROWS (NUM_CHANNELS / GRID_COLS)

static uint8_t channelValues[NUM_CHANNELS];
static int selectedChannel = -1;

static const uint32_t FONT_ID_BODY = 0;

static Clay_Color ChannelColor(uint8_t value) {
    float t = (float)value / 255.0f;
    return (Clay_Color){
        20.0f + t * 40.0f,
        40.0f + t * 170.0f,
        60.0f + t * 195.0f,
        255.0f,
    };
}

static void UpdateChannelValues(double time) {
    for (int i = 0; i < NUM_CHANNELS; i++) {
        float wave = sinf((float)time * 2.0f + (float)i * 0.05f);
        channelValues[i] = (uint8_t)(127.5f + 127.5f * wave);
    }
}

static Clay_RenderCommandArray CreateLayout(void) {
    Clay_BeginLayout();

    char headerBuffer[128];
    if (selectedChannel >= 0) {
        snprintf(headerBuffer, sizeof(headerBuffer), "512-Channel DMX Simulator  -  Channel %d: %d/255",
                  selectedChannel + 1, channelValues[selectedChannel]);
    } else {
        snprintf(headerBuffer, sizeof(headerBuffer), "512-Channel DMX Simulator  -  click a channel to inspect it");
    }
    Clay_String headerText = { .isStaticallyAllocated = false, .length = (int32_t)strlen(headerBuffer), .chars = headerBuffer };

    CLAY(CLAY_ID("Root"), {
        .layout = {
            .layoutDirection = CLAY_TOP_TO_BOTTOM,
            .sizing = { CLAY_SIZING_GROW(0), CLAY_SIZING_GROW(0) },
            .padding = CLAY_PADDING_ALL(16),
            .childGap = 12,
        },
        .backgroundColor = { 18, 18, 22, 255 },
    }) {
        CLAY(CLAY_ID("Header"), {
            .layout = {
                .sizing = { CLAY_SIZING_GROW(0), CLAY_SIZING_FIXED(28) },
                .childAlignment = { .y = CLAY_ALIGN_Y_CENTER },
            },
        }) {
            CLAY_TEXT(headerText, CLAY_TEXT_CONFIG({ .fontId = FONT_ID_BODY, .fontSize = 18, .textColor = { 220, 220, 230, 255 } }));
        }

        CLAY(CLAY_ID("Grid"), {
            .layout = {
                .layoutDirection = CLAY_TOP_TO_BOTTOM,
                .sizing = { CLAY_SIZING_GROW(0), CLAY_SIZING_GROW(0) },
                .childGap = 3,
            },
        }) {
            for (int row = 0; row < GRID_ROWS; row++) {
                CLAY(CLAY_IDI("Row", row), {
                    .layout = {
                        .sizing = { CLAY_SIZING_GROW(0), CLAY_SIZING_GROW(0) },
                        .childGap = 3,
                    },
                }) {
                    for (int col = 0; col < GRID_COLS; col++) {
                        int idx = row * GRID_COLS + col;
                        bool isSelected = (idx == selectedChannel);
                        CLAY(CLAY_IDI("Cell", idx), {
                            .layout = { .sizing = { CLAY_SIZING_GROW(0), CLAY_SIZING_GROW(0) } },
                            .backgroundColor = ChannelColor(channelValues[idx]),
                            .cornerRadius = CLAY_CORNER_RADIUS(3),
                            .border = {
                                .color = isSelected ? (Clay_Color){ 255, 255, 255, 255 } : (Clay_Hovered() ? (Clay_Color){ 255, 255, 255, 120 } : (Clay_Color){ 0, 0, 0, 0 }),
                                .width = CLAY_BORDER_OUTSIDE(isSelected ? 2 : 1),
                            },
                        }) {
                            if (Clay_Hovered() && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                                selectedChannel = idx;
                            }
                        }
                    }
                }
            }
        }
    }

    return Clay_EndLayout(GetFrameTime());
}

void HandleClayErrors(Clay_ErrorData errorData) {
    fprintf(stderr, "%s\n", errorData.errorText.chars);
}

int main(void) {
    uint64_t totalMemorySize = Clay_MinMemorySize();
    Clay_Arena clayMemory = Clay_CreateArenaWithCapacityAndMemory(totalMemorySize, malloc(totalMemorySize));
    Clay_Initialize(clayMemory, (Clay_Dimensions){ 1024, 640 }, (Clay_ErrorHandler){ HandleClayErrors, 0 });

    Clay_Raylib_Initialize(1024, 640, "512-Channel DMX Simulator", FLAG_VSYNC_HINT | FLAG_WINDOW_RESIZABLE | FLAG_MSAA_4X_HINT);

    Font fonts[1];
    fonts[FONT_ID_BODY] = GetFontDefault();
    Clay_SetMeasureTextFunction(Raylib_MeasureText, fonts);

    while (!WindowShouldClose()) {
        Clay_SetLayoutDimensions((Clay_Dimensions){ (float)GetScreenWidth(), (float)GetScreenHeight() });
        Clay_Vector2 mousePosition = { GetMousePosition().x, GetMousePosition().y };
        Clay_SetPointerState(mousePosition, IsMouseButtonDown(MOUSE_BUTTON_LEFT));

        UpdateChannelValues(GetTime());
        Clay_RenderCommandArray renderCommands = CreateLayout();

        BeginDrawing();
        ClearBackground(BLACK);
        Clay_Raylib_Render(renderCommands, fonts);
        EndDrawing();
    }

    Clay_Raylib_Close();
    return 0;
}
