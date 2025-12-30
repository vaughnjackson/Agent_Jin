"""
Expense tracking module for Airbnb Investment Analyzer.
Processes and categorizes Airbnb operating expenses with budget variance analysis.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import utils


@dataclass
class Expense:
    """Data class for individual expense."""
    date: str
    category: str
    amount: float
    description: str
    property_id: Optional[str] = None


class ExpenseTracker:
    """Track and analyze Airbnb property operating expenses."""

    # Standard expense categories for Airbnb properties
    EXPENSE_CATEGORIES = {
        "mortgage": "Mortgage Payment",
        "property_tax": "Property Tax",
        "insurance": "Property Insurance",
        "hoa_fees": "HOA Fees",
        "utilities": "Utilities (Electric, Gas, Water, Internet)",
        "cleaning": "Cleaning & Laundry",
        "maintenance": "Maintenance & Repairs",
        "supplies": "Supplies & Amenities",
        "platform_fees": "Platform Fees (Airbnb, VRBO)",
        "property_management": "Property Management Fees",
        "furnishings": "Furnishings & Equipment",
        "marketing": "Marketing & Photography",
        "accounting": "Accounting & Legal",
        "other": "Other Expenses"
    }

    # Typical expense percentages (as % of gross rental income)
    TYPICAL_EXPENSE_RANGES = {
        "property_tax": (0.08, 0.12),
        "insurance": (0.03, 0.06),
        "utilities": (0.05, 0.10),
        "cleaning": (0.10, 0.15),
        "maintenance": (0.05, 0.10),
        "supplies": (0.03, 0.05),
        "platform_fees": (0.03, 0.05),
        "property_management": (0.15, 0.25)
    }

    def __init__(self, property_id: Optional[str] = None):
        """
        Initialize expense tracker.

        Args:
            property_id: Optional property identifier
        """
        self.property_id = property_id
        self.expenses: List[Expense] = []

    def add_expense(
        self,
        date: str,
        category: str,
        amount: float,
        description: str
    ) -> None:
        """
        Add an expense to the tracker.

        Args:
            date: Expense date (YYYY-MM-DD format)
            category: Expense category (must be valid category)
            amount: Expense amount
            description: Expense description

        Raises:
            ValueError: If category is invalid
        """
        if category not in self.EXPENSE_CATEGORIES:
            raise ValueError(f"Invalid category: {category}. Must be one of {list(self.EXPENSE_CATEGORIES.keys())}")

        expense = Expense(
            date=date,
            category=category,
            amount=amount,
            description=description,
            property_id=self.property_id
        )
        self.expenses.append(expense)

    def add_expenses_bulk(self, expenses_data: List[Dict[str, Any]]) -> None:
        """
        Add multiple expenses at once.

        Args:
            expenses_data: List of expense dictionaries
        """
        for exp_data in expenses_data:
            self.add_expense(
                date=exp_data["date"],
                category=exp_data["category"],
                amount=exp_data["amount"],
                description=exp_data.get("description", "")
            )

    def calculate_total_by_category(self) -> Dict[str, float]:
        """
        Calculate total expenses by category.

        Returns:
            Dictionary with category totals
        """
        category_totals = {cat: 0.0 for cat in self.EXPENSE_CATEGORIES}

        for expense in self.expenses:
            category_totals[expense.category] += expense.amount

        return category_totals

    def calculate_total_expenses(self) -> float:
        """
        Calculate total of all expenses.

        Returns:
            Total expenses
        """
        return sum(expense.amount for expense in self.expenses)

    def calculate_monthly_average(self) -> Dict[str, float]:
        """
        Calculate average monthly expenses by category.

        Returns:
            Dictionary with monthly averages
        """
        if not self.expenses:
            return {cat: 0.0 for cat in self.EXPENSE_CATEGORIES}

        # Get date range
        dates = [datetime.strptime(exp.date, "%Y-%m-%d") for exp in self.expenses]
        min_date = min(dates)
        max_date = max(dates)

        # Calculate number of months
        months_diff = (max_date.year - min_date.year) * 12 + (max_date.month - min_date.month) + 1

        category_totals = self.calculate_total_by_category()

        return {
            cat: utils.safe_divide(total, months_diff)
            for cat, total in category_totals.items()
        }

    def analyze_expense_ratios(
        self,
        annual_gross_income: float
    ) -> Dict[str, Any]:
        """
        Analyze expense ratios as percentage of gross income.

        Args:
            annual_gross_income: Annual gross rental income

        Returns:
            Dictionary with expense ratio analysis
        """
        category_totals = self.calculate_total_by_category()
        total_expenses = self.calculate_total_expenses()

        # Calculate ratios
        expense_ratios = {}
        warnings = []

        for category, amount in category_totals.items():
            if amount == 0:
                continue

            ratio = utils.safe_percentage(amount, annual_gross_income)
            expense_ratios[category] = {
                "amount": amount,
                "ratio": ratio,
                "ratio_percentage": ratio * 100
            }

            # Check against typical ranges
            if category in self.TYPICAL_EXPENSE_RANGES:
                low, high = self.TYPICAL_EXPENSE_RANGES[category]
                if ratio > high:
                    warnings.append(
                        f"{self.EXPENSE_CATEGORIES[category]} is {ratio*100:.1f}% of income "
                        f"(typical: {low*100:.1f}-{high*100:.1f}%)"
                    )

        # Calculate NOI
        noi = annual_gross_income - total_expenses
        noi_margin = utils.safe_percentage(noi, annual_gross_income)

        return {
            "total_expenses": total_expenses,
            "annual_gross_income": annual_gross_income,
            "net_operating_income": noi,
            "noi_margin": noi_margin,
            "expense_ratio": utils.safe_percentage(total_expenses, annual_gross_income),
            "expense_ratios_by_category": expense_ratios,
            "warnings": warnings
        }

    def compare_to_budget(
        self,
        budgeted_expenses: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Compare actual expenses to budgeted amounts.

        Args:
            budgeted_expenses: Dictionary of budgeted amounts by category

        Returns:
            Dictionary with budget variance analysis
        """
        actual_totals = self.calculate_total_by_category()
        variances = {}

        total_actual = 0.0
        total_budget = 0.0

        for category in self.EXPENSE_CATEGORIES:
            actual = actual_totals.get(category, 0.0)
            budget = budgeted_expenses.get(category, 0.0)

            if budget > 0:
                variance = actual - budget
                variance_percent = utils.safe_percentage(variance, budget)

                variances[category] = {
                    "budgeted": budget,
                    "actual": actual,
                    "variance": variance,
                    "variance_percent": variance_percent,
                    "status": "over_budget" if variance > 0 else "under_budget"
                }

                total_actual += actual
                total_budget += budget

        total_variance = total_actual - total_budget
        total_variance_percent = utils.safe_percentage(total_variance, total_budget)

        return {
            "total_budgeted": total_budget,
            "total_actual": total_actual,
            "total_variance": total_variance,
            "total_variance_percent": total_variance_percent,
            "category_variances": variances,
            "over_budget": total_variance > 0
        }

    def get_expenses_by_date_range(
        self,
        start_date: str,
        end_date: str
    ) -> List[Expense]:
        """
        Get expenses within a date range.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of expenses in date range
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        filtered_expenses = []
        for expense in self.expenses:
            expense_date = datetime.strptime(expense.date, "%Y-%m-%d")
            if start <= expense_date <= end:
                filtered_expenses.append(expense)

        return filtered_expenses

    def generate_expense_report(
        self,
        annual_gross_income: Optional[float] = None
    ) -> str:
        """
        Generate human-readable expense report.

        Args:
            annual_gross_income: Optional annual gross income for ratio analysis

        Returns:
            Formatted expense report
        """
        category_totals = self.calculate_total_by_category()
        total_expenses = self.calculate_total_expenses()
        monthly_avg = self.calculate_monthly_average()

        report_lines = [
            "=== EXPENSE REPORT ===",
            "",
            f"Total Expenses: {utils.format_currency(total_expenses)}",
            f"Total Transactions: {len(self.expenses)}",
            ""
        ]

        if annual_gross_income:
            ratio_analysis = self.analyze_expense_ratios(annual_gross_income)
            report_lines.extend([
                "EXPENSE ANALYSIS:",
                f"  Annual Gross Income: {utils.format_currency(annual_gross_income)}",
                f"  Total Expenses: {utils.format_currency(total_expenses)}",
                f"  Net Operating Income: {utils.format_currency(ratio_analysis['net_operating_income'])}",
                f"  NOI Margin: {utils.format_percentage(ratio_analysis['noi_margin'])}",
                f"  Operating Expense Ratio: {utils.format_percentage(ratio_analysis['expense_ratio'])}",
                ""
            ])

            if ratio_analysis['warnings']:
                report_lines.append("WARNINGS:")
                for warning in ratio_analysis['warnings']:
                    report_lines.append(f"  ⚠ {warning}")
                report_lines.append("")

        report_lines.append("EXPENSES BY CATEGORY:")

        # Sort categories by amount (highest first)
        sorted_categories = sorted(
            [(cat, amt) for cat, amt in category_totals.items() if amt > 0],
            key=lambda x: x[1],
            reverse=True
        )

        for category, amount in sorted_categories:
            cat_name = self.EXPENSE_CATEGORIES[category]
            monthly = monthly_avg[category]

            line = f"  {cat_name}: {utils.format_currency(amount)}"
            if monthly > 0:
                line += f" (avg {utils.format_currency(monthly)}/month)"

            if annual_gross_income:
                ratio = utils.safe_percentage(amount, annual_gross_income)
                line += f" [{utils.format_percentage(ratio)} of income]"

            report_lines.append(line)

        return "\n".join(report_lines)

    def estimate_annual_operating_expenses(
        self,
        gross_annual_income: float,
        expense_ratio: float = 0.35
    ) -> Dict[str, float]:
        """
        Estimate annual operating expenses based on income.

        Args:
            gross_annual_income: Annual gross rental income
            expense_ratio: Estimated operating expense ratio (default: 0.35 or 35%)

        Returns:
            Dictionary with estimated expenses by category
        """
        total_operating_expenses = gross_annual_income * expense_ratio

        # Distribute across categories using typical ranges (midpoint)
        estimated_expenses = {}

        # Calculate based on typical percentages
        for category, (low, high) in self.TYPICAL_EXPENSE_RANGES.items():
            midpoint = (low + high) / 2
            estimated_expenses[category] = gross_annual_income * midpoint

        # Calculate remaining for categories without typical ranges
        accounted_for = sum(estimated_expenses.values())
        remaining = total_operating_expenses - accounted_for

        # Distribute remaining to other categories
        other_categories = [cat for cat in self.EXPENSE_CATEGORIES if cat not in estimated_expenses]
        if other_categories:
            per_category = remaining / len(other_categories)
            for category in other_categories:
                estimated_expenses[category] = per_category

        return estimated_expenses
