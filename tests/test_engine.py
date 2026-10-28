import json
from pathlib import Path
import subprocess
import sys
import unittest
from novasia_proptech import NetYieldCalculator as C, RentalCashFlowProjection as P, ForeignOwnershipAuditor as F

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/loss.json'

class EngineTests(unittest.TestCase):
    def setUp(self):
        self.inputs = json.loads(EXAMPLE.read_text())
        self.inputs.pop('currency')

    def test_loss_and_all_costs(self):
        result = C.audit_yield(**self.inputs)
        self.assertEqual(result['total_acquisition_cost'], 103600)
        self.assertEqual(result['noi_breakdown']['total_operating_expenses'], 2000)
        self.assertEqual(result['noi_breakdown']['net_operating_income'], -1000)
        self.assertEqual(result['audited_net_yield_pct'], -0.97)

    def test_positive_hand_calculation(self):
        self.inputs['gross_annual_revenue'] = 10000
        result = C.audit_yield(**self.inputs)
        self.assertEqual(result['noi_breakdown']['net_operating_income'], 5300)
        self.assertEqual(result['audited_net_yield_pct'], 5.12)

    def test_zero_income_still_pays_fixed_costs(self):
        self.inputs['gross_annual_revenue'] = 0
        self.assertEqual(C.audit_yield(**self.inputs)['noi_breakdown']['net_operating_income'], -1700)

    def test_explicit_zero_costs(self):
        self.inputs = {key: 0 for key in self.inputs}
        self.inputs['base_price'] = 100
        self.assertEqual(C.audit_yield(**self.inputs)['audited_net_yield_pct'], 0)

    def test_no_hidden_defaults(self):
        for key in self.inputs:
            with self.subTest(key=key):
                incomplete = dict(self.inputs)
                del incomplete[key]
                with self.assertRaises(TypeError): C.audit_yield(**incomplete)

    def test_invalid_numbers(self):
        for key in self.inputs:
            for bad in (True, None, 'NaN', 'Infinity', -1, 1e20):
                with self.subTest(key=key, bad=bad):
                    values = dict(self.inputs, **{key: bad})
                    with self.assertRaises(ValueError): C.audit_yield(**values)

    def test_rate_ceiling(self):
        for key in ('transfer_tax_rate', 'withholding_tax_rate', 'property_management_fee_rate'):
            with self.assertRaises(ValueError): C.audit_yield(**dict(self.inputs, **{key: 1.01}))

    def test_zero_base_rejected(self):
        with self.assertRaises(ValueError): C.audit_yield(**dict(self.inputs, base_price=0))

    def test_decimal_strings(self):
        self.assertEqual(C.calculate_total_acquisition_cost('100.01', '0', '.005', '0', '0'), 100.02)

    def test_projection_retains_loss_and_capex(self):
        result = P.simulate_10_year_cash_flow(10000, -100, 0, 500)
        self.assertEqual(result['annual_net_cash_flows'][4], -600)
        self.assertEqual(result['10_year_total_net_dividends'], -1500)
        self.assertEqual(sum(result['annual_net_cash_flows']), -1500)

    def test_projection_explicit_defaults(self):
        with self.assertRaises(TypeError): P.simulate_10_year_cash_flow(100, 10)

    def test_projection_negative_growth(self):
        result = P.simulate_10_year_cash_flow(100, 100, -0.5, 0)
        self.assertEqual(result['annual_net_cash_flows'][:3], [100, 50, 25])
        with self.assertRaises(ValueError): P.simulate_10_year_cash_flow(100, 100, -1.1, 0)

    def test_unsupported_legal_verdicts_fail_closed(self):
        for method in (F.audit_bali_leasehold, F.audit_cambodia_strata_title, F.audit_thailand_condominium):
            with self.assertRaises(NotImplementedError): method()

    def test_cli(self):
        run = subprocess.run([sys.executable, '-m', 'novasia_proptech', str(EXAMPLE)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['currency'], 'USD')
        self.assertEqual(json.loads(run.stdout)['noi_breakdown']['net_operating_income'], -1000)

    def test_cli_rejects_missing_currency(self):
        run = subprocess.run([sys.executable, '-m', 'novasia_proptech', '-'], input=json.dumps(self.inputs), capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)

if __name__ == '__main__': unittest.main()
