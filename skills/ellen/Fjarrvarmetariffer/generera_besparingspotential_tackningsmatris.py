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
# katalogen. Aktuell disposition av 77 produkter (signal
# APPROVED_FOR_ACTIVATION: Claude, 2026-10-17, våg 3h publikt aktiverad): 60
# `godkand_publik_10_15_20` (våg 1 + WAVE_2/3A/3B/3C/3D/3E/3F/3G/
# 3H_PRODUCT_IDS, inkl. våg 3f: goteborg-energi, partille-energi-partille,
# sodertorns-fjarrvarme-sodertorns-fjarrvarme, våg 3g: lidkoping-energi-
# lidkoping-041-kw, lidkoping-energi-lidkoping-42-kw, och våg 3h:
# gotlands-energi-gotland-taxa-21-over-50-mwh-ar, molndal-energi,
# norrenergi — tre verkliga, icke kontraktsgatade legacyprodukter med
# befintlig `legacy_besparing`-väg — IDENTISK med Neptune-kodens
# WAVE_3F_PRODUCT_IDS/WAVE_3G_PRODUCT_IDS/WAVE_3H_PRODUCT_IDS i
# optimateScenario.ts, vars `stodjerOptimateScenario` och
# `stodjerOptimateScenarioPubliktAktiverad` nu båda är TRUE för samtliga
# åtta), 0 `godkand_intern_pilot_ej_publik`, 1
# `synlig_sarskild_preliminar_prototyp` (Stockholm Exergi) och de
# återstående 16 "not_reviewed".
# `synlig_sarskild_preliminar_prototyp` innebär INTE publik UI-aktivering.
# `godkand_publik_10_15_20` innebär att leverantorId ÄR publikt aktiverat i
# Neptunes stodjerOptimateScenarioPubliktAktiverad-grind — men avgör
# fortfarande inte tariffens `stodjer_besparing`-flagga, som förblir
# oändrad. `godkand_intern_pilot_ej_publik` innebär bara en intern
# beräkningspilot (stodjerOptimateScenario) — ingen publik aktivering.
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
    # Våg 3b ("årsvis volymled", publik 10/15/20-aktivering, signal
    # 2026-10-05-003): exakt de 6 produkter vars
    # `adjustment_types` innehåller `volume` (skalär, årsvis flode_m3 × rate,
    # inga månadsseriefält) OCH `cost_path == kontrakt_arskostnad` OCH
    # `capacity_rule == effekt` — se WAVE_3B_PRODUCT_IDS nedan, som binder
    # denna delmängd mot snapshoten via ID (INTE via adjustment_types ensamt,
    # eftersom `volume` förekommer brett i katalogen för produkter utanför
    # denna pilot). IDENTISK med Neptune-kodens WAVE_3B_PRODUCT_IDS i
    # optimateScenario.ts. `godkand_publik_10_15_20` — publikt aktiverad,
    # precis som våg 1/2/3a (SCENARIO_PUBLIKT_AKTIVERADE_ID nu 40 i
    # Neptune-koden).
    "borlange-energi-borlange": "godkand_publik_10_15_20",
    "falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo": "godkand_publik_10_15_20",
    "falu-energi-vatten-falun": "godkand_publik_10_15_20",
    "habo-energi-habo": "godkand_publik_10_15_20",
    "mjolby-svartadalen-energi-mjolby": "godkand_publik_10_15_20",
    "vanerenergi-mariestad-och-toreboda": "godkand_publik_10_15_20",
    # Våg 3c ("årsvis säsongsviktad volymled", publik 10/15/20-aktivering,
    # signal 2026-10-06-006 — APPROVED_FOR_ACTIVATION: Claude, slutgranskning
    # av handoff 2026-10-06-002/rättningsrundan 2026-10-06-004/005): exakt de
    # 8 produkter vars `adjustment_types` innehåller `volume` med en
    # säsongsbegränsad `months`-delmängd OCH `cost_path == kontrakt_arskostnad`
    # OCH `capacity_rule == effekt` OCH ett genuint tolvmånadersseriefält
    # `flode_m3` (INTE bara en skalär årsvolym som våg 3b) — se
    # WAVE_3C_PRODUCT_IDS nedan, som binder denna delmängd mot snapshoten via
    # ID. IDENTISK med Neptune-kodens WAVE_3C_PRODUCT_IDS i
    # optimateScenario.ts. `godkand_publik_10_15_20` — publikt aktiverad,
    # precis som våg 1/2/3a/3b (SCENARIO_PUBLIKT_AKTIVERADE_ID nu 48 i
    # Neptune-koden). Statusen `godkand_intern_pilot_ej_publik` var den
    # tidigare interna pilotstatusen (APPROVED_FOR_IMPLEMENTATION: Claude,
    # handoff 2026-10-06-002) och kvarstår i ALLOWED_SCENARIO_REVIEW_STATUSES
    # som reserverad vokabulär för en framtida intern pilot, men bärs INTE
    # längre av någon rad i registret.
    "lulea-energi-lulea": "godkand_publik_10_15_20",
    "malarenergi-vasteras-och-hallstahammar-24-lagenheter": "godkand_publik_10_15_20",
    "nevel-gimo-osterbybruk-och-osthammar": "godkand_publik_10_15_20",
    "oresundskraft-angelholm-normal": "godkand_publik_10_15_20",
    "oresundskraft-helsingborg-normal": "godkand_publik_10_15_20",
    "piteenergi-norrfjarden-och-sjulnas": "godkand_publik_10_15_20",
    "piteenergi-pitea-centrala-natet": "godkand_publik_10_15_20",
    "tekniska-verken-linkoping-linkoping": "godkand_publik_10_15_20",
    # Våg 3d ("flödesdifferens", publik 10/15/20-aktivering, signal
    # APPROVED_FOR_ACTIVATION: Claude, 2026-10-07 — handoff 2026-10-07-002,
    # APPROVED_FOR_IMPLEMENTATION: Claude, lade ursprungligen till dem som
    # INTERN pilot ENDAST): exakt de tre Jämtkraft-produkter vars
    # `adjustment_types` innehåller `flow_difference` OCH
    # `cost_path == kontrakt_arskostnad` OCH `capacity_rule == effekt` med
    # fem effektband OCH ett årsupplöst `flode_okt_apr_m3`-fält (ingen
    # månadsserie) — se WAVE_3D_PRODUCT_IDS nedan, som binder denna
    # delmängd mot snapshoten via ID. IDENTISK med Neptune-kodens
    # WAVE_3D_PRODUCT_IDS i optimateScenario.ts. `godkand_publik_10_15_20`
    # — publikt aktiverad, precis som våg 1/2/3a/3b/3c
    # (SCENARIO_PUBLIKT_AKTIVERADE_ID nu 51 i Neptune-koden). Statusen
    # `godkand_intern_pilot_ej_publik` var den tidigare interna
    # pilotstatusen och kvarstår i ALLOWED_SCENARIO_REVIEW_STATUSES som
    # reserverad vokabulär för en framtida intern pilot, men bärs INTE
    # längre av någon rad i registret.
    "jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge": "godkand_publik_10_15_20",
    "jamtkraft-brunflo-och-opevagen": "godkand_publik_10_15_20",
    "jamtkraft-ostersund-froson-as": "godkand_publik_10_15_20",
    # Våg 3e ("asymmetrisk flödesdifferens", publik 10/15/20-aktivering,
    # signal APPROVED_FOR_ACTIVATION: Claude, 2026-10-08 — handoff
    # 2026-10-08-001, APPROVED_FOR_IMPLEMENTATION: Claude, lade ursprungligen
    # till den som INTERN pilot ENDAST): det enda kvarvarande produkt vars
    # `adjustment_types` innehåller `asymmetric_flow_difference` — se
    # WAVE_3E_PRODUCT_IDS nedan, som binder denna delmängd mot snapshoten via
    # ID. IDENTISK med Neptune-kodens WAVE_3E_PRODUCT_IDS i
    # optimateScenario.ts. `godkand_publik_10_15_20` — publikt aktiverad,
    # precis som våg 1/2/3a/3b/3c/3d (SCENARIO_PUBLIKT_AKTIVERADE_ID nu 52 i
    # Neptune-koden). Statusen `godkand_intern_pilot_ej_publik` var den
    # tidigare interna pilotstatusen och kvarstår i
    # ALLOWED_SCENARIO_REVIEW_STATUSES som reserverad vokabulär för en
    # framtida intern pilot, men bärs INTE längre av någon rad i registret.
    "umea-energi-umea-enkel": "godkand_publik_10_15_20",
    # Våg 3f ("temperaturdifferens", publik 10/15/20-aktivering, signal
    # APPROVED_FOR_ACTIVATION: Claude, 2026-10-12 — session 2026-10-11-002,
    # lade ursprungligen till dem som INTERN pilot ENDAST): exakt de 3
    # produkter vars `adjustment_types` innehåller `temperature_difference`
    # — IDENTISK med Neptune-kodens WAVE_3F_PRODUCT_IDS i
    # optimateScenario.ts. `godkand_publik_10_15_20` — publikt aktiverad,
    # precis som våg 1/2/3a/3b/3c/3d/3e (SCENARIO_PUBLIKT_AKTIVERADE_ID nu
    # 55 i Neptune-koden). Statusen `godkand_intern_pilot_ej_publik` var den
    # tidigare interna pilotstatusen och kvarstår i
    # ALLOWED_SCENARIO_REVIEW_STATUSES som reserverad vokabulär för en
    # framtida intern pilot, men bärs INTE längre av någon rad i registret.
    "goteborg-energi": "godkand_publik_10_15_20",
    "partille-energi-partille": "godkand_publik_10_15_20",
    "sodertorns-fjarrvarme-sodertorns-fjarrvarme": "godkand_publik_10_15_20",
    # Våg 3g ("Lidköpings signerade månadsvisa flödesjustering", publik
    # 10/15/20-aktivering, signal APPROVED_FOR_ACTIVATION: Claude,
    # 2026-10-14 — handoff/session 2026-10-12-012, lade ursprungligen till
    # dem som INTERN pilot ENDAST): exakt de 2 produkter vars
    # `adjustment_types` innehåller `signed_monthly_flow_adjustment` —
    # IDENTISK med Neptune-kodens WAVE_3G_PRODUCT_IDS i optimateScenario.ts.
    # `godkand_publik_10_15_20` — publikt aktiverad, precis som våg
    # 1/2/3a/3b/3c/3d/3e/3f (SCENARIO_PUBLIKT_AKTIVERADE_ID nu 57 i
    # Neptune-koden). Statusen `godkand_intern_pilot_ej_publik` var den
    # tidigare interna pilotstatusen och kvarstår i
    # ALLOWED_SCENARIO_REVIEW_STATUSES som reserverad vokabulär för en
    # framtida intern pilot, men bärs INTE längre av någon rad i registret.
    "lidkoping-energi-lidkoping-041-kw": "godkand_publik_10_15_20",
    "lidkoping-energi-lidkoping-42-kw": "godkand_publik_10_15_20",
    # Våg 3h ("verkliga legacyprodukter", publik 10/15/20-aktivering, signal
    # APPROVED_FOR_ACTIVATION: Claude, 2026-10-17 — handoff
    # 2026-10-16-optimate-vag-3h-legacyprodukter lade ursprungligen till dem
    # som INTERN pilot ENDAST): exakt de 3 verkliga, icke kontraktsgatade
    # legacyprodukter (`cost_path == legacy_besparing`, befintligt
    # `legacy_arskostnad`-besparingsstöd) som återstod bland de 19
    # ogranskade — se WAVE_3H_PRODUCT_IDS/WAVE_3H_PRODUCT_PARAMS nedan, som
    # binder dessa mot snapshotens råa pris-/justeringskontrakt. IDENTISK
    # med Neptune-kodens WAVE_3H_PRODUCT_IDS i optimateScenario.ts, som nu
    # lagts till i SCENARIO_PUBLIKT_AKTIVERADE_ID (Neptune-koden 60).
    # `godkand_publik_10_15_20` — publikt aktiverad, precis som våg
    # 1/2/3a/3b/3c/3d/3e/3f/3g. Statusen `godkand_intern_pilot_ej_publik` var
    # den tidigare interna pilotstatusen och kvarstår i
    # ALLOWED_SCENARIO_REVIEW_STATUSES som reserverad vokabulär för en
    # framtida intern pilot, men bärs INTE längre av någon rad i registret.
    "gotlands-energi-gotland-taxa-21-over-50-mwh-ar": "godkand_publik_10_15_20",
    "molndal-energi": "godkand_publik_10_15_20",
    "norrenergi": "godkand_publik_10_15_20",
    # Optimate våg 3i (handoff 2026-10-17-006/007,
    # APPROVED_FOR_IMPLEMENTATION: Claude): exakt 1 kontraktsgatad produkt —
    # telge-nat-telge-foretag-och-bostadsrattsforeningar — den enda
    # återstående, ogranskade, verkliga produkten med kombinationen
    # `low_utilization` + `incremental_return_temperature` (Norrenergi har
    # samma två justeringstyper men är redan granskad och publik via
    # `legacy_arskostnad`, Våg 3h). INTERN pilot ENDAST — IDENTISK med
    # Neptune-kodens WAVE_3I_PRODUCT_IDS i optimateScenario.ts, tillagd i
    # SCENARIO_PILOT_TARIFFER men INTE i SCENARIO_PUBLIKT_AKTIVERADE_ID
    # (Neptune-koden förblir 60 publika).
    "telge-nat-telge-foretag-och-bostadsrattsforeningar": "godkand_intern_pilot_ej_publik",
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

