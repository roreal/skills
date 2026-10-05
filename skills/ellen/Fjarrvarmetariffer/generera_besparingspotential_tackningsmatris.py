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

# Namngiven, fail-closed statuskonfiguration för de enda produkter som har en
# granskad scenariostatus (handoff 2026-09-25-002, del B.4; aktivering våg 1
# signal 2026-09-25-015, våg 2 signal 2026-09-30-002). Varje nyckel MÅSTE
# finnas exakt en gång i den inlästa snapshoten (kontrolleras i build_matrix)
# — ingen tyst fallback för ett ID som skrivits fel eller tagits bort ur
# katalogen. Alla övriga 36 produkter förblir "not_reviewed".
# `synlig_sarskild_preliminar_prototyp` innebär INTE publik UI-aktivering.
# `godkand_publik_10_15_20` innebär att leverantorId ÄR publikt aktiverat i
# Neptunes stodjerOptimateScenarioPubliktAktiverad-grind — men avgör
# fortfarande inte tariffens `stodjer_besparing`-flagga, som förblir
# oändrad. Samtliga 17 raderna nedan (våg 1, WAVE_1_PRODUCT_IDS, plus våg 2,
# EXAKT Neptune-kodens `WAVE_2_PRODUCT_IDS` i optimateScenario.ts) är nu
# `godkand_publik_10_15_20` efter signal 2026-09-30-002 — de 15 våg
# 2-produkterna gick från `godkand_intern_pilot_ej_publik` (intern
# beräkningspilot, handoff 2026-09-29-001 §C.3) till publikt aktiverade,
# precis som våg 1 tidigare.
SCENARIO_STATUS_REGISTRY: dict[str, str] = {
    "stockholm-exergi": "synlig_sarskild_preliminar_prototyp",
    "sundsvall-energi-indal-liden-och-lucksta": "godkand_publik_10_15_20",
    "gotlands-energi-gotland-taxa-17-under-50-mwh-ar": "godkand_publik_10_15_20",
    "boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad": "godkand_publik_10_15_20",
    "c4-energi-kristianstad": "godkand_publik_10_15_20",
    "gavle-energi-gavle": "godkand_publik_10_15_20",
    "halmstads-energi-och-miljo": "godkand_publik_10_15_20",
    "harnosand-energi-miljo-harnosand": "godkand_publik_10_15_20",
    "karlstads-energi-karlstad": "godkand_publik_10_15_20",
    "kils-energi-kil": "godkand_publik_10_15_20",
    "oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024": "godkand_publik_10_15_20",
    "ovik-energi-ornskoldsvik": "godkand_publik_10_15_20",
    "sandviken-energi-sandviken-normal": "godkand_publik_10_15_20",
    "skovde-energi-skovde": "godkand_publik_10_15_20",
    "soderhamn-nara-soderhamn-taxa-11-och-12": "godkand_publik_10_15_20",
    "tekniska-verken-katrineholm-katrineholm": "godkand_publik_10_15_20",
    "temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus": "godkand_publik_10_15_20",
    "trollhattan-energi-trollhattan": "godkand_publik_10_15_20",
    # Våg 3a ("flödes-/temperaturled", publik 10/15/20-aktivering, signal
    # 2026-10-03-003/004): exakt de 17 produkter vars `adjustment_types`
    # innehåller `supply_temperature_adjusted_flow` — se WAVE_3A_PRODUCT_IDS
    # nedan, som binder denna delmängd mot snapshoten, och Neptune-kodens
    # EXAKT samma 17 ID:n i SCENARIO_PUBLIKT_AKTIVERADE_ID/
    # WAVE_3A_PRODUCT_IDS (optimateScenario.ts). `godkand_publik_10_15_20`
    # betyder HÄR, precis som för tidigare våg 1/2-rader, att BÅDE
    # `stodjerOptimateScenario` OCH `stodjerOptimateScenarioPubliktAktiverad`
    # är sanna — Neptunes kalkylator visar nu 10/15/20-scenariot för dessa
    # 17 leverantorId.
    "e-on-jarfalla-jarfalla-och-upplands-bro-bostader": "godkand_publik_10_15_20",
    "e-on-jarfalla-jarfalla-och-upplands-bro-bostader--bas-delvarme": "godkand_publik_10_15_20",
    "e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter": "godkand_publik_10_15_20",
    "e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter--bas-delvarme": "godkand_publik_10_15_20",
    "e-on-malmo-malmo-och-burlov-bostader": "godkand_publik_10_15_20",
    "e-on-malmo-malmo-och-burlov-bostader--bas-delvarme": "godkand_publik_10_15_20",
    "e-on-malmo-malmo-och-burlov-ovriga-fastigheter": "godkand_publik_10_15_20",
    "e-on-malmo-malmo-och-burlov-ovriga-fastigheter--bas-delvarme": "godkand_publik_10_15_20",
    "kraftringen-kraftringen": "godkand_publik_10_15_20",
    "navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader": "godkand_publik_10_15_20",
    "navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader--bas-delvarme": "godkand_publik_10_15_20",
    "navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter": "godkand_publik_10_15_20",
    "navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter--bas-delvarme": "godkand_publik_10_15_20",
    "navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader": "godkand_publik_10_15_20",
    "navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader--bas-delvarme": "godkand_publik_10_15_20",
    "navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter": "godkand_publik_10_15_20",
    "navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter--bas-delvarme": "godkand_publik_10_15_20",
    # Våg 3b ("årsvis volymled", handoff 2026-10-05-001,
    # APPROVED_FOR_IMPLEMENTATION: Claude): exakt de 6 produkter vars
    # `adjustment_types` innehåller `volume` (skalär, årsvis flode_m3 × rate,
    # inga månadsseriefält) OCH `cost_path == kontrakt_arskostnad` OCH
    # `capacity_rule == effekt` — se WAVE_3B_PRODUCT_IDS nedan, som binder
    # denna delmängd mot snapshoten via ID (INTE via adjustment_types ensamt,
    # eftersom `volume` förekommer brett i katalogen för produkter utanför
    # denna pilot). IDENTISK med Neptune-kodens WAVE_3B_PRODUCT_IDS i
    # optimateScenario.ts. `godkand_intern_pilot_ej_publik` — INTERN pilot,
    # INTE publikt aktiverad (SCENARIO_PUBLIKT_AKTIVERADE_ID oförändrad vid
    # 34 i Neptune-koden).
    "borlange-energi-borlange": "godkand_intern_pilot_ej_publik",
    "falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo": "godkand_intern_pilot_ej_publik",
    "falu-energi-vatten-falun": "godkand_intern_pilot_ej_publik",
    "habo-energi-habo": "godkand_intern_pilot_ej_publik",
    "mjolby-svartadalen-energi-mjolby": "godkand_intern_pilot_ej_publik",
    "vanerenergi-mariestad-och-toreboda": "godkand_intern_pilot_ej_publik",
}

