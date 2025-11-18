#pragma once
#include <windows.h>
#include "XTTPSession.h"

class OverlayRenderer {
public:
    static void Init(HWND hwnd);
    static void Render(HWND hwnd);
    static void DrawSessionInfo(HDC hdc, const XTTPSession& session);
};
