"""Regressionsgrind för den tekniska Optimate-täckningsmatrisen."""

from pathlib import Path
import re
import sys
import unittest
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
        self.assertEqual(len(not_reviewed), 75)
        self.assertTrue(all(row["price_source"] for row in self.matrix["rows"]))

    def test_scenario_status_registry_is_bound_and_fail_closed(self) -> None:
        stockholm = self.by_id["stockholm-exergi"]
        self.assertEqual(stockholm["scenario_review_status"], "synlig_sarskild_preliminar_prototyp")
        sundsvall = self.by_id["sundsvall-energi-indal-liden-och-lucksta"]
        self.assertEqual(sundsvall["scenario_review_status"], "godkand_intern_pilot_ej_publik")
        others = [
            row for pid, row in self.by_id.items()
            if pid not in {"stockholm-exergi", "sundsvall-energi-indal-liden-och-lucksta"}
        ]
        self.assertTrue(all(row["scenario_review_status"] == "not_reviewed" for row in others))
        self.assertEqual(
            self.matrix["counts"]["scenario_review_status"],
            {
                "godkand_intern_pilot_ej_publik": 1,
                "not_reviewed": 75,
                "synlig_sarskild_preliminar_prototyp": 1,
            },
        )

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