# Mekanisk, fail-closed lista över exakt Optimate våg 3a-ID:na (handoff
# 2026-10-02-optimate-vag-3a-eon-navirum-kraftringen) — IDENTISK med
# Neptune-kodens WAVE_3A_PRODUCT_IDS i optimateScenario.ts. build_matrix
# kontrollerar att mängden produkter vars `adjustment_types` innehåller
# `supply_temperature_adjusted_flow` i den inlästa snapshoten är EXAKT denna
# lista — ingen framtida katalogändring får tyst lägga till eller ta bort en
# våg 3a-rad utan att detta test faller.
WAVE_3A_PRODUCT_IDS: frozenset[str] = frozenset({
    "e-on-jarfalla-jarfalla-och-upplands-bro-bostader",
    "e-on-jarfalla-jarfalla-och-upplands-bro-bostader--bas-delvarme",
    "e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter",
    "e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter--bas-delvarme",
    "e-on-malmo-malmo-och-burlov-bostader",
    "e-on-malmo-malmo-och-burlov-bostader--bas-delvarme",
    "e-on-malmo-malmo-och-burlov-ovriga-fastigheter",
    "e-on-malmo-malmo-och-burlov-ovriga-fastigheter--bas-delvarme",
    "kraftringen-kraftringen",
    "navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader",
    "navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader--bas-delvarme",
    "navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter",
    "navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter--bas-delvarme",
    "navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader",
    "navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader--bas-delvarme",
    "navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter",
    "navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter--bas-delvarme",
})

# Mekanisk, fail-closed lista över exakt Optimate våg 3b-ID:na (handoff
# 2026-10-05-001, APPROVED_FOR_IMPLEMENTATION: Claude) — IDENTISK med
# Neptune-kodens WAVE_3B_PRODUCT_IDS i optimateScenario.ts. build_matrix
# kontrollerar att samtliga sex har `volume` i `adjustment_types`,
# `cost_path == kontrakt_arskostnad` och `capacity_rule == effekt` i den
# inlästa snapshoten — men (till skillnad från WAVE_3A_PRODUCT_IDS) INTE att
# detta är den EXAKTA mängden rader med `volume`, eftersom `volume` som
# justeringstyp inte är unik för denna pilot i hela katalogen.
WAVE_3B_PRODUCT_IDS: frozenset[str] = frozenset({
    "borlange-energi-borlange",
    "falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo",
    "falu-energi-vatten-falun",
    "habo-energi-habo",
    "mjolby-svartadalen-energi-mjolby",
    "vanerenergi-mariestad-och-toreboda",
})

