"""
Data models for PropTech property due diligence.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FinancialMetrics:
    base_price_usd: float
    total_acquisition_cost_usd: float
    advertised_gross_yield_pct: float
    audited_net_yield_pct: float
    cam_fee_monthly_sqm: float
    sinking_fund_usd_sqm: float


@dataclass
class DueDiligenceResult:
    is_compliant: bool
    quota_available: bool
    risk_score: float
    flags: List[str] = field(default_factory=list)


@dataclass
class PropertyDevelopment:
    project_name: str
    country: str
    city: str
    district: str
    property_type: str
    ownership_type: str
    built_area_sqm: float
    financials: FinancialMetrics
    audit: Optional[DueDiligenceResult] = None