# Mekanisk, fail-closed lista över exakt Optimate våg 3c-ID:na (publik
# aktivering, signal 2026-10-06-006) — IDENTISK med Neptune-kodens
# WAVE_3C_PRODUCT_IDS i optimateScenario.ts. Precis som våg 1/2/3a/3b är
# denna nu bunden till statusen `godkand_publik_10_15_20` — den
# kompletterande Neptune-ändringen lade mekaniskt till hela
# WAVE_3C_PRODUCT_IDS i sin publika aktiveringslista. build_matrix
# kontrollerar att samtliga åtta har `volume` i `adjustment_types`,
# `cost_path == kontrakt_arskostnad`, `capacity_rule == effekt`, ett genuint
# `flode_m3`-seriefält med månadsvis upplösning och status
# `godkand_publik_10_15_20` i den inlästa snapshoten.
WAVE_3C_PRODUCT_IDS: frozenset[str] = frozenset({
    "lulea-energi-lulea",
    "malarenergi-vasteras-och-hallstahammar-24-lagenheter",
    "nevel-gimo-osterbybruk-och-osthammar",
    "oresundskraft-angelholm-normal",
    "oresundskraft-helsingborg-normal",
    "piteenergi-norrfjarden-och-sjulnas",
    "piteenergi-pitea-centrala-natet",
    "tekniska-verken-linkoping-linkoping",
})

# Mekanisk, fail-closed lista över exakt Optimate våg 3d-ID:na (publik
# aktivering, signal APPROVED_FOR_ACTIVATION: Claude, 2026-10-07 — handoff
# 2026-10-07-002, APPROVED_FOR_IMPLEMENTATION: Claude) — IDENTISK med
# Neptune-kodens WAVE_3D_PRODUCT_IDS i optimateScenario.ts. build_matrix
# kontrollerar att samtliga tre har `flow_difference` i adjustment_types,
# cost_path==kontrakt_arskostnad, capacity_rule==effekt, exakt fem
# effektband, series_fields==[] (årsupplöst flode_okt_apr_m3, inte en
# månadsserie) och status godkand_publik_10_15_20 i den inlästa snapshoten.
# Precis som våg 1/2/3a/3b/3c är denna nu publikt aktiverad i Neptunes
# SCENARIO_PUBLIKT_AKTIVERADE_ID.
WAVE_3D_PRODUCT_IDS: frozenset[str] = frozenset({
    "jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge",
    "jamtkraft-brunflo-och-opevagen",
    "jamtkraft-ostersund-froson-as",
})

# Per-ID effekt-/bandnyckelbindning för WAVE_3D_PRODUCT_IDS, direkt ur
# tariffer.generated.ts::policy.kapacitet_bindning/kapacitet_band_bindning
# (granskning 2026-10-07-004, P1: `adjustment_types`-grinden kontrollerade
# tidigare bara medlemskap, inte exakthet, och saknade helt en bindning mot
# produktens egna effekt-/bandnycklar — en extra justeringstyp eller fel
# nyckelpar passerade därför tyst). build_matrix kräver nu exakt dessa två
# nycklar per produkt i required_policy_fields/history_fields nedan.
WAVE_3D_PRODUCT_KEYS: dict[str, dict[str, str]] = {
    "jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge": {
        "effekt": "jamtkraft_are_debiterbar_effekt_kw",
        "band": "jamtkraft_are_vald_niva_id",
    },
    "jamtkraft-brunflo-och-opevagen": {
        "effekt": "jamtkraft_brunflo_debiterbar_effekt_kw",
        "band": "jamtkraft_brunflo_vald_niva_id",
    },
    "jamtkraft-ostersund-froson-as": {
        "effekt": "jamtkraft_ostersund_debiterbar_effekt_kw",
        "band": "jamtkraft_ostersund_vald_niva_id",
    },
}

# Mekanisk, fail-closed lista över exakt Optimate våg 3e-ID:t (publik
# 10/15/20-aktivering, signal APPROVED_FOR_ACTIVATION: Claude, 2026-10-08 —
# handoff 2026-10-08-001, APPROVED_FOR_IMPLEMENTATION: Claude, lade
# ursprungligen till det som INTERN pilot ENDAST) — IDENTISK med
# Neptune-kodens WAVE_3E_PRODUCT_IDS i optimateScenario.ts. build_matrix
# kontrollerar att detta är EXAKT mängden produkter vars `adjustment_types`
# innehåller `asymmetric_flow_difference` (unikt i hela katalogen för denna
# rad), med exakt de fyra krävda policyfälten, exakt ett historikfält (A),
# inget seriefält, sju effektband och status `godkand_publik_10_15_20`.
WAVE_3E_PRODUCT_IDS: frozenset[str] = frozenset({
    "umea-energi-umea-enkel",
})

# Per-ID effekt-/band-/B-nyckelbindning för WAVE_3E_PRODUCT_IDS, direkt ur
# tariffer.generated.ts::policy.kapacitet_bindning/kapacitet_band_bindning/
# kapacitet_multiplikator_bindning — samma mönster som WAVE_3D_PRODUCT_KEYS,
# men med en tredje nyckel (B) eftersom Umeå Energi Enkel även kräver en
# leverantörsberäknad kapacitetsfaktor.
WAVE_3E_PRODUCT_KEYS: dict[str, dict[str, str]] = {
    "umea-energi-umea-enkel": {
        "effekt": "umea_enkel_arseffekt_a_kw",
        "band": "umea_enkel_vald_niva_id",
        "b": "umea_enkel_kapacitetsfaktor_b",
    },
}

# Mekanisk, fail-closed lista över exakt Optimate våg 3f-ID:na (session
# 2026-10-11-002, INTERN PILOT ENDAST, ej publikt aktiverad) — IDENTISK med
# Neptune-kodens WAVE_3F_PRODUCT_IDS i optimateScenario.ts. build_matrix
# kontrollerar att detta är EXAKT mängden produkter vars `adjustment_types`
# innehåller `temperature_difference`, med exakt en justering per produkt,
# säsongsmånaderna okt–apr, satsen/referensen/formeln, avvikelse_c:s råa
# indatafältskontrakt, capacity_rule='effekt' och bandantal 6/7/4
# (Göteborg/Partille/Södertörn), Göteborgs legacy_besparing-backend utan
# kontraktsfält, och Partilles/Södertörns kontrakt_arskostnad-backend med
# exakta policyfält/bindningar och tomma serie-/historikfält.
WAVE_3F_PRODUCT_IDS: frozenset[str] = frozenset({
    "goteborg-energi",
    "partille-energi-partille",
    "sodertorns-fjarrvarme-sodertorns-fjarrvarme",
})

# Per produkt: rate, reference och (för de kontraktsgatade) effekt-/
# bandnyckelbindning, direkt ur tariffer.generated.ts — handoff
# 2026-10-11-002 §"Fail-closed-grindar". Göteborg har ingen policy (legacy,
# inget kontraktsfält) och saknar därför nycklar här.
WAVE_3F_PRODUCT_PARAMS: dict[str, dict[str, Any]] = {
    "goteborg-energi": {
        "rate": 7,
        "reference": "network_monthly_mean",
        "capacity_bands": 6,
        "cost_path": "legacy_besparing",
    },
    "partille-energi-partille": {
        "rate": 7,
        "reference": "network_monthly_mean",
        "capacity_bands": 7,
        "cost_path": "kontrakt_arskostnad",
        "keys": {"effekt": "partille_debiterbar_effekt_kw", "band": "partille_vald_niva_id"},
    },
    "sodertorns-fjarrvarme-sodertorns-fjarrvarme": {
        "rate": 2.2,
        "reference": "previous_winter_network_mean",
        "capacity_bands": 4,
        "cost_path": "kontrakt_arskostnad",
        "keys": {"effekt": "sodertorn_debiterbar_effekt_kw", "band": "sodertorn_vald_niva_id"},
    },
}

WAVE_3F_FORMULA = "energy_MWh * rate * (customer_return_degC - reference_return_degC)"

# avvikelse_c:s råa indatafältskontrakt (Göteborgs `indatafalt`, inte en
# policy.kravda_falt-post) — identiskt för samtliga tre produkter.
WAVE_3F_AVVIKELSE_C_CONTRACT: dict[str, Any] = {
    "enhet": "°C",
    "default": 0,
    "min_varde": -10,
    "max_varde": 10,
    "heltal": False,
}

# Mekanisk, fail-closed lista över exakt Optimate våg 3g-ID:na (handoff/
# session 2026-10-12-012, INTERN PILOT ENDAST, ej publikt aktiverad) —
# IDENTISK med Neptune-kodens WAVE_3G_PRODUCT_IDS i optimateScenario.ts.
# build_matrix kontrollerar att detta är EXAKT mängden produkter vars
# `adjustment_types` innehåller `signed_monthly_flow_adjustment`, med
# faktor_n=5 och exakt de tre fältnycklarna, cost_path='kontrakt_arskostnad',
# capacity_rule='effekt' med exakt 2 band, exakt fem krävda policyfält
# (effekt+band årsvis, tre tolv-månaders number_series manadsvis) och status
# `godkand_intern_pilot_ej_publik` i SCENARIO_STATUS_REGISTRY.
WAVE_3G_PRODUCT_IDS: frozenset[str] = frozenset({
    "lidkoping-energi-lidkoping-041-kw",
    "lidkoping-energi-lidkoping-42-kw",
})