# Mekanisk, fail-closed lista över exakt våg-1-ID:na (handoff 2026-09-25-007,
# del C.2). build_matrix kontrollerar att mängden produkter med
# review_wave == 1 i den inlästa snapshoten är IDENTISK med denna lista —
# ingen framtida katalogändring får tyst lägga till eller ta bort ett
# våg-1-ID utan att detta test faller.
WAVE_1_PRODUCT_IDS: frozenset[str] = frozenset({
    "sundsvall-energi-indal-liden-och-lucksta",
    "gotlands-energi-gotland-taxa-17-under-50-mwh-ar",
})

# Sluten vokabulär för scenario_review_status. build_matrix avvisar varje
# registervärde som inte finns här, så ett stavfel i registret blir ett fel
# i stället för en ny, tyst tolererad status.
ALLOWED_SCENARIO_REVIEW_STATUSES = frozenset({
    "not_reviewed",
    "synlig_sarskild_preliminar_prototyp",
    "godkand_intern_pilot_ej_publik",
    "godkand_publik_10_15_20",
})


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"Dubblerad JSON-nyckel i tariff-snapshoten: {key!r}.")
        seen.add(key)
        result[key] = value
    return result


def parse_snapshot(text: str) -> tuple[dict[str, Any], dict[str, str]]:
    marker = "export const TARIFFER = "
    if text.count(marker) != 1 or text.count(" as const;") != 1:
        raise ValueError("Förväntade exakt ett genererat TARIFFER-objekt.")
    payload = text.split(marker, 1)[1].split(" as const;", 1)[0]
    tariffs = json.loads(payload, object_pairs_hook=_reject_duplicate_keys)
    if not isinstance(tariffs, dict) or not tariffs:
        raise ValueError("Tariff-snapshoten måste vara ett icke-tomt objekt.")
    generated = re.search(r"export const GENERERAD = '([^']+)';", text)
    origin = re.search(
        r"Källkatalog: sha256=([0-9a-f]{64}) commit=([0-9a-f]{7,40})[ \t]*$",
        text,
        re.MULTILINE,
    )
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
    for registered_id, status in SCENARIO_STATUS_REGISTRY.items():
        if registered_id not in product_ids:
            raise ValueError(
                f"SCENARIO_STATUS_REGISTRY refererar {registered_id!r}, som saknas i snapshoten."
            )
        if status not in ALLOWED_SCENARIO_REVIEW_STATUSES:
            raise ValueError(
                f"Okänt scenario_review_status {status!r} för {registered_id!r} i SCENARIO_STATUS_REGISTRY."
            )
    wave_1_ids = {row["product_id"] for row in rows if row["review_wave"] == 1}
    if wave_1_ids != WAVE_1_PRODUCT_IDS:
        raise ValueError(
            "review_wave==1 i snapshoten matchar inte WAVE_1_PRODUCT_IDS. "
            f"Endast i snapshoten: {sorted(wave_1_ids - WAVE_1_PRODUCT_IDS)}; "
            f"endast i listan: {sorted(WAVE_1_PRODUCT_IDS - wave_1_ids)}."
        )
    wave_3a_ids = {
        row["product_id"] for row in rows
        if "supply_temperature_adjusted_flow" in row["adjustment_types"]
    }
    if wave_3a_ids != WAVE_3A_PRODUCT_IDS:
        raise ValueError(
            "supply_temperature_adjusted_flow-raderna i snapshoten matchar inte "
            "WAVE_3A_PRODUCT_IDS. "
            f"Endast i snapshoten: {sorted(wave_3a_ids - WAVE_3A_PRODUCT_IDS)}; "
            f"endast i listan: {sorted(WAVE_3A_PRODUCT_IDS - wave_3a_ids)}."
        )
    for product_id in WAVE_3A_PRODUCT_IDS:
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_publik_10_15_20":
            raise ValueError(
                f"Våg 3a-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_publik_10_15_20' i SCENARIO_STATUS_REGISTRY."
            )
    rows_by_id = {row["product_id"]: row for row in rows}
    for product_id in WAVE_3B_PRODUCT_IDS:
        row = rows_by_id.get(product_id)
        if row is None:
            raise ValueError(f"WAVE_3B_PRODUCT_IDS refererar {product_id!r}, som saknas i snapshoten.")
        if "volume" not in row["adjustment_types"]:
            raise ValueError(
                f"Våg 3b-produkten {product_id!r} saknar 'volume' i adjustment_types."
            )
        if row["cost_path"] != "kontrakt_arskostnad":
            raise ValueError(
                f"Våg 3b-produkten {product_id!r} har cost_path {row['cost_path']!r}, "
                "förväntat 'kontrakt_arskostnad'."
            )
        if row["capacity_rule"] != "effekt":
            raise ValueError(
                f"Våg 3b-produkten {product_id!r} har capacity_rule {row['capacity_rule']!r}, "
                "förväntat 'effekt'."
            )
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_intern_pilot_ej_publik":
            raise ValueError(
                f"Våg 3b-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_intern_pilot_ej_publik' i SCENARIO_STATUS_REGISTRY."
            )
    counts = {
        "products": len(rows),
        "real_products": sum(not row["synthetic"] for row in rows),
        "synthetic_products": sum(row["synthetic"] for row in rows),
        "existing_savings": sum(row["savings_today"] for row in rows),
        "current_cost_only": sum(row["cost_path"] == "kontrakt_arskostnad" for row in rows),
        "review_waves": {str(k): v for k, v in sorted(Counter(row["review_wave"] for row in rows).items())},
        "scenario_review_status": dict(sorted(Counter(row["scenario_review_status"] for row in rows).items())),
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
        "godkänner inte något nytt besparingsscenario eller någon tariffaktivering** —",
        "aktiveringen sker separat i Neptune-koden; matrisen redovisar bara dess status.",
        "`scenario_review_status=not_reviewed` gäller alla rader utom de två nedan,",
        "tills prisledens före/efter-beroenden har granskats separat. Ingen av",
        "statusarna nedan ändrar tariffens befintliga `stodjer_besparing`-spärr.",
        "",
        "- `scenario_review_status=synlig_sarskild_preliminar_prototyp` (stockholm-exergi):",
        "  10/15/20-scenariot är synligt som en avgränsad, preliminär prototyp — inte en",
        "  godkänd publik besparingsprodukt.",
        "- `scenario_review_status=godkand_publik_10_15_20`",
        "  (34 produkter — våg 1: sundsvall-energi-indal-liden-och-lucksta,",
        "  gotlands-energi-gotland-taxa-17-under-50-mwh-ar, publikt aktiverad signal",
        "  2026-09-25-015; våg 2: samtliga 15 review_wave==2-produkter i Neptune-kodens",
        "  `WAVE_2_PRODUCT_IDS`, publikt aktiverad signal 2026-09-30-002; våg 3a:",
        "  samtliga 17 review_wave==3-produkter vars `adjustment_types` innehåller",
        "  `supply_temperature_adjusted_flow` (E.ON Järfälla/Malmö, Navirum",
        "  Norrköping/Söderköping och Örebro/Kumla/Hallsberg, Kraftringen), exakt",
        "  Neptune-kodens `WAVE_3A_PRODUCT_IDS`, publikt aktiverad signal",
        "  2026-10-03-003/004):",
        "  `stodjerOptimateScenarioPubliktAktiverad` är sann för dessa 34 leverantorId,",
        "  och Neptunes kalkylator visar 10/15/20-scenariot för dem.",
        "",
        f"- Källa: `{matrix['source_file']}`, SHA-256 `{matrix['source_sha256']}`.",
        f"- Genererad tariffdata: {matrix['generated_on']}; källkatalog `{matrix['catalog_commit']}` / SHA-256 `{matrix['catalog_sha256']}`.",
        f"- Produktval: {counts['products']} totalt = {counts['real_products']} verkliga leverantörsprodukter + {counts['synthetic_products']} syntetiskt riksgenomsnitt. Utrullningens måltal är de {counts['real_products']} verkliga produkterna; riksgenomsnittet redovisas separat och ingår inte i måltalet. {counts['existing_savings']} har befintlig besparingsväg och {counts['current_cost_only']} har enbart kontraktsstyrd årskostnad.",
        "- Vågnumret är endast en mekanisk sortering för granskning: 1 utan identifierat effekt-/flödesberoende, 2 effekt, 3 flöde/temperatur/serie, 4 behörighet. Även legacyprodukter kan ligga i våg 2–3 och flera beroenden kan finnas på samma rad.",
        "- `historikfält` avser policyfält märkta rullande, källperiod eller snapshot; det är **inte** ett fullständigt bevis för tariffens historiska prisregler.",
        "- Källreferens, mätupplösning per policyfält, dokumenterade exkluderingar och granskningsstatus finns i JSON-filen. `katalog` betyder källkatalogen ovan, inte en direktlänk till prislistan.",
        "- Scenariostatusfördelning: " + ", ".join(
            f"{status}: {count}" for status, count in counts["scenario_review_status"].items()
        ) + ".",
        "",
        "| Våg | Produkt-ID | Nät/produkt | Befintlig väg | Scenariostatus | Energiregel | Kapacitet | Justeringstyper | Krävda policyfält | Historik/serie/behörighet | Exkluderingar |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
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
            row["scenario_review_status"],
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
