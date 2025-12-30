"""
Property valuation module for Airbnb Investment Analyzer.
Performs property valuations using multiple approaches (income, sales comparison, GRM).
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import statistics
import utils


@dataclass
class SalesComparable:
    """Data class for sales comparable property."""
    address: str
    sale_price: float
    sale_date: str
    bedrooms: int
    bathrooms: float
    square_feet: int
    distance_miles: float


class PropertyValuator:
    """Perform property valuations using multiple approaches."""

    def __init__(self, subject_property: Dict[str, Any]):
        """
        Initialize property valuator.

        Args:
            subject_property: Dictionary with subject property characteristics
        """
        self.subject = subject_property

    def income_approach_valuation(
        self,
        annual_noi: float,
        cap_rate: float
    ) -> Dict[str, Any]:
        """
        Value property using income capitalization approach.

        Property Value = Net Operating Income / Capitalization Rate

        Args:
            annual_noi: Annual Net Operating Income
            cap_rate: Capitalization rate (as decimal, e.g., 0.08 for 8%)

        Returns:
            Dictionary with valuation details
        """
        utils.validate_positive(annual_noi, "Annual NOI")
        utils.validate_positive(cap_rate, "Cap rate")

        property_value = utils.safe_divide(annual_noi, cap_rate)

        return {
            "approach": "Income Capitalization",
            "annual_noi": annual_noi,
            "cap_rate": cap_rate,
            "estimated_value": property_value,
            "value_per_sqft": utils.safe_divide(property_value, self.subject.get("square_feet", 1)),
            "assumptions": [
                f"Cap rate of {cap_rate*100:.2f}% is appropriate for this market",
                "NOI is stabilized and sustainable",
                "Property condition is average to good"
            ]
        }

    def gross_rent_multiplier_valuation(
        self,
        annual_gross_income: float,
        market_grm: float
    ) -> Dict[str, Any]:
        """
        Value property using Gross Rent Multiplier (GRM) approach.

        Property Value = Annual Gross Income × GRM

        Args:
            annual_gross_income: Annual gross rental income
            market_grm: Market Gross Rent Multiplier

        Returns:
            Dictionary with valuation details
        """
        utils.validate_positive(annual_gross_income, "Annual gross income")
        utils.validate_positive(market_grm, "GRM")

        property_value = annual_gross_income * market_grm

        return {
            "approach": "Gross Rent Multiplier",
            "annual_gross_income": annual_gross_income,
            "market_grm": market_grm,
            "estimated_value": property_value,
            "value_per_sqft": utils.safe_divide(property_value, self.subject.get("square_feet", 1)),
            "assumptions": [
                f"Market GRM of {market_grm:.2f} is appropriate",
                "Gross income is representative of market",
                "Property is typical for the area"
            ]
        }

    def sales_comparison_approach(
        self,
        comparable_sales: List[SalesComparable]
    ) -> Dict[str, Any]:
        """
        Value property using sales comparison approach.

        Args:
            comparable_sales: List of SalesComparable instances

        Returns:
            Dictionary with valuation details
        """
        if not comparable_sales:
            return {
                "approach": "Sales Comparison",
                "estimated_value": 0,
                "error": "No comparable sales provided"
            }

        subject_sqft = self.subject.get("square_feet", 0)
        subject_bedrooms = self.subject.get("bedrooms", 0)
        subject_bathrooms = self.subject.get("bathrooms", 0)

        if subject_sqft == 0:
            return {
                "approach": "Sales Comparison",
                "estimated_value": 0,
                "error": "Subject property square footage required"
            }

        # Calculate price per square foot for each comp
        adjusted_values = []

        for comp in comparable_sales:
            if comp.square_feet == 0:
                continue

            price_per_sqft = comp.sale_price / comp.square_feet

            # Apply adjustments for differences
            adjustment_factor = 1.0

            # Bedroom adjustment (+/- 5% per bedroom difference)
            bedroom_diff = subject_bedrooms - comp.bedrooms
            adjustment_factor += (bedroom_diff * 0.05)

            # Bathroom adjustment (+/- 3% per bathroom difference)
            bathroom_diff = subject_bathrooms - comp.bathrooms
            adjustment_factor += (bathroom_diff * 0.03)

            # Distance adjustment (reduce value by 2% per mile away)
            adjustment_factor -= (comp.distance_miles * 0.02)

            # Ensure adjustment factor is reasonable
            adjustment_factor = max(0.7, min(1.3, adjustment_factor))

            # Adjusted price per sqft
            adjusted_price_per_sqft = price_per_sqft * adjustment_factor

            # Calculate subject property value using this comp
            comp_indicated_value = adjusted_price_per_sqft * subject_sqft

            adjusted_values.append({
                "comp_address": comp.address,
                "sale_price": comp.sale_price,
                "price_per_sqft": price_per_sqft,
                "adjustment_factor": adjustment_factor,
                "adjusted_price_per_sqft": adjusted_price_per_sqft,
                "indicated_value": comp_indicated_value
            })

        # Calculate average indicated value
        indicated_values = [av["indicated_value"] for av in adjusted_values]
        avg_value = statistics.mean(indicated_values)
        median_value = statistics.median(indicated_values)

        # Use median to reduce impact of outliers
        estimated_value = median_value

        return {
            "approach": "Sales Comparison",
            "estimated_value": estimated_value,
            "value_range": {
                "low": min(indicated_values),
                "high": max(indicated_values),
                "average": avg_value,
                "median": median_value
            },
            "price_per_sqft": estimated_value / subject_sqft,
            "comparables_used": len(comparable_sales),
            "comparable_details": adjusted_values,
            "assumptions": [
                "Comparables are recent (within 6 months)",
                "Adjustments are appropriate for market",
                "Properties are in similar condition"
            ]
        }

    def calculate_airbnb_specific_value(
        self,
        annual_airbnb_income: float,
        market_cap_rate: float,
        premium_multiplier: float = 1.1
    ) -> Dict[str, Any]:
        """
        Calculate Airbnb-specific property value with premium.

        Airbnb properties may command premium over traditional rentals.

        Args:
            annual_airbnb_income: Annual Airbnb net operating income
            market_cap_rate: Market cap rate for traditional rentals
            premium_multiplier: Premium for Airbnb income (default: 1.1 = 10% premium)

        Returns:
            Dictionary with Airbnb-specific valuation
        """
        # Base value using income approach
        base_value = utils.safe_divide(annual_airbnb_income, market_cap_rate)

        # Apply Airbnb premium
        airbnb_value = base_value * premium_multiplier

        # Calculate implied cap rate for Airbnb
        implied_cap_rate = utils.safe_divide(annual_airbnb_income, airbnb_value)

        return {
            "approach": "Airbnb Income Approach",
            "annual_airbnb_noi": annual_airbnb_income,
            "market_cap_rate": market_cap_rate,
            "premium_multiplier": premium_multiplier,
            "base_value": base_value,
            "airbnb_specific_value": airbnb_value,
            "implied_airbnb_cap_rate": implied_cap_rate,
            "premium_amount": airbnb_value - base_value,
            "assumptions": [
                f"Airbnb income commands {(premium_multiplier-1)*100:.0f}% premium",
                "Short-term rental regulations remain favorable",
                "Market demand for STR continues",
                "Property is well-suited for Airbnb use"
            ]
        }

    def reconcile_valuations(
        self,
        valuations: List[Dict[str, Any]],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Reconcile multiple valuation approaches into final estimate.

        Args:
            valuations: List of valuation dictionaries from different approaches
            weights: Optional weights for each approach (by approach name)

        Returns:
            Dictionary with reconciled final value
        """
        if not valuations:
            return {"error": "No valuations to reconcile"}

        # Default equal weighting if not provided
        if weights is None:
            weights = {v["approach"]: 1.0 for v in valuations}

        # Calculate weighted average
        weighted_sum = 0.0
        weight_total = 0.0

        valuation_summary = []

        for valuation in valuations:
            approach = valuation["approach"]
            value = valuation.get("estimated_value", 0)

            if value > 0:
                weight = weights.get(approach, 1.0)
                weighted_sum += value * weight
                weight_total += weight

                valuation_summary.append({
                    "approach": approach,
                    "value": value,
                    "weight": weight,
                    "weighted_contribution": value * weight
                })

        final_value = utils.safe_divide(weighted_sum, weight_total)

        # Calculate value range
        values = [v.get("estimated_value", 0) for v in valuations if v.get("estimated_value", 0) > 0]

        if values:
            value_range = {
                "low": min(values),
                "high": max(values),
                "spread": max(values) - min(values),
                "spread_percent": utils.safe_percentage(max(values) - min(values), final_value)
            }
        else:
            value_range = None

        return {
            "final_estimated_value": final_value,
            "value_range": value_range,
            "valuation_approaches": valuation_summary,
            "confidence_level": self._assess_confidence(value_range) if value_range else "Low"
        }

    def _assess_confidence(self, value_range: Dict[str, float]) -> str:
        """
        Assess confidence level based on value range spread.

        Args:
            value_range: Dictionary with value range data

        Returns:
            Confidence level string
        """
        spread_percent = value_range.get("spread_percent", 1.0)

        if spread_percent < 0.10:
            return "High"
        elif spread_percent < 0.20:
            return "Moderate"
        else:
            return "Low"

    def generate_valuation_report(
        self,
        valuations: List[Dict[str, Any]],
        weights: Optional[Dict[str, float]] = None
    ) -> str:
        """
        Generate comprehensive valuation report.

        Args:
            valuations: List of valuation dictionaries
            weights: Optional weights for reconciliation

        Returns:
            Formatted valuation report
        """
        reconciliation = self.reconcile_valuations(valuations, weights)

        report_lines = [
            "=== PROPERTY VALUATION REPORT ===",
            "",
            "SUBJECT PROPERTY:",
            f"  Bedrooms: {self.subject.get('bedrooms', 'N/A')}",
            f"  Bathrooms: {self.subject.get('bathrooms', 'N/A')}",
            f"  Square Feet: {self.subject.get('square_feet', 'N/A'):,}",
            f"  Location: {self.subject.get('location', 'N/A')}",
            "",
            "VALUATION APPROACHES:"
        ]

        for valuation in valuations:
            approach = valuation["approach"]
            value = valuation.get("estimated_value", 0)

            if value > 0:
                report_lines.append(f"\n{approach}:")
                report_lines.append(f"  Estimated Value: {utils.format_currency(value)}")

                # Add approach-specific details
                if "price_per_sqft" in valuation:
                    report_lines.append(f"  Price per Sq Ft: {utils.format_currency(valuation['price_per_sqft'])}")

                if "cap_rate" in valuation:
                    report_lines.append(f"  Cap Rate: {utils.format_percentage(valuation['cap_rate'])}")

                if "market_grm" in valuation:
                    report_lines.append(f"  GRM: {valuation['market_grm']:.2f}")

                if "comparables_used" in valuation:
                    report_lines.append(f"  Comparables Used: {valuation['comparables_used']}")

                if "assumptions" in valuation:
                    report_lines.append("  Key Assumptions:")
                    for assumption in valuation["assumptions"]:
                        report_lines.append(f"    - {assumption}")

        report_lines.extend([
            "",
            "RECONCILIATION:",
            f"  Final Estimated Value: {utils.format_currency(reconciliation['final_estimated_value'])}"
        ])

        if reconciliation.get("value_range"):
            vr = reconciliation["value_range"]
            report_lines.extend([
                f"  Value Range: {utils.format_currency(vr['low'])} - {utils.format_currency(vr['high'])}",
                f"  Range Spread: {utils.format_percentage(vr['spread_percent'])}",
                f"  Confidence Level: {reconciliation['confidence_level']}"
            ])

        return "\n".join(report_lines)
