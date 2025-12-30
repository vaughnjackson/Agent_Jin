"""
Comparative analysis module for Airbnb Investment Analyzer.
Compares multiple properties side-by-side with scoring and ranking.
"""

from typing import Dict, List, Any, Optional
import statistics
import utils


class ComparativeAnalyzer:
    """Compare multiple Airbnb investment properties."""

    # Scoring weights for overall property score
    DEFAULT_WEIGHTS = {
        "financial_performance": 0.40,  # ROI, cash flow, cap rate
        "market_strength": 0.25,        # Location, demand, competition
        "risk_factors": 0.20,           # Regulatory, market saturation
        "operational_ease": 0.15        # Management, maintenance, turnover
    }

    def __init__(self, properties: List[Dict[str, Any]]):
        """
        Initialize comparative analyzer.

        Args:
            properties: List of property dictionaries with financial and market data
        """
        self.properties = properties

    def score_financial_performance(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score property based on financial metrics.

        Args:
            property_data: Property data including financial metrics

        Returns:
            Dictionary with financial score and breakdown
        """
        metrics = property_data.get("metrics", {})

        # Extract key metrics
        cap_rate = metrics.get("cap_rate", 0)
        coc_return = metrics.get("cash_on_cash_return", 0)
        monthly_cash_flow = metrics.get("monthly_cash_flow", 0)
        dscr = metrics.get("debt_service_coverage_ratio", 1.0)

        # Score each metric (0-100)
        scores = {}

        # Cap rate score (8% = 80 points, 12% = 100 points)
        scores["cap_rate"] = min(100, (cap_rate / 0.12) * 100)

        # Cash-on-cash return score (10% = 67 points, 15% = 100 points)
        scores["coc_return"] = min(100, (coc_return / 0.15) * 100)

        # Cash flow score ($500/month = 100 points)
        scores["cash_flow"] = min(100, (monthly_cash_flow / 500) * 100)

        # DSCR score (1.25 = 100 points)
        scores["dscr"] = min(100, (dscr / 1.25) * 100)

        # Weighted average
        overall_score = (
            scores["cap_rate"] * 0.30 +
            scores["coc_return"] * 0.35 +
            scores["cash_flow"] * 0.25 +
            scores["dscr"] * 0.10
        )

        return {
            "overall_financial_score": overall_score,
            "component_scores": scores,
            "grade": self._score_to_grade(overall_score)
        }

    def score_market_strength(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score property based on market factors.

        Args:
            property_data: Property data including market information

        Returns:
            Dictionary with market score and breakdown
        """
        market = property_data.get("market", {})

        # Extract market factors
        occupancy_rate = market.get("avg_occupancy_rate", 0.65)
        competition_level = market.get("competition_level", "Medium")
        tourism_score = market.get("tourism_score", 5)  # 1-10 scale
        regulatory_score = market.get("regulatory_friendliness", 5)  # 1-10 scale

        scores = {}

        # Occupancy score (75% = 100 points)
        scores["occupancy"] = min(100, (occupancy_rate / 0.75) * 100)

        # Competition score (inverse - Low = 100, High = 50)
        competition_scores = {"Low": 100, "Medium": 75, "High": 50}
        scores["competition"] = competition_scores.get(competition_level, 75)

        # Tourism score (10 = 100 points)
        scores["tourism"] = tourism_score * 10

        # Regulatory score (10 = 100 points)
        scores["regulatory"] = regulatory_score * 10

        # Weighted average
        overall_score = (
            scores["occupancy"] * 0.30 +
            scores["competition"] * 0.25 +
            scores["tourism"] * 0.25 +
            scores["regulatory"] * 0.20
        )

        return {
            "overall_market_score": overall_score,
            "component_scores": scores,
            "grade": self._score_to_grade(overall_score)
        }

    def score_risk_factors(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score property based on risk factors (lower risk = higher score).

        Args:
            property_data: Property data including risk information

        Returns:
            Dictionary with risk score and breakdown
        """
        risk = property_data.get("risk", {})
        market = property_data.get("market", {})

        # Extract risk factors
        regulatory_risk = risk.get("regulatory_risk", "Medium")  # Low/Medium/High
        market_saturation = market.get("saturation_level", "Medium")
        property_age = property_data.get("property_age_years", 20)
        vacancy_risk = 1 - market.get("avg_occupancy_rate", 0.65)

        scores = {}

        # Regulatory risk (Low = 100, High = 40)
        reg_risk_scores = {"Low": 100, "Medium": 70, "High": 40}
        scores["regulatory_risk"] = reg_risk_scores.get(regulatory_risk, 70)

        # Market saturation (Low = 100, High = 50)
        saturation_scores = {"Low": 100, "Medium": 75, "High": 50}
        scores["market_saturation"] = saturation_scores.get(market_saturation, 75)

        # Property age risk (newer = better, 0-10 years = 100, 30+ years = 60)
        age_score = max(60, 100 - (property_age * 1.3))
        scores["property_age"] = age_score

        # Vacancy risk (lower vacancy = higher score)
        scores["vacancy_risk"] = max(0, 100 - (vacancy_risk * 200))

        # Weighted average (higher score = lower risk)
        overall_score = (
            scores["regulatory_risk"] * 0.35 +
            scores["market_saturation"] * 0.30 +
            scores["property_age"] * 0.20 +
            scores["vacancy_risk"] * 0.15
        )

        return {
            "overall_risk_score": overall_score,
            "component_scores": scores,
            "grade": self._score_to_grade(overall_score),
            "risk_level": "Low" if overall_score >= 80 else "Medium" if overall_score >= 60 else "High"
        }

    def score_operational_ease(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score property based on operational factors.

        Args:
            property_data: Property data including operational information

        Returns:
            Dictionary with operational score and breakdown
        """
        operational = property_data.get("operational", {})

        # Extract operational factors
        management_available = operational.get("property_management_available", True)
        cleaning_cost = operational.get("avg_cleaning_cost", 100)
        maintenance_level = operational.get("expected_maintenance", "Medium")  # Low/Medium/High
        guest_turnover_days = operational.get("avg_days_between_guests", 3)

        scores = {}

        # Management availability (available = 100, not = 60)
        scores["management"] = 100 if management_available else 60

        # Cleaning cost (lower = better, $75 = 100, $150 = 50)
        scores["cleaning_cost"] = max(50, 100 - ((cleaning_cost - 75) * 0.67))

        # Maintenance level (Low = 100, High = 60)
        maintenance_scores = {"Low": 100, "Medium": 80, "High": 60}
        scores["maintenance"] = maintenance_scores.get(maintenance_level, 80)

        # Turnover efficiency (2 days = 100, 5+ days = 70)
        scores["turnover"] = max(70, 100 - ((guest_turnover_days - 2) * 10))

        # Weighted average
        overall_score = (
            scores["management"] * 0.35 +
            scores["cleaning_cost"] * 0.25 +
            scores["maintenance"] * 0.25 +
            scores["turnover"] * 0.15
        )

        return {
            "overall_operational_score": overall_score,
            "component_scores": scores,
            "grade": self._score_to_grade(overall_score)
        }

    def calculate_overall_property_score(
        self,
        property_data: Dict[str, Any],
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculate overall property investment score.

        Args:
            property_data: Complete property data
            custom_weights: Optional custom weights for scoring categories

        Returns:
            Dictionary with overall score and all component scores
        """
        weights = custom_weights if custom_weights else self.DEFAULT_WEIGHTS

        # Calculate all component scores
        financial = self.score_financial_performance(property_data)
        market = self.score_market_strength(property_data)
        risk = self.score_risk_factors(property_data)
        operational = self.score_operational_ease(property_data)

        # Calculate weighted overall score
        overall_score = (
            financial["overall_financial_score"] * weights["financial_performance"] +
            market["overall_market_score"] * weights["market_strength"] +
            risk["overall_risk_score"] * weights["risk_factors"] +
            operational["overall_operational_score"] * weights["operational_ease"]
        )

        return {
            "property_id": property_data.get("property_id", "Unknown"),
            "property_address": property_data.get("address", "Unknown"),
            "overall_score": overall_score,
            "overall_grade": self._score_to_grade(overall_score),
            "recommendation": self._score_to_recommendation(overall_score),
            "category_scores": {
                "financial_performance": financial,
                "market_strength": market,
                "risk_factors": risk,
                "operational_ease": operational
            },
            "weights_used": weights
        }

    def compare_all_properties(
        self,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Compare all properties and generate ranking.

        Args:
            custom_weights: Optional custom weights for scoring

        Returns:
            Dictionary with comparative analysis and rankings
        """
        property_scores = []

        for prop in self.properties:
            score_data = self.calculate_overall_property_score(prop, custom_weights)
            property_scores.append(score_data)

        # Sort by overall score (highest first)
        property_scores.sort(key=lambda x: x["overall_score"], reverse=True)

        # Add rankings
        for rank, prop_score in enumerate(property_scores, 1):
            prop_score["rank"] = rank

        # Calculate summary statistics
        scores = [ps["overall_score"] for ps in property_scores]
        summary = {
            "total_properties": len(property_scores),
            "average_score": statistics.mean(scores),
            "median_score": statistics.median(scores),
            "score_range": {
                "highest": max(scores),
                "lowest": min(scores)
            }
        }

        return {
            "ranked_properties": property_scores,
            "summary": summary,
            "top_recommendation": property_scores[0] if property_scores else None
        }

    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _score_to_recommendation(self, score: float) -> str:
        """Convert score to investment recommendation."""
        if score >= 85:
            return "Strong Buy"
        elif score >= 75:
            return "Buy"
        elif score >= 65:
            return "Consider"
        elif score >= 55:
            return "Pass"
        else:
            return "Avoid"

    def generate_comparison_report(
        self,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> str:
        """
        Generate human-readable comparison report.

        Args:
            custom_weights: Optional custom weights

        Returns:
            Formatted comparison report
        """
        comparison = self.compare_all_properties(custom_weights)

        report_lines = [
            "=== PROPERTY COMPARISON REPORT ===",
            "",
            f"Total Properties Analyzed: {comparison['summary']['total_properties']}",
            f"Average Score: {comparison['summary']['average_score']:.1f}/100",
            "",
            "RANKED PROPERTIES:"
        ]

        for prop_score in comparison["ranked_properties"]:
            report_lines.extend([
                f"\n#{prop_score['rank']}. {prop_score['property_address']}",
                f"   Overall Score: {prop_score['overall_score']:.1f}/100 (Grade: {prop_score['overall_grade']})",
                f"   Recommendation: {prop_score['recommendation']}",
                "",
                "   Category Scores:"
            ])

            for category, data in prop_score["category_scores"].items():
                cat_display = category.replace("_", " ").title()
                score = data[f"overall_{category.replace('_', '_')}_score"]
                grade = data["grade"]
                report_lines.append(f"     {cat_display}: {score:.1f} ({grade})")

        # Top recommendation details
        if comparison["top_recommendation"]:
            top = comparison["top_recommendation"]
            report_lines.extend([
                "",
                "=== TOP RECOMMENDATION ===",
                f"Property: {top['property_address']}",
                f"Overall Score: {top['overall_score']:.1f}/100",
                f"Recommendation: {top['recommendation']}",
                "",
                "Why this property stands out:"
            ])

            # Highlight best categories
            categories = top["category_scores"]
            best_categories = sorted(
                [(k, v[f"overall_{k}_score"]) for k, v in categories.items()],
                key=lambda x: x[1],
                reverse=True
            )[:2]

            for cat_name, cat_score in best_categories:
                cat_display = cat_name.replace("_", " ").title()
                report_lines.append(f"  - Excellent {cat_display}: {cat_score:.1f}/100")

        return "\n".join(report_lines)

    def side_by_side_comparison(
        self,
        property_indices: List[int]
    ) -> Dict[str, Any]:
        """
        Generate detailed side-by-side comparison of specific properties.

        Args:
            property_indices: List of property indices to compare

        Returns:
            Dictionary with side-by-side comparison data
        """
        selected_properties = [self.properties[i] for i in property_indices if i < len(self.properties)]

        if not selected_properties:
            return {"error": "No valid properties selected"}

        comparison_data = {
            "properties": [],
            "metrics_comparison": {}
        }

        # Collect metrics for each property
        for prop in selected_properties:
            metrics = prop.get("metrics", {})
            market = prop.get("market", {})

            prop_data = {
                "address": prop.get("address", "Unknown"),
                "purchase_price": prop.get("purchase_price", 0),
                "cap_rate": metrics.get("cap_rate", 0),
                "cash_on_cash_return": metrics.get("cash_on_cash_return", 0),
                "monthly_cash_flow": metrics.get("monthly_cash_flow", 0),
                "annual_gross_income": metrics.get("annual_gross_rental_income", 0),
                "occupancy_rate": market.get("avg_occupancy_rate", 0),
                "competition": market.get("competition_level", "Unknown")
            }

            comparison_data["properties"].append(prop_data)

        # Identify best in each metric
        if comparison_data["properties"]:
            metrics_to_compare = ["cap_rate", "cash_on_cash_return", "monthly_cash_flow", "occupancy_rate"]

            for metric in metrics_to_compare:
                values = [(i, p[metric]) for i, p in enumerate(comparison_data["properties"])]
                best_idx, best_value = max(values, key=lambda x: x[1])

                comparison_data["metrics_comparison"][metric] = {
                    "best_property_index": best_idx,
                    "best_value": best_value,
                    "all_values": [v[1] for v in values]
                }

        return comparison_data
