# UI-Verbesserungen – Implementierungsplan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Vier UI-Verbesserungen: mathematische Formel-Anzeige, höhere Max-Iterationen, Icon-Neugenerierung und Reset-Knopf.

**Architecture:** Alle Änderungen in `MandelbrotExplorer.app/Contents/Resources/index.html` (HTML + CSS + JS). Kein Swift-Rebuild nötig. Das App-Icon wird via Python-Skript + `iconutil` neu gebaut.

**Tech Stack:** Vanilla HTML/CSS/JavaScript, WebGL 1.0 (GLSL ES 1.0), Python 3 (Icon), Swift 5/Cocoa (kein Rebuild nötig)

---

## Task 1: Mathematische Formel-Anzeige

**Files:**
- Modify: `MandelbrotExplorer.app/Contents/Resources/index.html`

**Schritt 1: CSS für die Formel-Anzeige hinzufügen**

Im `<style>`-Block, direkt nach `.slider-group { ... }` einfügen:

```css
.formula-display {
    background: #0a1628;
    border: 1px solid #0f3460;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 14px;
    text-align: center;
    color: #4fc3f7;
    letter-spacing: 0.5px;
    line-height: 1.8;
    font-family: 'Georgia', 'Times New Roman', serif;
}
```

**Schritt 2: HTML-Element für Formel-Anzeige einbauen**

Im 2D-Panel, direkt VOR dem `<div>` mit der `section-label` "Formel (GLSL)" einfügen:

```html
<div>
    <div class="section-label">Formel</div>
    <div class="formula-display" id="formula-display">
        z<sub>n+1</sub> = z<sub>n</sub>² + c
    </div>
</div>
```

**Schritt 3: JavaScript-Map für Formel-Anzeigen hinzufügen**

Im `<script>`-Block, direkt nach dem `PRESETS`-Objekt (nach Zeile `};` des PRESETS) einfügen:

```javascript
// ============================================================
// Mathematische Formel-Anzeige pro Preset
// ============================================================
const FORMULA_DISPLAY = {
    'mandelbrot':   'z<sub>n+1</sub> = z<sub>n</sub>² + c',
    'burning-ship': 'z<sub>n+1</sub> = (|Re z<sub>n</sub>| + i·|Im z<sub>n</sub>|)² + c',
    'tricorn':      'z<sub>n+1</sub> = z̄<sub>n</sub>² + c',
    'multibrot3':   'z<sub>n+1</sub> = z<sub>n</sub>³ + c',
    'custom':       'z<sub>n+1</sub> = f(z<sub>n</sub>, c)'
};
```

**Schritt 4: Preset-Change-Handler aktualisieren**

Den bestehenden `preset-select` change-Listener finden:

```javascript
document.getElementById('preset-select').addEventListener('change', e => {
    const val = e.target.value;
    if (val !== 'custom') {
        document.getElementById('formula-editor').value = PRESETS[val];
    }
    isDefaultFormula = (val === 'mandelbrot');
    needsRender = true;
});
```

Ersetzen durch:

```javascript
document.getElementById('preset-select').addEventListener('change', e => {
    const val = e.target.value;
    if (val !== 'custom') {
        document.getElementById('formula-editor').value = PRESETS[val];
    }
    isDefaultFormula = (val === 'mandelbrot');
    document.getElementById('formula-display').innerHTML = FORMULA_DISPLAY[val] || FORMULA_DISPLAY['custom'];
    needsRender = true;
});
```

**Schritt 5: Im Browser testen**

```bash
open MandelbrotExplorer.app/Contents/Resources/index.html
```

Erwartung:
- Über dem GLSL-Editor erscheint die Formelzeile „z_{n+1} = z_n² + c"
- Beim Wechsel auf „Burning Ship" ändert sich die Anzeige entsprechend
- Beim Wechsel auf „Eigener Code" steht „z_{n+1} = f(z_n, c)"

**Schritt 6: Commit**

```bash
git add MandelbrotExplorer.app/Contents/Resources/index.html
git commit -m "feat: mathematische Formel-Anzeige über GLSL-Editor"
```

---

## Task 2: Max. Iterationen erhöhen

**Files:**
- Modify: `MandelbrotExplorer.app/Contents/Resources/index.html`

**Schritt 1: Slider-Bereich im HTML anpassen**

Den bestehenden `max-iter`-Slider finden:

```html
<input type="range" id="max-iter" min="64" max="2048" step="64" value="256">
```

Ersetzen durch:

```html
<input type="range" id="max-iter" min="64" max="16384" step="64" value="256">
```

**Schritt 2: GLSL-Loop-Grenze im Standard-2D-Shader erhöhen**

In `build2dFragSrc` die Schleife finden:

```glsl
for (int i = 0; i < 4096; i++) {
    if (i >= u_maxIter) break;
```

Ersetzen durch:

```glsl
for (int i = 0; i < 16384; i++) {
    if (i >= u_maxIter) break;
```

**Schritt 3: GLSL-Loop-Grenze im Perturbations-Shader erhöhen**

In `build2dPerturbFragSrc` dieselbe Schleife finden:

```glsl
for (int i = 0; i < 4096; i++) {
    if (i >= u_maxIter) break;
```

Ersetzen durch:

```glsl
for (int i = 0; i < 16384; i++) {
    if (i >= u_maxIter) break;
```

