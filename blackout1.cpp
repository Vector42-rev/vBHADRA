#include <windows.h>
#include <iostream>



HWND hOverlay;  // Global handle for the overlay window

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            HBRUSH hBrush = CreateSolidBrush(RGB(0, 0, 0));  // Black color
            FillRect(hdc, &ps.rcPaint, hBrush);
            DeleteObject(hBrush);
            EndPaint(hwnd, &ps);
        } break;

        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;

        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
    return 0;
}

void CreateOverlay(int x, int y, int width, int height) {
    WNDCLASS wc = { 0 };
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = "PartialOverlay";

    RegisterClass(&wc);

    hOverlay = CreateWindowEx(
        WS_EX_TOPMOST | WS_EX_LAYERED | WS_EX_TRANSPARENT,  // Make window non-interactive
        "PartialOverlay", "Overlay Window",
        WS_POPUP,  // No border, custom size
        x, y, width, height,  // Set position and size
        NULL, NULL, GetModuleHandle(NULL), NULL
    );

    if (!hOverlay) {
        std::cout << "Failed to create overlay window!" << std::endl;
        return;
    }

    // Adjust transparency level (0 = fully transparent, 255 = fully black)
    SetLayeredWindowAttributes(hOverlay, 0, 255, LWA_ALPHA);  // 255 = fully black

    ShowWindow(hOverlay, SW_SHOW);
    UpdateWindow(hOverlay);
}

void RemoveOverlay() {
    if (hOverlay) {
        DestroyWindow(hOverlay);
        hOverlay = NULL;
    }
}

int main() {
    std::cout << "Blacking out 3 regions..." << std::endl;

// Original box coordinates
int x = 571;
int y = 470;
int width = 1220 - 571;   // 442
int height = 1032 - 470;   // 333

// Translation values: 
// positive dx moves right, negative dx moves left
// positive dy moves down, negative dy moves up
int dx = -100;   // move left by 2 pixels
int dy = -100;  // move up by 40 pixels

// Calculate new top-left corner after translation
int new_x = x + dx;
int new_y = y + dy;

// Width and height remain unchanged
CreateOverlay(new_x, new_y, width, height);




    Sleep(6000);  // Keep the effect for 5 seconds

    std::cout << "Restoring screen..." << std::endl;
    RemoveOverlay();

    return 0;
}
