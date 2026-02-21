import Cocoa
import WebKit

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    var webView: WKWebView!

    func applicationDidFinishLaunching(_ notification: Notification) {
        let config = WKWebViewConfiguration()
        // Erlaubt Zugriff auf lokale Dateien
        let prefs = WKPreferences()
        config.preferences = prefs

        webView = WKWebView(frame: .zero, configuration: config)

        window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 1440, height: 900),
            styleMask: [.titled, .closable, .miniaturizable, .resizable],
            backing: .buffered,
            defer: false
        )
        window.title = "Mandelbrot Explorer"
        window.contentView = webView
        window.center()
        window.makeKeyAndOrderFront(nil)

        guard let htmlPath = Bundle.main.path(forResource: "index", ofType: "html") else {
            fatalError("index.html nicht im Bundle gefunden")
        }
        let url = URL(fileURLWithPath: htmlPath)
        webView.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()
