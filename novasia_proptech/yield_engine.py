"""Scenario arithmetic only: no market forecasts or jurisdictional tax defaults."""
from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_UP


def number(value, name, *, minimum=Decimal(0), maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        raise ValueError(f"{name} must be a finite number")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not result.is_finite() or abs(result) > Decimal('1e15'):
        raise ValueError(f"{name} must be finite and no larger than 1e15 in magnitude")
    if minimum is not None and result < minimum:
        raise ValueError(f"{name} is below its minimum {minimum}")
    if maximum is not None and result > maximum:
        raise ValueError(f"{name} exceeds its maximum {maximum}")
    return result


def rounded(value):
    with localcontext() as context:
        context.prec = 60
        return float(value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))


class NetYieldCalculator:
    @staticmethod
    def calculate_total_acquisition_cost(base_price, transfer_tax_rate,
                                         legal_due_diligence_fee,
                                         furniture_package_cost, utility_connection_fee):
        base = number(base_price, 'base_price', minimum=Decimal('.01'))
        rate = number(transfer_tax_rate, 'transfer_tax_rate', maximum=Decimal(1))
        return rounded(base * (1 + rate) + number(legal_due_diligence_fee, 'legal_fee')
                       + number(furniture_package_cost, 'furniture_cost')
                       + number(utility_connection_fee, 'utility_fee'))

    @staticmethod
    def calculate_net_operating_income(gross_annual_revenue, cam_fee_monthly_sqm,
                                       built_area_sqm, sinking_fund_annual_reserve,
                                       property_management_fee_rate, withholding_tax_rate,
                                       annual_maintenance_reserve):
        gross = number(gross_annual_revenue, 'gross_annual_revenue')
        cam = number(cam_fee_monthly_sqm, 'cam_fee_monthly_sqm') * number(built_area_sqm, 'built_area_sqm') * 12
        reserve = number(sinking_fund_annual_reserve, 'sinking_fund_annual_reserve')
        management = gross * number(property_management_fee_rate, 'property_management_fee_rate', maximum=Decimal(1))
        tax = gross * number(withholding_tax_rate, 'withholding_tax_rate', maximum=Decimal(1))
        maintenance = number(annual_maintenance_reserve, 'annual_maintenance_reserve')
        expenses = cam + reserve + management + tax + maintenance
        return {key: rounded(value) for key, value in {
            'gross_revenue': gross, 'annual_cam_fee': cam, 'sinking_fund_reserve': reserve,
            'management_commission': management, 'withholding_tax': tax,
            'annual_maintenance_reserve': maintenance, 'total_operating_expenses': expenses,
            'net_operating_income': gross - expenses}.items()}

    @classmethod
    def audit_yield(cls, base_price, gross_annual_revenue, cam_fee_monthly_sqm,
                    built_area_sqm, sinking_fund_annual_reserve,
                    property_management_fee_rate, withholding_tax_rate, transfer_tax_rate,
                    legal_fee, furniture_cost, utility_fee, annual_maintenance_reserve):
        """Legacy method name retained. Outputs are modelled, never verified/audited facts."""
        cost = cls.calculate_total_acquisition_cost(base_price, transfer_tax_rate, legal_fee,
                                                     furniture_cost, utility_fee)
        noi = cls.calculate_net_operating_income(gross_annual_revenue, cam_fee_monthly_sqm,
                  built_area_sqm, sinking_fund_annual_reserve, property_management_fee_rate,
                  withholding_tax_rate, annual_maintenance_reserve)
        gross_yield = number(gross_annual_revenue, 'gross_annual_revenue') / number(base_price, 'base_price') * 100
        net_yield = Decimal(str(noi['net_operating_income'])) / Decimal(str(cost)) * 100
        return {'base_price': float(base_price), 'total_acquisition_cost': cost,
                'advertised_gross_yield_pct': rounded(gross_yield),
                'audited_net_yield_pct': rounded(net_yield),
                'yield_leakage_spread_pct': rounded(gross_yield - net_yield),
                'result_status': 'modelled_scenario', 'noi_breakdown': noi}


class RentalCashFlowProjection:
    @staticmethod
    def simulate_10_year_cash_flow(initial_equity, base_annual_noi,
                                   organic_rental_growth_rate, year_5_capex_injection):
        equity = number(initial_equity, 'initial_equity', minimum=Decimal('.01'))
        noi = number(base_annual_noi, 'base_annual_noi', minimum=None)
        growth = number(organic_rental_growth_rate, 'organic_rental_growth_rate',
                        minimum=Decimal(-1), maximum=Decimal(1))
        capex = number(year_5_capex_injection, 'year_5_capex_injection')
        annual, cumulative, total = [], [], Decimal(0)
        for year in range(1, 11):
            cash = Decimal(str(rounded(noi * (1 + growth) ** (year - 1) - (capex if year == 5 else 0))))
            annual.append(float(cash))
            total += cash
            cumulative.append(rounded(total))
        return {'initial_investment': float(equity), 'annual_net_cash_flows': annual,
                'cumulative_cash_flows': cumulative, '10_year_total_net_dividends': rounded(total),
                'result_status': 'modelled_scenario'}