# Per produkt: faktor_n, de tre fältnycklarna (gemensamma för båda) samt
# effekt-/bandnyckelbindning och exakt effektgräns, direkt ur
# tariffer.generated.ts — handoff 2026-10-12-012 §"Bindande
# scenariokontrakt" och §"Fail-closed-grindar".
WAVE_3G_PRODUCT_PARAMS: dict[str, dict[str, Any]] = {
    "lidkoping-energi-lidkoping-041-kw": {
        "faktor_n": 5,
        "capacity_bands": 2,
        "effekt_min": 3,
        "effekt_max": 41,
        "keys": {"effekt": "lidkoping_debiterbar_effekt_kw", "band": "lidkoping_vald_niva_id"},
        "kapacitet_typ": "effekt",
        "kw_faktor": 1.0,
        "min_debiteringsbas": 3,
        "capacity_band_values": [
            {"id": "1", "min": 0, "max": 10, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 1906},
            {"id": "2", "min": 11, "max": 41, "avgift_kr_ar": 3852, "pris_kr_per_enhet_ar": 1521},
        ],
    },
    "lidkoping-energi-lidkoping-42-kw": {
        "faktor_n": 5,
        "capacity_bands": 2,
        "effekt_min": 42,
        "effekt_max": None,
        "keys": {"effekt": "lidkoping_debiterbar_effekt_kw", "band": "lidkoping_vald_niva_id"},
        "kapacitet_typ": "effekt",
        "kw_faktor": 1.0,
        "min_debiteringsbas": 3,
        "capacity_band_values": [
            {"id": "1", "min": 42, "max": 163, "avgift_kr_ar": 11670, "pris_kr_per_enhet_ar": 1317},
            {"id": "2", "min": 164, "max": None, "avgift_kr_ar": 23342, "pris_kr_per_enhet_ar": 1245},
        ],
    },
}

WAVE_3G_SERIES_FIELDS: tuple[str, ...] = (
    "lidkoping_kund_avkylning_c", "lidkoping_kund_volym_m3", "lidkoping_nat_avkylning_c",
)

# Exakt Q/T/Tm-kontrakt per fältnyckel, direkt ur handoff 2026-10-12-012
# §"Bindande scenariokontrakt": Q (volym) är inklusiv noll, T (kundens
# avkylning) har inget dokumenterat min/max, Tm (nätets avkylning) är
# exklusiv noll och kräver attestering. Omgranskning 2026-10-13-001 (P1)
# band detta mekaniskt eftersom Codex kunde mutera alla tre tyst förbi
# build_matrix.
WAVE_3G_SERIES_FIELD_CONTRACT: dict[str, dict[str, Any]] = {
    "lidkoping_kund_volym_m3": {
        "minvarde": 0, "minvarde_exklusiv": False, "maxvarde": None, "krav_attestering": False,
    },
    "lidkoping_kund_avkylning_c": {
        "minvarde": None, "minvarde_exklusiv": False, "maxvarde": None, "krav_attestering": False,
    },
    "lidkoping_nat_avkylning_c": {
        "minvarde": 0, "minvarde_exklusiv": True, "maxvarde": None, "krav_attestering": True,
    },
}

# Den enda tillåtna nyckelmängden i den råa justeringsposten. Omgranskning
# 2026-10-13-001 (P1): tysta extra justeringsparametrar fick tidigare
# passera build_matrix.
WAVE_3G_ADJUSTMENT_KEYS: frozenset[str] = frozenset({
    "type", "faktor_n", "kund_volym_falt", "kund_avkylning_falt", "nat_avkylning_falt",
})

# Mekanisk, fail-closed lista över exakt Optimate våg 3h-ID:na (publik
# 10/15/20-aktivering, signal APPROVED_FOR_ACTIVATION: Claude, 2026-10-17 —
# handoff 2026-10-16-optimate-vag-3h-legacyprodukter lade ursprungligen till
# dem som INTERN pilot ENDAST) — IDENTISK med Neptune-kodens
# WAVE_3H_PRODUCT_IDS i optimateScenario.ts. Till skillnad från tidigare
# vågor delar dessa tre produkter ingen gemensam `adjustment_types`-signatur
# (Gotland: dödband + volymrabatt; Mölndal: årsvis volymled; Norrenergi:
# lågutnyttjande + marginell returtemperatur), så build_matrix binder i
# stället direkt mot denna fasta lista (status godkand_publik_10_15_20 per
# produkt) och kräver separat att INGEN rad i snapshoten längre bär den
# gamla interna pilotstatusen `godkand_intern_pilot_ej_publik` — en
# bindning som ersätter den tidigare statusbaserade härledningen (reserverad
# vokabulär sedan våg 3c/3d/3e/3f/3g, buren av exakt dessa tre fram till
# denna aktivering). Alla tre är icke kontraktsgatade legacyprodukter med
# `cost_path=legacy_besparing`, `savings_today=true`, backend
# `legacy_arskostnad`.
WAVE_3H_PRODUCT_IDS: frozenset[str] = frozenset({
    "gotlands-energi-gotland-taxa-21-over-50-mwh-ar",
    "molndal-energi",
    "norrenergi",
})

# Per produkt: hela det råa pris-/justerings-/indatafältskontraktet, direkt
# ur tariffer.generated.ts — handoff 2026-10-16-optimate-vag-3h-
# legacyprodukter §"Fail-closed-grindar". Dessa tre saknar `policy` (ingen
# `_kraver_kontrakt`-markör) eftersom de är legacyprodukter — därför är
# required_policy_fields/series_fields/history_fields tomma för alla tre,
# precis som Göteborg Energi i WAVE_3F_PRODUCT_PARAMS.
WAVE_3H_PRODUCT_PARAMS: dict[str, dict[str, Any]] = {
    "gotlands-energi-gotland-taxa-21-over-50-mwh-ar": {
        "adjustment_types": ["cooling_deadband", "volume_discount"],
        "capacity_rule": "effekt",
        "capacity_bands": 0,
        "has_capacity_charge": False,
        "manadspriser": [1020] * 12,
        "kapacitet": {
            "typ": "effekt", "enhet": "kW", "kw_faktor": 1.0, "nivaer": [],
            "min_debiteringsbas": None,
        },
        "fast_avgift": {"kr_ar": 0, "periodisering": "days_in_month/days_in_year"},
        "manadsperiodisering": "days_in_month/days_in_year",
        "justeringar": [
            {
                "type": "cooling_deadband", "rate": 10, "unit": "SEK/MWh/degC",
                "months": [1, 2, 3, 4, 5, 9, 10, 11, 12],
                "fee_below_degC": 38, "bonus_above_degC": 48,
                "measurement": "monthly_mean_cooling_delta_temperature",
                "formula": "energy_MWh * 10 * (max(38-cooling_degC,0)-max(cooling_degC-48,0))",
            },
            {
                "type": "volume_discount", "basis": "previous_calendar_year_MWh",
                "unit": "SEK/MWh", "application": "selected_rate_applies_to_all_purchased_energy",
                "source_vat": "inclusive; divided by 1.25",
                "band": [
                    {"min": 0, "max": 249, "sats": 0},
                    {"min": 250, "max": 1249, "sats": 4},
                    {"min": 1250, "max": 2500, "sats": 8},
                    {"min": 2500, "max": None, "sats": 12},
                ],
            },
        ],
        "indatafalt": {
            "avkylning_c": {
                "enhet": "°C", "default": 43, "min_varde": 20, "max_varde": 70,
                "ar_gissning": False, "heltal": False,
            },
            "foregaende_ars_mwh": {
                "enhet": "MWh", "default": None, "min_varde": 0, "max_varde": 100000,
                "ar_gissning": True, "heltal": False,
            },
        },
    },
    "molndal-energi": {
        "adjustment_types": ["volume"],
        "capacity_rule": "effekt",
        "capacity_bands": 14,
        "has_capacity_charge": True,
        "manadspriser": [484, 484, 356, 215.5, 152, 152, 152, 152, 152, 215.5, 356, 484],
        "kapacitet": {
            "typ": "effekt", "enhet": "kWh/dygn", "kw_faktor": 24.0,
            "nivaer": [
                {"id": "1", "min": 0, "max": 299, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 83.4},
                {"id": "2", "min": 300, "max": 600, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 77.03999999999999},
                {"id": "3", "min": 601, "max": 1200, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 72.84},
                {"id": "4", "min": 1201, "max": 2400, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 65.03999999999999},
                {"id": "5", "min": 2401, "max": 4800, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 63.599999999999994},
                {"id": "6", "min": 4801, "max": 7200, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 62.16},
                {"id": "7", "min": 7201, "max": 9600, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 60.72},
                {"id": "8", "min": 9601, "max": 12000, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 58.67999999999999},
                {"id": "9", "min": 12001, "max": 14400, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 57.12},
                {"id": "10", "min": 14401, "max": 16800, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 55.199999999999996},
                {"id": "11", "min": 16801, "max": 19200, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 53.519999999999996},
                {"id": "12", "min": 19201, "max": 21600, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 51.72},
                {"id": "13", "min": 21601, "max": 24000, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 50.16},
                {"id": "14", "min": 24001, "max": None, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 48.12},
            ],
            "min_debiteringsbas": None,
        },
        "fast_avgift": None,
        "manadsperiodisering": "monthly_rate_no_annual_proration",
        "justeringar": [
            {"type": "volume", "rate": 4.31, "unit": "SEK/m3", "months": list(range(1, 13))},
        ],
        "indatafalt": {
            "flode_m3": {
                "enhet": "m³/år", "default": None, "min_varde": 0, "max_varde": 1000000,
                "ar_gissning": True, "heltal": False,
            },
            "hogsta_dygnsenergi_kwh": {
                "enhet": "kWh/dygn", "default": None, "min_varde": 0, "max_varde": 1000000,
                "ar_gissning": True, "heltal": True,
            },
        },
    },
    "norrenergi": {
        "adjustment_types": ["incremental_return_temperature", "low_utilization"],
        "capacity_rule": "effekt",
        "capacity_bands": 7,
        "has_capacity_charge": True,
        "manadspriser": [694.75, 694.75, 557, 557, 334, 334, 334, 334, 334, 557, 557, 694.75],
        "kapacitet": {
            "typ": "effekt", "enhet": "kW", "kw_faktor": 1.0,
            "nivaer": [
                {"id": "1", "min": 10, "max": 50, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 1185},
                {"id": "2", "min": 51, "max": 300, "avgift_kr_ar": 2849, "pris_kr_per_enhet_ar": 1128},
                {"id": "3", "min": 301, "max": 600, "avgift_kr_ar": 48055, "pris_kr_per_enhet_ar": 979},
                {"id": "4", "min": 601, "max": 1000, "avgift_kr_ar": 62653, "pris_kr_per_enhet_ar": 954},
                {"id": "5", "min": 1001, "max": 2000, "avgift_kr_ar": 94518, "pris_kr_per_enhet_ar": 923},
                {"id": "6", "min": 2001, "max": 5000, "avgift_kr_ar": 197955, "pris_kr_per_enhet_ar": 871},
                {"id": "7", "min": 5001, "max": None, "avgift_kr_ar": 301358, "pris_kr_per_enhet_ar": 819},
            ],
            "min_debiteringsbas": None,
        },
        "fast_avgift": None,
        "manadsperiodisering": "days_in_month/days_in_year",
        "justeringar": [
            {
                "type": "low_utilization", "threshold_hours": 2100, "rate": 0.38,
                "unit": "SEK/kW/hour",
                "formula": "max(0, 2100-utilization_hours) * billing_kW * 0.38",
                "utilization_basis": "normal_year_corrected_energy_June_May_kWh / billing_kW",
            },
            {
                "type": "incremental_return_temperature", "months": [1, 2, 3, 4, 10, 11, 12],
                "thresholds_degC": [30, 60], "rates": [3.4, 26.5], "unit": "SEK/MWh/degC",
                "temperature_weighting": "flow_weighted_monthly",
            },
        ],
        "indatafalt": {
            "normalarskorrigerad_energi_mwh": {
                "enhet": "MWh", "default": None, "min_varde": 0, "max_varde": 100000,
                "ar_gissning": False, "heltal": False,
            },
            "returtemperatur_c": {
                "enhet": "°C", "default": 30, "min_varde": 20, "max_varde": 90,
                "ar_gissning": False, "heltal": False,
            },
        },
    },
}

