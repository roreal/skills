#!/usr/bin/env python3
"""Inventera valbara tariffprodukter utan att aktivera besparingsförmåga.

Källa: Neptunes genererade TARIFFER-snapshot. Matrisen beskriver existerande
pris-/indataberoenden, INTE att ett efter-scenario redan är verifierat.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parents[3] / "neptune_academy/neptune-marketing/src/data/tariffer.generated.ts"
JSON_OUTPUT = HERE / "besparingspotential-tackningsmatris-2026.json"
MARKDOWN_OUTPUT = HERE / "besparingspotential-tackningsmatris-2026.md"

FLOW_TEMPERATURE_TYPES = frozenset({
    "volume", "flow_difference", "temperature_difference",
    "supply_temperature_adjusted_flow", "signed_monthly_flow_adjustment",
    "categorical_flow_rate_estimate", "conditional_flow", "cooling_deadband",
    "incremental_return_temperature", "asymmetric_flow_difference",
})
HISTORY_BAND_TYPES = frozenset({
    "low_utilization", "volume_discount", "seasonal_banded_volume_discount_estimate",
})

# Namngiven, fail-closed statuskonfiguration för de enda två produkter som
# har en granskad scenariostatus (handoff 2026-09-25-002, del B.4). Varje
# nyckel MÅSTE finnas exakt en gång i den inlästa snapshoten (kontrolleras i
# build_matrix) — ingen tyst fallback för ett ID som skrivits fel eller
# tagits bort ur katalogen. Alla övriga 75 produkter förblir "not_reviewed".
# Ingen av dessa statusar innebär publik UI-aktivering eller
# stodjer_besparing-ändring; det avgörs separat i Neptune-koden.
SCENARIO_STATUS_REGISTRY: dict[str, str] = {
    "stockholm-exergi": "synlig_saerskild_preliminar_prototyp",
    "sundsvall-energi-indal-liden-och-lucksta": "godkand_intern_pilot_ej_publik",
}


def parse_snapshot(text: str) -> tuple[dict[str, Any], dict[str, str]]:
    marker = "export const TARIFFER = "
    if text.count(marker) != 1 or text.count(" as const;") != 1:
        raise ValueError("Förväntade exakt ett genererat TARIFFER-objekt.")
    payload = text.split(marker, 1)[1].split(" as const;", 1)[0]
    tariffs = json.loads(payload)
    if not isinstance(tariffs, dict) or not tariffs:
        raise ValueError("Tariff-snapshoten måste vara ett icke-tomt objekt.")
    generated = re.search(r"export const GENERERAD = '([^']+)';", text)
    origin = re.search(r"Källkatalog: sha256=([0-9a-f]{64}) commit=([0-9a-f]{7,40})", text)
    if not generated or not origin:
        raise ValueError("Genereringsdatum eller katalogproveniens saknas.")
    return tariffs, {
        "generated_on": generated.group(1),
        "catalog_sha256": origin.group(1),
        "catalog_commit": origin.group(2),
    }


def latest_price(entry: dict[str, Any]) -> dict[str, Any]:
    prices = entry.get("prisar")
    if not isinstance(prices, list) or not prices:
        raise ValueError(f"{entry.get('id')}: saknar prisår.")
    if any(not isinstance(price.get("ar"), int) for price in prices):
        raise ValueError(f"{entry.get('id')}: ogiltigt prisår.")
    return max(prices, key=lambda price: price["ar"])


def product_row(product_id: str, entry: dict[str, Any]) -> dict[str, Any]:
    price = latest_price(entry)
    policy = price.get("policy")
    has_marker = "_kraver_kontrakt" in price
    if has_marker and (price["_kraver_kontrakt"] is not True or not isinstance(policy, dict)):
        raise ValueError(f"{product_id}: kontraktsmarkör och policy stämmer inte.")
    if not has_marker and policy is not None:
        raise ValueError(f"{product_id}: policy utan kontraktsmarkör kräver separat granskning.")

    required_fields = policy.get("kravda_falt", []) if policy else []
    adjustment_types = sorted({item["type"] for item in price.get("justeringar", [])})
    exclusions = sorted({
        item["component"] for item in price.get("justeringar", [])
        if item["type"] == "documented_exclusion"
    })
    measurement_resolutions = {
        field["nyckel"]: field["matupplosning"] for field in required_fields
        if field.get("matupplosning")
    }
    history_fields = sorted({
        field["nyckel"] for field in required_fields
        if field.get("rullande") or field.get("kalperiod_definition")
        or field.get("takad_till_snapshot")
    })
    series_fields = sorted({
        field["nyckel"] for field in required_fields
        if field.get("vardetyp") == "number_series"
    })
    capacity = price.get("kapacitet") or {}
    capacity_type = capacity.get("typ", "none")
    capacity_bands = len(capacity.get("nivaer") or [])
    has_capacity_charge = capacity_bands > 0 or capacity_type in {
        "piecewise_polynomial", "heterogeneous_bands",
    }
    eligibility = price.get("eligibility") is not None
    risk_flags = []
    if has_capacity_charge:
        risk_flags.append("debiterbar_effekt")
    if capacity_type in {"piecewise_polynomial", "heterogeneous_bands"}:
        risk_flags.append("specialeffekt")
    if price.get("returtemperatur") is not None or FLOW_TEMPERATURE_TYPES.intersection(adjustment_types):
        risk_flags.append("flode_eller_temperatur")
    if history_fields or HISTORY_BAND_TYPES.intersection(adjustment_types):
        risk_flags.append("historik_eller_band")
    if series_fields:
        risk_flags.append("manadsserie")
    if eligibility:
        risk_flags.append("behorighet")

    if not has_marker:
        cost_path = "legacy_besparing"
        savings_today = True
    elif policy.get("stodjer_besparing") is True:
        cost_path = "kontrakt_besparing"
        savings_today = True
    elif policy.get("stodjer_aktuell_arskostnad") is True:
        cost_path = "kontrakt_arskostnad"
        savings_today = False
    else:
        raise ValueError(f"{product_id}: ingen användbar årsprodukt i snapshoten.")

    # Endast teknisk sortering av framtida granskningsordning, INTE
    # godkännande av ett efter-scenario eller påstående om fysisk påverkan.
    wave = 4 if eligibility else 3 if "flode_eller_temperatur" in risk_flags or series_fields else 2 if has_capacity_charge else 1
    return {
        "product_id": product_id,
        "product_name": entry["namn"],
        "tariff_id": price.get("tariff_id"),
        "price_year": price["ar"],
        "price_source": price.get("kalla") or entry.get("kalla") or entry.get("prislista"),
        "synthetic": entry.get("syntetisk") is True,
        "vat_basis": price["moms"],
        "cost_path": cost_path,
        "savings_today": savings_today,
        "energy_rule_keys": sorted(price.get("energi", {}).keys()),
        "capacity_rule": capacity_type,
        "capacity_bands": capacity_bands,
        "has_capacity_charge": has_capacity_charge,
        "has_return_temperature_rule": price.get("returtemperatur") is not None,
        "adjustment_types": adjustment_types,
        "documented_exclusions": exclusions,
        "required_policy_fields": sorted({field["nyckel"] for field in required_fields}),
        "measurement_resolutions": measurement_resolutions,
        "series_fields": series_fields,
        "history_fields": history_fields,
        "has_eligibility_rule": eligibility,
        "risk_flags": risk_flags,
        "review_wave": wave,
        "scenario_review_status": SCENARIO_STATUS_REGISTRY.get(product_id, "not_reviewed"),
    }


def build_matrix(text: str) -> dict[str, Any]:
    tariffs, provenance = parse_snapshot(text)
    rows = [product_row(product_id, tariffs[product_id]) for product_id in sorted(tariffs)]
    if len({row["product_id"] for row in rows}) != len(rows):
        raise ValueError("Dubbla produkt-ID:n i matrisen.")
    tariff_ids = [row["tariff_id"] for row in rows if row["tariff_id"] is not None]
    if len(set(tariff_ids)) != len(tariff_ids):
        raise ValueError("Dubbla tariff-ID:n i matrisen.")
    product_ids = {row["product_id"] for row in rows}
    for registered_id in SCENARIO_STATUS_REGISTRY:
        if registered_id not in product_ids:
            raise ValueError(
                f"SCENARIO_STATUS_REGISTRY refererar {registered_id!r}, som saknas i snapshoten."
            )
    counts = {
        "products": len(rows),
        "real_products": sum(not row["synthetic"] for row in rows),
        "synthetic_products": sum(row["synthetic"] for row in rows),
        "existing_savings": sum(row["savings_today"] for row in rows),
        "current_cost_only": sum(row["cost_path"] == "kontrakt_arskostnad" for row in rows),
        "review_waves": {str(k): v for k, v in sorted(Counter(row["review_wave"] for row in rows).items())},
    }
    return {
        "source_file": "neptune-marketing/src/data/tariffer.generated.ts",
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        **provenance,
        "counts": counts,
        "rows": rows,
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    counts = matrix["counts"]
    lines = [
        "# Täckningsmatris för preliminär Optimate-potential, 2026",
        "",
        "Maskingenererad inventering av den valbara tariff-snapshoten. **Denna matris",
        "godkänner inte något nytt besparingsscenario eller någon tariffaktivering.**",
        "`scenario_review_status=not_reviewed` gäller alla rader utom de två nedan,",
        "tills prisledens före/efter-beroenden har granskats separat. Varken Stockholms",
        "synliga prototyp eller Sundsvalls interna pilot ändrar tariffens befintliga",
        "`stodjer_besparing`-spärr eller aktiverar något publikt UI.",
        "",
        "- `scenario_review_status=synlig_saerskild_preliminar_prototyp` (stockholm-exergi):",
        "  10/15/20-scenariot är synligt som en avgränsad, preliminär prototyp — inte en",
        "  godkänd publik besparingsprodukt.",
        "- `scenario_review_status=godkand_intern_pilot_ej_publik`",
        "  (sundsvall-energi-indal-liden-och-lucksta): godkänd för intern beräkningspilot,",
        "  inte publikt aktiverad (se `stodjerOptimateScenarioPubliktAktiverad`).",
        "",
        f"- Källa: `{matrix['source_file']}`, SHA-256 `{matrix['source_sha256']}`.",
        f"- Genererad tariffdata: {matrix['generated_on']}; källkatalog `{matrix['catalog_commit']}` / SHA-256 `{matrix['catalog_sha256']}`.",
        f"- Produktval: {counts['products']} totalt = {counts['real_products']} verkliga leverantörsprodukter + {counts['synthetic_products']} syntetiskt riksgenomsnitt. Utrullningens måltal är de {counts['real_products']} verkliga produkterna; riksgenomsnittet redovisas separat och ingår inte i måltalet. {counts['existing_savings']} har befintlig besparingsväg och {counts['current_cost_only']} har enbart kontraktsstyrd årskostnad.",
        "- Vågnumret är endast en mekanisk sortering för granskning: 1 utan identifierat effekt-/flödesberoende, 2 effekt, 3 flöde/temperatur/serie, 4 behörighet. Även legacyprodukter kan ligga i våg 2–3 och flera beroenden kan finnas på samma rad.",
        "- `historikfält` avser policyfält märkta rullande, källperiod eller snapshot; det är **inte** ett fullständigt bevis för tariffens historiska prisregler.",
        "- Källreferens, mätupplösning per policyfält, dokumenterade exkluderingar och granskningsstatus finns i JSON-filen. `katalog` betyder källkatalogen ovan, inte en direktlänk till prislistan.",
        "",
        "| Våg | Produkt-ID | Nät/produkt | Befintlig väg | Energiregel | Kapacitet | Justeringstyper | Krävda policyfält | Historik/serie/behörighet | Exkluderingar |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in matrix["rows"]:
        capacity = row["capacity_rule"] if row["has_capacity_charge"] else "ingen debiterbar kapacitetsdel"
        if row["capacity_bands"]:
            capacity += f" ({row['capacity_bands']} band)"
        special = []
        if row["history_fields"]:
            special.append("historik: " + ", ".join(row["history_fields"]))
        if row["series_fields"]:
            special.append("serie: " + ", ".join(row["series_fields"]))
        if row["has_eligibility_rule"]:
            special.append("behörighet")
        if row["has_return_temperature_rule"]:
            special.append("returregel")
        values = [
            str(row["review_wave"]), row["product_id"], row["product_name"], row["cost_path"],
            ", ".join(row["energy_rule_keys"]), capacity,
            ", ".join(row["adjustment_types"]) or "—",
            ", ".join(row["required_policy_fields"]) or "—",
            "; ".join(special) or "—",
            ", ".join(row["documented_exclusions"]) or "—",
        ]
        lines.append("| " + " | ".join(value.replace("|", "\\|") for value in values) + " |")
    lines.extend([
        "",
        "## Nästa granskning",
        "",
        "För varje rad ska tariffens energi-, effekt-, flödes-, temperatur-, fasta",
        "och historikberoenden klassificeras som ändrade, låsta eller okända i",
        "ett före/efter-scenario. Först därefter kan en separat preliminär",
        "scenarioförmåga prövas och aktiveras. De tekniska fältnamnen ovan är",
        "spårbar inventering, inte en kausal Optimate-modell.",
        "",
        "Generera/validera med `python Fjarrvarmetariffer/generera_besparingspotential_tackningsmatris.py --write`",
        "respektive `--check` från Ellen-repot när Neptune ligger som syskonrepo.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source_text = args.source.read_text(encoding="utf-8")
    matrix = build_matrix(source_text)
    expected = {
        JSON_OUTPUT: json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
        MARKDOWN_OUTPUT: render_markdown(matrix),
    }
    if args.write:
        for path, content in expected.items():
            path.write_text(content, encoding="utf-8")
        print(f"Skrev {matrix['counts']['products']} produkter i JSON och Markdown.")
        return 0
    stale = [str(path) for path, content in expected.items() if not path.exists() or path.read_text(encoding="utf-8") != content]
    if stale:
        print("Täckningsmatrisen är inaktuell: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(f"Täckningsmatrisen matchar {matrix['counts']['products']} produkter och källhashen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
