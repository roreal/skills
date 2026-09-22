"""Regressionsgrind för den tekniska Optimate-täckningsmatrisen."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

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
        self.assertEqual(counts["products"], 75)
        self.assertEqual(counts["real_products"], 74)
        self.assertEqual(counts["synthetic_products"], 1)
        self.assertEqual(counts["existing_savings"], 8)
        self.assertEqual(counts["current_cost_only"], 67)
        self.assertEqual(counts["review_waves"], {"1": 2, "2": 13, "3": 48, "4": 12})
        self.assertEqual(len(self.by_id), 75)
        self.assertEqual({row["price_year"] for row in self.matrix["rows"]}, {2026})
        self.assertTrue(all(row["scenario_review_status"] == "not_reviewed" for row in self.matrix["rows"]))
        self.assertTrue(all(row["price_source"] for row in self.matrix["rows"]))

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
        self.assertEqual(len([line for line in rendered.splitlines() if line.startswith("| ")]) - 2, 75)
        self.assertIn("scenario_review_status=not_reviewed", rendered)
        self.assertIn("stockholm-exergi", rendered)

    def test_snapshot_parser_rejects_missing_provenance(self) -> None:
        text = self.source_text.replace("Källkatalog: sha256=", "Källkatalog: annan=")
        with self.assertRaisesRegex(ValueError, "proveniens"):
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
