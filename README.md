# Landing Factory

Dieses Repository erzeugt automatisiert Landingpages aus `data/leads.csv`.
Jeder Datensatz wird in eine eigenständige HTML-Seite unter `pages/` umgewandelt.
Die Verarbeitung wird getrackt, damit keine Seite doppelt erstellt wird.

## Voraussetzungen
- Python 3.10+
- CSV-Datenquelle: `data/leads.csv` (Felder: `slug`, `business_name`, `city`, `service`, `pain_point`, `offer`)

## Manuell ausführen
```bash
python scripts/generate_pages.py
```
- Erstellt bis zu 40 neue Seiten auf Basis der Leads.
- Legt erzeugte Dateien unter `pages/<slug>.html` an.
- Aktualisiert `data/generated.json` mit Zeitstempel und Quelle.

## Tägliche Automatisierung (GitHub Action)
- Workflow: `.github/workflows/daily-pages.yml`
- Läuft täglich um 04:00 UTC (sowie manuell via "Run workflow").
- Schritte:
  1. Checkt den Code aus.
  2. Führt `python scripts/generate_pages.py` aus.
  3. Erstellt einen Pull Request mit den neuen Seiten und dem aktualisierten Tracking-File.

## Tracking
`data/generated.json` enthält alle bereits erzeugten Slugs mit Zeitstempel.
Neue Durchläufe überspringen vorhandene Einträge, damit keine Seite doppelt gebaut wird.

## Inhalt der Seiten
Jede Landingpage enthält:
- Eine eindeutige Überschrift mit Unternehmensname, Service und Stadt.
- Beschreibenden Text mit dem Pain Point und dem Angebot aus der CSV.
- FAQ-Sektion mit drei Fragen & Antworten.
- Deutliche Call-to-Action Buttons.

## Erweiterung
- Weitere Leads einfach als neue Zeilen in `data/leads.csv` hinzufügen.
- Bei mehr als 40 neuen Leads werden überschüssige Datensätze automatisch am nächsten Tag verarbeitet.
