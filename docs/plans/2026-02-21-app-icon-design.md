# App-Icon Design – Mandelbrot Explorer

## Ziel

Ein macOS App-Icon (`.icns`) für den Mandelbrot Explorer, das einen echten Mandelbrot-Render zeigt.

## Design

- **Format:** 1024×1024 PNG, abgerundete Ecken (~180px Radius)
- **Ansicht:** Klassische Mandelbrot-Menge, Mittelpunkt `(-0.75, 0)`, 256 Iterationen
- **Hintergrund:** `#1a1a2e` (identisch zur App)
- **Colorizer:** HSV – identisch zur App (`t*3+0.6`, `s=0.85`, `v=sqrt(t)`)

## Implementierung

1. Python-Skript `make_icon.py` rendert 1024×1024 Mandelbrot-PNG (pure stdlib: `zlib`, `struct`)
2. `sips` erzeugt alle macOS-Icon-Größen (16, 32, 128, 256, 512 @1x und @2x)
3. `iconutil` kompiliert `AppIcon.iconset/` → `AppIcon.icns`
4. `AppIcon.icns` → `MandelbrotExplorer.app/Contents/Resources/`
5. `Info.plist` erhält `CFBundleIconFile = AppIcon`
6. Swift-Binary neu kompilieren

## Dateien

- Create: `make_icon.py`
- Create: `MandelbrotExplorer.app/Contents/Resources/AppIcon.icns`
- Modify: `MandelbrotExplorer.app/Contents/Info.plist`
