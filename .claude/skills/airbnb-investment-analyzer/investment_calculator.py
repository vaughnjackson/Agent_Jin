"""
Investment calculation module for Airbnb Investment Analyzer.
Calculates investment metrics including ROI, cap rate, cash-on-cash return, and break-even analysis.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import utils


@dataclass
class PropertyFinancials:
    """Data class for property financial inputs."""
    purchase_price: float
    down_payment_percent: float
    interest_rate: float
    loan_term_years: int
    annual_gross_rental_income: float
    annual_operating_expenses: float
    closing_costs: float = 0.0
    renovation_costs: float = 0.0
    furniture_costs: float = 0.0


class InvestmentCalculator:
    """Calculate investment metrics for Airbnb properties."""

    def __init__(self, property_financials: PropertyFinancials):
        """
        Initialize calculator with property financials.

        Args:
            property_financials: PropertyFinancials dataclass instance
        """
        self.pf = property_financials
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """Validate input parameters."""
        utils.validate_positive(self.pf.purchase_price, "Purchase price")
        utils.validate_percentage(self.pf.down_payment_percent, "Down payment percent")
        utils.validate_positive(self.pf.interest_rate, "Interest rate")
        utils.validate_positive(self.pf.loan_term_years, "Loan term")
        utils.validate_positive(self.pf.annual_gross_rental_income, "Annual gross rental income")

        if self.pf.annual_operating_expenses < 0:
            raise ValueError("Annual operating expenses cannot be negative")

    def calculate_mortgage_payment(self) -> float:
        """
        Calculate monthly mortgage payment (principal and interest).

        Returns:
            Monthly mortgage payment
        """
        loan_amount = self.pf.purchase_price * (1 - self.pf.down_payment_percent)

        if loan_amount == 0:
            return 0.0

        monthly_rate = self.pf.interest_rate / 12
        num_payments = self.pf.loan_term_years * 12

        if monthly_rate == 0:
            # No interest case
            return loan_amount / num_payments

        # Standard mortgage payment formula
        payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
                  ((1 + monthly_rate) ** num_payments - 1)

        return payment

    def calculate_total_cash_invested(self) -> float:
        """
        Calculate total cash invested upfront.

        Returns:
            Total cash invested
        """
        down_payment = self.pf.purchase_price * self.pf.down_payment_percent
        total_cash = (
            down_payment +
            self.pf.closing_costs +
            self.pf.renovation_costs +
            self.pf.furniture_costs
        )
        return total_cash

    def calculate_annual_debt_service(self) -> float:
        """
        Calculate annual debt service (mortgage payments).

        Returns:
            Annual debt service
        """
        monthly_payment = self.calculate_mortgage_payment()
        return monthly_payment * 12

    def calculate_noi(self) -> float:
        """
        Calculate Net Operating Income (NOI).

        NOI = Gross Rental Income - Operating Expenses

        Returns:
            Net Operating Income
        """
        return self.pf.annual_gross_rental_income - self.pf.annual_operating_expenses

    def calculate_annual_cash_flow(self) -> float:
        """
        Calculate annual cash flow after debt service.

        Cash Flow = NOI - Annual Debt Service

        Returns:
            Annual cash flow
        """
        noi = self.calculate_noi()
        annual_debt_service = self.calculate_annual_debt_service()
        return noi - annual_debt_service

    def calculate_cap_rate(self) -> float:
        """
        Calculate capitalization rate (cap rate).

        Cap Rate = NOI / Purchase Price

        Returns:
            Cap rate as decimal (e.g., 0.08 for 8%)
        """
        noi = self.calculate_noi()
        return utils.safe_divide(noi, self.pf.purchase_price)

    def calculate_cash_on_cash_return(self) -> float:
        """
        Calculate cash-on-cash return.

        CoC Return = Annual Cash Flow / Total Cash Invested

        Returns:
            Cash-on-cash return as decimal (e.g., 0.12 for 12%)
        """
        annual_cash_flow = self.calculate_annual_cash_flow()
        total_cash_invested = self.calculate_total_cash_invested()
        return utils.safe_divide(annual_cash_flow, total_cash_invested)

    def calculate_roi(self) -> float:
        """
        Calculate simple ROI (same as cash-on-cash for year 1).

        ROI = Annual Cash Flow / Total Cash Invested

        Returns:
            ROI as decimal (e.g., 0.15 for 15%)
        """
        return self.calculate_cash_on_cash_return()

    def calculate_break_even_occupancy(
        self,
        avg_nightly_rate: float,
        nights_per_year: int = 365
    ) -> float:
        """
        Calculate break-even occupancy rate.

        Args:
            avg_nightly_rate: Average nightly rental rate
            nights_per_year: Total nights available (default: 365)

        Returns:
            Break-even occupancy rate as decimal (e.g., 0.45 for 45%)
        """
        # Calculate expenses + debt service
        total_annual_expenses = self.pf.annual_operating_expenses + self.calculate_annual_debt_service()

        # Calculate potential gross revenue at 100% occupancy
        potential_gross_revenue = avg_nightly_rate * nights_per_year

        # Break-even occupancy
        break_even_occupancy = utils.safe_divide(total_annual_expenses, potential_gross_revenue)

        return break_even_occupancy

    def calculate_payback_period(self) -> float:
        """
        Calculate simple payback period in years.

        Payback Period = Total Cash Invested / Annual Cash Flow

        Returns:
            Payback period in years (e.g., 6.5 for 6.5 years)
        """
        annual_cash_flow = self.calculate_annual_cash_flow()
        total_cash_invested = self.calculate_total_cash_invested()

        if annual_cash_flow <= 0:
            return float('inf')  # Never pays back if cash flow is zero or negative

        return total_cash_invested / annual_cash_flow

    def calculate_debt_service_coverage_ratio(self) -> float:
        """
        Calculate Debt Service Coverage Ratio (DSCR).

        DSCR = NOI / Annual Debt Service

        Returns:
            DSCR (e.g., 1.25 means NOI is 1.25x debt service)
        """
        noi = self.calculate_noi()
        annual_debt_service = self.calculate_annual_debt_service()
        return utils.safe_divide(noi, annual_debt_service)

    def calculate_all_metrics(self) -> Dict[str, Any]:
        """
        Calculate all investment metrics.

        Returns:
            Dictionary containing all calculated metrics
        """
        monthly_mortgage = self.calculate_mortgage_payment()
        total_cash_invested = self.calculate_total_cash_invested()
        noi = self.calculate_noi()
        annual_cash_flow = self.calculate_annual_cash_flow()

        return {
            "purchase_price": self.pf.purchase_price,
            "down_payment": self.pf.purchase_price * self.pf.down_payment_percent,
            "loan_amount": self.pf.purchase_price * (1 - self.pf.down_payment_percent),
            "monthly_mortgage_payment": monthly_mortgage,
            "annual_debt_service": self.calculate_annual_debt_service(),
            "total_cash_invested": total_cash_invested,
            "annual_gross_rental_income": self.pf.annual_gross_rental_income,
            "annual_operating_expenses": self.pf.annual_operating_expenses,
            "net_operating_income": noi,
            "annual_cash_flow": annual_cash_flow,
            "monthly_cash_flow": annual_cash_flow / 12,
            "cap_rate": self.calculate_cap_rate(),
            "cash_on_cash_return": self.calculate_cash_on_cash_return(),
            "roi": self.calculate_roi(),
            "payback_period_years": self.calculate_payback_period(),
            "debt_service_coverage_ratio": self.calculate_debt_service_coverage_ratio()
        }

    def generate_investment_summary(self) -> str:
        """
        Generate human-readable investment summary.

        Returns:
            Formatted investment summary string
        """
        metrics = self.calculate_all_metrics()

        summary_lines = [
            "=== INVESTMENT SUMMARY ===",
            "",
            "ACQUISITION:",
            f"  Purchase Price: {utils.format_currency(metrics['purchase_price'])}",
            f"  Down Payment ({self.pf.down_payment_percent*100:.0f}%): {utils.format_currency(metrics['down_payment'])}",
            f"  Loan Amount: {utils.format_currency(metrics['loan_amount'])}",
            f"  Total Cash Invested: {utils.format_currency(metrics['total_cash_invested'])}",
            "",
            "FINANCING:",
            f"  Interest Rate: {utils.format_percentage(self.pf.interest_rate)}",
            f"  Loan Term: {self.pf.loan_term_years} years",
            f"  Monthly Mortgage: {utils.format_currency(metrics['monthly_mortgage_payment'])}",
            f"  Annual Debt Service: {utils.format_currency(metrics['annual_debt_service'])}",
            "",
            "INCOME & EXPENSES:",
            f"  Gross Rental Income: {utils.format_currency(metrics['annual_gross_rental_income'])}/year",
            f"  Operating Expenses: {utils.format_currency(metrics['annual_operating_expenses'])}/year",
            f"  Net Operating Income (NOI): {utils.format_currency(metrics['net_operating_income'])}/year",
            "",
            "CASH FLOW:",
            f"  Annual Cash Flow: {utils.format_currency(metrics['annual_cash_flow'])}",
            f"  Monthly Cash Flow: {utils.format_currency(metrics['monthly_cash_flow'])}",
            "",
            "KEY METRICS:",
            f"  Cap Rate: {utils.format_percentage(metrics['cap_rate'])}",
            f"  Cash-on-Cash Return: {utils.format_percentage(metrics['cash_on_cash_return'])}",
            f"  ROI (Year 1): {utils.format_percentage(metrics['roi'])}",
            f"  Payback Period: {metrics['payback_period_years']:.1f} years",
            f"  Debt Service Coverage Ratio: {metrics['debt_service_coverage_ratio']:.2f}",
            "",
            "INVESTMENT ASSESSMENT:",
            self._assess_investment(metrics)
        ]

        return "\n".join(summary_lines)

    def _assess_investment(self, metrics: Dict[str, Any]) -> str:
        """
        Assess investment quality based on metrics.

        Args:
            metrics: Calculated metrics dictionary

        Returns:
            Assessment string
        """
        assessments = []

        # Cap rate assessment
        cap_rate = metrics["cap_rate"]
        if cap_rate >= 0.10:
            assessments.append("  ✓ Excellent cap rate (10%+)")
        elif cap_rate >= 0.08:
            assessments.append("  ✓ Good cap rate (8-10%)")
        elif cap_rate >= 0.06:
            assessments.append("  → Fair cap rate (6-8%)")
        else:
            assessments.append("  ✗ Low cap rate (<6%)")

        # Cash-on-cash return assessment
        coc = metrics["cash_on_cash_return"]
        if coc >= 0.15:
            assessments.append("  ✓ Excellent cash-on-cash return (15%+)")
        elif coc >= 0.10:
            assessments.append("  ✓ Good cash-on-cash return (10-15%)")
        elif coc >= 0.08:
            assessments.append("  → Fair cash-on-cash return (8-10%)")
        else:
            assessments.append("  ✗ Low cash-on-cash return (<8%)")

        # Cash flow assessment
        monthly_cf = metrics["monthly_cash_flow"]
        if monthly_cf > 500:
            assessments.append("  ✓ Strong positive cash flow")
        elif monthly_cf > 0:
            assessments.append("  → Positive cash flow (marginal)")
        else:
            assessments.append("  ✗ Negative cash flow")

        # DSCR assessment
        dscr = metrics["debt_service_coverage_ratio"]
        if dscr >= 1.25:
            assessments.append("  ✓ Strong debt coverage (1.25+ DSCR)")
        elif dscr >= 1.0:
            assessments.append("  → Adequate debt coverage (1.0-1.25 DSCR)")
        else:
            assessments.append("  ✗ Insufficient debt coverage (<1.0 DSCR)")

        return "\n".join(assessments)

    def run_sensitivity_analysis(
        self,
        occupancy_scenarios: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Run sensitivity analysis with different occupancy scenarios.

        Args:
            occupancy_scenarios: List of occupancy rates to test (default: [0.5, 0.65, 0.75, 0.85])

        Returns:
            Dictionary with sensitivity analysis results
        """
        if occupancy_scenarios is None:
            occupancy_scenarios = [0.50, 0.65, 0.75, 0.85]

        # Calculate base metrics
        base_metrics = self.calculate_all_metrics()
        base_occupancy = utils.safe_divide(
            self.pf.annual_gross_rental_income,
            base_metrics["purchase_price"] * 0.01  # Rough estimate
        )

        scenarios = []

        for occupancy in occupancy_scenarios:
            # Adjust gross rental income proportionally
            adjusted_income = self.pf.annual_gross_rental_income * (occupancy / base_occupancy) if base_occupancy > 0 else self.pf.annual_gross_rental_income * occupancy

            # Create temporary property financials
            temp_pf = PropertyFinancials(
                purchase_price=self.pf.purchase_price,
                down_payment_percent=self.pf.down_payment_percent,
                interest_rate=self.pf.interest_rate,
                loan_term_years=self.pf.loan_term_years,
                annual_gross_rental_income=adjusted_income,
                annual_operating_expenses=self.pf.annual_operating_expenses,
                closing_costs=self.pf.closing_costs,
                renovation_costs=self.pf.renovation_costs,
                furniture_costs=self.pf.furniture_costs
            )

            temp_calc = InvestmentCalculator(temp_pf)
            temp_metrics = temp_calc.calculate_all_metrics()

            scenarios.append({
                "occupancy_rate": occupancy,
                "annual_gross_income": adjusted_income,
                "noi": temp_metrics["net_operating_income"],
                "annual_cash_flow": temp_metrics["annual_cash_flow"],
                "monthly_cash_flow": temp_metrics["monthly_cash_flow"],
                "cap_rate": temp_metrics["cap_rate"],
                "cash_on_cash_return": temp_metrics["cash_on_cash_return"]
            })

        return {
            "base_metrics": base_metrics,
            "scenarios": scenarios,
            "summary": self._summarize_sensitivity(scenarios)
        }

    def _summarize_sensitivity(self, scenarios: list) -> str:
        """
        Summarize sensitivity analysis results.

        Args:
            scenarios: List of scenario dictionaries

        Returns:
            Summary string
        """
        positive_cf_scenarios = [s for s in scenarios if s["annual_cash_flow"] > 0]

        if not positive_cf_scenarios:
            return "No scenarios produce positive cash flow."

        best_scenario = max(scenarios, key=lambda x: x["cash_on_cash_return"])
        worst_scenario = min(scenarios, key=lambda x: x["cash_on_cash_return"])

        summary = [
            f"Best case ({best_scenario['occupancy_rate']*100:.0f}% occupancy): {utils.format_percentage(best_scenario['cash_on_cash_return'])} CoC return",
            f"Worst case ({worst_scenario['occupancy_rate']*100:.0f}% occupancy): {utils.format_percentage(worst_scenario['cash_on_cash_return'])} CoC return",
            f"Positive cash flow in {len(positive_cf_scenarios)}/{len(scenarios)} scenarios"
        ]

        return "\n".join(summary)
