# Mandelbrot Explorer – UI-Verbesserungen Design-Dokument

**Datum:** 2026-02-23
**Status:** Genehmigt

---

## Überblick

Vier Verbesserungen an der Mandelbrot-Explorer-App:

1. Mathematische Formel-Anzeige im Panel
2. Max. Iterationen deutlich erhöhen (bis 16 384)
3. App-Icon neu generieren
4. Reset-Knopf für Ursprungsposition

---

## 1. Mathematische Formel-Anzeige

### Problem
Die Formel wird aktuell nur als roher GLSL-Code angezeigt. Das ist für Nicht-Programmierer schwer lesbar.

### Lösung
Oberhalb des GLSL-Editors erscheint eine stilisierte Anzeige mit der mathematischen Formel in HTML (`<sub>`, `<sup>`, Unicode).

```
┌─────────────────────────────┐
│ FORMEL                      │
│  z_{n+1} = z_n² + c        │
├─────────────────────────────┤
│ Formel (GLSL)               │
│ vec2 formula(vec2 z, ...) { │
└─────────────────────────────┘
```

### Formeln pro Preset

| Preset | HTML-Anzeige |
|---|---|
| Mandelbrot | z<sub>n+1</sub> = z<sub>n</sub>² + c |
| Burning Ship | z<sub>n+1</sub> = (\|Re z\| + i·\|Im z\|)² + c |
| Tricorn | z<sub>n+1</sub> = z̄<sub>n</sub>² + c |
| Multibrot z³ | z<sub>n+1</sub> = z<sub>n</sub>³ + c |
| Eigener Code | z<sub>n+1</sub> = f(z<sub>n</sub>, c) |

### Umsetzung
- Neues `<div id="formula-display">` mit CSS-Styling (größere Schrift, zentriert, akzentuiert)
- JavaScript-Map `FORMULA_DISPLAY` von Preset-Name → HTML-String
- Bei `preset-select` change-Event: `formulaDisplay.innerHTML = FORMULA_DISPLAY[val]`
- Bei Wechsel zu "custom": `f(zₙ, c)` anzeigen

---

## 2. Max. Iterationen erhöhen

### Problem
Aktuell max. 2048 Iterationen. Bei tiefen Zooms (Perturbationstheorie aktiv) sind 4096–16 384 nötig für scharfe Details.

### Lösung
- Slider: `min=64`, `max=16384`, `step=64`, default bleibt `256`
- GLSL-Loop-Grenze in `build2dFragSrc`: von `4096` auf `16384`
- GLSL-Loop-Grenze in `build2dPerturbFragSrc`: von `4096` auf `16384`

---

## 3. App-Icon neu generieren

### Umsetzung
```bash
python3 make_icon.py
iconutil -c icns AppIcon.iconset -o MandelbrotExplorer.app/Contents/Resources/AppIcon.icns
```

Das Skript bleibt unverändert; es rendert bereits die korrekte Mandelbrot-Ansicht (CX=-0.75, SCALE=1.35).

---

## 4. Reset-Knopf

### Problem
Wenn man sich tief in die Mandelbrot-Menge hineingezoomt hat, gibt es keinen einfachen Weg zur Ausgangsansicht zurückzukehren.

### Lösung
Ein `⌂ Reset`-Button im 2D-Panel, der `center`, `zoom` auf die Ausgangswerte zurücksetzt und neu rendert.

### Position
Unterhalb des Zoom-Info-Blocks im 2D-Panel, als schmaler sekundärer Button (abgesetzt von "Apply" durch andere Farbe).

### Verhalten
```javascript
function resetView() {
    center = { x: -0.5, y: 0.0 };
    zoom = 1.0;
    computeOrbit();
    updateInfo();
    needsRender = true;
}
```
