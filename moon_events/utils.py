import sys
import os

def get_resource_path(relative_path: str) -> str:
    """
    Ermittelt den absoluten Pfad zu Ressourcen (Bilder, Konfigurationsdateien).
    Unterstützt normalen Entwicklungsmodus sowie PyInstaller/auto-py-to-exe
    im Onefile- (sys._MEIPASS) und Onedir-Modus.
    """
    if hasattr(sys, '_MEIPASS'):
        bundle_path = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(bundle_path):
            return bundle_path

    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        exe_path = os.path.join(exe_dir, relative_path)
        if os.path.exists(exe_path):
            return exe_path

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    project_path = os.path.join(base_dir, relative_path)
    if os.path.exists(project_path):
        return project_path

    return os.path.abspath(relative_path)


def get_storage_path(filename: str = "mond_einstellungen.json") -> str:
    """
    Ermittelt den Speicherpfad für veränderliche Benutzerdaten (z. B. Einstellungen).
    Im gepackten Zustand (.exe) werden die Daten neben der .exe-Datei gespeichert,
    im Entwicklungsmodus im Projekt-Hauptverzeichnis.
    """
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        return os.path.join(exe_dir, filename)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, filename)