# Mekanisk, fail-closed lista över exakt Optimate våg 3i-ID:na (handoff
# 2026-10-17-006/007, APPROVED_FOR_IMPLEMENTATION: Claude, INTERN PILOT
# ENDAST) — IDENTISK med Neptune-kodens WAVE_3I_PRODUCT_IDS i
# optimateScenario.ts: telge-nat-telge-foretag-och-bostadsrattsforeningar,
# den enda återstående, ogranskade, verkliga kontraktsgatade produkten med
# kombinationen `low_utilization` + `incremental_return_temperature`.
# Precis som WAVE_3B_PRODUCT_IDS (och till skillnad från WAVE_3A/3G, vars
# justeringstyp råkar vara unik i hela katalogen) binder build_matrix
# Telge direkt mot denna fasta lista i stället för ett generiskt
# `adjustment_types`-filter, eftersom kombinationen low_utilization +
# incremental_return_temperature INTE är unik för denna pilot — Norrenergi
# (Våg 3h) bär samma två justeringstyper men är redan granskad och publik
# via backend 'legacy_arskostnad'.
WAVE_3I_PRODUCT_IDS: frozenset[str] = frozenset({
    "telge-nat-telge-foretag-och-bostadsrattsforeningar",
})

# Telges fulla råa pris-/justerings-/policykontrakt, direkt ur
# tariffer.generated.ts — handoff 2026-10-17-006/007 §"Fail-closed-grindar".
# Till skillnad från Norrenergi (Våg 3h, legacyprodukt utan policy) ÄR
# Telge kontraktsgatad (`_kraver_kontrakt=true`), så required_policy_fields
# binds här mot policy.kravda_falt i stället för att vara tomma.
WAVE_3I_PRODUCT_PARAMS: dict[str, dict[str, Any]] = {
    "telge-nat-telge-foretag-och-bostadsrattsforeningar": {
        "adjustment_types": ["incremental_return_temperature", "low_utilization"],
        "capacity_rule": "effekt",
        "capacity_bands": 3,
        "has_capacity_charge": True,
        "manadspriser": [584, 584, 584, 442, 294, 294, 294, 294, 294, 442, 442, 584],
        "kapacitet": {
            "typ": "effekt", "enhet": "kW", "kw_faktor": 1.0,
            "nivaer": [
                {"id": "1", "min": 0, "max": 299, "avgift_kr_ar": 0, "pris_kr_per_enhet_ar": 1661},
                {"id": "2", "min": 300, "max": 999, "avgift_kr_ar": 41725, "pris_kr_per_enhet_ar": 1529},
                {"id": "3", "min": 1000, "max": None, "avgift_kr_ar": 143238, "pris_kr_per_enhet_ar": 1426},
            ],
            "min_debiteringsbas": None,
        },
        "fast_avgift": None,
        "manadsperiodisering": "days_in_month/days_in_year",
        "justeringar": [
            {
                "type": "low_utilization", "threshold_hours": 2300, "rate": 0.31,
                "unit": "SEK/kW/hour",
                "formula": "max(0, 2300-utilization_hours) * billing_kW * 0.31",
                "rate_period": "year",
                "utilization_basis":
                    "normal_year_corrected_energy_previous_July_June_divided_by_billing_capacity",
                "monthly_proration": "days_in_month/days_in_year",
            },
            {
                "type": "incremental_return_temperature", "months": [1, 2, 3, 4, 10, 11, 12],
                "thresholds_degC": [30, 60], "rates": [2.4, 28], "unit": "SEK/MWh/degC",
                "temperature_weighting": "flow_weighted",
                "formula":
                    "energy_MWh * (2.4 * min(max(return_degC-30, 0), 30) + 28 * max(return_degC-60, 0))",
            },
        ],
        # Fulla, ordnade, råa indatafalt-objekten (samtliga egenskaper,
        # inklusive nyckel/etikett/hjalptext) — omgranskning 2026-10-17-009
        # (P1, Codex): den tidigare dict-by-key-formen jämförde bara en
        # delmängd av egenskaperna, så en extra eller ändrad odokumenterad
        # rå egenskap kunde passera. Jämförs nu som en hel, ordnad lista
        # mot raw_price["indatafalt"] via _strict_numeric_equal.
        "indatafalt": [
            {
                "nyckel": "normalarskorrigerad_energi_mwh",
                "etikett": "Normalårskorrigerad energi juni–maj",
                "enhet": "MWh", "default": None, "min_varde": 0, "max_varde": 100000,
                "hjalptext": "Begärs från leverantören.", "ar_gissning": False, "heltal": False,
            },
            {
                "nyckel": "returtemperatur_c", "etikett": "Returtemperatur", "enhet": "°C",
                "default": 30, "min_varde": 20, "max_varde": 90,
                "hjalptext": (
                    "Flödesviktat månadsmedel, angett som ett enda årsvärde — approximation "
                    "om returtemperaturen varierar mycket mellan säsonger."
                ),
                "ar_gissning": False, "heltal": False,
            },
        ],
        # Fulla, ordnade, råa kravda_falt-objekten (samtliga fyra fält,
        # samtliga egenskaper) — omgranskning 2026-10-17-009 (P1, Codex):
        # den tidigare koden plockade bara ut effekt_field/band_field och
        # kontrollerade var och en mot ett fåtal enskilda egenskaper
        # (heltal/minvarde/maxvarde respektive vardetyp), och validerade
        # normalarskorrigerad_energi_mwh/returtemperatur_c INTE alls.
        # Jämförs nu som en hel, ordnad lista mot
        # raw_price["policy"]["kravda_falt"] via _strict_numeric_equal, så
        # ordning, saknade/extra fält och varje enskild rå egenskap binds.
        "kravda_falt": [
            {
                "nyckel": "telge_debiterbar_effekt_kw", "enhet": "kW", "kravs_for": ["annual"],
                "tillatna_kallor": ["supplier_value"], "matupplosning": "arsvis",
                "kalperiod_definition": "", "tillamplighet": "samtliga manader",
                "kalla": (
                    "Telge Näts prisvillkor och 2026-prislista (telge-attachment/telge-terms) — "
                    "effektsignatur vid -11°C, heltalsavrundad (villkorens s.3: \"Den debiterade "
                    "effekten avrundas till närmaste heltal.\")."
                ),
                "rullande": False, "takad_till_snapshot": False, "matchning_mot_manad": False,
                "tillampliga_manader": None, "minvarde": 0, "minvarde_exklusiv": False,
                "maxvarde": None, "heltal": True, "vardetyp": "number", "antal_varden": None,
                "tillatna_varden": None, "varden_etiketter": None, "etikett": "Debiterbar effekt",
                "hjalptext": "Leverantörens effektsignatur, från fakturan.",
                "krav_attestering": False,
            },
            {
                "nyckel": "normalarskorrigerad_energi_mwh", "enhet": "MWh",
                "kravs_for": ["annual"], "tillatna_kallor": ["supplier_value"],
                "matupplosning": "arsvis", "kalperiod_definition": "",
                "tillamplighet": "samtliga manader",
                "kalla": "Telge Näts prisvillkor (telge-terms) — nyttjandetidstillägg.",
                "rullande": False, "takad_till_snapshot": False, "matchning_mot_manad": False,
                "tillampliga_manader": None, "minvarde": 0, "minvarde_exklusiv": False,
                "maxvarde": 100000, "heltal": False, "vardetyp": "number", "antal_varden": None,
                "tillatna_varden": None, "varden_etiketter": None,
                "etikett": "Normalårskorrigerad energi juni–maj",
                "hjalptext": "Begärs från leverantören.", "krav_attestering": False,
            },
            {
                "nyckel": "returtemperatur_c", "enhet": "°C", "kravs_for": ["annual"],
                "tillatna_kallor": ["supplier_value"], "matupplosning": "arsvis",
                "kalperiod_definition": "", "tillamplighet": "samtliga manader",
                "kalla": "Telge Näts prisvillkor (telge-terms) — stegvis returtemperaturavgift.",
                "rullande": False, "takad_till_snapshot": False, "matchning_mot_manad": False,
                "tillampliga_manader": None, "minvarde": 20, "minvarde_exklusiv": False,
                "maxvarde": 90, "heltal": False, "vardetyp": "number", "antal_varden": None,
                "tillatna_varden": None, "varden_etiketter": None, "etikett": "Returtemperatur",
                "hjalptext": "Flödesviktat månadsmedel, från fakturan.",
                "krav_attestering": False,
            },
            {
                "nyckel": "telge_vald_niva_id", "enhet": "", "kravs_for": ["annual"],
                "tillatna_kallor": ["supplier_value"], "matupplosning": "arsvis",
                "kalperiod_definition": "", "tillamplighet": "samtliga manader",
                "kalla": (
                    "Telge Näts prisvillkor och 2026-prislista — bekräftat effektband."
                ),
                "rullande": False, "takad_till_snapshot": False, "matchning_mot_manad": False,
                "tillampliga_manader": None, "minvarde": None, "minvarde_exklusiv": False,
                "maxvarde": None, "heltal": False, "vardetyp": "band_id", "antal_varden": None,
                "tillatna_varden": None, "varden_etiketter": None, "etikett": "Effektband",
                "hjalptext": "Leverantörens bekräftade effektband.", "krav_attestering": False,
            },
        ],
        "keys": {"effekt": "telge_debiterbar_effekt_kw", "band": "telge_vald_niva_id"},
        "kapacitet_bindning": "telge_debiterbar_effekt_kw",
        "kapacitet_band_bindning": "telge_vald_niva_id",
    },
}

# Umeå Energi Enkels asymmetriska flödesdifferens-justeringsparametrar,
# direkt ur den checkade-in tariffer.generated.ts — handoff 2026-10-08-001
# §"Bindande scenariokontrakt". build_matrix binder dessa EXAKT mot den
# råa katalograden (inte bara mot adjustment_types), så en framtida
# katalogändring av satserna/referensen/säsongsmånaderna faller här.
WAVE_3E_ADJUSTMENT_PARAMS: dict[str, Any] = {
    "reference_m3_per_MWh": 17,
    "bonus_rate": 3,
    "fee_rate": 7,
    "months": [1, 2, 3, 4, 10, 11, 12],
}

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


