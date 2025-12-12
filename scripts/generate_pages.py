#!/usr/bin/env python3
"""
Generate landing pages from CSV leads.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

BATCH_SIZE = 40
ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "leads.csv"
GENERATED_PATH = ROOT / "data" / "generated.json"
OUTPUT_DIR = ROOT / "pages"
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class Lead:
    slug: str
    business_name: str
    city: str
    service: str
    pain_point: str
    offer: str

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> "Lead":
        required_fields = ["slug", "business_name", "city", "service", "pain_point", "offer"]
        missing = [field for field in required_fields if not row.get(field)]
        if missing:
            raise ValueError(f"Missing fields in CSV row: {missing}")
        return cls(
            slug=row["slug"].strip(),
            business_name=row["business_name"].strip(),
            city=row["city"].strip(),
            service=row["service"].strip(),
            pain_point=row["pain_point"].strip(),
            offer=row["offer"].strip(),
        )


@dataclass
class GeneratedEntry:
    slug: str
    created_at: str
    source: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "slug": self.slug,
            "created_at": self.created_at,
            "source": self.source,
        }


def load_leads(path: Path) -> List[Lead]:
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Lead.from_row(row) for row in reader]


def load_generated(path: Path) -> List[GeneratedEntry]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    entries = data.get("generated", []) if isinstance(data, dict) else data
    result = []
    for item in entries:
        if not isinstance(item, dict) or "slug" not in item:
            continue
        result.append(
            GeneratedEntry(
                slug=item["slug"],
                created_at=item.get("created_at", ""),
                source=item.get("source", "data/leads.csv"),
            )
        )
    return result


def save_generated(path: Path, entries: Iterable[GeneratedEntry]) -> None:
    payload = {"generated": [entry.to_dict() for entry in entries]}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_faq(lead: Lead) -> str:
    faqs = [
        (
            f"Wie kann {lead.business_name} mehr {lead.service.lower()}-Anfragen in {lead.city} gewinnen?",
            f"Wir stellen die Stärken von {lead.business_name} heraus, zeigen Referenzen und bauen klare Conversion-Elemente ein, damit Interessenten sofort Kontakt aufnehmen.",
        ),
        (
            f"Was bedeutet das Angebot \"{lead.offer}\" konkret?",
            f"Wir entwickeln eine individuelle Landingpage, die das {lead.offer} für {lead.business_name} erklärt und Besuchern einen einfachen nächsten Schritt bietet.",
        ),
        (
            "Wie schnell geht die Umsetzung?",
            "In der Regel liefern wir innerhalb weniger Tage eine veröffentlichbare Seite und optimieren anschließend anhand echter Daten.",
        ),
    ]
    items = []
    for question, answer in faqs:
        items.append(
            f"<div class=\"faq-item\">\n"
            f"  <h3>{question}</h3>\n"
            f"  <p>{answer}</p>\n"
            f"</div>"
        )
    return "\n".join(items)


def render_page(lead: Lead) -> str:
    tagline = f"{lead.service} in {lead.city}: {lead.offer}"
    hero = (
        f"<section class=\"hero\">\n"
        f"  <h1>{lead.business_name} – {lead.service} in {lead.city}</h1>\n"
        f"  <p class=\"tagline\">{tagline}</p>\n"
        f"  <a class=\"cta\" href=\"mailto:hello@example.com?subject={lead.business_name}%20Landingpage\">Jetzt Beratung sichern</a>\n"
        f"</section>"
    )
    pain_section = (
        f"<section class=\"pain\">\n"
        f"  <h2>Wir lösen: {lead.pain_point}</h2>\n"
        f"  <p>Viele {lead.service}-Teams in {lead.city} verlieren täglich potenzielle Kunden, weil ihre Website nicht überzeugt. {lead.business_name} bekommt eine Seite, die Vertrauen aufbaut, Fragen beantwortet und immer auf einen klaren CTA führt.</p>\n"
        f"  <ul>\n"
        f"    <li>Storytelling rund um {lead.business_name}</li>\n"
        f"    <li>Lokale Beweise aus {lead.city}</li>\n"
        f"    <li>Schlanke Kontaktwege für mehr Abschlüsse</li>\n"
        f"  </ul>\n"
        f"</section>"
    )
    faq_section = f"<section class=\"faq\">\n  <h2>Häufige Fragen</h2>\n  {render_faq(lead)}\n</section>"
    footer = (
        f"<footer>\n"
        f"  <p>Seite für {lead.business_name} erstellt am {datetime.utcnow().strftime('%d.%m.%Y')}.</p>\n"
        f"  <a class=\"cta secondary\" href=\"mailto:hello@example.com?subject={lead.business_name}%20Projekt\">Kostenloses Gespräch anfragen</a>\n"
        f"</footer>"
    )
    style = """
    <style>
      :root { font-family: 'Inter', Arial, sans-serif; color: #111827; background: #f9fafb; }
      body { max-width: 900px; margin: 0 auto; padding: 24px; line-height: 1.6; }
      h1, h2, h3 { color: #0f172a; margin-bottom: 8px; }
      .hero { background: linear-gradient(120deg, #e0f2fe, #ecfeff); padding: 32px; border-radius: 16px; margin-bottom: 24px; }
      .tagline { font-size: 1.1rem; margin-bottom: 16px; }
      .cta { display: inline-block; padding: 12px 18px; background: #2563eb; color: #fff; border-radius: 12px; text-decoration: none; font-weight: 600; }
      .cta.secondary { background: #0ea5e9; }
      .pain, .faq { background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05); margin-bottom: 24px; }
      ul { padding-left: 20px; }
      .faq-item { margin-bottom: 14px; }
      footer { display: flex; justify-content: space-between; align-items: center; background: #f1f5f9; padding: 16px; border-radius: 12px; }
      @media (max-width: 640px) { footer { flex-direction: column; align-items: flex-start; gap: 12px; } }
    </style>
    """
    html = (
        f"<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n  <meta charset=\"UTF-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n  <title>{lead.business_name} – {lead.service} in {lead.city}</title>\n  {style}\n</head>\n<body>\n  {hero}\n  {pain_section}\n  {faq_section}\n  {footer}\n</body>\n</html>\n"
    )
    return html


def main() -> None:
    leads = load_leads(CSV_PATH)
    generated_entries = load_generated(GENERATED_PATH)
    generated_slugs = {entry.slug for entry in generated_entries}

    fresh_leads = [lead for lead in leads if lead.slug not in generated_slugs]
    batch = fresh_leads[:BATCH_SIZE]

    if not batch:
        print("No new leads to generate.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    now_str = datetime.utcnow().strftime(TIMESTAMP_FORMAT)
    for lead in batch:
        output_file = OUTPUT_DIR / f"{lead.slug}.html"
        output_file.write_text(render_page(lead), encoding="utf-8")
        generated_entries.append(
            GeneratedEntry(slug=lead.slug, created_at=now_str, source=str(CSV_PATH.relative_to(ROOT)))
        )
        print(f"Generated {output_file.relative_to(ROOT)}")

    save_generated(GENERATED_PATH, generated_entries)
    print(f"Saved log to {GENERATED_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
