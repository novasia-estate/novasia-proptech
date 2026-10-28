# Migrating from 0.1.0 to 1.0.0

This is a deliberate breaking correction, not a change to published market facts.

- Negative net income and yields now remain negative. 0.1.0 incorrectly clipped income at zero.
- All tax, fee, maintenance, growth and capital-expenditure arguments are required. Pass zero deliberately when appropriate; the library has no local-market defaults.
- Money outputs use decimal arithmetic and half-up rounding to two places. Annual projection cash flows are rounded before accumulation so displayed totals reconcile.
- All amounts in a scenario must use the same currency. The CLI requires a three-letter currency label and performs no exchange conversion.
- Legacy `advertised_gross_yield_pct` and `audited_net_yield_pct` output names remain for migration, but denote modelled gross and modelled net yield. They do not establish an advertised offer or verified return.
- `ForeignOwnershipAuditor` methods now raise `NotImplementedError`. Several user-entered fields cannot establish legal eligibility. No automatic substitute legal verdict is supplied.
- Legacy dataclasses remain importable from `novasia_proptech.models` and the package root; they store caller data, not verified compliance decisions.
- The projection is a constant annual growth scenario with one explicit year-five cost. It models no seasonality, financing, resale proceeds, IRR or statutory tax liability.

Previous wheels and Git history remain available. Re-run stored scenarios with complete assumptions before comparing results.
