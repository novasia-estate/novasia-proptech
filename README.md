# novasia-proptech

Explicit-assumption rental yield and cash-flow modelling for Python property-data workflows. Maintained by [NovAsia Estate](https://novasia.estate/), covering research and property workflows in Thailand, Cambodia and Bali, Indonesia.

**1.0.0 corrects 0.1.0:** losses are retained, hidden tax/fee defaults are removed, and unsupported automatic legal verdicts are withdrawn. [Migration guide](https://github.com/novasia-estate/novasia-proptech/blob/main/MIGRATION.md).

## Install and run

```sh
pip install novasia-proptech==1.0.0
novasia-proptech examples/loss.json
```

Download the [complete example](https://github.com/novasia-estate/novasia-proptech/blob/main/examples/loss.json), or run `python -m novasia_proptech your-scenario.json`. Every cost/rate must be supplied; explicit zero is accepted. All amounts must share one currency; no conversion occurs. Decimal arithmetic is used internally and output is rounded half-up to two decimals.

```python
from novasia_proptech import NetYieldCalculator
result = NetYieldCalculator.audit_yield(
    base_price=100000, gross_annual_revenue=1000,
    cam_fee_monthly_sqm=2, built_area_sqm=50,
    sinking_fund_annual_reserve=300,
    property_management_fee_rate=0.2, withholding_tax_rate=0.1,
    transfer_tax_rate=0.01, legal_fee=500,
    furniture_cost=2000, utility_fee=100,
    annual_maintenance_reserve=200,
)
assert result['noi_breakdown']['net_operating_income'] == -1000
assert result['audited_net_yield_pct'] == -0.97
```

These are synthetic assumptions, not an offer, market evidence or local tax rates. Legacy output names containing `audited` remain for compatibility and mean a modelled scenario, not independent verification.

## Model

Annual CAM = monthly fee per square metre × area × 12.
Modelled operating income = gross annual revenue − annual CAM − annual sinking-fund reserve − management percentage of gross − caller-supplied tax percentage of gross − maintenance reserve.
All-in cost = base purchase price + base × caller-supplied transfer rate + legal fees + furniture + utilities.
Net yield = modelled operating income / all-in cost × 100. Gross yield uses base purchase price. Neither is a levered equity return.

The sinking-fund input is an **annual reserve**, not an upfront fund contribution. Include any upfront payment in your acquisition assumptions outside this limited model. The tax percentage is an explicit simplification on gross revenue, not a statutory tax calculator. Financing, depreciation, resale, occupancy patterns and FX are not inferred.

`RentalCashFlowProjection.simulate_10_year_cash_flow` requires explicit annual growth and year-five capex. Negative cash flows are preserved. It is not an IRR or occupancy forecast.

## Reproducible scenarios

[Hugging Face fixture dataset](https://huggingface.co/datasets/novasia-estate/southeast-asia-property-net-yield-benchmark) supplies synthetic test cases with all inputs and generation metadata. They are not named-property returns or observed prices.

## Development

```sh
python -m unittest discover -s tests -v
python -m novasia_proptech examples/loss.json
python -m build
```

No runtime dependencies, network requests, telemetry, install hooks, API keys or account required to calculate.

## Property research and publisher

- [NovAsia Estate — Southeast Asia property research and projects](https://novasia.estate/)
- [English property guides](https://novasia.estate/en/)
- [Research and expert team](https://novasia.estate/en/experts/)
- [Open browser tools: prices, areas, CSV and payment milestones](https://tools.novasia.estate/)
- [Source, issues and examples](https://github.com/novasia-estate/novasia-proptech)

The homepage links from the original published README are retained. This package does not replace title verification, legal advice or verified property-specific underwriting. MIT licensed.
