"""Regressionsgrind för den tekniska Optimate-täckningsmatrisen."""

from pathlib import Path
import re
import sys
import unittest
from typing import Any
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generera_besparingspotential_tackningsmatris as matrix_module  # noqa: E402
from generera_besparingspotential_tackningsmatris import (  # noqa: E402
    DEFAULT_SOURCE,
    build_matrix,
    parse_snapshot,
    product_row,
    render_markdown,
)


class TariffMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not DEFAULT_SOURCE.exists():
            raise unittest.SkipTest("Neptunes genererade tariff-snapshot saknas i denna checkout.")
        cls.source_text = DEFAULT_SOURCE.read_text(encoding="utf-8")
        cls.matrix = build_matrix(cls.source_text)
        cls.by_id = {row["product_id"]: row for row in cls.matrix["rows"]}

    def test_current_portfolio_is_complete_and_unique(self) -> None:
        counts = self.matrix["counts"]
        self.assertEqual(counts["products"], 77)
        self.assertEqual(counts["real_products"], 76)
        self.assertEqual(counts["synthetic_products"], 1)
        self.assertEqual(counts["existing_savings"], 8)
        self.assertEqual(counts["current_cost_only"], 69)
        self.assertEqual(counts["review_waves"], {"1": 2, "2": 15, "3": 48, "4": 12})
        self.assertEqual(len(self.by_id), 77)
        self.assertEqual({row["price_year"] for row in self.matrix["rows"]}, {2026})
        not_reviewed = {
            row["product_id"] for row in self.matrix["rows"]
            if row["scenario_review_status"] == "not_reviewed"
        }
        self.assertEqual(len(not_reviewed), 15)
        self.assertTrue(all(row["price_source"] for row in self.matrix["rows"]))

    def test_scenario_status_registry_is_bound_and_fail_closed(self) -> None:
        stockholm = self.by_id["stockholm-exergi"]
        self.assertEqual(stockholm["scenario_review_status"], "synlig_sarskild_preliminar_prototyp")
        sundsvall = self.by_id["sundsvall-energi-indal-liden-och-lucksta"]
        self.assertEqual(sundsvall["scenario_review_status"], "godkand_publik_10_15_20")
        gotland_taxa_17 = self.by_id["gotlands-energi-gotland-taxa-17-under-50-mwh-ar"]
        self.assertEqual(gotland_taxa_17["scenario_review_status"], "godkand_publik_10_15_20")
        wave_2_ids = {
            "boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad",
            "c4-energi-kristianstad",
            "gavle-energi-gavle",
            "halmstads-energi-och-miljo",
            "harnosand-energi-miljo-harnosand",
            "karlstads-energi-karlstad",
            "kils-energi-kil",
            "oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024",
            "ovik-energi-ornskoldsvik",
            "sandviken-energi-sandviken-normal",
            "skovde-energi-skovde",
            "soderhamn-nara-soderhamn-taxa-11-och-12",
            "tekniska-verken-katrineholm-katrineholm",
            "temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus",
            "trollhattan-energi-trollhattan",
        }
        self.assertTrue(
            all(self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20" for pid in wave_2_ids)
        )
        wave_3a_ids = matrix_module.WAVE_3A_PRODUCT_IDS
        self.assertTrue(
            all(self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20" for pid in wave_3a_ids)
        )
        wave_3b_ids = matrix_module.WAVE_3B_PRODUCT_IDS
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20"
                for pid in wave_3b_ids
            )
        )
        wave_3c_ids = matrix_module.WAVE_3C_PRODUCT_IDS
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20"
                for pid in wave_3c_ids
            )
        )
        wave_3d_ids = matrix_module.WAVE_3D_PRODUCT_IDS
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20"
                for pid in wave_3d_ids
            )
        )
        wave_3e_ids = matrix_module.WAVE_3E_PRODUCT_IDS
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20"
                for pid in wave_3e_ids
            )
        )
        wave_3f_ids = {
            "goteborg-energi",
            "partille-energi-partille",
            "sodertorns-fjarrvarme-sodertorns-fjarrvarme",
        }
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20"
                for pid in wave_3f_ids
            )
        )
        wave_3g_ids = matrix_module.WAVE_3G_PRODUCT_IDS
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20"
                for pid in wave_3g_ids
            )
        )
        wave_3h_ids = matrix_module.WAVE_3H_PRODUCT_IDS
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20"
                for pid in wave_3h_ids
            )
        )
        pilot_ids = {
            "stockholm-exergi",
            "sundsvall-energi-indal-liden-och-lucksta",
            "gotlands-energi-gotland-taxa-17-under-50-mwh-ar",
        } | wave_2_ids | wave_3a_ids | wave_3b_ids | wave_3c_ids | wave_3d_ids | wave_3e_ids | wave_3f_ids \
            | wave_3g_ids | wave_3h_ids
        wave_3i_ids = matrix_module.WAVE_3I_PRODUCT_IDS
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_intern_pilot_ej_publik"
                for pid in wave_3i_ids
            )
        )
        pilot_ids = pilot_ids | wave_3i_ids
        others = [row for pid, row in self.by_id.items() if pid not in pilot_ids]
        self.assertTrue(all(row["scenario_review_status"] == "not_reviewed" for row in others))
        self.assertEqual(
            self.matrix["counts"]["scenario_review_status"],
            {
                "godkand_publik_10_15_20": 60,
                "not_reviewed": 15,
                "godkand_intern_pilot_ej_publik": 1,
                "synlig_sarskild_preliminar_prototyp": 1,
            },
        )

    def test_scenario_status_vocabulary_still_allows_reserved_internal_pilot_status(self) -> None:
        # godkand_intern_pilot_ej_publik bars tidigare av WAVE_3C_PRODUCT_IDS
        # (handoff 2026-10-06-002, intern pilot), sedan av WAVE_3D_PRODUCT_IDS
        # (handoff 2026-10-07-002, intern pilot), därefter av
        # WAVE_3E_PRODUCT_IDS (handoff 2026-10-08-001, intern pilot), sedan
        # av WAVE_3F_PRODUCT_IDS (session 2026-10-11-002, intern pilot) och
        # sedan av WAVE_3G_PRODUCT_IDS (handoff/session 2026-10-12-012,
        # intern pilot), och därefter av WAVE_3H_PRODUCT_IDS (handoff
        # 2026-10-16-optimate-vag-3h-legacyprodukter, intern pilot) innan
        # samtliga publikt aktiverades (signal
        # APPROVED_FOR_ACTIVATION-2026-10-07/-2026-10-08/-2026-10-12/
        # -2026-10-14/-2026-10-17). Statusen bars sedan 2026-10-17 av 0
        # produkter — ren reserverad vokabulär för en framtida intern pilot,
        # ingen rad bär den just nu.
        self.assertIn(
            "godkand_intern_pilot_ej_publik", matrix_module.ALLOWED_SCENARIO_REVIEW_STATUSES
        )
        self.assertIn(
            "godkand_publik_10_15_20", matrix_module.ALLOWED_SCENARIO_REVIEW_STATUSES
        )

    def test_wave_1_membership_is_mechanically_locked(self) -> None:
        wave_1_ids = {
            row["product_id"] for row in self.matrix["rows"] if row["review_wave"] == 1
        }
        self.assertEqual(wave_1_ids, matrix_module.WAVE_1_PRODUCT_IDS)

    def test_wave_3a_membership_is_mechanically_locked(self) -> None:
        wave_3a_ids = {
            row["product_id"] for row in self.matrix["rows"]
            if "supply_temperature_adjusted_flow" in row["adjustment_types"]
        }
        self.assertEqual(wave_3a_ids, matrix_module.WAVE_3A_PRODUCT_IDS)
        self.assertEqual(len(wave_3a_ids), 17)

    def test_wave_2_scenario_status_is_mechanically_locked_to_wave_2_membership(self) -> None:
        # Handoff 2026-09-29-001, §C.3 + aktivering signal 2026-09-30-002:
        # samtliga och ENDAST review_wave==2-produkter ska ha status
        # godkand_publik_10_15_20 (publikt aktiverade, samma status som
        # våg 1).
        wave_2_ids = {
            row["product_id"] for row in self.matrix["rows"] if row["review_wave"] == 2
        }
        activated_wave_2_ids = {
            row["product_id"] for row in self.matrix["rows"]
            if row["review_wave"] == 2 and row["scenario_review_status"] == "godkand_publik_10_15_20"
        }
        self.assertEqual(wave_2_ids, activated_wave_2_ids)
        self.assertEqual(len(wave_2_ids), 15)

    def test_wave_3a_scenario_status_is_mechanically_locked_to_wave_3a_membership(self) -> None:
        # Signal 2026-10-03-003/004: samtliga WAVE_3A_PRODUCT_IDS ska ha
        # status godkand_publik_10_15_20 (publikt aktiverade, samma status
        # som våg 1/2) — ingen godkand_intern_pilot_ej_publik-rad kvarstår.
        wave_3a_status_ids = {
            row["product_id"] for row in self.matrix["rows"]
            if row["product_id"] in matrix_module.WAVE_3A_PRODUCT_IDS
        }
        self.assertTrue(
            all(
                self.by_id[pid]["scenario_review_status"] == "godkand_publik_10_15_20"
                for pid in wave_3a_status_ids
            )
        )
        self.assertEqual(wave_3a_status_ids, matrix_module.WAVE_3A_PRODUCT_IDS)
        self.assertEqual(len(wave_3a_status_ids), 17)
        # Signal 2026-10-05-003: våg 3b publikt aktiverad också. Signal
        # 2026-10-06-006 aktiverade därefter våg 3c publikt också, och
        # signal APPROVED_FOR_ACTIVATION-2026-10-07 aktiverade våg 3d
        # publikt också (handoff 2026-10-07-002 hade ursprungligen lagt in
        # dem som INTERN pilot ENDAST, se WAVE_3D_PRODUCT_IDS). Signal
        # APPROVED_FOR_ACTIVATION-2026-10-08 aktiverade slutligen våg 3e
        # publikt också (handoff 2026-10-08-001 hade ursprungligen lagt in
        # Umeå Energi som en NY intern pilot, se WAVE_3E_PRODUCT_IDS).
        # Session 2026-10-11-002 (Optimate våg 3f, temperaturdifferens) lade
        # till EXAKT tre nya rader som INTERN PILOT ENDAST — goteborg-energi,
        # partille-energi-partille och
        # sodertorns-fjarrvarme-sodertorns-fjarrvarme — och signal
        # APPROVED_FOR_ACTIVATION-2026-10-12 aktiverade dem publikt också.
        # Handoff/session 2026-10-12-012 (Optimate våg 3g, Lidköpings
        # signerade flödesjustering) lade därefter till EXAKT två nya rader
        # som INTERN PILOT ENDAST — lidkoping-energi-lidkoping-041-kw och
        # lidkoping-energi-lidkoping-42-kw — och signal
        # APPROVED_FOR_ACTIVATION-2026-10-14 aktiverade dem publikt också.
        # Handoff 2026-10-16-optimate-vag-3h-legacyprodukter lade därefter
        # till EXAKT tre nya rader som REN INTERN PILOT — Gotland taxa 21,
        # Mölndal och Norrenergi — se WAVE_3H_PRODUCT_IDS, och signal
        # APPROVED_FOR_ACTIVATION-2026-10-17 aktiverade dem publikt också.
        # Handoff 2026-10-17-006/007 (Optimate våg 3i, Telge Nät) lade
        # därefter till EXAKT en ny rad som INTERN PILOT ENDAST — se
        # WAVE_3I_PRODUCT_IDS — så godkand_intern_pilot_ej_publik bärs nu
        # av exakt den raden.
        internal_pilot_ids = {
            row["product_id"] for row in self.matrix["rows"]
            if row["scenario_review_status"] == "godkand_intern_pilot_ej_publik"
        }
        self.assertEqual(internal_pilot_ids, matrix_module.WAVE_3I_PRODUCT_IDS)

    def test_wave_3b_membership_and_status_is_mechanically_locked(self) -> None:
        # Signal 2026-10-05-003 (publik aktivering): samtliga
        # WAVE_3B_PRODUCT_IDS har volume i adjustment_types,
        # cost_path==kontrakt_arskostnad, capacity_rule==effekt och status
        # godkand_publik_10_15_20 — publikt aktiverad, precis som våg 1/2/3a
        # (det senare verifieras på Neptune-sidan, inte i denna matris).
        wave_3b_ids = matrix_module.WAVE_3B_PRODUCT_IDS
        self.assertEqual(len(wave_3b_ids), 6)
        for pid in wave_3b_ids:
            row = self.by_id[pid]
            self.assertIn("volume", row["adjustment_types"])
            self.assertEqual(row["cost_path"], "kontrakt_arskostnad")
            self.assertEqual(row["capacity_rule"], "effekt")
            self.assertEqual(row["scenario_review_status"], "godkand_publik_10_15_20")

    def test_wave_3c_membership_and_status_is_mechanically_locked(self) -> None:
        # Signal 2026-10-06-006 (APPROVED_FOR_ACTIVATION: Claude, slutgranskning
        # av handoff 2026-10-06-002/rättningsrundan 004/005): samtliga
        # WAVE_3C_PRODUCT_IDS har volume i adjustment_types,
        # cost_path==kontrakt_arskostnad, capacity_rule==effekt, ett genuint
        # flode_m3-seriefält och status godkand_publik_10_15_20 — publikt
        # aktiverad, precis som våg 1/2/3a/3b (det senare verifieras på
        # Neptune-sidan, som nu mekaniskt lägger till hela WAVE_3C_PRODUCT_IDS
        # i sin publika lista).
        wave_3c_ids = matrix_module.WAVE_3C_PRODUCT_IDS
        self.assertEqual(len(wave_3c_ids), 8)
        for pid in wave_3c_ids:
            row = self.by_id[pid]
            self.assertIn("volume", row["adjustment_types"])
            self.assertEqual(row["cost_path"], "kontrakt_arskostnad")
            self.assertEqual(row["capacity_rule"], "effekt")
            self.assertEqual(row["series_fields"], ["flode_m3"])
            self.assertEqual(row["measurement_resolutions"].get("flode_m3"), "manadsvis")
            self.assertEqual(row["scenario_review_status"], "godkand_publik_10_15_20")

        malarenergi = self.by_id["malarenergi-vasteras-och-hallstahammar-24-lagenheter"]
        self.assertFalse(malarenergi["has_capacity_charge"])
        self.assertEqual(malarenergi["capacity_bands"], 0)
        for pid in wave_3c_ids - {"malarenergi-vasteras-och-hallstahammar-24-lagenheter"}:
            row = self.by_id[pid]
            self.assertTrue(row["has_capacity_charge"])
            self.assertGreater(row["capacity_bands"], 0)

    def test_wave_3c_extra_series_field_is_fail_closed(self) -> None:
        # Handoff 2026-10-06-002 kräver exakt series_fields=[flode_m3] för
        # WAVE_3C_PRODUCT_IDS. Codex (granskning 2026-10-06-004, P1) visade att
        # ett extra seriefält tidigare passerade fail-open eftersom gaten bara
        # kontrollerade medlemskap, inte exakt likhet.
        mutated_id = next(iter(matrix_module.WAVE_3C_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["series_fields"] = sorted({*row["series_fields"], "extra_series"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "series_fields"):
                build_matrix(self.source_text)

    def test_wave_3c_wrong_resolution_is_fail_closed(self) -> None:
        # Samma P1: måndsupplösningen kontrollerades inte alls innan
        # rättningen. Ett muterat flode_m3 med annan upplösning ska nu kastas.
        mutated_id = next(iter(matrix_module.WAVE_3C_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["measurement_resolutions"] = {
                    **row["measurement_resolutions"],
                    "flode_m3": "arsvis",
                }
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "measurement_resolutions"):
                build_matrix(self.source_text)

    def test_wave_3c_missing_resolution_is_fail_closed(self) -> None:
        # Signal 2026-10-06-006, P.5: koden blockerar redan både fel värde
        # (ovan) och en helt SAKNAD flode_m3-upplösning (.get returnerar None,
        # som aldrig är "manadsvis") — det här testet ger den andra grenen
        # egen testtäckning i stället för att bara lita på den delade
        # kodvägen.
        mutated_id = next(iter(matrix_module.WAVE_3C_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["measurement_resolutions"] = {
                    k: v for k, v in row["measurement_resolutions"].items() if k != "flode_m3"
                }
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "measurement_resolutions"):
                build_matrix(self.source_text)

    def test_wave_3d_membership_and_status_is_mechanically_locked(self) -> None:
        # Signal APPROVED_FOR_ACTIVATION-2026-10-07 (publik aktivering av
        # handoff 2026-10-07-002, tidigare APPROVED_FOR_IMPLEMENTATION:
        # Claude): de tre Jämtkraft-produkterna har flow_difference i
        # adjustment_types, cost_path==kontrakt_arskostnad,
        # capacity_rule==effekt, exakt fem effektband, series_fields==[]
        # (årsupplöst flode_okt_apr_m3, inte en månadsserie) och status
        # godkand_publik_10_15_20 — publikt aktiverad, precis som våg
        # 1/2/3a/3b/3c (det verifieras på Neptune-sidan: WAVE_3D_PRODUCT_IDS
        # ingår nu i SCENARIO_PUBLIKT_AKTIVERADE_ID).
        wave_3d_ids = matrix_module.WAVE_3D_PRODUCT_IDS
        self.assertEqual(len(wave_3d_ids), 3)
        for pid in wave_3d_ids:
            row = self.by_id[pid]
            keys = matrix_module.WAVE_3D_PRODUCT_KEYS[pid]
            self.assertEqual(row["adjustment_types"], ["flow_difference"])
            self.assertEqual(
                row["required_policy_fields"],
                sorted({"flode_okt_apr_m3", keys["effekt"], keys["band"]}),
            )
            self.assertEqual(row["history_fields"], [keys["effekt"]])
            self.assertEqual(row["cost_path"], "kontrakt_arskostnad")
            self.assertEqual(row["capacity_rule"], "effekt")
            self.assertEqual(row["capacity_bands"], 5)
            self.assertEqual(row["series_fields"], [])
            self.assertEqual(row["measurement_resolutions"].get("flode_okt_apr_m3"), "arsvis")
            self.assertEqual(row["scenario_review_status"], "godkand_publik_10_15_20")
            self.assertTrue(row["has_capacity_charge"])
            self.assertIn("flode_eller_temperatur", row["risk_flags"])

    def test_wave_3d_wrong_adjustment_type_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["adjustment_types"] = [t for t in row["adjustment_types"] if t != "flow_difference"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "flow_difference"):
                build_matrix(self.source_text)

    def test_wave_3d_extra_adjustment_type_is_fail_closed(self) -> None:
        # Granskning 2026-10-07-004, P1: Codex reproducerade att en extra
        # justeringstyp (t.ex. 'volume' bredvid 'flow_difference') tidigare
        # passerade grinden eftersom den bara kontrollerade medlemskap
        # ("flow_difference" in adjustment_types), inte exakthet.
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["adjustment_types"] = sorted({*row["adjustment_types"], "volume"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "adjustment_types"):
                build_matrix(self.source_text)

    def test_wave_3d_wrong_required_policy_fields_is_fail_closed(self) -> None:
        # Granskning 2026-10-07-004, P1: Codex reproducerade att helt
        # felaktiga produktnycklar (fel effekt-/bandnyckel) passerade
        # grinden tyst, eftersom den aldrig band required_policy_fields mot
        # produktens egna nycklar.
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["required_policy_fields"] = ["flode_okt_apr_m3", "fel_effekt_kw", "fel_band_id"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "required_policy_fields"):
                build_matrix(self.source_text)

    def test_wave_3d_wrong_history_fields_is_fail_closed(self) -> None:
        # Granskning 2026-10-07-004, P1: history_fields kontrollerades
        # tidigare inte alls mot produktens effektnyckel.
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["history_fields"] = ["fel_effekt_kw"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "history_fields"):
                build_matrix(self.source_text)

    def test_wave_3d_extra_series_field_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["series_fields"] = sorted({*row["series_fields"], "extra_series"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "series_fields"):
                build_matrix(self.source_text)

    def test_wave_3d_wrong_resolution_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["measurement_resolutions"] = {
                    **row["measurement_resolutions"],
                    "flode_okt_apr_m3": "manadsvis",
                }
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "measurement_resolutions"):
                build_matrix(self.source_text)

    def test_wave_3d_missing_resolution_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["measurement_resolutions"] = {
                    k: v for k, v in row["measurement_resolutions"].items() if k != "flode_okt_apr_m3"
                }
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "measurement_resolutions"):
                build_matrix(self.source_text)

    def test_wave_3d_wrong_band_count_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["capacity_bands"] = 4
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "effektband"):
                build_matrix(self.source_text)

    def test_wave_3d_wrong_capacity_rule_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3D_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["capacity_rule"] = "piecewise_polynomial"
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "capacity_rule"):
                build_matrix(self.source_text)

    def test_wave_3d_is_now_publicly_activated_by_this_matrix(self) -> None:
        # Signal APPROVED_FOR_ACTIVATION-2026-10-07: precis som våg
        # 1/2/3a/3b/3c bärs samtliga tre våg 3d-produkter nu av
        # godkand_publik_10_15_20 — ingen av dem bär längre
        # godkand_intern_pilot_ej_publik.
        for pid in matrix_module.WAVE_3D_PRODUCT_IDS:
            self.assertEqual(self.by_id[pid]["scenario_review_status"], "godkand_publik_10_15_20")

    def test_wave_3e_membership_and_status_is_mechanically_locked(self) -> None:
        # Signal APPROVED_FOR_ACTIVATION-2026-10-08 (publik aktivering av
        # handoff 2026-10-08-001, tidigare APPROVED_FOR_IMPLEMENTATION:
        # Claude): Umeå Energis asymmetric_flow_difference-produkt har
        # exakt en justering, cost_path==kontrakt_arskostnad,
        # capacity_rule==effekt, exakt sju effektband, fyra krävda
        # policyfält (effekt/band/B/flöde), series_fields==[] och status
        # godkand_publik_10_15_20 — publikt aktiverad, precis som våg
        # 1/2/3a/3b/3c/3d (det verifieras på Neptune-sidan:
        # WAVE_3E_PRODUCT_IDS ingår nu i SCENARIO_PUBLIKT_AKTIVERADE_ID).
        wave_3e_ids = matrix_module.WAVE_3E_PRODUCT_IDS
        self.assertEqual(len(wave_3e_ids), 1)
        for pid in wave_3e_ids:
            row = self.by_id[pid]
            keys = matrix_module.WAVE_3E_PRODUCT_KEYS[pid]
            self.assertEqual(row["adjustment_types"], ["asymmetric_flow_difference"])
            self.assertEqual(
                row["required_policy_fields"],
                sorted({"flode_okt_apr_m3", keys["effekt"], keys["band"], keys["b"]}),
            )
            self.assertEqual(row["history_fields"], [keys["effekt"]])
            self.assertEqual(row["cost_path"], "kontrakt_arskostnad")
            self.assertEqual(row["capacity_rule"], "effekt")
            self.assertEqual(row["capacity_bands"], 7)
            self.assertEqual(row["series_fields"], [])
            self.assertEqual(row["measurement_resolutions"].get("flode_okt_apr_m3"), "arsvis")
            self.assertEqual(row["scenario_review_status"], "godkand_publik_10_15_20")
            self.assertTrue(row["has_capacity_charge"])
            self.assertIn("flode_eller_temperatur", row["risk_flags"])

    def test_wave_3e_is_now_publicly_activated_by_this_matrix(self) -> None:
        # Signal APPROVED_FOR_ACTIVATION-2026-10-08: precis som våg
        # 1/2/3a/3b/3c/3d bärs Umeås asymmetric_flow_difference-produkt nu
        # av godkand_publik_10_15_20 — den bär inte längre
        # godkand_intern_pilot_ej_publik.
        for pid in matrix_module.WAVE_3E_PRODUCT_IDS:
            self.assertEqual(self.by_id[pid]["scenario_review_status"], "godkand_publik_10_15_20")

    def test_wave_3e_wrong_adjustment_type_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["adjustment_types"] = [
                    t for t in row["adjustment_types"] if t != "asymmetric_flow_difference"
                ]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "asymmetric_flow_difference"):
                build_matrix(self.source_text)

    def test_wave_3e_extra_adjustment_type_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["adjustment_types"] = sorted({*row["adjustment_types"], "volume"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "adjustment_types"):
                build_matrix(self.source_text)

    def test_wave_3e_wrong_required_policy_fields_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["required_policy_fields"] = ["flode_okt_apr_m3", "fel_effekt_kw", "fel_band_id"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "required_policy_fields"):
                build_matrix(self.source_text)

    def test_wave_3e_wrong_history_fields_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["history_fields"] = ["fel_effekt_kw"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "history_fields"):
                build_matrix(self.source_text)

    def test_wave_3e_extra_series_field_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["series_fields"] = sorted({*row["series_fields"], "extra_series"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "series_fields"):
                build_matrix(self.source_text)

    def test_wave_3e_wrong_resolution_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["measurement_resolutions"] = {
                    **row["measurement_resolutions"],
                    "flode_okt_apr_m3": "manadsvis",
                }
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "measurement_resolutions"):
                build_matrix(self.source_text)

    def test_wave_3e_missing_resolution_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["measurement_resolutions"] = {
                    k: v for k, v in row["measurement_resolutions"].items() if k != "flode_okt_apr_m3"
                }
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "measurement_resolutions"):
                build_matrix(self.source_text)

    def test_wave_3e_wrong_band_count_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["capacity_bands"] = 4
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "effektband"):
                build_matrix(self.source_text)

    def test_wave_3e_wrong_capacity_rule_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["capacity_rule"] = "piecewise_polynomial"
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "capacity_rule"):
                build_matrix(self.source_text)

    def test_wave_3e_wrong_status_is_fail_closed(self) -> None:
        # Sedan signal APPROVED_FOR_ACTIVATION-2026-10-08 är
        # godkand_publik_10_15_20 den korrekta statusen för Umeå — en
        # mutation TILL den gamla interna pilotstatusen ska nu falla.
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        mutated_registry["umea-energi-umea-enkel"] = "godkand_intern_pilot_ej_publik"
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_publik_10_15_20"):
                build_matrix(self.source_text)

    def test_wave_3e_raw_adjustment_params_are_bound_and_fail_closed(self) -> None:
        # Handoff 2026-10-08-001 §"Bindande scenariokontrakt": bonus_rate=3,
        # fee_rate=7, reference_m3_per_MWh=17, säsongsmånaderna okt-apr. En
        # mutation av NÅGON av dessa råa justeringsparametrar (inte bara
        # adjustment_types) ska falla här, inte bara upptäckas i Neptune.
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [{**price["justeringar"][0], "bonus_rate": 999}],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "bonus_rate"):
                build_matrix(self.source_text)

    def test_wave_3e_extra_adjustment_entry_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [*price["justeringar"], dict(price["justeringar"][0])],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3e_second_product_with_adjustment_type_is_fail_closed(self) -> None:
        # Rättning, granskning 2026-10-08-003 (P1): WAVE_3E_PRODUCT_IDS
        # påstods vara exakt hela katalogmängden med
        # asymmetric_flow_difference, men ingen kontroll jämförde den
        # härledda mängden globalt mot listan. Codex reproducerade felet
        # genom att låta en andra katalograd rapportera typen — build_matrix
        # slutförde då ändå (GLOBAL_SET_FAIL_OPEN).
        wave_3e_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        second_id = "partille-energi-partille"
        self.assertIn(second_id, self.by_id)
        self.assertNotIn(second_id, matrix_module.WAVE_3E_PRODUCT_IDS)
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == second_id:
                row["adjustment_types"] = sorted({*row["adjustment_types"], "asymmetric_flow_difference"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "WAVE_3E_PRODUCT_IDS"):
                build_matrix(self.source_text)
        # Kontrollgrupp: samma mutation på det egna Våg 3e-ID:t ska INTE
        # falla på denna kontroll (bara på en oväntad ANDRA rad).
        def noop_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            return original_product_row(product_id, entry)

        with patch.object(matrix_module, "product_row", noop_product_row):
            build_matrix(self.source_text)
        self.assertIsNotNone(wave_3e_id)

    def test_wave_3e_wrong_raw_capacity_binding_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_bindning": "fel_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_bindning"):
                build_matrix(self.source_text)

    def test_wave_3e_wrong_raw_band_binding_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_band_bindning": "fel_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_band_bindning"):
                build_matrix(self.source_text)

    def test_wave_3e_wrong_raw_multiplier_binding_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_multiplikator_bindning": "fel_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_multiplikator_bindning"):
                build_matrix(self.source_text)

    def test_wave_3e_b_field_raw_contract_is_fail_closed(self) -> None:
        # Låser B-fältets råa kontrakt (vardetyp/matupplosning/det slutna
        # intervallet 0,93-1,401) — en framtida ändring av maxvarde ska
        # falla här, inte bara upptäckas i Neptune-testerna.
        mutated_id = next(iter(matrix_module.WAVE_3E_PRODUCT_IDS))
        keys = matrix_module.WAVE_3E_PRODUCT_KEYS[mutated_id]
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "maxvarde": 999} if field.get("nyckel") == keys["b"] else field
                    for field in price["policy"]["kravda_falt"]
                ]
                price = {
                    **price,
                    "policy": {**price["policy"], "kravda_falt": mutated_fields},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "maxvarde"):
                build_matrix(self.source_text)

    def test_wave_3f_membership_and_status_is_mechanically_locked(self) -> None:
        # Rättning, omgranskning 2026-10-12-003: bevisar att en OMUTERAD
        # snapshot fortfarande ger exakt publik status för samtliga tre
        # Wave-3f-ID:n (Göteborg Energi, Partille Energi, Södertörns
        # Fjärrvärme) — kravet från granskning 2026-10-12-001/-003 p.3.
        # Signal APPROVED_FOR_ACTIVATION-2026-10-12 aktiverade dem publikt.
        wave_3f_ids = matrix_module.WAVE_3F_PRODUCT_IDS
        self.assertEqual(len(wave_3f_ids), 3)
        for pid, params in matrix_module.WAVE_3F_PRODUCT_PARAMS.items():
            row = self.by_id[pid]
            self.assertEqual(row["adjustment_types"], ["temperature_difference"])
            self.assertEqual(row["cost_path"], params["cost_path"])
            self.assertEqual(row["capacity_rule"], "effekt")
            self.assertEqual(row["capacity_bands"], params["capacity_bands"])
            self.assertEqual(row["series_fields"], [])
            self.assertEqual(row["history_fields"], [])
            self.assertFalse(row["has_eligibility_rule"])
            self.assertEqual(row["scenario_review_status"], "godkand_publik_10_15_20")
            if "keys" in params:
                keys = params["keys"]
                self.assertEqual(
                    row["required_policy_fields"],
                    sorted({"avvikelse_c", keys["effekt"], keys["band"]}),
                )
                for falt in (keys["effekt"], keys["band"], "avvikelse_c"):
                    self.assertEqual(row["measurement_resolutions"].get(falt), "arsvis")
            else:
                self.assertEqual(row["required_policy_fields"], [])

    def test_wave_3f_params_registry_missing_product_is_fail_closed(self) -> None:
        # Den konkreta P1-regressionen från omgranskning 2026-10-12-003:
        # WAVE_3F_PRODUCT_PARAMS tappar en produkt som WAVE_3F_PRODUCT_IDS
        # fortfarande innehåller. Innan fail-closed-grinden lades till
        # slutförde build_matrix ändå (params_missing FAIL_OPEN), eftersom
        # per-produktloopen bara itererade WAVE_3F_PRODUCT_PARAMS.
        mutated_params = dict(matrix_module.WAVE_3F_PRODUCT_PARAMS)
        del mutated_params["sodertorns-fjarrvarme-sodertorns-fjarrvarme"]
        with patch.object(matrix_module, "WAVE_3F_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "WAVE_3F_PRODUCT_PARAMS"):
                build_matrix(self.source_text)

    def test_wave_3f_params_registry_extra_product_is_fail_closed(self) -> None:
        mutated_params = dict(matrix_module.WAVE_3F_PRODUCT_PARAMS)
        mutated_params["stockholm-exergi"] = dict(
            next(iter(matrix_module.WAVE_3F_PRODUCT_PARAMS.values()))
        )
        with patch.object(matrix_module, "WAVE_3F_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "WAVE_3F_PRODUCT_PARAMS"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_adjustment_type_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["adjustment_types"] = [
                    t for t in row["adjustment_types"] if t != "temperature_difference"
                ]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "temperature_difference"):
                build_matrix(self.source_text)

    def test_wave_3f_extra_adjustment_type_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["adjustment_types"] = sorted({*row["adjustment_types"], "volume"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "adjustment_types"):
                build_matrix(self.source_text)

    def test_wave_3f_second_product_with_adjustment_type_is_fail_closed(self) -> None:
        # Samma mönster som motsvarande våg 3e-kontroll: en oväntad ANDRA
        # katalograd som tyst får temperature_difference ska falla på den
        # globala wave_3f_ids-kontrollen, inte bara upptäckas i Neptune.
        third_id = "stockholm-exergi"
        self.assertIn(third_id, self.by_id)
        self.assertNotIn(third_id, matrix_module.WAVE_3F_PRODUCT_IDS)
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == third_id:
                row["adjustment_types"] = sorted({*row["adjustment_types"], "temperature_difference"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "WAVE_3F_PRODUCT_IDS"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_months_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [{**price["justeringar"][0], "months": [1, 2, 3]}],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "months"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_rate_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [{**price["justeringar"][0], "rate": 999}],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "rate"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_reference_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [{**price["justeringar"][0], "reference": "fel_referens"}],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "reference"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_formula_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [{**price["justeringar"][0], "formula": "fel_formel"}],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "formula"):
                build_matrix(self.source_text)

    def test_wave_3f_extra_adjustment_entry_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [*price["justeringar"], dict(price["justeringar"][0])],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3f_avvikelse_c_wrong_unit_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "enhet": "K"} if field.get("nyckel") == "avvikelse_c" else field
                    for field in price["indatafalt"]
                ]
                price = {**price, "indatafalt": mutated_fields}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "avvikelse_c.enhet"):
                build_matrix(self.source_text)

    def test_wave_3f_avvikelse_c_wrong_default_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "default": 5} if field.get("nyckel") == "avvikelse_c" else field
                    for field in price["indatafalt"]
                ]
                price = {**price, "indatafalt": mutated_fields}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "avvikelse_c.default"):
                build_matrix(self.source_text)

    def test_wave_3f_avvikelse_c_wrong_min_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "min_varde": -999} if field.get("nyckel") == "avvikelse_c" else field
                    for field in price["indatafalt"]
                ]
                price = {**price, "indatafalt": mutated_fields}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "avvikelse_c.min_varde"):
                build_matrix(self.source_text)

    def test_wave_3f_avvikelse_c_wrong_max_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "max_varde": 999} if field.get("nyckel") == "avvikelse_c" else field
                    for field in price["indatafalt"]
                ]
                price = {**price, "indatafalt": mutated_fields}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "avvikelse_c.max_varde"):
                build_matrix(self.source_text)

    def test_wave_3f_avvikelse_c_wrong_heltal_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "heltal": True} if field.get("nyckel") == "avvikelse_c" else field
                    for field in price["indatafalt"]
                ]
                price = {**price, "indatafalt": mutated_fields}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "avvikelse_c.heltal"):
                build_matrix(self.source_text)

    def test_wave_3f_missing_avvikelse_c_field_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    field for field in price["indatafalt"] if field.get("nyckel") != "avvikelse_c"
                ]
                price = {**price, "indatafalt": mutated_fields}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "indatafalt"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_cost_path_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["cost_path"] = (
                    "legacy_besparing" if row["cost_path"] != "legacy_besparing" else "kontrakt_arskostnad"
                )
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "cost_path"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_capacity_rule_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["capacity_rule"] = "piecewise_polynomial"
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "capacity_rule"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_band_count_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["capacity_bands"] = row["capacity_bands"] + 1
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "effektband"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_required_policy_fields_is_fail_closed(self) -> None:
        mutated_id = next(
            pid for pid, params in matrix_module.WAVE_3F_PRODUCT_PARAMS.items() if "keys" in params
        )
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["required_policy_fields"] = ["avvikelse_c", "fel_effekt_kw", "fel_band_id"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "required_policy_fields"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_measurement_resolution_is_fail_closed(self) -> None:
        # Rättning, slutomgranskning 2026-10-12-005: ingen tidigare Wave-3f-
        # mutation ändrade measurement_resolutions, så en felaktig upplösning
        # (t.ex. 'manadsvis' i stället för 'arsvis') kunde i teorin passera
        # obemärkt. Muterar ett kontraktsgatat fälts upplösning och verifierar
        # att build_matrix faller typat på measurement_resolutions.
        mutated_id = next(
            pid for pid, params in matrix_module.WAVE_3F_PRODUCT_PARAMS.items() if "keys" in params
        )
        mutated_keys = matrix_module.WAVE_3F_PRODUCT_PARAMS[mutated_id]["keys"]
        mutated_field = mutated_keys["effekt"]
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["measurement_resolutions"] = {
                    **row["measurement_resolutions"],
                    mutated_field: "manadsvis",
                }
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "measurement_resolutions"):
                build_matrix(self.source_text)

    def test_wave_3f_extra_series_field_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["series_fields"] = ["extra_series"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "series_fields"):
                build_matrix(self.source_text)

    def test_wave_3f_extra_history_field_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["history_fields"] = ["extra_history"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "history_fields"):
                build_matrix(self.source_text)

    def test_wave_3f_eligibility_rule_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["has_eligibility_rule"] = True
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "behörighetsvillkor"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_status_is_fail_closed(self) -> None:
        # Sedan signal APPROVED_FOR_ACTIVATION-2026-10-12 är
        # godkand_publik_10_15_20 den korrekta statusen för samtliga tre — en
        # mutation TILL den gamla interna pilotstatusen ska nu falla.
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        mutated_registry[next(iter(matrix_module.WAVE_3F_PRODUCT_IDS))] = "godkand_intern_pilot_ej_publik"
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_publik_10_15_20"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_raw_capacity_binding_is_fail_closed(self) -> None:
        mutated_id = next(
            pid for pid, params in matrix_module.WAVE_3F_PRODUCT_PARAMS.items() if "keys" in params
        )
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_bindning": "fel_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_bindning"):
                build_matrix(self.source_text)

    def test_wave_3f_wrong_raw_band_binding_is_fail_closed(self) -> None:
        mutated_id = next(
            pid for pid, params in matrix_module.WAVE_3F_PRODUCT_PARAMS.items() if "keys" in params
        )
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_band_bindning": "fel_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_band_bindning"):
                build_matrix(self.source_text)

    def test_wave_3f_extra_multiplier_binding_is_fail_closed(self) -> None:
        # Till skillnad från våg 3e har ingen våg 3f-produkt en
        # B-multiplikator; policy.kapacitet_multiplikator_bindning måste
        # förbli None.
        mutated_id = next(
            pid for pid, params in matrix_module.WAVE_3F_PRODUCT_PARAMS.items() if "keys" in params
        )
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_multiplikator_bindning": "ovantad_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_multiplikator_bindning"):
                build_matrix(self.source_text)

    # -------------------------------------------------------------------
    # Våg 3g ("Lidköpings signerade månadsvisa flödesjustering", handoff/
    # session 2026-10-12-012, lade ursprungligen till som INTERN PILOT
    # ENDAST; signal APPROVED_FOR_ACTIVATION: Claude, 2026-10-14 aktiverade
    # dem publikt) — samma mutationsmönster som våg 3f ovan.
    # -------------------------------------------------------------------
    def test_wave_3g_membership_and_status_is_mechanically_locked(self) -> None:
        wave_3g_ids = matrix_module.WAVE_3G_PRODUCT_IDS
        self.assertEqual(len(wave_3g_ids), 2)
        for pid, params in matrix_module.WAVE_3G_PRODUCT_PARAMS.items():
            row = self.by_id[pid]
            self.assertEqual(row["adjustment_types"], ["signed_monthly_flow_adjustment"])
            self.assertEqual(row["cost_path"], "kontrakt_arskostnad")
            self.assertEqual(row["capacity_rule"], "effekt")
            self.assertEqual(row["capacity_bands"], params["capacity_bands"])
            self.assertEqual(
                row["series_fields"], sorted(matrix_module.WAVE_3G_SERIES_FIELDS)
            )
            self.assertEqual(
                row["history_fields"], sorted(matrix_module.WAVE_3G_SERIES_FIELDS)
            )
            self.assertFalse(row["has_eligibility_rule"])
            self.assertEqual(row["scenario_review_status"], "godkand_publik_10_15_20")
            keys = params["keys"]
            self.assertEqual(
                row["required_policy_fields"],
                sorted({keys["effekt"], keys["band"], *matrix_module.WAVE_3G_SERIES_FIELDS}),
            )
            for falt in (keys["effekt"], keys["band"]):
                self.assertEqual(row["measurement_resolutions"].get(falt), "arsvis")
            for falt in matrix_module.WAVE_3G_SERIES_FIELDS:
                self.assertEqual(row["measurement_resolutions"].get(falt), "manadsvis")

    def test_wave_3g_params_registry_missing_product_is_fail_closed(self) -> None:
        mutated_params = dict(matrix_module.WAVE_3G_PRODUCT_PARAMS)
        del mutated_params["lidkoping-energi-lidkoping-42-kw"]
        with patch.object(matrix_module, "WAVE_3G_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "WAVE_3G_PRODUCT_PARAMS"):
                build_matrix(self.source_text)

    def test_wave_3g_params_registry_extra_product_is_fail_closed(self) -> None:
        mutated_params = dict(matrix_module.WAVE_3G_PRODUCT_PARAMS)
        mutated_params["stockholm-exergi"] = dict(
            next(iter(matrix_module.WAVE_3G_PRODUCT_PARAMS.values()))
        )
        with patch.object(matrix_module, "WAVE_3G_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "WAVE_3G_PRODUCT_PARAMS"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_adjustment_type_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["adjustment_types"] = [
                    t for t in row["adjustment_types"] if t != "signed_monthly_flow_adjustment"
                ]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "signed_monthly_flow_adjustment"):
                build_matrix(self.source_text)

    def test_wave_3g_extra_adjustment_type_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["adjustment_types"] = sorted({*row["adjustment_types"], "volume"})
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "adjustment_types"):
                build_matrix(self.source_text)

    def test_wave_3g_second_product_with_adjustment_type_is_fail_closed(self) -> None:
        third_id = "stockholm-exergi"
        self.assertIn(third_id, self.by_id)
        self.assertNotIn(third_id, matrix_module.WAVE_3G_PRODUCT_IDS)
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == third_id:
                row["adjustment_types"] = sorted(
                    {*row["adjustment_types"], "signed_monthly_flow_adjustment"}
                )
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "WAVE_3G_PRODUCT_IDS"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_faktor_n_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [{**price["justeringar"][0], "faktor_n": 999}],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "faktor_n"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_field_key_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [{**price["justeringar"][0], "kund_volym_falt": "fel_nyckel"}],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kund_volym_falt"):
                build_matrix(self.source_text)

    def test_wave_3g_extra_adjustment_entry_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "justeringar": [*price["justeringar"], dict(price["justeringar"][0])],
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_cost_path_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["cost_path"] = "legacy_besparing"
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "cost_path"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_capacity_rule_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["capacity_rule"] = "piecewise_polynomial"
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "capacity_rule"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_band_count_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["capacity_bands"] = row["capacity_bands"] + 1
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "effektband"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_required_policy_fields_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["required_policy_fields"] = ["fel_effekt_kw", "fel_band_id"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "required_policy_fields"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_measurement_resolution_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        mutated_field = matrix_module.WAVE_3G_PRODUCT_PARAMS[mutated_id]["keys"]["effekt"]
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["measurement_resolutions"] = {
                    **row["measurement_resolutions"],
                    mutated_field: "manadsvis",
                }
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "measurement_resolutions"):
                build_matrix(self.source_text)

    def test_wave_3g_extra_series_field_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["series_fields"] = [*row["series_fields"], "extra_series"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "series_fields"):
                build_matrix(self.source_text)

    def test_wave_3g_missing_series_field_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["series_fields"] = row["series_fields"][:-1]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "series_fields"):
                build_matrix(self.source_text)

    def test_wave_3g_extra_history_field_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["history_fields"] = [*row["history_fields"], "extra_history"]
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "history_fields"):
                build_matrix(self.source_text)

    def test_wave_3g_eligibility_rule_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_product_row = matrix_module.product_row

        def mutated_product_row(product_id: str, entry: Any) -> dict[str, Any]:
            row = original_product_row(product_id, entry)
            if product_id == mutated_id:
                row["has_eligibility_rule"] = True
            return row

        with patch.object(matrix_module, "product_row", mutated_product_row):
            with self.assertRaisesRegex(ValueError, "behörighetsvillkor"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_status_is_fail_closed(self) -> None:
        # Sedan signal APPROVED_FOR_ACTIVATION-2026-10-14 är
        # godkand_publik_10_15_20 den korrekta statusen för båda — en
        # mutation TILL den gamla interna pilotstatusen ska nu falla.
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        mutated_registry[next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))] = "godkand_intern_pilot_ej_publik"
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_publik_10_15_20"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_raw_capacity_binding_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_bindning": "fel_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_bindning"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_raw_band_binding_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_band_bindning": "fel_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_band_bindning"):
                build_matrix(self.source_text)

    def test_wave_3g_extra_multiplier_binding_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = {
                    **price,
                    "policy": {**price["policy"], "kapacitet_multiplikator_bindning": "ovantad_nyckel"},
                }
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "kapacitet_multiplikator_bindning"):
                build_matrix(self.source_text)

    def test_wave_3g_wrong_effekt_min_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "minvarde": 999} if field.get("nyckel") == "lidkoping_debiterbar_effekt_kw" else field
                    for field in price["policy"]["kravda_falt"]
                ]
                price = {**price, "policy": {**price["policy"], "kravda_falt": mutated_fields}}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "lidkoping_debiterbar_effekt_kw.minvarde"):
                build_matrix(self.source_text)

    def test_wave_3g_tm_wrong_min_exclusivity_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "minvarde_exklusiv": False} if field.get("nyckel") == "lidkoping_nat_avkylning_c" else field
                    for field in price["policy"]["kravda_falt"]
                ]
                price = {**price, "policy": {**price["policy"], "kravda_falt": mutated_fields}}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "lidkoping_nat_avkylning_c"):
                build_matrix(self.source_text)

    def test_wave_3g_tm_missing_attestation_requirement_is_fail_closed(self) -> None:
        mutated_id = next(iter(matrix_module.WAVE_3G_PRODUCT_IDS))
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                mutated_fields = [
                    {**field, "krav_attestering": False} if field.get("nyckel") == "lidkoping_nat_avkylning_c" else field
                    for field in price["policy"]["kravda_falt"]
                ]
                price = {**price, "policy": {**price["policy"], "kravda_falt": mutated_fields}}
            return price

        with patch.object(matrix_module, "latest_price", mutated_latest_price):
            with self.assertRaisesRegex(ValueError, "krav_attestering"):
                build_matrix(self.source_text)

    # Omgranskning 2026-10-13-001 (P1): Codex muterade dessa tio råa
    # katalogfält via samma latest_price-söm och visade att build_matrix
    # tidigare accepterade varje mutation tyst (FAIL_OPEN). Varje test här
    # reproducerar exakt en av de listade mutationerna och bevisar att den
    # nu fälls mekaniskt.

    def _mutate_wave_3g_price(self, mutator: Any) -> Any:
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") in matrix_module.WAVE_3G_PRODUCT_IDS:
                price = mutator(price)
            return price

        return patch.object(matrix_module, "latest_price", mutated_latest_price)

    def _mutate_wave_3g_price_for(self, mutated_id: str, mutator: Any) -> Any:
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = mutator(price)
            return price

        return patch.object(matrix_module, "latest_price", mutated_latest_price)

    def test_wave_3g_band_price_mutation_is_fail_closed(self) -> None:
        # Omgranskning 2026-10-14-001 (testlucka): build_matrix stoppar vid
        # första produkten, så en mutation som träffar båda produkterna
        # samtidigt bevisar bara att 0-41 kW-raden faller. Mutera varje
        # produkt isolerat så att båda bandtabellerna faktiskt exekveras.
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            kapacitet = price["kapacitet"]
            nivaer = [
                {**niva, "pris_kr_per_enhet_ar": niva["pris_kr_per_enhet_ar"] + 1} if niva["id"] == "1" else niva
                for niva in kapacitet["nivaer"]
            ]
            return {**price, "kapacitet": {**kapacitet, "nivaer": nivaer}}

        for mutated_id in matrix_module.WAVE_3G_PRODUCT_IDS:
            with self.subTest(product_id=mutated_id):
                with self._mutate_wave_3g_price_for(mutated_id, mutator):
                    with self.assertRaisesRegex(ValueError, "kapacitet.nivaer"):
                        build_matrix(self.source_text)

    def test_wave_3g_kw_faktor_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "kapacitet": {**price["kapacitet"], "kw_faktor": 2.0}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet.kw_faktor"):
                build_matrix(self.source_text)

    def test_wave_3g_min_debiteringsbas_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "kapacitet": {**price["kapacitet"], "min_debiteringsbas": 4}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "min_debiteringsbas"):
                build_matrix(self.source_text)

    def test_wave_3g_q_minvarde_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "minvarde": 1} if field.get("nyckel") == "lidkoping_kund_volym_m3" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_kund_volym_m3.minvarde"):
                build_matrix(self.source_text)

    def test_wave_3g_q_minvarde_exklusiv_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "minvarde_exklusiv": True} if field.get("nyckel") == "lidkoping_kund_volym_m3" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_kund_volym_m3.minvarde_exklusiv"):
                build_matrix(self.source_text)

    def test_wave_3g_q_antal_varden_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "antal_varden": 11} if field.get("nyckel") == "lidkoping_kund_volym_m3" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_kund_volym_m3.antal_varden"):
                build_matrix(self.source_text)

    def test_wave_3g_q_krav_attestering_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "krav_attestering": True} if field.get("nyckel") == "lidkoping_kund_volym_m3" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_kund_volym_m3.krav_attestering"):
                build_matrix(self.source_text)

    def test_wave_3g_t_fabricated_minvarde_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "minvarde": 0} if field.get("nyckel") == "lidkoping_kund_avkylning_c" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_kund_avkylning_c.minvarde"):
                build_matrix(self.source_text)

    def test_wave_3g_t_fabricated_maxvarde_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "maxvarde": 99} if field.get("nyckel") == "lidkoping_kund_avkylning_c" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_kund_avkylning_c.maxvarde"):
                build_matrix(self.source_text)

    def test_wave_3g_tm_antal_varden_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "antal_varden": 11} if field.get("nyckel") == "lidkoping_nat_avkylning_c" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_nat_avkylning_c.antal_varden"):
                build_matrix(self.source_text)

    def test_wave_3g_adjustment_extra_key_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**adj, "ovantad_nyckel": True} for adj in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "justeringsnycklar"):
                build_matrix(self.source_text)

    def test_wave_3g_policy_stodjer_besparing_non_boolean_mutation_is_fail_closed(self) -> None:
        # stodjer_besparing=None håller fortfarande cost_path på
        # 'kontrakt_arskostnad' i product_row (bara literalt True byter
        # väg), så mutationen kan bara fångas av den explicita råkontrollen
        # mot exakt False.
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "policy": {**price["policy"], "stodjer_besparing": None}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "stodjer_besparing"):
                build_matrix(self.source_text)

    # Omgranskning 2026-10-14-001 (P1): product_row() reducerar kravda_falt
    # till mängder/kartor, så en duplicerad post (en sjätte rad som
    # upprepar en befintlig nyckel ordagrant) passerade tidigare tyst.
    def test_wave_3g_duplicate_kravda_falt_entry_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = list(price["policy"]["kravda_falt"])
            fields.append(dict(fields[0]))
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt-poster"):
                build_matrix(self.source_text)

    def test_wave_3g_kravda_falt_duplicate_key_with_distinct_value_is_fail_closed(self) -> None:
        # Samma nyckel i två poster med olika värden, alla fem förväntade
        # nycklar fortfarande representerade: bevisar att nyckelunikheten
        # kontrolleras mekaniskt och inte bara den råa listans längd.
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = list(price["policy"]["kravda_falt"])
            duplicate = {**fields[0], "minvarde": 999}
            fields.append(duplicate)
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt-poster"):
                build_matrix(self.source_text)

    # Omgranskning 2026-10-14-001 (P1): vanlig Python-likhet gör att
    # True == 1 och False == 0, så ett booleskt råvärde kunde tidigare
    # passera tyst förbi ett numeriskt Wave 3g-kontrakt.
    def test_wave_3g_kw_faktor_boolean_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "kapacitet": {**price["kapacitet"], "kw_faktor": True}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet.kw_faktor"):
                build_matrix(self.source_text)

    def test_wave_3g_band_min_boolean_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            kapacitet = price["kapacitet"]
            nivaer = [
                {**niva, "min": False} if niva["id"] == "1" else niva
                for niva in kapacitet["nivaer"]
            ]
            return {**price, "kapacitet": {**kapacitet, "nivaer": nivaer}}

        for mutated_id in matrix_module.WAVE_3G_PRODUCT_IDS:
            with self.subTest(product_id=mutated_id):
                with self._mutate_wave_3g_price_for(mutated_id, mutator):
                    with self.assertRaisesRegex(ValueError, "kapacitet.nivaer"):
                        build_matrix(self.source_text)

    def test_wave_3g_q_minvarde_boolean_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "minvarde": False} if field.get("nyckel") == "lidkoping_kund_volym_m3" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_kund_volym_m3.minvarde"):
                build_matrix(self.source_text)

    def test_wave_3g_tm_minvarde_boolean_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "minvarde": False} if field.get("nyckel") == "lidkoping_nat_avkylning_c" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3g_price(mutator):
            with self.assertRaisesRegex(ValueError, "lidkoping_nat_avkylning_c.minvarde"):
                build_matrix(self.source_text)

    def _mutate_wave_3h_price_for(self, mutated_id: str, mutator: Any) -> Any:
        original_latest_price = matrix_module.latest_price

        def mutated_latest_price(entry: Any) -> dict[str, Any]:
            price = original_latest_price(entry)
            if entry.get("id") == mutated_id:
                price = mutator(price)
            return price

        return patch.object(matrix_module, "latest_price", mutated_latest_price)

    def test_wave_3h_membership_and_status_is_mechanically_locked(self) -> None:
        # Signal APPROVED_FOR_ACTIVATION: Claude, 2026-10-17 — publikt
        # aktiverad. Exakt tre verkliga, icke kontraktsgatade
        # legacyprodukter.
        wave_3h_ids = matrix_module.WAVE_3H_PRODUCT_IDS
        self.assertEqual(
            wave_3h_ids,
            frozenset({
                "gotlands-energi-gotland-taxa-21-over-50-mwh-ar",
                "molndal-energi",
                "norrenergi",
            }),
        )
        self.assertEqual(len(wave_3h_ids), 3)
        for pid in wave_3h_ids:
            row = self.by_id[pid]
            self.assertEqual(row["cost_path"], "legacy_besparing")
            self.assertTrue(row["savings_today"])
            self.assertEqual(row["scenario_review_status"], "godkand_publik_10_15_20")
            self.assertEqual(row["required_policy_fields"], [])
            self.assertEqual(row["series_fields"], [])
            self.assertEqual(row["history_fields"], [])
            self.assertFalse(row["has_eligibility_rule"])
        # Ingen överlappning med tidigare vågors ID:n eller publik aktivering.
        self.assertFalse(wave_3h_ids & matrix_module.WAVE_3F_PRODUCT_IDS)
        self.assertFalse(wave_3h_ids & matrix_module.WAVE_3G_PRODUCT_IDS)

    def test_wave_3h_params_registry_missing_product_is_fail_closed(self) -> None:
        mutated_params = dict(matrix_module.WAVE_3H_PRODUCT_PARAMS)
        del mutated_params["norrenergi"]
        with patch.object(matrix_module, "WAVE_3H_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "WAVE_3H_PRODUCT_PARAMS"):
                build_matrix(self.source_text)

    def test_wave_3h_params_registry_extra_product_is_fail_closed(self) -> None:
        mutated_params = dict(matrix_module.WAVE_3H_PRODUCT_PARAMS)
        mutated_params["sundsvall-energi-indal-liden-och-lucksta"] = dict(
            next(iter(matrix_module.WAVE_3H_PRODUCT_PARAMS.values()))
        )
        with patch.object(matrix_module, "WAVE_3H_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "WAVE_3H_PRODUCT_PARAMS"):
                build_matrix(self.source_text)

    def test_wave_3h_extra_product_with_status_is_fail_closed(self) -> None:
        # Sedan signal APPROVED_FOR_ACTIVATION-2026-10-17 ska ingen rad
        # bära godkand_intern_pilot_ej_publik; en tyst återinförd
        # intern-pilot-rad på en icke-3h-produkt ska falla på den globala
        # kontrollen, inte på WAVE_3H_PRODUCT_IDS-bindningen.
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        mutated_registry["sundsvall-energi-indal-liden-och-lucksta"] = "godkand_intern_pilot_ej_publik"
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_intern_pilot_ej_publik"):
                build_matrix(self.source_text)

    def test_wave_3h_missing_product_status_is_fail_closed(self) -> None:
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        del mutated_registry["norrenergi"]
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_publik_10_15_20"):
                build_matrix(self.source_text)

    def test_wave_3h_wrong_status_is_fail_closed(self) -> None:
        # Sedan signal APPROVED_FOR_ACTIVATION-2026-10-17 är
        # godkand_publik_10_15_20 den korrekta statusen för samtliga tre —
        # en mutation TILL den gamla interna pilotstatusen ska nu falla på
        # den globala "inga kvarvarande intern-pilot-rader"-kontrollen.
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        mutated_registry["molndal-energi"] = "godkand_intern_pilot_ej_publik"
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_intern_pilot_ej_publik"):
                build_matrix(self.source_text)

    def test_wave_3h_wrong_adjustment_types_is_fail_closed(self) -> None:
        mutated_params = {
            pid: (dict(params, adjustment_types=["volume"]) if pid == "norrenergi" else params)
            for pid, params in matrix_module.WAVE_3H_PRODUCT_PARAMS.items()
        }
        with patch.object(matrix_module, "WAVE_3H_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "adjustment_types"):
                build_matrix(self.source_text)

    def test_wave_3h_wrong_capacity_rule_is_fail_closed(self) -> None:
        mutated_params = {
            pid: (dict(params, capacity_rule="heterogeneous_bands") if pid == "molndal-energi" else params)
            for pid, params in matrix_module.WAVE_3H_PRODUCT_PARAMS.items()
        }
        with patch.object(matrix_module, "WAVE_3H_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "capacity_rule"):
                build_matrix(self.source_text)

    def test_wave_3h_wrong_capacity_bands_is_fail_closed(self) -> None:
        mutated_params = {
            pid: (dict(params, capacity_bands=99) if pid == "norrenergi" else params)
            for pid, params in matrix_module.WAVE_3H_PRODUCT_PARAMS.items()
        }
        with patch.object(matrix_module, "WAVE_3H_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "kapacitetsband"):
                build_matrix(self.source_text)

    def test_wave_3h_wrong_has_capacity_charge_is_fail_closed(self) -> None:
        mutated_params = {
            pid: (dict(params, has_capacity_charge=True) if pid == "gotlands-energi-gotland-taxa-21-over-50-mwh-ar" else params)
            for pid, params in matrix_module.WAVE_3H_PRODUCT_PARAMS.items()
        }
        with patch.object(matrix_module, "WAVE_3H_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "has_capacity_charge"):
                build_matrix(self.source_text)

    def test_wave_3h_product_with_policy_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {
                **price,
                "_kraver_kontrakt": True,
                "policy": {"stodjer_aktuell_arskostnad": True, "stodjer_besparing": False, "kravda_falt": []},
            }

        with self._mutate_wave_3h_price_for("molndal-energi", mutator):
            with self.assertRaisesRegex(ValueError, "cost_path"):
                build_matrix(self.source_text)

    def test_wave_3h_gotland_deadband_rate_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "rate": 11} if a.get("type") == "cooling_deadband" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for("gotlands-energi-gotland-taxa-21-over-50-mwh-ar", mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3h_gotland_deadband_fee_below_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "fee_below_degC": 37} if a.get("type") == "cooling_deadband" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for("gotlands-energi-gotland-taxa-21-over-50-mwh-ar", mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3h_gotland_volume_discount_band_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "band": [{**a["band"][0], "sats": 1}, *a["band"][1:]]}
                if a.get("type") == "volume_discount" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for("gotlands-energi-gotland-taxa-21-over-50-mwh-ar", mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3h_gotland_foregaende_ars_mwh_default_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "ar_gissning": False} if field.get("nyckel") == "foregaende_ars_mwh" else field
                for field in price["indatafalt"]
            ]
            return {**price, "indatafalt": fields}

        with self._mutate_wave_3h_price_for("gotlands-energi-gotland-taxa-21-over-50-mwh-ar", mutator):
            with self.assertRaisesRegex(ValueError, "foregaende_ars_mwh"):
                build_matrix(self.source_text)

    def test_wave_3h_molndal_flow_rate_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [{**a, "rate": 4.5} for a in price["justeringar"]]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for("molndal-energi", mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3h_molndal_capacity_band_price_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            nivaer = [
                {**band, "pris_kr_per_enhet_ar": 999} if band["id"] == "3" else band
                for band in price["kapacitet"]["nivaer"]
            ]
            return {**price, "kapacitet": {**price["kapacitet"], "nivaer": nivaer}}

        with self._mutate_wave_3h_price_for("molndal-energi", mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet"):
                build_matrix(self.source_text)

    def test_wave_3h_molndal_hogsta_dygnsenergi_heltal_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "heltal": False} if field.get("nyckel") == "hogsta_dygnsenergi_kwh" else field
                for field in price["indatafalt"]
            ]
            return {**price, "indatafalt": fields}

        with self._mutate_wave_3h_price_for("molndal-energi", mutator):
            with self.assertRaisesRegex(ValueError, "hogsta_dygnsenergi_kwh"):
                build_matrix(self.source_text)

    def test_wave_3h_norrenergi_low_utilization_threshold_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "threshold_hours": 2000} if a.get("type") == "low_utilization" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for("norrenergi", mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3h_norrenergi_incremental_return_temperature_rate_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "rates": [3.4, 27]} if a.get("type") == "incremental_return_temperature" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for("norrenergi", mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3h_norrenergi_incremental_return_temperature_months_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "months": [1, 2, 3, 4, 11, 12]} if a.get("type") == "incremental_return_temperature" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for("norrenergi", mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3h_norrenergi_capacity_band_fee_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            nivaer = [
                {**band, "avgift_kr_ar": 1} if band["id"] == "2" else band
                for band in price["kapacitet"]["nivaer"]
            ]
            return {**price, "kapacitet": {**price["kapacitet"], "nivaer": nivaer}}

        with self._mutate_wave_3h_price_for("norrenergi", mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet"):
                build_matrix(self.source_text)

    def test_wave_3h_norrenergi_returtemperatur_c_default_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "default": 35} if field.get("nyckel") == "returtemperatur_c" else field
                for field in price["indatafalt"]
            ]
            return {**price, "indatafalt": fields}

        with self._mutate_wave_3h_price_for("norrenergi", mutator):
            with self.assertRaisesRegex(ValueError, "returtemperatur_c"):
                build_matrix(self.source_text)

    def test_wave_3h_extra_indatafalt_key_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [*price["indatafalt"], {"nyckel": "extra_falt", "enhet": "X"}]
            return {**price, "indatafalt": fields}

        with self._mutate_wave_3h_price_for("norrenergi", mutator):
            with self.assertRaisesRegex(ValueError, "indatafalt-nycklar"):
                build_matrix(self.source_text)

    def test_wave_3h_manadspriser_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            manadspriser = list(price["energi"]["manadspriser"])
            manadspriser[0] += 1
            return {**price, "energi": {**price["energi"], "manadspriser": manadspriser}}

        with self._mutate_wave_3h_price_for("norrenergi", mutator):
            with self.assertRaisesRegex(ValueError, "manadspriser"):
                build_matrix(self.source_text)

    def test_wave_3h_manadsperiodisering_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "manadsperiodisering": "monthly_rate_no_annual_proration"}

        with self._mutate_wave_3h_price_for("gotlands-energi-gotland-taxa-21-over-50-mwh-ar", mutator):
            with self.assertRaisesRegex(ValueError, "manadsperiodisering"):
                build_matrix(self.source_text)

    def test_wave_3h_moms_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "moms": "inkl"}

        with self._mutate_wave_3h_price_for("molndal-energi", mutator):
            with self.assertRaisesRegex(ValueError, "moms"):
                build_matrix(self.source_text)

    # -------------------------------------------------------------------
    # Våg 3i ("Telge Nät, låg utnyttjning och returtemperatur", handoff
    # 2026-10-17-006/007, INTERN PILOT ENDAST). Till skillnad från
    # Norrenergi (Våg 3h, legacyprodukt) ÄR Telge kontraktsgatad, så
    # policybindningarna (kapacitet_bindning/kapacitet_band_bindning/
    # kravda_falt) mutationstestas också, precis som Våg 3g.
    # -------------------------------------------------------------------
    TELGE_ID = "telge-nat-telge-foretag-och-bostadsrattsforeningar"

    def test_wave_3i_membership_and_status_is_mechanically_locked(self) -> None:
        wave_3i_ids = matrix_module.WAVE_3I_PRODUCT_IDS
        self.assertEqual(wave_3i_ids, frozenset({self.TELGE_ID}))
        row = self.by_id[self.TELGE_ID]
        self.assertEqual(row["cost_path"], "kontrakt_arskostnad")
        self.assertFalse(row["savings_today"])
        self.assertEqual(row["scenario_review_status"], "godkand_intern_pilot_ej_publik")
        self.assertEqual(
            row["required_policy_fields"],
            sorted([
                "telge_debiterbar_effekt_kw", "telge_vald_niva_id",
                "normalarskorrigerad_energi_mwh", "returtemperatur_c",
            ]),
        )
        self.assertEqual(row["series_fields"], [])
        self.assertEqual(row["history_fields"], [])
        self.assertFalse(row["has_eligibility_rule"])
        self.assertEqual(sorted(row["adjustment_types"]), sorted(["low_utilization", "incremental_return_temperature"]))
        # Inte publikt aktiverad och ingen överlappning med tidigare vågor.
        self.assertNotIn(self.TELGE_ID, matrix_module.WAVE_3H_PRODUCT_IDS)

    def test_wave_3i_params_registry_missing_product_is_fail_closed(self) -> None:
        mutated_params: dict[str, Any] = {}
        with patch.object(matrix_module, "WAVE_3I_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "WAVE_3I_PRODUCT_PARAMS"):
                build_matrix(self.source_text)

    def test_wave_3i_params_registry_extra_product_is_fail_closed(self) -> None:
        mutated_params = dict(matrix_module.WAVE_3I_PRODUCT_PARAMS)
        mutated_params["norrenergi"] = dict(next(iter(matrix_module.WAVE_3I_PRODUCT_PARAMS.values())))
        with patch.object(matrix_module, "WAVE_3I_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "WAVE_3I_PRODUCT_PARAMS"):
                build_matrix(self.source_text)

    def test_wave_3i_wrong_adjustment_types_is_fail_closed(self) -> None:
        mutated_params = {
            pid: dict(params, adjustment_types=["volume"])
            for pid, params in matrix_module.WAVE_3I_PRODUCT_PARAMS.items()
        }
        with patch.object(matrix_module, "WAVE_3I_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "adjustment_types"):
                build_matrix(self.source_text)

    def test_wave_3i_wrong_cost_path_status_mismatch_is_fail_closed(self) -> None:
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        mutated_registry[self.TELGE_ID] = "godkand_publik_10_15_20"
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_intern_pilot_ej_publik"):
                build_matrix(self.source_text)

    def test_wave_3i_missing_product_status_is_fail_closed(self) -> None:
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        del mutated_registry[self.TELGE_ID]
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_intern_pilot_ej_publik"):
                build_matrix(self.source_text)

    def test_wave_3i_extra_internal_pilot_row_is_fail_closed(self) -> None:
        mutated_registry = dict(matrix_module.SCENARIO_STATUS_REGISTRY)
        mutated_registry["norrenergi"] = "godkand_intern_pilot_ej_publik"
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", mutated_registry):
            with self.assertRaisesRegex(ValueError, "godkand_intern_pilot_ej_publik"):
                build_matrix(self.source_text)

    def test_wave_3i_wrong_capacity_rule_is_fail_closed(self) -> None:
        mutated_params = {
            pid: dict(params, capacity_rule="heterogeneous_bands")
            for pid, params in matrix_module.WAVE_3I_PRODUCT_PARAMS.items()
        }
        with patch.object(matrix_module, "WAVE_3I_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "capacity_rule"):
                build_matrix(self.source_text)

    def test_wave_3i_wrong_capacity_bands_is_fail_closed(self) -> None:
        mutated_params = {
            pid: dict(params, capacity_bands=99)
            for pid, params in matrix_module.WAVE_3I_PRODUCT_PARAMS.items()
        }
        with patch.object(matrix_module, "WAVE_3I_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "kapacitetsband"):
                build_matrix(self.source_text)

    def test_wave_3i_wrong_required_policy_fields_is_fail_closed(self) -> None:
        mutated_params = {
            pid: dict(params, keys={"effekt": "telge_debiterbar_effekt_kw", "band": "fel_nyckel"})
            for pid, params in matrix_module.WAVE_3I_PRODUCT_PARAMS.items()
        }
        with patch.object(matrix_module, "WAVE_3I_PRODUCT_PARAMS", mutated_params):
            with self.assertRaisesRegex(ValueError, "required_policy_fields"):
                build_matrix(self.source_text)

    def test_wave_3i_eligibility_rule_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "eligibility": {"min_varde": 0}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "behörighetsvillkor"):
                build_matrix(self.source_text)

    def test_wave_3i_extra_series_field_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                *price["policy"]["kravda_falt"],
                {
                    "nyckel": "telge_extra_serie", "vardetyp": "number_series", "antal_varden": 12,
                    "rullande": True, "matupplosning": "manadsvis",
                },
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "required_policy_fields"):
                build_matrix(self.source_text)

    def test_wave_3i_policy_wrong_capacity_binding_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "policy": {**price["policy"], "kapacitet_bindning": "fel_nyckel"}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet_bindning"):
                build_matrix(self.source_text)

    def test_wave_3i_policy_wrong_band_binding_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "policy": {**price["policy"], "kapacitet_band_bindning": "fel_nyckel"}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet_band_bindning"):
                build_matrix(self.source_text)

    def test_wave_3i_policy_extra_multiplier_binding_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "policy": {**price["policy"], "kapacitet_multiplikator_bindning": "extra"}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet_multiplikator_bindning"):
                build_matrix(self.source_text)

    def test_wave_3i_policy_stodjer_besparing_mutation_is_fail_closed(self) -> None:
        # stodjer_besparing=True flyttar produkten till cost_path
        # 'kontrakt_besparing' (se build_matrix's cost_path-härledning),
        # vilket fäller på cost_path-kontrollen innan någon dedikerad
        # stodjer_besparing-kontroll nås — fortfarande fail-closed.
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "policy": {**price["policy"], "stodjer_besparing": True}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "cost_path"):
                build_matrix(self.source_text)

    def test_wave_3i_low_utilization_threshold_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "threshold_hours": 2000} if a.get("type") == "low_utilization" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_low_utilization_rate_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "rate": 0.5} if a.get("type") == "low_utilization" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_incremental_return_temperature_rate_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "rates": [2.4, 27]} if a.get("type") == "incremental_return_temperature" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_incremental_return_temperature_months_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "months": [1, 2, 3, 4, 11, 12]} if a.get("type") == "incremental_return_temperature" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_incremental_return_temperature_thresholds_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "thresholds_degC": [25, 60]} if a.get("type") == "incremental_return_temperature" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_extra_adjustment_entry_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [*price["justeringar"], {"type": "volume", "rate": 1, "months": list(range(1, 13))}]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "(justeringar|adjustment_types)"):
                build_matrix(self.source_text)

    def test_wave_3i_capacity_band_price_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            nivaer = [
                {**band, "pris_kr_per_enhet_ar": 1} if band["id"] == "1" else band
                for band in price["kapacitet"]["nivaer"]
            ]
            return {**price, "kapacitet": {**price["kapacitet"], "nivaer": nivaer}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet"):
                build_matrix(self.source_text)

    def test_wave_3i_capacity_band_fee_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            nivaer = [
                {**band, "avgift_kr_ar": 999} if band["id"] == "2" else band
                for band in price["kapacitet"]["nivaer"]
            ]
            return {**price, "kapacitet": {**price["kapacitet"], "nivaer": nivaer}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kapacitet"):
                build_matrix(self.source_text)

    def test_wave_3i_manadspriser_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            priser = list(price["energi"]["manadspriser"])
            priser[0] = 1.0
            return {**price, "energi": {**price["energi"], "manadspriser": priser}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "manadspriser"):
                build_matrix(self.source_text)

    def test_wave_3i_fast_avgift_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "fast_avgift": {"kr_ar": 1, "periodisering": "days_in_month/days_in_year"}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "fast_avgift"):
                build_matrix(self.source_text)

    def test_wave_3i_manadsperiodisering_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "manadsperiodisering": "monthly_rate_no_annual_proration"}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "manadsperiodisering"):
                build_matrix(self.source_text)

    def test_wave_3i_moms_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "moms": "inkl"}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "moms"):
                build_matrix(self.source_text)

    def test_wave_3i_returtemperatur_c_default_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "default": 35} if field.get("nyckel") == "returtemperatur_c" else field
                for field in price["indatafalt"]
            ]
            return {**price, "indatafalt": fields}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "returtemperatur_c"):
                build_matrix(self.source_text)

    def test_wave_3i_effekt_heltal_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "heltal": False} if field.get("nyckel") == "telge_debiterbar_effekt_kw" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "heltal"):
                build_matrix(self.source_text)

    def test_wave_3i_band_vardetyp_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "vardetyp": "number"} if field.get("nyckel") == "telge_vald_niva_id" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "band_id"):
                build_matrix(self.source_text)

    # Omgranskning 2026-10-17-009 (P1, Codex): indatafalt och
    # policy.kravda_falt jämfördes tidigare bara mot en delmängd av
    # egenskaperna (indatafalt saknade nyckel/etikett/hjalptext i
    # kontraktet; kravda_falt validerade bara effekt-/bandfältet mot ett
    # fåtal enskilda egenskaper, och lämnade
    # normalarskorrigerad_energi_mwh/returtemperatur_c helt ovaliderade).
    # Testerna nedan binder ordning, extra/saknade egenskaper och de
    # tidigare ovaliderade fälten.

    def test_wave_3i_adjustment_order_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            return {**price, "justeringar": list(reversed(price["justeringar"]))}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_adjustment_formula_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "formula": "0"} if a.get("type") == "low_utilization" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_adjustment_unit_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {**a, "unit": "SEK/kW/day"} if a.get("type") == "low_utilization" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_monthly_proration_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            adjustments = [
                {k: v for k, v in a.items() if k != "monthly_proration"}
                if a.get("type") == "low_utilization" else a
                for a in price["justeringar"]
            ]
            return {**price, "justeringar": adjustments}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "justeringar"):
                build_matrix(self.source_text)

    def test_wave_3i_kravda_falt_order_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = list(price["policy"]["kravda_falt"])
            fields[0], fields[1] = fields[1], fields[0]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt"):
                build_matrix(self.source_text)

    def test_wave_3i_kravda_falt_extra_property_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "bogus_extra_property": True}
                if field.get("nyckel") == "telge_debiterbar_effekt_kw" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt"):
                build_matrix(self.source_text)

    def test_wave_3i_kravda_falt_matupplosning_mutation_is_fail_closed(self) -> None:
        # matupplosning är gemensam för samtliga fyra kravda_falt-poster
        # men validerades tidigare inte alls. Kör samma mutation mot var
        # och en av de fyra nycklarna isolerat. För effekt-/bandnyckeln
        # fäller den tidigare, separata measurement_resolutions-kontrollen
        # (som härleds från samma råa matupplosning) innan den nya
        # kravda_falt-jämförelsen ens nås — fortfarande fail-closed, bara
        # via en annan av de två kontrollerna.
        for nyckel in (
            "telge_debiterbar_effekt_kw",
            "normalarskorrigerad_energi_mwh",
            "returtemperatur_c",
            "telge_vald_niva_id",
        ):
            with self.subTest(nyckel=nyckel):
                def mutator(price: dict[str, Any], nyckel: str = nyckel) -> dict[str, Any]:
                    fields = [
                        {**field, "matupplosning": "manadsvis"} if field.get("nyckel") == nyckel else field
                        for field in price["policy"]["kravda_falt"]
                    ]
                    return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

                with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
                    with self.assertRaisesRegex(ValueError, "(kravda_falt|measurement_resolutions)"):
                        build_matrix(self.source_text)

    def test_wave_3i_normalarskorrigerad_energi_mwh_maxvarde_mutation_is_fail_closed(self) -> None:
        # Tidigare helt ovaliderat fält (effekt_field/band_field var de
        # enda som kontrollerades individuellt).
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "maxvarde": 50000}
                if field.get("nyckel") == "normalarskorrigerad_energi_mwh" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt"):
                build_matrix(self.source_text)

    def test_wave_3i_normalarskorrigerad_energi_mwh_vardetyp_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "vardetyp": "band_id"}
                if field.get("nyckel") == "normalarskorrigerad_energi_mwh" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt"):
                build_matrix(self.source_text)

    def test_wave_3i_returtemperatur_c_policy_minvarde_mutation_is_fail_closed(self) -> None:
        # Tidigare helt ovaliderat fält.
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "minvarde": 10} if field.get("nyckel") == "returtemperatur_c" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt"):
                build_matrix(self.source_text)

    def test_wave_3i_returtemperatur_c_policy_vardetyp_mutation_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "vardetyp": "band_id"} if field.get("nyckel") == "returtemperatur_c" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt"):
                build_matrix(self.source_text)

    def test_wave_3i_extra_indatafalt_entry_is_fail_closed(self) -> None:
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                *price["indatafalt"],
                {
                    "nyckel": "telge_historik_extra", "etikett": "Historik (extra)", "enhet": "MWh",
                    "default": None, "min_varde": 0, "max_varde": 100000,
                    "hjalptext": "Odokumenterat extra fält.", "ar_gissning": True, "heltal": False,
                },
            ]
            return {**price, "indatafalt": fields}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "indatafalt"):
                build_matrix(self.source_text)

    def test_wave_3i_kravda_falt_documented_exclusion_mutation_is_fail_closed(self) -> None:
        # "Documented exclusion"-kontroll: tillampliga_manader är null i
        # det råa kontraktet för samtliga fyra fält (ingen månadsvis
        # begränsning dokumenterad för Telge). Sätts den i stället till en
        # konkret lista ska det fångas som en kontraktsändring, inte tyst
        # tolereras som en ofarlig precisering.
        def mutator(price: dict[str, Any]) -> dict[str, Any]:
            fields = [
                {**field, "tillampliga_manader": [1, 2, 3]}
                if field.get("nyckel") == "returtemperatur_c" else field
                for field in price["policy"]["kravda_falt"]
            ]
            return {**price, "policy": {**price["policy"], "kravda_falt": fields}}

        with self._mutate_wave_3h_price_for(self.TELGE_ID, mutator):
            with self.assertRaisesRegex(ValueError, "kravda_falt"):
                build_matrix(self.source_text)

    def test_scenario_status_registry_rejects_unknown_status_value(self) -> None:
        bad_registry = {"stockholm-exergi": "not_a_real_status"}
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", bad_registry):
            with self.assertRaisesRegex(ValueError, "scenario_review_status"):
                build_matrix(self.source_text)

    def test_scenario_status_registry_rejects_unknown_product_id(self) -> None:
        bad_registry = {"does-not-exist-in-snapshot": "not_reviewed"}
        with patch.object(matrix_module, "SCENARIO_STATUS_REGISTRY", bad_registry):
            with self.assertRaisesRegex(ValueError, "saknas"):
                build_matrix(self.source_text)

    def test_gavle_and_harnosand_are_present_in_wave_2(self) -> None:
        self.assertEqual(self.by_id["gavle-energi-gavle"]["review_wave"], 2)
        self.assertEqual(self.by_id["harnosand-energi-miljo-harnosand"]["review_wave"], 2)

    def test_distinct_tariff_dependencies_are_not_confused_with_savings_approval(self) -> None:
        stockholm = self.by_id["stockholm-exergi"]
        self.assertEqual(stockholm["cost_path"], "kontrakt_arskostnad")
        self.assertFalse(stockholm["savings_today"])
        self.assertIn("kall_energi_mwh_arsserie", stockholm["series_fields"])
        self.assertIn("flode_eller_temperatur", stockholm["risk_flags"])
        self.assertEqual(stockholm["measurement_resolutions"]["kall_energi_mwh_arsserie"], "manadsvis, tolv varden")
        self.assertTrue(stockholm["price_source"].startswith("https://www.stockholmexergi.se/"))

        sandviken = self.by_id["sandviken-energi-sandviken-normal"]
        self.assertEqual(sandviken["cost_path"], "kontrakt_besparing")
        self.assertTrue(sandviken["savings_today"])

        sundsvall = self.by_id["sundsvall-energi-indal-liden-och-lucksta"]
        self.assertFalse(sundsvall["has_capacity_charge"])
        self.assertEqual(sundsvall["cost_path"], "kontrakt_arskostnad")

        finspang = self.by_id["finspangs-tekniska-verk-finspang"]
        self.assertEqual(finspang["capacity_rule"], "piecewise_polynomial")
        self.assertIn("specialeffekt", finspang["risk_flags"])

        vattenfall = self.by_id["vattenfall-uppsala-uppsala-standard"]
        self.assertTrue(vattenfall["has_eligibility_rule"])
        self.assertEqual(vattenfall["review_wave"], 4)
        self.assertIn("capacity_overrun", vattenfall["documented_exclusions"])
        self.assertIn("industrial_deduction", vattenfall["documented_exclusions"])

    def test_markdown_has_one_row_per_product(self) -> None:
        rendered = render_markdown(self.matrix)
        self.assertEqual(len([line for line in rendered.splitlines() if line.startswith("| ")]) - 2, 77)
        self.assertIn("scenario_review_status=not_reviewed", rendered)
        self.assertIn("stockholm-exergi", rendered)

    def test_markdown_scenario_status_column_matches_json(self) -> None:
        rendered = render_markdown(self.matrix)
        self.assertIn("Scenariostatus", rendered)
        lines_by_product = {
            row["product_id"]: next(
                line for line in rendered.splitlines()
                if line.startswith("| ") and f"| {row['product_id']} |" in line
            )
            for row in self.matrix["rows"]
        }
        for product_id, line in lines_by_product.items():
            row = self.by_id[product_id]
            self.assertIn(f"| {row['scenario_review_status']} |", line)
        for status, count in self.matrix["counts"]["scenario_review_status"].items():
            self.assertIn(f"{status}: {count}", rendered)

    def test_snapshot_parser_rejects_missing_provenance(self) -> None:
        text = self.source_text.replace("Källkatalog: sha256=", "Källkatalog: annan=")
        with self.assertRaisesRegex(ValueError, "proveniens"):
            parse_snapshot(text)

    def test_snapshot_parser_accepts_short_and_full_commit_hash(self) -> None:
        sha = "a" * 64
        for commit in ("6c0877d", "0123456789abcdef0123456789abcdef01234567"):
            text = re.sub(
                r"Källkatalog: sha256=[0-9a-f]{64} commit=[0-9a-f]{7,40}",
                f"Källkatalog: sha256={sha} commit={commit}",
                self.source_text,
            )
            _, provenance = parse_snapshot(text)
            self.assertEqual(provenance["catalog_commit"], commit)

    def test_snapshot_parser_rejects_commit_shorter_than_seven_hex_chars(self) -> None:
        sha = "a" * 64
        text = re.sub(
            r"Källkatalog: sha256=[0-9a-f]{64} commit=[0-9a-f]{7,40}",
            f"Källkatalog: sha256={sha} commit=abc123",
            self.source_text,
        )
        with self.assertRaisesRegex(ValueError, "proveniens"):
            parse_snapshot(text)

    def test_snapshot_parser_rejects_commit_longer_than_forty_hex_chars(self) -> None:
        sha = "a" * 64
        text = re.sub(
            r"Källkatalog: sha256=[0-9a-f]{64} commit=[0-9a-f]{7,40}",
            f"Källkatalog: sha256={sha} commit={'b' * 41}",
            self.source_text,
        )
        with self.assertRaisesRegex(ValueError, "proveniens"):
            parse_snapshot(text)

    def test_snapshot_parser_rejects_commit_with_trailing_non_hex_char(self) -> None:
        sha = "a" * 64
        text = re.sub(
            r"Källkatalog: sha256=[0-9a-f]{64} commit=[0-9a-f]{7,40}",
            f"Källkatalog: sha256={sha} commit={'c' * 40}g",
            self.source_text,
        )
        with self.assertRaisesRegex(ValueError, "proveniens"):
            parse_snapshot(text)

    def test_snapshot_parser_rejects_duplicate_json_keys(self) -> None:
        marker = "export const TARIFFER = {"
        idx = self.source_text.index(marker) + len(marker)
        text = self.source_text[:idx] + '"stockholm-exergi":true,' + self.source_text[idx:]
        with self.assertRaisesRegex(ValueError, "[Dd]ubbl"):
            parse_snapshot(text)


class FailClosedTests(unittest.TestCase):
    def test_contract_marker_without_policy_is_rejected(self) -> None:
        entry = {
            "namn": "Test",
            "prisar": [{
                "ar": 2026, "moms": "exkl", "energi": {"manadspriser": []},
                "kapacitet": {"typ": "effekt", "nivaer": []},
                "_kraver_kontrakt": True,
            }],
        }
        with self.assertRaisesRegex(ValueError, "kontraktsmarkör"):
            product_row("test", entry)

    def test_current_only_does_not_become_approved_savings(self) -> None:
        entry = {
            "namn": "Test",
            "prisar": [{
                "ar": 2026, "moms": "exkl", "energi": {"manadspriser": []},
                "kapacitet": {"typ": "effekt", "nivaer": []},
                "_kraver_kontrakt": True,
                "policy": {
                    "kravda_falt": [], "stodjer_aktuell_arskostnad": True,
                    "stodjer_besparing": False,
                },
            }],
        }
        row = product_row("test", entry)
        self.assertEqual(row["cost_path"], "kontrakt_arskostnad")
        self.assertFalse(row["savings_today"])
        self.assertEqual(row["scenario_review_status"], "not_reviewed")


if __name__ == "__main__":
    unittest.main()
