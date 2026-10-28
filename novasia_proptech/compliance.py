"""Legacy names retained solely to reject unsupported automatic legal verdicts."""

class ForeignOwnershipAuditor:
    @staticmethod
    def _unsupported(*args, **kwargs):
        raise NotImplementedError(
            'Automatic legal eligibility verdicts were withdrawn in 1.0.0. '
            'The 0.1.0 inputs cannot establish title, quota, zoning, permit or contract validity. '
            'Use a qualified local professional and current primary documents; see MIGRATION.md.')

    audit_thailand_condominium = _unsupported
    audit_cambodia_strata_title = _unsupported
    audit_bali_leasehold = _unsupported