**Schritt 4: Im Browser testen**

```bash
open MandelbrotExplorer.app/Contents/Resources/index.html
```

Erwartung:
- Slider geht jetzt bis 16 384
- Bei hohem Wert (z.B. 8192) und tiefem Zoom sind mehr Details sichtbar

**Schritt 5: Commit**

```bash
git add MandelbrotExplorer.app/Contents/Resources/index.html
git commit -m "feat: Max-Iterationen bis 16384 (Slider + GLSL-Loops)"
```

---

## Task 3: App-Icon neu generieren

**Files:**
- Kein Code ändern – nur ausführen

**Schritt 1: Icon-Basis rendern**

```bash
cd /Users/jjr/mandelbrot
python3 make_icon.py
```

Erwartung:
```
Rendere 512x512 Mandelbrot-Icon ...
  0/512
  64/512
  ...
  448/512
icon_base.png geschrieben
```

**Schritt 2: PNG-Größen aus icon_base.png erzeugen**

```bash
sips -z 16 16     icon_base.png --out AppIcon.iconset/icon_16x16.png
sips -z 32 32     icon_base.png --out AppIcon.iconset/icon_16x16@2x.png
sips -z 32 32     icon_base.png --out AppIcon.iconset/icon_32x32.png
sips -z 64 64     icon_base.png --out AppIcon.iconset/icon_32x32@2x.png
sips -z 128 128   icon_base.png --out AppIcon.iconset/icon_128x128.png
sips -z 256 256   icon_base.png --out AppIcon.iconset/icon_128x128@2x.png
sips -z 256 256   icon_base.png --out AppIcon.iconset/icon_256x256.png
sips -z 512 512   icon_base.png --out AppIcon.iconset/icon_256x256@2x.png
sips -z 512 512   icon_base.png --out AppIcon.iconset/icon_512x512.png
sips -z 1024 1024 icon_base.png --out AppIcon.iconset/icon_512x512@2x.png
```

**Schritt 3: .icns bauen und in Bundle kopieren**

```bash
iconutil -c icns AppIcon.iconset -o MandelbrotExplorer.app/Contents/Resources/AppIcon.icns
```

**Schritt 4: App starten und Icon prüfen**

```bash
open MandelbrotExplorer.app
```

Erwartung: Im Dock erscheint das farbige Mandelbrot-Icon mit gerundeten Ecken.

**Schritt 5: Commit**

```bash
git add MandelbrotExplorer.app/Contents/Resources/AppIcon.icns AppIcon.iconset/
git commit -m "feat: App-Icon aktualisiert (Mandelbrot-Render neugebaut)"
```

---

## Task 4: Reset-Knopf für Ursprungsposition

**Files:**
- Modify: `MandelbrotExplorer.app/Contents/Resources/index.html`

**Schritt 1: CSS für Reset-Button hinzufügen**

Im `<style>`-Block, direkt nach `button.apply-btn:hover { background: #c73652; }` einfügen:

```css
button.reset-btn {
    width: 100%;
    padding: 7px;
    background: transparent;
    border: 1px solid #0f3460;
    border-radius: 4px;
    color: #888;
    cursor: pointer;
    font-family: inherit;
    font-size: 11px;
    letter-spacing: 1px;
    transition: all 0.2s;
}
button.reset-btn:hover {
    border-color: #4fc3f7;
    color: #4fc3f7;
}
```

**Schritt 2: Reset-Button im 2D-Panel einfügen**

Im 2D-Panel direkt NACH der Info-Box (also nach dem schließenden `</div>` des Info-Blocks) einfügen:

```html
<button class="reset-btn" id="reset-view">&#8962; Ursprung</button>
```

**Schritt 3: JavaScript-Handler für Reset einfügen**

Im `<script>`-Block, direkt vor `window.addEventListener('load', init)`, einfügen:

```javascript
// ============================================================
// Reset-Knopf: Ursprungsansicht
// ============================================================
document.getElementById('reset-view').addEventListener('click', () => {
    center = { x: -0.5, y: 0.0 };
    zoom = 1.0;
    computeOrbit();
    updateInfo();
    needsRender = true;
});
```

**Schritt 4: Im Browser testen**

```bash
open MandelbrotExplorer.app/Contents/Resources/index.html
```

Testablauf:
1. Mehrfach zoomen und panen
2. Auf „⌂ Ursprung" klicken
3. Erwartung: Ansicht springt zurück zu center=(-0.5, 0.0), Zoom=1.0 – die klassische Gesamtansicht

**Schritt 5: Commit**

```bash
git add MandelbrotExplorer.app/Contents/Resources/index.html
git commit -m "feat: Reset-Knopf zum Zurückkehren zur Ursprungsansicht"
```

---

## Abschluss: Swift neu bauen

```bash
swiftc -framework Cocoa -framework WebKit main.swift \
  -o MandelbrotExplorer.app/Contents/MacOS/MandelbrotExplorer
open MandelbrotExplorer.app
```

Finaler Funktionstest:
- [ ] Formel-Anzeige aktualisiert sich bei Preset-Wechsel
- [ ] Max-Iter-Slider geht bis 16 384
- [ ] App-Icon im Dock zeigt Mandelbrot
- [ ] Reset-Knopf setzt Ansicht zurück