# Omgranskning 2026-10-14-001 (P1): vanlig Python-likhet gör att
# True == 1 och False == 0, så ett booleskt JSON-värde kan tyst passera
# ett numeriskt Wave 3g-kontrakt (kapacitet.kw_faktor, bandtabellens
# nivåer, Q/T/Tm-seriekontraktet). Denna jämförelse avvisar varje
# bool/tal-korsning i båda riktningarna, rekursivt genom listor och dict.
def _strict_numeric_equal(actual: Any, expected: Any) -> bool:
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(expected, dict) and isinstance(actual, dict):
        return actual.keys() == expected.keys() and all(
            _strict_numeric_equal(actual[key], expected[key]) for key in expected
        )
    if isinstance(expected, list) and isinstance(actual, list):
        return len(actual) == len(expected) and all(
            _strict_numeric_equal(a, e) for a, e in zip(actual, expected)
        )
    return actual == expected


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
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_publik_10_15_20":
            raise ValueError(
                f"Våg 3b-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_publik_10_15_20' i SCENARIO_STATUS_REGISTRY."
            )
    for product_id in WAVE_3C_PRODUCT_IDS:
        row = rows_by_id.get(product_id)
        if row is None:
            raise ValueError(f"WAVE_3C_PRODUCT_IDS refererar {product_id!r}, som saknas i snapshoten.")
        if "volume" not in row["adjustment_types"]:
            raise ValueError(
                f"Våg 3c-produkten {product_id!r} saknar 'volume' i adjustment_types."
            )
        if row["cost_path"] != "kontrakt_arskostnad":
            raise ValueError(
                f"Våg 3c-produkten {product_id!r} har cost_path {row['cost_path']!r}, "
                "förväntat 'kontrakt_arskostnad'."
            )
        if row["capacity_rule"] != "effekt":
            raise ValueError(
                f"Våg 3c-produkten {product_id!r} har capacity_rule {row['capacity_rule']!r}, "
                "förväntat 'effekt'."
            )
        if row["series_fields"] != ["flode_m3"]:
            raise ValueError(
                f"Våg 3c-produkten {product_id!r} har series_fields "
                f"{row['series_fields']!r}, förväntat exakt ['flode_m3']."
            )
        if row["measurement_resolutions"].get("flode_m3") != "manadsvis":
            raise ValueError(
                f"Våg 3c-produkten {product_id!r} har measurement_resolutions.flode_m3 "
                f"{row['measurement_resolutions'].get('flode_m3')!r}, förväntat 'manadsvis'."
            )
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_publik_10_15_20":
            raise ValueError(
                f"Våg 3c-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_publik_10_15_20' i SCENARIO_STATUS_REGISTRY."
            )
    for product_id in WAVE_3D_PRODUCT_IDS:
        row = rows_by_id.get(product_id)
        if row is None:
            raise ValueError(f"WAVE_3D_PRODUCT_IDS refererar {product_id!r}, som saknas i snapshoten.")
        if row["adjustment_types"] != ["flow_difference"]:
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} har adjustment_types "
                f"{row['adjustment_types']!r}, förväntat exakt ['flow_difference']."
            )
        keys = WAVE_3D_PRODUCT_KEYS[product_id]
        expected_required_fields = sorted({"flode_okt_apr_m3", keys["effekt"], keys["band"]})
        if row["required_policy_fields"] != expected_required_fields:
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} har required_policy_fields "
                f"{row['required_policy_fields']!r}, förväntat exakt {expected_required_fields!r}."
            )
        if row["history_fields"] != [keys["effekt"]]:
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} har history_fields "
                f"{row['history_fields']!r}, förväntat exakt {[keys['effekt']]!r}."
            )
        if row["cost_path"] != "kontrakt_arskostnad":
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} har cost_path {row['cost_path']!r}, "
                "förväntat 'kontrakt_arskostnad'."
            )
        if row["capacity_rule"] != "effekt":
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} har capacity_rule {row['capacity_rule']!r}, "
                "förväntat 'effekt'."
            )
        if row["capacity_bands"] != 5:
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} har {row['capacity_bands']} effektband, "
                "förväntat exakt 5."
            )
        if row["series_fields"] != []:
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} har series_fields "
                f"{row['series_fields']!r}, förväntat exakt []."
            )
        if row["measurement_resolutions"].get("flode_okt_apr_m3") != "arsvis":
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} har measurement_resolutions.flode_okt_apr_m3 "
                f"{row['measurement_resolutions'].get('flode_okt_apr_m3')!r}, förväntat 'arsvis'."
            )
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_publik_10_15_20":
            raise ValueError(
                f"Våg 3d-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_publik_10_15_20' i SCENARIO_STATUS_REGISTRY."
            )
    # Rättning, granskning 2026-10-08-003 (P1): WAVE_3E_PRODUCT_IDS påstods
    # vara exakt hela katalogmängden med asymmetric_flow_difference, men
    # ingen kontroll jämförde den härledda mängden mot listan — en andra
    # katalograd kunde tyst få samma justeringstyp utan att build_matrix
    # föll. Samma mönster som wave_3a_ids ovan.
    wave_3e_ids = {
        row["product_id"] for row in rows
        if "asymmetric_flow_difference" in row["adjustment_types"]
    }
    if wave_3e_ids != WAVE_3E_PRODUCT_IDS:
        raise ValueError(
            "asymmetric_flow_difference-raderna i snapshoten matchar inte "
            "WAVE_3E_PRODUCT_IDS. "
            f"Endast i snapshoten: {sorted(wave_3e_ids - WAVE_3E_PRODUCT_IDS)}; "
            f"endast i listan: {sorted(WAVE_3E_PRODUCT_IDS - wave_3e_ids)}."
        )
    for product_id in WAVE_3E_PRODUCT_IDS:
        row = rows_by_id.get(product_id)
        if row is None:
            raise ValueError(f"WAVE_3E_PRODUCT_IDS refererar {product_id!r}, som saknas i snapshoten.")
        if row["adjustment_types"] != ["asymmetric_flow_difference"]:
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} har adjustment_types "
                f"{row['adjustment_types']!r}, förväntat exakt ['asymmetric_flow_difference']."
            )
        keys = WAVE_3E_PRODUCT_KEYS[product_id]
        expected_required_fields = sorted({"flode_okt_apr_m3", keys["effekt"], keys["band"], keys["b"]})
        if row["required_policy_fields"] != expected_required_fields:
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} har required_policy_fields "
                f"{row['required_policy_fields']!r}, förväntat exakt {expected_required_fields!r}."
            )
        if row["history_fields"] != [keys["effekt"]]:
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} har history_fields "
                f"{row['history_fields']!r}, förväntat exakt {[keys['effekt']]!r}."
            )
        if row["cost_path"] != "kontrakt_arskostnad":
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} har cost_path {row['cost_path']!r}, "
                "förväntat 'kontrakt_arskostnad'."
            )
        if row["capacity_rule"] != "effekt":
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} har capacity_rule {row['capacity_rule']!r}, "
                "förväntat 'effekt'."
            )
        if row["capacity_bands"] != 7:
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} har {row['capacity_bands']} effektband, "
                "förväntat exakt 7."
            )
        if row["series_fields"] != []:
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} har series_fields "
                f"{row['series_fields']!r}, förväntat exakt []."
            )
        for falt in (keys["effekt"], keys["band"], keys["b"], "flode_okt_apr_m3"):
            if row["measurement_resolutions"].get(falt) != "arsvis":
                raise ValueError(
                    f"Våg 3e-produkten {product_id!r} har measurement_resolutions.{falt} "
                    f"{row['measurement_resolutions'].get(falt)!r}, förväntat 'arsvis'."
                )
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_publik_10_15_20":
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_publik_10_15_20' i SCENARIO_STATUS_REGISTRY."
            )
        # Binder även RÅA justeringsparametrarna (inte bara adjustment_types)
        # mot handoff 2026-10-08-001 §"Bindande scenariokontrakt" — en
        # framtida ändring av bonus_rate/fee_rate/referens/säsongsmånader i
        # katalogen ska falla här, inte bara upptäckas i Neptune-testerna.
        raw_price = latest_price(tariffs[product_id])
        raw_adjustments = raw_price.get("justeringar", [])
        if len(raw_adjustments) != 1:
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} har {len(raw_adjustments)} justeringar, "
                "förväntat exakt 1."
            )
        raw_adjustment = raw_adjustments[0]
        for key, expected in WAVE_3E_ADJUSTMENT_PARAMS.items():
            if raw_adjustment.get(key) != expected:
                raise ValueError(
                    f"Våg 3e-produkten {product_id!r} har {key}={raw_adjustment.get(key)!r} "
                    f"i justeringen, förväntat exakt {expected!r}."
                )

        # Rättning, granskning 2026-10-08-003 (P1): required_policy_fields
        # bevisar bara att B FINNS bland kravda_falt, inte att
        # kapacitetsmotorn faktiskt binder till den. Kontrollera därför de
        # tre RÅA policybindningarna direkt, och lås samtidigt B-fältets
        # råa kontrakt (vardetyp/matupplosning/det slutna intervallet
        # [0,93; 1,401]) mot handoff 2026-10-08-001.
        raw_policy = raw_price.get("policy") or {}
        raw_bindings = {
            "kapacitet_bindning": keys["effekt"],
            "kapacitet_band_bindning": keys["band"],
            "kapacitet_multiplikator_bindning": keys["b"],
        }
        for binding_key, expected_nyckel in raw_bindings.items():
            if raw_policy.get(binding_key) != expected_nyckel:
                raise ValueError(
                    f"Våg 3e-produkten {product_id!r} har policy.{binding_key}="
                    f"{raw_policy.get(binding_key)!r}, förväntat exakt {expected_nyckel!r}."
                )
        raw_required_fields = raw_policy.get("kravda_falt") or []
        b_field = next(
            (field for field in raw_required_fields if field.get("nyckel") == keys["b"]),
            None,
        )
        if b_field is None:
            raise ValueError(
                f"Våg 3e-produkten {product_id!r} saknar kravda_falt-posten för {keys['b']!r}."
            )
        expected_b_contract = {
            "vardetyp": "number",
            "matupplosning": "arsvis",
            "minvarde": 0.93,
            "minvarde_exklusiv": False,
            "maxvarde": 1.401,
        }
        for contract_key, expected_value in expected_b_contract.items():
            if b_field.get(contract_key) != expected_value:
                raise ValueError(
                    f"Våg 3e-produkten {product_id!r} har {keys['b']}.{contract_key}="
                    f"{b_field.get(contract_key)!r}, förväntat exakt {expected_value!r}."
                )
    # Rättning, omgranskning 2026-10-12-001 (P1): skills-sidan godkände
    # tidigare våg 3f utan någon matrisgrind alls — de tre ID:na låg bara i
    # SCENARIO_STATUS_REGISTRY, och build_matrix kontrollerade varken den
    # globala temperature_difference-mängden eller det råa
    # justerings-/policykontraktet. Samma mönster som wave_3e_ids ovan,
    # utökat med Göteborgs legacy-indatafalt och Partilles/Södertörns råa
    # policybindningar.
    wave_3f_ids = {
        row["product_id"] for row in rows
        if "temperature_difference" in row["adjustment_types"]
    }
    if wave_3f_ids != WAVE_3F_PRODUCT_IDS:
        raise ValueError(
            "temperature_difference-raderna i snapshoten matchar inte "
            "WAVE_3F_PRODUCT_IDS. "
            f"Endast i snapshoten: {sorted(wave_3f_ids - WAVE_3F_PRODUCT_IDS)}; "
            f"endast i listan: {sorted(WAVE_3F_PRODUCT_IDS - wave_3f_ids)}."
        )
    # Rättning, omgranskning 2026-10-12-003 (P1): loopen nedan itererade bara
    # WAVE_3F_PRODUCT_PARAMS, så om registret tappade en produkt som
    # WAVE_3F_PRODUCT_IDS fortfarande innehöll slutfördes build_matrix utan
    # fel (params_missing FAIL_OPEN). Kräv att mängderna är EXAKT lika innan
    # per-produktkontrollerna körs.
    if set(WAVE_3F_PRODUCT_PARAMS) != WAVE_3F_PRODUCT_IDS:
        raise ValueError(
            "WAVE_3F_PRODUCT_PARAMS matchar inte WAVE_3F_PRODUCT_IDS. "
            f"Endast i WAVE_3F_PRODUCT_PARAMS: {sorted(set(WAVE_3F_PRODUCT_PARAMS) - WAVE_3F_PRODUCT_IDS)}; "
            f"endast i WAVE_3F_PRODUCT_IDS: {sorted(WAVE_3F_PRODUCT_IDS - set(WAVE_3F_PRODUCT_PARAMS))}."
        )
    for product_id, params in WAVE_3F_PRODUCT_PARAMS.items():
        row = rows_by_id.get(product_id)
        if row is None:
            raise ValueError(f"WAVE_3F_PRODUCT_IDS refererar {product_id!r}, som saknas i snapshoten.")
        if row["adjustment_types"] != ["temperature_difference"]:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har adjustment_types "
                f"{row['adjustment_types']!r}, förväntat exakt ['temperature_difference']."
            )
        if row["cost_path"] != params["cost_path"]:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har cost_path {row['cost_path']!r}, "
                f"förväntat {params['cost_path']!r}."
            )
        if row["capacity_rule"] != "effekt":
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har capacity_rule {row['capacity_rule']!r}, "
                "förväntat 'effekt'."
            )
        if row["capacity_bands"] != params["capacity_bands"]:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har {row['capacity_bands']} effektband, "
                f"förväntat exakt {params['capacity_bands']}."
            )
        if row["series_fields"] != []:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har series_fields "
                f"{row['series_fields']!r}, förväntat exakt []."
            )
        if row["history_fields"] != []:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har history_fields "
                f"{row['history_fields']!r}, förväntat exakt []."
            )
        if row["has_eligibility_rule"]:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har ett behörighetsvillkor, förväntat inget."
            )
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_publik_10_15_20":
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_publik_10_15_20' i SCENARIO_STATUS_REGISTRY."
            )

        raw_price = latest_price(tariffs[product_id])
        raw_adjustments = raw_price.get("justeringar", [])
        if len(raw_adjustments) != 1:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har {len(raw_adjustments)} justeringar, "
                "förväntat exakt 1."
            )
        raw_adjustment = raw_adjustments[0]
        if raw_adjustment.get("months") != [1, 2, 3, 4, 10, 11, 12]:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har months {raw_adjustment.get('months')!r}, "
                "förväntat exakt [1, 2, 3, 4, 10, 11, 12]."
            )
        if raw_adjustment.get("rate") != params["rate"]:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har rate {raw_adjustment.get('rate')!r}, "
                f"förväntat exakt {params['rate']!r}."
            )
        if raw_adjustment.get("reference") != params["reference"]:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har reference {raw_adjustment.get('reference')!r}, "
                f"förväntat exakt {params['reference']!r}."
            )
        if raw_adjustment.get("formula") != WAVE_3F_FORMULA:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har formula {raw_adjustment.get('formula')!r}, "
                f"förväntat exakt {WAVE_3F_FORMULA!r}."
            )

        raw_indatafalt = raw_price.get("indatafalt") or []
        avvikelse_falt = next(
            (field for field in raw_indatafalt if field.get("nyckel") == "avvikelse_c"), None
        )
        if avvikelse_falt is None:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} saknar indatafalt-posten för 'avvikelse_c'."
            )
        for contract_key, expected_value in WAVE_3F_AVVIKELSE_C_CONTRACT.items():
            if avvikelse_falt.get(contract_key) != expected_value:
                raise ValueError(
                    f"Våg 3f-produkten {product_id!r} har avvikelse_c.{contract_key}="
                    f"{avvikelse_falt.get(contract_key)!r}, förväntat exakt {expected_value!r}."
                )

        if "keys" not in params:
            if raw_price.get("policy") is not None:
                raise ValueError(
                    f"Våg 3f-produkten {product_id!r} förväntas sakna policy, men har en."
                )
            continue

        keys = params["keys"]
        expected_required_fields = sorted({"avvikelse_c", keys["effekt"], keys["band"]})
        if row["required_policy_fields"] != expected_required_fields:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har required_policy_fields "
                f"{row['required_policy_fields']!r}, förväntat exakt {expected_required_fields!r}."
            )
        for falt in (keys["effekt"], keys["band"], "avvikelse_c"):
            if row["measurement_resolutions"].get(falt) != "arsvis":
                raise ValueError(
                    f"Våg 3f-produkten {product_id!r} har measurement_resolutions.{falt} "
                    f"{row['measurement_resolutions'].get(falt)!r}, förväntat 'arsvis'."
                )
        raw_policy = raw_price.get("policy") or {}
        raw_bindings = {
            "kapacitet_bindning": keys["effekt"],
            "kapacitet_band_bindning": keys["band"],
        }
        for binding_key, expected_nyckel in raw_bindings.items():
            if raw_policy.get(binding_key) != expected_nyckel:
                raise ValueError(
                    f"Våg 3f-produkten {product_id!r} har policy.{binding_key}="
                    f"{raw_policy.get(binding_key)!r}, förväntat exakt {expected_nyckel!r}."
                )
        if raw_policy.get("kapacitet_multiplikator_bindning") is not None:
            raise ValueError(
                f"Våg 3f-produkten {product_id!r} har "
                f"policy.kapacitet_multiplikator_bindning={raw_policy.get('kapacitet_multiplikator_bindning')!r}, "
                "förväntat None."
            )

    # Våg 3g ("Lidköpings signerade månadsvisa flödesjustering", handoff/
    # session 2026-10-12-012, INTERN PILOT ENDAST): samma mönster som
    # wave_3e_ids/wave_3f_ids ovan — bevisar att WAVE_3G_PRODUCT_IDS är
    # EXAKT mängden katalograder med signed_monthly_flow_adjustment, inte
    # bara en delmängd.
    wave_3g_ids = {
        row["product_id"] for row in rows
        if "signed_monthly_flow_adjustment" in row["adjustment_types"]
    }
    if wave_3g_ids != WAVE_3G_PRODUCT_IDS:
        raise ValueError(
            "signed_monthly_flow_adjustment-raderna i snapshoten matchar inte "
            "WAVE_3G_PRODUCT_IDS. "
            f"Endast i snapshoten: {sorted(wave_3g_ids - WAVE_3G_PRODUCT_IDS)}; "
            f"endast i listan: {sorted(WAVE_3G_PRODUCT_IDS - wave_3g_ids)}."
        )
    if set(WAVE_3G_PRODUCT_PARAMS) != WAVE_3G_PRODUCT_IDS:
        raise ValueError(
            "WAVE_3G_PRODUCT_PARAMS matchar inte WAVE_3G_PRODUCT_IDS. "
            f"Endast i WAVE_3G_PRODUCT_PARAMS: {sorted(set(WAVE_3G_PRODUCT_PARAMS) - WAVE_3G_PRODUCT_IDS)}; "
            f"endast i WAVE_3G_PRODUCT_IDS: {sorted(WAVE_3G_PRODUCT_IDS - set(WAVE_3G_PRODUCT_PARAMS))}."
        )
    for product_id, params in WAVE_3G_PRODUCT_PARAMS.items():
        row = rows_by_id.get(product_id)
        if row is None:
            raise ValueError(f"WAVE_3G_PRODUCT_IDS refererar {product_id!r}, som saknas i snapshoten.")
        if row["adjustment_types"] != ["signed_monthly_flow_adjustment"]:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har adjustment_types "
                f"{row['adjustment_types']!r}, förväntat exakt ['signed_monthly_flow_adjustment']."
            )
        if row["cost_path"] != "kontrakt_arskostnad":
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har cost_path {row['cost_path']!r}, "
                "förväntat 'kontrakt_arskostnad'."
            )
        if row["capacity_rule"] != "effekt":
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har capacity_rule {row['capacity_rule']!r}, "
                "förväntat 'effekt'."
            )
        if row["capacity_bands"] != params["capacity_bands"]:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har {row['capacity_bands']} effektband, "
                f"förväntat exakt {params['capacity_bands']}."
            )
        raw_capacity = latest_price(tariffs[product_id]).get("kapacitet") or {}
        if raw_capacity.get("typ") != params["kapacitet_typ"]:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har kapacitet.typ={raw_capacity.get('typ')!r}, "
                f"förväntat exakt {params['kapacitet_typ']!r}."
            )
        if not _strict_numeric_equal(raw_capacity.get("kw_faktor"), params["kw_faktor"]):
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har kapacitet.kw_faktor="
                f"{raw_capacity.get('kw_faktor')!r}, förväntat exakt {params['kw_faktor']!r}."
            )
        if not _strict_numeric_equal(raw_capacity.get("min_debiteringsbas"), params["min_debiteringsbas"]):
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har kapacitet.min_debiteringsbas="
                f"{raw_capacity.get('min_debiteringsbas')!r}, förväntat exakt "
                f"{params['min_debiteringsbas']!r}."
            )
        if not _strict_numeric_equal(raw_capacity.get("nivaer") or [], params["capacity_band_values"]):
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har kapacitet.nivaer="
                f"{raw_capacity.get('nivaer')!r}, förväntat exakt "
                f"{params['capacity_band_values']!r}."
            )
        keys = params["keys"]
        expected_required_fields = sorted({keys["effekt"], keys["band"], *WAVE_3G_SERIES_FIELDS})
        if row["required_policy_fields"] != expected_required_fields:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har required_policy_fields "
                f"{row['required_policy_fields']!r}, förväntat exakt {expected_required_fields!r}."
            )
        if row["series_fields"] != sorted(WAVE_3G_SERIES_FIELDS):
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har series_fields "
                f"{row['series_fields']!r}, förväntat exakt {sorted(WAVE_3G_SERIES_FIELDS)!r}."
            )
        if row["history_fields"] != sorted(WAVE_3G_SERIES_FIELDS):
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har history_fields "
                f"{row['history_fields']!r}, förväntat exakt {sorted(WAVE_3G_SERIES_FIELDS)!r}."
            )
        if row["has_eligibility_rule"]:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har ett behörighetsvillkor, förväntat inget."
            )
        for falt in (keys["effekt"], keys["band"]):
            if row["measurement_resolutions"].get(falt) != "arsvis":
                raise ValueError(
                    f"Våg 3g-produkten {product_id!r} har measurement_resolutions.{falt} "
                    f"{row['measurement_resolutions'].get(falt)!r}, förväntat 'arsvis'."
                )
        for falt in WAVE_3G_SERIES_FIELDS:
            if row["measurement_resolutions"].get(falt) != "manadsvis":
                raise ValueError(
                    f"Våg 3g-produkten {product_id!r} har measurement_resolutions.{falt} "
                    f"{row['measurement_resolutions'].get(falt)!r}, förväntat 'manadsvis'."
                )
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_publik_10_15_20":
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_publik_10_15_20' i SCENARIO_STATUS_REGISTRY."
            )

        raw_price = latest_price(tariffs[product_id])
        raw_adjustments = raw_price.get("justeringar", [])
        if len(raw_adjustments) != 1:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har {len(raw_adjustments)} justeringar, "
                "förväntat exakt 1."
            )
        raw_adjustment = raw_adjustments[0]
        if raw_adjustment.get("faktor_n") != params["faktor_n"]:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har faktor_n {raw_adjustment.get('faktor_n')!r}, "
                f"förväntat exakt {params['faktor_n']!r}."
            )
        expected_field_keys = {
            "kund_volym_falt": "lidkoping_kund_volym_m3",
            "kund_avkylning_falt": "lidkoping_kund_avkylning_c",
            "nat_avkylning_falt": "lidkoping_nat_avkylning_c",
        }
        for adjustment_key, expected_nyckel in expected_field_keys.items():
            if raw_adjustment.get(adjustment_key) != expected_nyckel:
                raise ValueError(
                    f"Våg 3g-produkten {product_id!r} har {adjustment_key}="
                    f"{raw_adjustment.get(adjustment_key)!r} i justeringen, förväntat exakt "
                    f"{expected_nyckel!r}."
                )
        if set(raw_adjustment) != WAVE_3G_ADJUSTMENT_KEYS:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har justeringsnycklar "
                f"{sorted(raw_adjustment)!r}, förväntat exakt "
                f"{sorted(WAVE_3G_ADJUSTMENT_KEYS)!r}."
            )

        raw_policy = raw_price.get("policy") or {}
        if raw_policy.get("stodjer_aktuell_arskostnad") is not True:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har policy.stodjer_aktuell_arskostnad="
                f"{raw_policy.get('stodjer_aktuell_arskostnad')!r}, förväntat exakt True."
            )
        if raw_policy.get("stodjer_besparing") is not False:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har policy.stodjer_besparing="
                f"{raw_policy.get('stodjer_besparing')!r}, förväntat exakt False."
            )
        raw_bindings = {
            "kapacitet_bindning": keys["effekt"],
            "kapacitet_band_bindning": keys["band"],
        }
        for binding_key, expected_nyckel in raw_bindings.items():
            if raw_policy.get(binding_key) != expected_nyckel:
                raise ValueError(
                    f"Våg 3g-produkten {product_id!r} har policy.{binding_key}="
                    f"{raw_policy.get(binding_key)!r}, förväntat exakt {expected_nyckel!r}."
                )
        if raw_policy.get("kapacitet_multiplikator_bindning") is not None:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har "
                f"policy.kapacitet_multiplikator_bindning={raw_policy.get('kapacitet_multiplikator_bindning')!r}, "
                "förväntat None."
            )
        raw_required_fields = raw_policy.get("kravda_falt") or []
        # Omgranskning 2026-10-14-001 (P1): product_row() reducerar
        # kravda_falt till mängder/kartor, så en duplicerad post (två
        # fält med samma nyckel) passerade tidigare tyst. Bind den råa
        # listans längd och nyckelunikhet innan fälten används.
        if len(raw_required_fields) != 5:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har {len(raw_required_fields)} "
                "kravda_falt-poster, förväntat exakt 5."
            )
        raw_required_keys = [field.get("nyckel") for field in raw_required_fields]
        if len(set(raw_required_keys)) != len(raw_required_keys):
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har duplicerade kravda_falt-nycklar "
                f"{raw_required_keys!r}, förväntat exakt fem unika nycklar."
            )
        if set(raw_required_keys) != set(expected_required_fields):
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har kravda_falt-nycklar "
                f"{sorted(raw_required_keys)!r}, förväntat exakt {expected_required_fields!r}."
            )
        effekt_field = next(
            (field for field in raw_required_fields if field.get("nyckel") == keys["effekt"]), None
        )
        if effekt_field is None:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} saknar kravda_falt-posten för {keys['effekt']!r}."
            )
        if effekt_field.get("minvarde") != params["effekt_min"]:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har {keys['effekt']}.minvarde="
                f"{effekt_field.get('minvarde')!r}, förväntat exakt {params['effekt_min']!r}."
            )
        if effekt_field.get("maxvarde") != params["effekt_max"]:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har {keys['effekt']}.maxvarde="
                f"{effekt_field.get('maxvarde')!r}, förväntat exakt {params['effekt_max']!r}."
            )
        if effekt_field.get("vardetyp") != "number":
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har {keys['effekt']}.vardetyp="
                f"{effekt_field.get('vardetyp')!r}, förväntat exakt 'number'."
            )
        band_field = next(
            (field for field in raw_required_fields if field.get("nyckel") == keys["band"]), None
        )
        if band_field is None:
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} saknar kravda_falt-posten för {keys['band']!r}."
            )
        if band_field.get("vardetyp") != "band_id":
            raise ValueError(
                f"Våg 3g-produkten {product_id!r} har {keys['band']}.vardetyp="
                f"{band_field.get('vardetyp')!r}, förväntat exakt 'band_id'."
            )

        # Q/T/Tm: binder exakt antal_varden, rullande och varje fälts
        # dokumenterade min/max/exklusivitet/attestering ur
        # WAVE_3G_SERIES_FIELD_CONTRACT (omgranskning 2026-10-13-001, P1) —
        # tidigare band endast Tm:s minvarde/exklusivitet/attestering.
        for serie_nyckel, contract in WAVE_3G_SERIES_FIELD_CONTRACT.items():
            serie_field = next(
                (field for field in raw_required_fields if field.get("nyckel") == serie_nyckel), None
            )
            if serie_field is None:
                raise ValueError(
                    f"Våg 3g-produkten {product_id!r} saknar kravda_falt-posten för {serie_nyckel!r}."
                )
            if serie_field.get("vardetyp") != "number_series":
                raise ValueError(
                    f"Våg 3g-produkten {product_id!r} har {serie_nyckel}.vardetyp="
                    f"{serie_field.get('vardetyp')!r}, förväntat exakt 'number_series'."
                )
            if not _strict_numeric_equal(serie_field.get("antal_varden"), 12):
                raise ValueError(
                    f"Våg 3g-produkten {product_id!r} har {serie_nyckel}.antal_varden="
                    f"{serie_field.get('antal_varden')!r}, förväntat exakt 12."
                )
            if serie_field.get("rullande") is not True:
                raise ValueError(
                    f"Våg 3g-produkten {product_id!r} har {serie_nyckel}.rullande="
                    f"{serie_field.get('rullande')!r}, förväntat exakt True."
                )
            for contract_key, expected_value in contract.items():
                if not _strict_numeric_equal(serie_field.get(contract_key), expected_value):
                    raise ValueError(
                        f"Våg 3g-produkten {product_id!r} har {serie_nyckel}.{contract_key}="
                        f"{serie_field.get(contract_key)!r}, förväntat exakt {expected_value!r}."
                    )

    # Våg 3h ("verkliga legacyprodukter", publik 10/15/20-aktivering, signal
    # APPROVED_FOR_ACTIVATION: Claude, 2026-10-17): till skillnad från
    # wave_3e_ids/wave_3f_ids/wave_3g_ids ovan delar dessa tre produkter
    # ingen gemensam `adjustment_types`-signatur, så bindningen sker direkt
    # mot den fasta WAVE_3H_PRODUCT_IDS-listan (status per produkt
    # kontrolleras i loopen nedan) i stället för en statusbaserad
    # härledning. Statusen `godkand_intern_pilot_ej_publik` bars tidigare av
    # exakt dessa tre rader; Våg 3h gjorde den tillfälligt obärd av någon
    # rad. Våg 3i (nedan) återinför statusen för exakt Telge — denna
    # kontroll binder därför nu att EXAKT WAVE_3I_PRODUCT_IDS bär statusen,
    # inte att ingen rad gör det, så en framtida våg som tyst lägger till
    # en FJÄRDE intern-pilot-rad utan att uppdatera WAVE_3I_PRODUCT_IDS
    # ändå faller.
    remaining_internal_pilot_ids = {
        row["product_id"] for row in rows
        if row["scenario_review_status"] == "godkand_intern_pilot_ej_publik"
    }
    if remaining_internal_pilot_ids != WAVE_3I_PRODUCT_IDS:
        raise ValueError(
            "godkand_intern_pilot_ej_publik bärs av "
            f"{sorted(remaining_internal_pilot_ids)} i snapshoten, förväntat exakt "
            f"WAVE_3I_PRODUCT_IDS ({sorted(WAVE_3I_PRODUCT_IDS)})."
        )
    if set(WAVE_3H_PRODUCT_PARAMS) != WAVE_3H_PRODUCT_IDS:
        raise ValueError(
            "WAVE_3H_PRODUCT_PARAMS matchar inte WAVE_3H_PRODUCT_IDS. "
            f"Endast i WAVE_3H_PRODUCT_PARAMS: {sorted(set(WAVE_3H_PRODUCT_PARAMS) - WAVE_3H_PRODUCT_IDS)}; "
            f"endast i WAVE_3H_PRODUCT_IDS: {sorted(WAVE_3H_PRODUCT_IDS - set(WAVE_3H_PRODUCT_PARAMS))}."
        )
    for product_id, params in WAVE_3H_PRODUCT_PARAMS.items():
        row = rows_by_id.get(product_id)
        if row is None:
            raise ValueError(f"WAVE_3H_PRODUCT_IDS refererar {product_id!r}, som saknas i snapshoten.")
        if row["cost_path"] != "legacy_besparing":
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har cost_path {row['cost_path']!r}, "
                "förväntat 'legacy_besparing'."
            )
        if row["savings_today"] is not True:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har savings_today {row['savings_today']!r}, "
                "förväntat exakt True."
            )
        if row["adjustment_types"] != params["adjustment_types"]:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har adjustment_types "
                f"{row['adjustment_types']!r}, förväntat exakt {params['adjustment_types']!r}."
            )
        if row["capacity_rule"] != params["capacity_rule"]:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har capacity_rule {row['capacity_rule']!r}, "
                f"förväntat exakt {params['capacity_rule']!r}."
            )
        if row["capacity_bands"] != params["capacity_bands"]:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har {row['capacity_bands']} kapacitetsband, "
                f"förväntat exakt {params['capacity_bands']}."
            )
        if row["has_capacity_charge"] != params["has_capacity_charge"]:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har has_capacity_charge "
                f"{row['has_capacity_charge']!r}, förväntat exakt {params['has_capacity_charge']!r}."
            )
        # Legacyprodukter saknar `policy` (ingen `_kraver_kontrakt`-markör),
        # så required_policy_fields/series_fields/history_fields/
        # measurement_resolutions ska alla vara tomma — precis som Göteborg
        # Energi i WAVE_3F_PRODUCT_PARAMS.
        if row["required_policy_fields"] != []:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har required_policy_fields "
                f"{row['required_policy_fields']!r}, förväntat exakt []."
            )
        if row["series_fields"] != []:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har series_fields "
                f"{row['series_fields']!r}, förväntat exakt []."
            )
        if row["history_fields"] != []:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har history_fields "
                f"{row['history_fields']!r}, förväntat exakt []."
            )
        if row["has_eligibility_rule"]:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har ett behörighetsvillkor, förväntat inget."
            )
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_publik_10_15_20":
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_publik_10_15_20' i SCENARIO_STATUS_REGISTRY."
            )

        raw_price = latest_price(tariffs[product_id])
        if raw_price.get("policy") is not None:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} förväntas sakna policy, men har en."
            )
        if raw_price.get("moms") != "exkl":
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har moms {raw_price.get('moms')!r}, "
                "förväntat 'exkl'."
            )
        raw_energi = raw_price.get("energi") or {}
        if not _strict_numeric_equal(raw_energi.get("manadspriser"), params["manadspriser"]):
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har energi.manadspriser="
                f"{raw_energi.get('manadspriser')!r}, förväntat exakt {params['manadspriser']!r}."
            )
        raw_capacity = raw_price.get("kapacitet") or {}
        for capacity_key, expected_value in params["kapacitet"].items():
            if not _strict_numeric_equal(raw_capacity.get(capacity_key), expected_value):
                raise ValueError(
                    f"Våg 3h-produkten {product_id!r} har kapacitet.{capacity_key}="
                    f"{raw_capacity.get(capacity_key)!r}, förväntat exakt {expected_value!r}."
                )
        if not _strict_numeric_equal(raw_price.get("fast_avgift"), params["fast_avgift"]):
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har fast_avgift="
                f"{raw_price.get('fast_avgift')!r}, förväntat exakt {params['fast_avgift']!r}."
            )
        if raw_price.get("manadsperiodisering") != params["manadsperiodisering"]:
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har manadsperiodisering="
                f"{raw_price.get('manadsperiodisering')!r}, förväntat exakt "
                f"{params['manadsperiodisering']!r}."
            )
        raw_adjustments = raw_price.get("justeringar") or []
        if not _strict_numeric_equal(raw_adjustments, params["justeringar"]):
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har justeringar="
                f"{raw_adjustments!r}, förväntat exakt {params['justeringar']!r}."
            )
        raw_indatafalt = raw_price.get("indatafalt") or []
        raw_indatafalt_by_key = {field.get("nyckel"): field for field in raw_indatafalt}
        if set(raw_indatafalt_by_key) != set(params["indatafalt"]):
            raise ValueError(
                f"Våg 3h-produkten {product_id!r} har indatafalt-nycklar "
                f"{sorted(raw_indatafalt_by_key)!r}, förväntat exakt "
                f"{sorted(params['indatafalt'])!r}."
            )
        for falt_nyckel, expected_falt in params["indatafalt"].items():
            raw_falt = raw_indatafalt_by_key[falt_nyckel]
            for contract_key, expected_value in expected_falt.items():
                if not _strict_numeric_equal(raw_falt.get(contract_key), expected_value):
                    raise ValueError(
                        f"Våg 3h-produkten {product_id!r} har {falt_nyckel}.{contract_key}="
                        f"{raw_falt.get(contract_key)!r}, förväntat exakt {expected_value!r}."
                    )

    # Våg 3i ("Telge Nät, låg utnyttjning och returtemperatur", handoff
    # 2026-10-17-006/007, INTERN PILOT ENDAST): till skillnad från
    # wave_3a_ids/wave_3g_ids ovan delar Telge sin adjustment_types-
    # kombination med Norrenergi (redan granskad, Våg 3h), så bindningen
    # sker direkt mot den fasta WAVE_3I_PRODUCT_IDS-listan (precis som
    # WAVE_3B_PRODUCT_IDS) i stället för ett generiskt filter. Till
    # skillnad från Norrenergi ÄR Telge kontraktsgatad, så
    # required_policy_fields/kapacitet_bindning binds här mot
    # policy.kravda_falt.
    if set(WAVE_3I_PRODUCT_PARAMS) != WAVE_3I_PRODUCT_IDS:
        raise ValueError(
            "WAVE_3I_PRODUCT_PARAMS matchar inte WAVE_3I_PRODUCT_IDS. "
            f"Endast i WAVE_3I_PRODUCT_PARAMS: {sorted(set(WAVE_3I_PRODUCT_PARAMS) - WAVE_3I_PRODUCT_IDS)}; "
            f"endast i WAVE_3I_PRODUCT_IDS: {sorted(WAVE_3I_PRODUCT_IDS - set(WAVE_3I_PRODUCT_PARAMS))}."
        )
    for product_id, params in WAVE_3I_PRODUCT_PARAMS.items():
        row = rows_by_id.get(product_id)
        if row is None:
            raise ValueError(f"WAVE_3I_PRODUCT_IDS refererar {product_id!r}, som saknas i snapshoten.")
        # Omgranskning 2026-10-17-011 (Codex): explicit produktgrind före den
        # generella justeringstypsjämförelsen nedan, så en tillagd
        # documented_exclusion-justering fångas av den avsedda invarianten
        # (Telge dokumenterar ingen exkludering) i stället för att bara råka
        # fälla den bredare adjustment_types/justeringar-jämförelsen.
        if row["documented_exclusions"] != []:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har documented_exclusions "
                f"{row['documented_exclusions']!r}, förväntat exakt []."
            )
        if row["adjustment_types"] != params["adjustment_types"]:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har adjustment_types "
                f"{row['adjustment_types']!r}, förväntat exakt {params['adjustment_types']!r}."
            )
        if row["cost_path"] != "kontrakt_arskostnad":
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har cost_path {row['cost_path']!r}, "
                "förväntat 'kontrakt_arskostnad'."
            )
        if row["savings_today"] is not False:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har savings_today {row['savings_today']!r}, "
                "förväntat exakt False."
            )
        if row["capacity_rule"] != params["capacity_rule"]:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har capacity_rule {row['capacity_rule']!r}, "
                f"förväntat exakt {params['capacity_rule']!r}."
            )
        if row["capacity_bands"] != params["capacity_bands"]:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har {row['capacity_bands']} kapacitetsband, "
                f"förväntat exakt {params['capacity_bands']}."
            )
        if row["has_capacity_charge"] != params["has_capacity_charge"]:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har has_capacity_charge "
                f"{row['has_capacity_charge']!r}, förväntat exakt {params['has_capacity_charge']!r}."
            )
        keys = params["keys"]
        indatafalt_keys = {field["nyckel"] for field in params["indatafalt"]}
        expected_required_fields = sorted({keys["effekt"], keys["band"], *indatafalt_keys})
        if row["required_policy_fields"] != expected_required_fields:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har required_policy_fields "
                f"{row['required_policy_fields']!r}, förväntat exakt {expected_required_fields!r}."
            )
        if row["series_fields"] != []:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har series_fields "
                f"{row['series_fields']!r}, förväntat exakt []."
            )
        if row["history_fields"] != []:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har history_fields "
                f"{row['history_fields']!r}, förväntat exakt []."
            )
        if row["has_eligibility_rule"]:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har ett behörighetsvillkor, förväntat inget."
            )
        if SCENARIO_STATUS_REGISTRY.get(product_id) != "godkand_intern_pilot_ej_publik":
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} måste ha scenario_review_status "
                "'godkand_intern_pilot_ej_publik' i SCENARIO_STATUS_REGISTRY."
            )
        for falt in (keys["effekt"], keys["band"]):
            if row["measurement_resolutions"].get(falt) != "arsvis":
                raise ValueError(
                    f"Våg 3i-produkten {product_id!r} har measurement_resolutions.{falt} "
                    f"{row['measurement_resolutions'].get(falt)!r}, förväntat 'arsvis'."
                )

        raw_price = latest_price(tariffs[product_id])
        raw_policy = raw_price.get("policy") or {}
        if raw_price.get("_kraver_kontrakt") is not True:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} saknar _kraver_kontrakt=true."
            )
        if raw_policy.get("stodjer_aktuell_arskostnad") is not True:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har policy.stodjer_aktuell_arskostnad="
                f"{raw_policy.get('stodjer_aktuell_arskostnad')!r}, förväntat exakt True."
            )
        if raw_policy.get("stodjer_besparing") is not False:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har policy.stodjer_besparing="
                f"{raw_policy.get('stodjer_besparing')!r}, förväntat exakt False."
            )
        if raw_policy.get("kapacitet_bindning") != params["kapacitet_bindning"]:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har policy.kapacitet_bindning="
                f"{raw_policy.get('kapacitet_bindning')!r}, förväntat exakt "
                f"{params['kapacitet_bindning']!r}."
            )
        if raw_policy.get("kapacitet_band_bindning") != params["kapacitet_band_bindning"]:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har policy.kapacitet_band_bindning="
                f"{raw_policy.get('kapacitet_band_bindning')!r}, förväntat exakt "
                f"{params['kapacitet_band_bindning']!r}."
            )
        if raw_policy.get("kapacitet_multiplikator_bindning") is not None:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har "
                f"policy.kapacitet_multiplikator_bindning="
                f"{raw_policy.get('kapacitet_multiplikator_bindning')!r}, förväntat None."
            )
        if raw_price.get("moms") != "exkl":
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har moms {raw_price.get('moms')!r}, "
                "förväntat 'exkl'."
            )
        raw_energi = raw_price.get("energi") or {}
        if not _strict_numeric_equal(raw_energi.get("manadspriser"), params["manadspriser"]):
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har energi.manadspriser="
                f"{raw_energi.get('manadspriser')!r}, förväntat exakt {params['manadspriser']!r}."
            )
        raw_capacity = raw_price.get("kapacitet") or {}
        for capacity_key, expected_value in params["kapacitet"].items():
            if not _strict_numeric_equal(raw_capacity.get(capacity_key), expected_value):
                raise ValueError(
                    f"Våg 3i-produkten {product_id!r} har kapacitet.{capacity_key}="
                    f"{raw_capacity.get(capacity_key)!r}, förväntat exakt {expected_value!r}."
                )
        if not _strict_numeric_equal(raw_price.get("fast_avgift"), params["fast_avgift"]):
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har fast_avgift="
                f"{raw_price.get('fast_avgift')!r}, förväntat exakt {params['fast_avgift']!r}."
            )
        if raw_price.get("manadsperiodisering") != params["manadsperiodisering"]:
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har manadsperiodisering="
                f"{raw_price.get('manadsperiodisering')!r}, förväntat exakt "
                f"{params['manadsperiodisering']!r}."
            )
        raw_adjustments = raw_price.get("justeringar") or []
        if not _strict_numeric_equal(raw_adjustments, params["justeringar"]):
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har justeringar="
                f"{raw_adjustments!r}, förväntat exakt {params['justeringar']!r}."
            )
        # Omgranskning 2026-10-17-009 (P1, Codex): indatafalt och
        # policy.kravda_falt jämförs nu som hela, ordnade listor av
        # kompletta råa objekt (samtliga egenskaper, inte en delmängd),
        # via samma _strict_numeric_equal-komparator som används för
        # övriga vågars kontrakt ovan. Det fångar extra/saknade/omordnade
        # fält, och varje enskild mutering av en enskild rå egenskap —
        # inte bara effekt-/bandfältet, utan samtliga fyra kravda_falt-
        # poster och båda indatafalt-posterna.
        raw_indatafalt = raw_price.get("indatafalt") or []
        if not _strict_numeric_equal(raw_indatafalt, params["indatafalt"]):
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har indatafalt="
                f"{raw_indatafalt!r}, förväntat exakt {params['indatafalt']!r}."
            )
        raw_required_fields = raw_policy.get("kravda_falt") or []
        if not _strict_numeric_equal(raw_required_fields, params["kravda_falt"]):
            raise ValueError(
                f"Våg 3i-produkten {product_id!r} har policy.kravda_falt="
                f"{raw_required_fields!r}, förväntat exakt {params['kravda_falt']!r}."
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
        "  (60 produkter — våg 1: sundsvall-energi-indal-liden-och-lucksta,",
        "  gotlands-energi-gotland-taxa-17-under-50-mwh-ar, publikt aktiverad signal",
        "  2026-09-25-015; våg 2: samtliga 15 review_wave==2-produkter i Neptune-kodens",
        "  `WAVE_2_PRODUCT_IDS`, publikt aktiverad signal 2026-09-30-002; våg 3a:",
        "  samtliga 17 review_wave==3-produkter vars `adjustment_types` innehåller",
        "  `supply_temperature_adjusted_flow` (E.ON Järfälla/Malmö, Navirum",
        "  Norrköping/Söderköping och Örebro/Kumla/Hallsberg, Kraftringen), exakt",
        "  Neptune-kodens `WAVE_3A_PRODUCT_IDS`, publikt aktiverad signal",
        "  2026-10-03-003/004; våg 3b: samtliga 6 produkter vars `adjustment_types`",
        "  innehåller `volume` (Borlänge, Falu Energi & Vatten, Habo,",
        "  Mjölby-Svartådalen, VänerEnergi), exakt Neptune-kodens",
        "  `WAVE_3B_PRODUCT_IDS`, publikt aktiverad signal 2026-10-05-003; våg 3c:",
        "  samtliga 8 produkter med en säsongsbunden `volume`-justering och en genuin",
        "  tolvmånaders `flode_m3`-serie (Luleå Energi, Mälarenergi, Nevel,",
        "  Öresundskraft Ängelholm/Helsingborg, PiteEnergi Norrfjärden/Sjulnäs och",
        "  Piteå centrala nätet, Tekniska Verken Linköping), exakt Neptune-kodens",
        "  `WAVE_3C_PRODUCT_IDS`, publikt aktiverad signal 2026-10-06-006; våg 3d:",
        "  Jämtkrafts tre `flow_difference`-produkter Åre/Järpen/Mörsil/Duved/Kall/",
        "  Hallen/Krokom/Nälden/Föllinge, Brunflo/Opevägen och Östersund/Frösön/Ås,",
        "  exakt Neptune-kodens `WAVE_3D_PRODUCT_IDS`, publikt aktiverad signal",
        "  APPROVED_FOR_ACTIVATION: Claude, 2026-10-07; våg 3e: Umeå Energis",
        "  `asymmetric_flow_difference`-produkt umea-energi-umea-enkel, exakt",
        "  Neptune-kodens `WAVE_3E_PRODUCT_IDS`, publikt aktiverad signal",
        "  APPROVED_FOR_ACTIVATION: Claude, 2026-10-08; våg 3f: Göteborg Energi,",
        "  Partille Energi och Södertörns Fjärrvärme, samtliga med en",
        "  `temperature_difference`-justering, exakt Neptune-kodens",
        "  `WAVE_3F_PRODUCT_IDS`, publikt aktiverad signal APPROVED_FOR_ACTIVATION:",
        "  Claude, 2026-10-12; våg 3g: Lidköping Energi 0–41 kW och 42+ kW,",
        "  samtliga med en `signed_monthly_flow_adjustment`-justering, exakt",
        "  Neptune-kodens `WAVE_3G_PRODUCT_IDS`, publikt aktiverad signal",
        "  APPROVED_FOR_ACTIVATION: Claude, 2026-10-14; våg 3h: Gotlands Energi",
        "  taxa 21, Mölndal Energi och Norrenergi, tre verkliga, icke",
        "  kontraktsgatade legacyprodukter med befintlig `legacy_besparing`-väg,",
        "  exakt Neptune-kodens `WAVE_3H_PRODUCT_IDS`, publikt aktiverad signal",
        "  APPROVED_FOR_ACTIVATION: Claude, 2026-10-17):",
        "  `stodjerOptimateScenarioPubliktAktiverad` är sann för dessa 60 leverantorId,",
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
