"""
Rental income projection module for Airbnb Investment Analyzer.
Projects rental income based on comparable properties, seasonality, and occupancy modeling.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import statistics
import utils


@dataclass
class ComparableProperty:
    """Data class for comparable property."""
    listing_id: str
    nightly_rate: float
    occupancy_rate: float
    bedrooms: int
    bathrooms: float
    reviews_count: int
    rating: float
    distance_miles: float


@dataclass
class SeasonalFactor:
    """Data class for seasonal adjustment factors."""
    month: str
    demand_multiplier: float  # 1.0 = average, >1.0 = high season, <1.0 = low season


class RentalIncomeProjector:
    """Project rental income for Airbnb properties."""

    # Default seasonal patterns (can be overridden with actual data)
    DEFAULT_SEASONALITY = {
        "beach_market": {
            "January": 0.7, "February": 0.8, "March": 1.1, "April": 1.2,
            "May": 1.3, "June": 1.5, "July": 1.6, "August": 1.5,
            "September": 1.2, "October": 1.0, "November": 0.8, "December": 0.9
        },
        "ski_market": {
            "January": 1.6, "February": 1.5, "March": 1.3, "April": 0.9,
            "May": 0.7, "June": 0.8, "July": 0.9, "August": 0.9,
            "September": 0.8, "October": 1.0, "November": 1.2, "December": 1.5
        },
        "urban_business": {
            "January": 1.1, "February": 1.1, "March": 1.2, "April": 1.2,
            "May": 1.1, "June": 1.0, "July": 0.8, "August": 0.9,
            "September": 1.2, "October": 1.3, "November": 1.2, "December": 0.9
        },
        "year_round": {
            "January": 1.0, "February": 1.0, "March": 1.0, "April": 1.0,
            "May": 1.0, "June": 1.0, "July": 1.0, "August": 1.0,
            "September": 1.0, "October": 1.0, "November": 1.0, "December": 1.0
        }
    }

    def __init__(
        self,
        subject_property: Dict[str, Any],
        comparable_properties: List[ComparableProperty]
    ):
        """
        Initialize rental income projector.

        Args:
            subject_property: Dictionary with subject property details
            comparable_properties: List of ComparableProperty instances
        """
        self.subject = subject_property
        self.comps = comparable_properties

    def calculate_average_nightly_rate(
        self,
        weight_by_similarity: bool = True
    ) -> float:
        """
        Calculate average nightly rate from comparables.

        Args:
            weight_by_similarity: Weight by distance and bedroom similarity

        Returns:
            Average nightly rate
        """
        if not self.comps:
            return 0.0

        if not weight_by_similarity:
            # Simple average
            return statistics.mean([comp.nightly_rate for comp in self.comps])

        # Weighted average based on similarity
        weighted_sum = 0.0
        weight_sum = 0.0

        subject_bedrooms = self.subject.get("bedrooms", 3)

        for comp in self.comps:
            # Calculate similarity weight (1.0 = perfect match, decreases with differences)
            bedroom_diff = abs(comp.bedrooms - subject_bedrooms)
            bedroom_weight = max(0.5, 1.0 - (bedroom_diff * 0.2))  # Penalty for bedroom difference

            distance_weight = max(0.5, 1.0 - (comp.distance_miles * 0.1))  # Penalty for distance

            # Rating weight (higher rated properties weighted more)
            rating_weight = comp.rating / 5.0 if comp.rating > 0 else 0.8

            # Combined weight
            total_weight = bedroom_weight * distance_weight * rating_weight

            weighted_sum += comp.nightly_rate * total_weight
            weight_sum += total_weight

        return utils.safe_divide(weighted_sum, weight_sum)

    def calculate_average_occupancy_rate(self) -> float:
        """
        Calculate average occupancy rate from comparables.

        Returns:
            Average occupancy rate as decimal (e.g., 0.70 for 70%)
        """
        if not self.comps:
            return 0.65  # Default conservative estimate

        # Weight by review count (more reviews = more reliable data)
        weighted_sum = 0.0
        weight_sum = 0.0

        for comp in self.comps:
            # Use review count as weight (more reviews = more bookings = more reliable)
            weight = max(1, comp.reviews_count)
            weighted_sum += comp.occupancy_rate * weight
            weight_sum += weight

        return utils.safe_divide(weighted_sum, weight_sum, default=0.65)

    def project_annual_income(
        self,
        seasonality_type: str = "year_round",
        custom_seasonality: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Project annual rental income with seasonal adjustments.

        Args:
            seasonality_type: Type of market seasonality ("beach_market", "ski_market", "urban_business", "year_round")
            custom_seasonality: Custom monthly multipliers (overrides seasonality_type if provided)

        Returns:
            Dictionary with annual income projection
        """
        avg_nightly_rate = self.calculate_average_nightly_rate()
        base_occupancy_rate = self.calculate_average_occupancy_rate()

        # Get seasonal factors
        if custom_seasonality:
            seasonal_factors = custom_seasonality
        else:
            seasonal_factors = self.DEFAULT_SEASONALITY.get(seasonality_type, self.DEFAULT_SEASONALITY["year_round"])

        # Calculate monthly projections
        monthly_projections = []
        total_annual_income = 0.0

        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        for month, days in zip(months, days_per_month):
            seasonal_multiplier = seasonal_factors.get(month, 1.0)

            # Adjust rate and occupancy for seasonality
            adjusted_rate = avg_nightly_rate * seasonal_multiplier
            # Occupancy also varies with season (high demand = higher occupancy)
            adjusted_occupancy = min(0.95, base_occupancy_rate * seasonal_multiplier)

            # Calculate monthly income
            monthly_income = adjusted_rate * days * adjusted_occupancy

            monthly_projections.append({
                "month": month,
                "days": days,
                "avg_nightly_rate": adjusted_rate,
                "occupancy_rate": adjusted_occupancy,
                "nights_booked": days * adjusted_occupancy,
                "gross_income": monthly_income
            })

            total_annual_income += monthly_income

        return {
            "annual_gross_income": total_annual_income,
            "average_monthly_income": total_annual_income / 12,
            "base_nightly_rate": avg_nightly_rate,
            "base_occupancy_rate": base_occupancy_rate,
            "seasonality_type": seasonality_type,
            "monthly_projections": monthly_projections,
            "comparables_used": len(self.comps)
        }

    def calculate_income_range(
        self,
        confidence_level: str = "conservative"
    ) -> Dict[str, float]:
        """
        Calculate income range based on confidence level.

        Args:
            confidence_level: "conservative", "realistic", or "optimistic"

        Returns:
            Dictionary with low, mid, and high income projections
        """
        base_projection = self.project_annual_income()
        base_income = base_projection["annual_gross_income"]

        if confidence_level == "conservative":
            # Conservative: -15% from base
            return {
                "low": base_income * 0.85,
                "mid": base_income,
                "high": base_income * 1.05,
                "confidence_level": "conservative"
            }
        elif confidence_level == "realistic":
            # Realistic: -10% to +10% from base
            return {
                "low": base_income * 0.90,
                "mid": base_income,
                "high": base_income * 1.10,
                "confidence_level": "realistic"
            }
        else:  # optimistic
            # Optimistic: base to +20%
            return {
                "low": base_income,
                "mid": base_income * 1.10,
                "high": base_income * 1.20,
                "confidence_level": "optimistic"
            }

    def analyze_comp_quality(self) -> Dict[str, Any]:
        """
        Analyze quality and reliability of comparable properties.

        Returns:
            Dictionary with comp quality analysis
        """
        if not self.comps:
            return {
                "quality_score": 0,
                "reliability": "No comparables",
                "warnings": ["No comparable properties provided"]
            }

        # Calculate quality metrics
        avg_reviews = statistics.mean([comp.reviews_count for comp in self.comps])
        avg_rating = statistics.mean([comp.rating for comp in self.comps if comp.rating > 0])
        avg_distance = statistics.mean([comp.distance_miles for comp in self.comps])

        # Calculate quality score (0-100)
        review_score = min(100, (avg_reviews / 50) * 40)  # 50+ reviews = max score
        rating_score = (avg_rating / 5.0) * 40  # 5.0 rating = max score
        distance_score = max(0, 20 - (avg_distance * 2))  # Closer = better

        quality_score = review_score + rating_score + distance_score

        # Determine reliability
        if quality_score >= 80:
            reliability = "Excellent"
        elif quality_score >= 60:
            reliability = "Good"
        elif quality_score >= 40:
            reliability = "Fair"
        else:
            reliability = "Poor"

        # Generate warnings
        warnings = []
        if len(self.comps) < 3:
            warnings.append("Limited number of comparables (recommend 5+)")
        if avg_reviews < 10:
            warnings.append("Comparables have low review counts (may not be representative)")
        if avg_rating < 4.0:
            warnings.append("Comparables have below-average ratings")
        if avg_distance > 5:
            warnings.append("Comparables are far from subject property (>5 miles)")

        return {
            "quality_score": round(quality_score, 2),
            "reliability": reliability,
            "comparables_count": len(self.comps),
            "avg_reviews": round(avg_reviews, 1),
            "avg_rating": round(avg_rating, 2),
            "avg_distance_miles": round(avg_distance, 2),
            "warnings": warnings
        }

    def generate_income_report(self) -> str:
        """
        Generate human-readable income projection report.

        Returns:
            Formatted report string
        """
        projection = self.project_annual_income()
        comp_quality = self.analyze_comp_quality()
        income_range = self.calculate_income_range(confidence_level="realistic")

        report_lines = [
            "=== RENTAL INCOME PROJECTION ===",
            "",
            "COMPARABLE PROPERTIES ANALYSIS:",
            f"  Comparables Used: {projection['comparables_used']}",
            f"  Data Quality: {comp_quality['reliability']} (score: {comp_quality['quality_score']:.1f}/100)",
            f"  Average Reviews per Comp: {comp_quality['avg_reviews']:.0f}",
            f"  Average Rating: {comp_quality['avg_rating']:.2f}/5.0",
            ""
        ]

        if comp_quality['warnings']:
            report_lines.append("WARNINGS:")
            for warning in comp_quality['warnings']:
                report_lines.append(f"  ⚠ {warning}")
            report_lines.append("")

        report_lines.extend([
            "BASE PROJECTIONS:",
            f"  Average Nightly Rate: {utils.format_currency(projection['base_nightly_rate'])}",
            f"  Average Occupancy Rate: {utils.format_percentage(projection['base_occupancy_rate'])}",
            f"  Seasonality Type: {projection['seasonality_type']}",
            "",
            "ANNUAL INCOME PROJECTION:",
            f"  Annual Gross Income: {utils.format_currency(projection['annual_gross_income'])}",
            f"  Average Monthly Income: {utils.format_currency(projection['average_monthly_income'])}",
            "",
            "INCOME RANGE (Realistic Scenario):",
            f"  Low: {utils.format_currency(income_range['low'])}",
            f"  Mid: {utils.format_currency(income_range['mid'])}",
            f"  High: {utils.format_currency(income_range['high'])}",
            "",
            "TOP MONTHS (by projected income):"
        ])

        # Sort months by income
        sorted_months = sorted(
            projection['monthly_projections'],
            key=lambda x: x['gross_income'],
            reverse=True
        )

        for month_data in sorted_months[:3]:
            report_lines.append(
                f"  {month_data['month']}: {utils.format_currency(month_data['gross_income'])} "
                f"({month_data['occupancy_rate']*100:.1f}% occupancy)"
            )

        return "\n".join(report_lines)

    def compare_to_target(self, target_monthly_income: float) -> Dict[str, Any]:
        """
        Compare projected income to target income goal.

        Args:
            target_monthly_income: Target monthly income goal

        Returns:
            Dictionary with comparison analysis
        """
        projection = self.project_annual_income()
        actual_monthly = projection['average_monthly_income']
        target_annual = target_monthly_income * 12

        variance = actual_monthly - target_monthly_income
        variance_percent = utils.safe_percentage(variance, target_monthly_income)

        meets_target = actual_monthly >= target_monthly_income

        # Calculate what would be needed to meet target
        if not meets_target:
            current_rate = projection['base_nightly_rate']
            current_occupancy = projection['base_occupancy_rate']

            # Calculate required rate at same occupancy
            required_annual = target_annual
            nights_per_year = 365 * current_occupancy
            required_rate = utils.safe_divide(required_annual, nights_per_year)

            # Calculate required occupancy at same rate
            potential_annual_at_100_occ = current_rate * 365
            required_occupancy = utils.safe_divide(required_annual, potential_annual_at_100_occ)

            improvement_needed = {
                "rate_increase_needed": required_rate - current_rate,
                "rate_increase_percent": utils.safe_percentage(required_rate - current_rate, current_rate),
                "OR_occupancy_increase_needed": required_occupancy - current_occupancy,
                "OR_occupancy_increase_percent": utils.safe_percentage(required_occupancy - current_occupancy, current_occupancy)
            }
        else:
            improvement_needed = None

        return {
            "target_monthly_income": target_monthly_income,
            "projected_monthly_income": actual_monthly,
            "variance": variance,
            "variance_percent": variance_percent,
            "meets_target": meets_target,
            "improvement_needed": improvement_needed
        }
