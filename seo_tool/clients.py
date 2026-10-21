"""Klantconfiguratie laden uit clients/<slug>/client.toml."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"


@dataclass
class Client:
    slug: str
    name: str
    domain: str
    language: str = "nl"
    country: str = "nl"
    gsc_property: str | None = None
    ga4_property_id: str | None = None
    competitors: list[str] = field(default_factory=list)
    key_pages: list[str] = field(default_factory=list)

    @property
    def dir(self) -> Path:
        return CLIENTS_DIR / self.slug

    @property
    def data_dir(self) -> Path:
        d = self.dir / "data"
        d.mkdir(parents=True, exist_ok=True)
        return d

    @property
    def base_url(self) -> str:
        d = self.domain.strip().rstrip("/")
        return d if d.startswith("http") else f"https://{d}"

    def data_path(self, kind: str, ext: str) -> Path:
        return self.data_dir / f"{date.today().isoformat()}-{kind}.{ext}"


def list_clients() -> list[str]:
    if not CLIENTS_DIR.exists():
        return []
    return sorted(
        p.name for p in CLIENTS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith("_") and (p / "client.toml").exists()
    )


def load_client(slug: str) -> Client:
    path = CLIENTS_DIR / slug / "client.toml"
    if not path.exists():
        known = ", ".join(list_clients()) or "geen"
        raise SystemExit(f"Klant '{slug}' niet gevonden ({path}). Bekende klanten: {known}")
    with path.open("rb") as f:
        raw = tomllib.load(f)
    general = raw.get("klant", {})
    conn = raw.get("koppelingen", {})
    return Client(
        slug=slug,
        name=general.get("naam", slug),
        domain=general["domein"],
        language=general.get("taal", "nl"),
        country=general.get("land", "nl"),
        gsc_property=conn.get("gsc_property") or None,
        ga4_property_id=str(conn["ga4_property_id"]) if conn.get("ga4_property_id") else None,
        competitors=raw.get("concurrenten", {}).get("domeinen", []),
        key_pages=raw.get("pagina", {}).get("belangrijk", []),
    )
