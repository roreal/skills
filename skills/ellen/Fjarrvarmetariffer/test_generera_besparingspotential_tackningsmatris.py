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
        self.assertEqual(len(not_reviewed), 24)
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
        pilot_ids = {
            "stockholm-exergi",
            "sundsvall-energi-indal-liden-och-lucksta",
            "gotlands-energi-gotland-taxa-17-under-50-mwh-ar",
        } | wave_2_ids | wave_3a_ids | wave_3b_ids | wave_3c_ids | wave_3d_ids | wave_3e_ids
        others = [row for pid, row in self.by_id.items() if pid not in pilot_ids]
        self.assertTrue(all(row["scenario_review_status"] == "not_reviewed" for row in others))
        self.assertEqual(
            self.matrix["counts"]["scenario_review_status"],
            {
                "godkand_publik_10_15_20": 52,
                "not_reviewed": 24,
                "synlig_sarskild_preliminar_prototyp": 1,
            },
        )

    def test_scenario_status_vocabulary_still_allows_reserved_internal_pilot_status(self) -> None:
        # godkand_intern_pilot_ej_publik bars tidigare av WAVE_3C_PRODUCT_IDS
        # (handoff 2026-10-06-002, intern pilot), sedan av WAVE_3D_PRODUCT_IDS
        # (handoff 2026-10-07-002, intern pilot) och därefter av
        # WAVE_3E_PRODUCT_IDS (handoff 2026-10-08-001, intern pilot) innan
        # samtliga tre publikt aktiverades (signal
        # APPROVED_FOR_ACTIVATION-2026-10-07/-2026-10-08) — statusen bars nu
        # av 0 produkter men kvarstår i ALLOWED_SCENARIO_REVIEW_STATUSES som
        # reserverad vokabulär för en framtida intern pilot.
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
        # Umeå Energi som en NY intern pilot, se WAVE_3E_PRODUCT_IDS) —
        # ingen rad bär längre godkand_intern_pilot_ej_publik.
        internal_pilot_ids = {
            row["product_id"] for row in self.matrix["rows"]
            if row["scenario_review_status"] == "godkand_intern_pilot_ej_publik"
        }
        self.assertEqual(internal_pilot_ids, set())

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
