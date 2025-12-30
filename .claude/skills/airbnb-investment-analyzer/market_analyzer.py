"""
Market analysis module for Airbnb Investment Analyzer.
Analyzes Airbnb market prevalence, demand factors, and investment potential across regions.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class MarketMetrics:
    """Data class for market-level metrics."""
    city: str
    state: str
    estimated_active_listings: int
    avg_nightly_rate: float
    avg_occupancy_rate: float
    tourism_score: int  # 1-10 scale
    regulation_friendliness: int  # 1-10 scale (10 = very friendly)
    competition_level: str  # "Low", "Medium", "High"
    market_growth_trend: str  # "Growing", "Stable", "Declining"


class MarketAnalyzer:
    """Analyzes Airbnb markets within a state or region."""

    # Market prevalence factors and scoring
    DEMAND_FACTORS = {
        "tourism_attractions": ["beaches", "mountains", "theme_parks", "historical_sites", "natural_wonders"],
        "business_travel": ["corporate_headquarters", "convention_centers", "airports", "business_districts"],
        "education": ["major_universities", "college_towns", "research_institutions"],
        "events": ["sports_venues", "concert_halls", "festivals", "conferences"],
        "medical": ["major_hospitals", "medical_centers", "health_tourism"]
    }

    REGULATORY_FACTORS = {
        "very_friendly": 9,    # No restrictions, simple registration
        "friendly": 7,         # Light regulations, reasonable fees
        "moderate": 5,         # Some restrictions (90-180 day limits)
        "restrictive": 3,      # Heavy restrictions (30-90 day limits, high fees)
        "very_restrictive": 1  # Near-prohibition or full prohibition
    }

    def __init__(self, state: str):
        """
        Initialize market analyzer for a specific state.

        Args:
            state: State to analyze (e.g., "Texas")
        """
        self.state = state
        self.markets: List[MarketMetrics] = []

    def analyze_market_prevalence(
        self,
        cities_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze where Airbnb is most prevalent in the state and why.

        Args:
            cities_data: List of dictionaries with city-level data

        Returns:
            Dictionary with prevalence analysis and rankings
        """
        ranked_markets = []

        for city_data in cities_data:
            # Calculate market score based on multiple factors
            market_score = self._calculate_market_score(city_data)

            ranked_markets.append({
                "city": city_data["city"],
                "market_score": market_score,
                "active_listings": city_data.get("active_listings", 0),
                "avg_nightly_rate": city_data.get("avg_nightly_rate", 0),
                "avg_occupancy_rate": city_data.get("avg_occupancy_rate", 0),
                "key_demand_drivers": self._identify_demand_drivers(city_data),
                "regulatory_environment": city_data.get("regulatory_environment", "Unknown"),
                "investment_potential": self._assess_investment_potential(city_data, market_score)
            })

        # Sort by market score (highest first)
        ranked_markets.sort(key=lambda x: x["market_score"], reverse=True)

        return {
            "state": self.state,
            "total_markets_analyzed": len(ranked_markets),
            "top_markets": ranked_markets[:10],  # Top 10 markets
            "market_insights": self._generate_market_insights(ranked_markets),
            "prevalence_explanation": self._explain_prevalence_patterns(ranked_markets)
        }

    def _calculate_market_score(self, city_data: Dict[str, Any]) -> float:
        """
        Calculate overall market score (0-100).

        Args:
            city_data: City-level data dictionary

        Returns:
            Market score from 0-100
        """
        # Weighted scoring components
        weights = {
            "demand": 0.35,        # Tourism, business travel, events
            "financial": 0.30,     # Nightly rates, occupancy, revenue potential
            "regulatory": 0.20,    # Regulation friendliness
            "competition": 0.15    # Competition level (inverse)
        }

        # Demand score (0-100)
        demand_score = city_data.get("tourism_score", 5) * 10

        # Financial score (0-100)
        avg_rate = city_data.get("avg_nightly_rate", 100)
        avg_occupancy = city_data.get("avg_occupancy_rate", 0.5)
        potential_monthly_revenue = avg_rate * 30 * avg_occupancy
        financial_score = min((potential_monthly_revenue / 6000) * 100, 100)  # $6k/month = 100 score

        # Regulatory score (0-100)
        reg_environment = city_data.get("regulatory_environment", "moderate")
        regulatory_score = self.REGULATORY_FACTORS.get(reg_environment, 5) * 10

        # Competition score (0-100, inverse - lower competition = higher score)
        competition = city_data.get("competition_level", "Medium")
        competition_scores = {"Low": 90, "Medium": 60, "High": 30}
        competition_score = competition_scores.get(competition, 60)

        # Calculate weighted total
        total_score = (
            demand_score * weights["demand"] +
            financial_score * weights["financial"] +
            regulatory_score * weights["regulatory"] +
            competition_score * weights["competition"]
        )

        return round(total_score, 2)

    def _identify_demand_drivers(self, city_data: Dict[str, Any]) -> List[str]:
        """
        Identify key demand drivers for a market.

        Args:
            city_data: City-level data dictionary

        Returns:
            List of key demand driver categories
        """
        drivers = []

        # Check each demand factor category
        for category, indicators in self.DEMAND_FACTORS.items():
            # Check if any indicators present in city data
            if any(indicator in city_data.get("features", []) for indicator in indicators):
                drivers.append(category)

        return drivers if drivers else ["general_tourism"]

    def _assess_investment_potential(
        self,
        city_data: Dict[str, Any],
        market_score: float
    ) -> str:
        """
        Assess investment potential based on market score and other factors.

        Args:
            city_data: City-level data dictionary
            market_score: Calculated market score

        Returns:
            Investment potential rating
        """
        # Consider market score and growth trend
        growth_trend = city_data.get("market_growth_trend", "Stable")

        if market_score >= 80 and growth_trend == "Growing":
            return "Excellent"
        elif market_score >= 70:
            return "Very Good"
        elif market_score >= 60:
            return "Good"
        elif market_score >= 50:
            return "Fair"
        else:
            return "Poor"

    def _generate_market_insights(self, ranked_markets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate insights about the overall market landscape.

        Args:
            ranked_markets: List of ranked market data

        Returns:
            Dictionary of market insights
        """
        if not ranked_markets:
            return {}

        # Calculate aggregates
        avg_score = sum(m["market_score"] for m in ranked_markets) / len(ranked_markets)
        avg_rate = sum(m["avg_nightly_rate"] for m in ranked_markets) / len(ranked_markets)
        avg_occupancy = sum(m["avg_occupancy_rate"] for m in ranked_markets) / len(ranked_markets)

        # Identify most common demand drivers
        all_drivers = []
        for market in ranked_markets:
            all_drivers.extend(market["key_demand_drivers"])

        driver_counts = {}
        for driver in all_drivers:
            driver_counts[driver] = driver_counts.get(driver, 0) + 1

        top_drivers = sorted(driver_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            "average_market_score": round(avg_score, 2),
            "average_nightly_rate": round(avg_rate, 2),
            "average_occupancy_rate": round(avg_occupancy, 4),
            "most_common_demand_drivers": [driver[0] for driver in top_drivers],
            "markets_with_excellent_potential": sum(1 for m in ranked_markets if m["investment_potential"] == "Excellent"),
            "markets_with_good_plus_potential": sum(1 for m in ranked_markets if m["investment_potential"] in ["Excellent", "Very Good", "Good"])
        }

    def _explain_prevalence_patterns(self, ranked_markets: List[Dict[str, Any]]) -> str:
        """
        Generate explanation of why Airbnb is prevalent in certain areas.

        Args:
            ranked_markets: List of ranked market data

        Returns:
            Explanation string
        """
        if not ranked_markets:
            return "Insufficient data for analysis."

        top_market = ranked_markets[0]

        explanation_parts = [
            f"Airbnb is most prevalent in {top_market['city']} (market score: {top_market['market_score']:.1f}/100) due to several factors:",
            ""
        ]

        # Explain demand drivers
        drivers = top_market["key_demand_drivers"]
        if drivers:
            explanation_parts.append("Key Demand Drivers:")
            for driver in drivers:
                driver_display = driver.replace("_", " ").title()
                explanation_parts.append(f"  - {driver_display}")
            explanation_parts.append("")

        # Explain financial attractiveness
        rate = top_market["avg_nightly_rate"]
        occupancy = top_market["avg_occupancy_rate"]
        monthly_revenue = rate * 30 * occupancy

        explanation_parts.append(f"Financial Performance:")
        explanation_parts.append(f"  - Average nightly rate: ${rate:.2f}")
        explanation_parts.append(f"  - Average occupancy: {occupancy*100:.1f}%")
        explanation_parts.append(f"  - Estimated monthly revenue: ${monthly_revenue:,.2f}")
        explanation_parts.append("")

        # Regulatory environment
        reg_env = top_market["regulatory_environment"]
        explanation_parts.append(f"Regulatory Environment: {reg_env.replace('_', ' ').title()}")
        explanation_parts.append("")

        # General patterns
        explanation_parts.append("General Patterns Across the State:")
        insights = self._generate_market_insights(ranked_markets)
        explanation_parts.append(f"  - Average market score: {insights['average_market_score']:.1f}/100")
        explanation_parts.append(f"  - Markets with good+ investment potential: {insights['markets_with_good_plus_potential']}")
        explanation_parts.append(f"  - Most common demand drivers: {', '.join(insights['most_common_demand_drivers'])}")

        return "\n".join(explanation_parts)

    def compare_markets(
        self,
        market_names: List[str],
        markets_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare specific markets side-by-side.

        Args:
            market_names: List of city names to compare
            markets_data: Full market data for all cities

        Returns:
            Comparison dictionary
        """
        comparison = {
            "markets": [],
            "winner": None,
            "comparison_summary": {}
        }

        selected_markets = [m for m in markets_data if m.get("city") in market_names]

        for market_data in selected_markets:
            score = self._calculate_market_score(market_data)
            comparison["markets"].append({
                "city": market_data["city"],
                "market_score": score,
                "avg_nightly_rate": market_data.get("avg_nightly_rate", 0),
                "avg_occupancy_rate": market_data.get("avg_occupancy_rate", 0),
                "active_listings": market_data.get("active_listings", 0),
                "regulatory_environment": market_data.get("regulatory_environment", "Unknown"),
                "investment_potential": self._assess_investment_potential(market_data, score)
            })

        # Determine winner
        if comparison["markets"]:
            winner = max(comparison["markets"], key=lambda x: x["market_score"])
            comparison["winner"] = winner["city"]
            comparison["comparison_summary"] = {
                "winner": winner["city"],
                "winner_score": winner["market_score"],
                "winner_advantages": self._identify_advantages(winner, comparison["markets"])
            }

        return comparison

    def _identify_advantages(
        self,
        winner: Dict[str, Any],
        all_markets: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Identify key advantages of the winning market.

        Args:
            winner: Winning market data
            all_markets: All markets being compared

        Returns:
            List of advantage descriptions
        """
        advantages = []

        # Compare rates
        avg_rate_others = sum(m["avg_nightly_rate"] for m in all_markets if m != winner) / max(len(all_markets) - 1, 1)
        if winner["avg_nightly_rate"] > avg_rate_others * 1.1:
            advantages.append(f"Higher nightly rates (${winner['avg_nightly_rate']:.2f} vs ${avg_rate_others:.2f} average)")

        # Compare occupancy
        avg_occ_others = sum(m["avg_occupancy_rate"] for m in all_markets if m != winner) / max(len(all_markets) - 1, 1)
        if winner["avg_occupancy_rate"] > avg_occ_others * 1.05:
            advantages.append(f"Higher occupancy ({winner['avg_occupancy_rate']*100:.1f}% vs {avg_occ_others*100:.1f}% average)")

        # Better regulatory environment
        if winner["regulatory_environment"] in ["very_friendly", "friendly"]:
            advantages.append("Favorable regulatory environment")

        return advantages if advantages else ["Overall strongest market fundamentals"]
