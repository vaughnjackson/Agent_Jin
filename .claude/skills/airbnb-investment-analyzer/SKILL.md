---
name: airbnb-investment-analyzer
description: Comprehensive Airbnb property investment analysis including market research, rental income modeling, expense tracking, and property valuation for short-term rental investors
---

# Airbnb Investment Analyzer

A comprehensive tool for analyzing short-term rental property investment opportunities, focusing on Airbnb properties. This skill provides market analysis, financial modeling, competitive research, and property valuation capabilities to help investors make data-driven decisions.

## Capabilities

- **Market Analysis**: Identify high-potential Airbnb markets within a state or region, analyzing demand patterns, regulatory environment, and competitive landscape
- **Investment Opportunity Evaluation**: Calculate ROI, cap rate, cash-on-cash return, break-even analysis, and payback periods for potential Airbnb properties
- **Rental Income Modeling**: Project rental income based on comparable properties in the area, seasonal adjustments, and occupancy rate analysis
- **Expense Tracking**: Process and categorize operating expenses including utilities, maintenance, cleaning, property management, and platform fees
- **Comparative Property Analysis**: Compare multiple properties side-by-side with financial metrics and investment potential scoring
- **Property Valuation Models**: Estimate property values using income approach, sales comparison approach, and Airbnb-specific multipliers
- **Market Prevalence Analysis**: Identify where Airbnb is most concentrated in a state and explain the underlying market drivers

## Input Requirements

### For Market Analysis:
- **State or Region**: Geographic area to analyze (e.g., "Texas", "Austin metro area")
- **Investment Criteria**: Budget range, property type preferences, target returns
- **Market Factors** (optional): Tourism attractions, business travel hubs, university towns

### For Investment Opportunity Analysis:
- **Property Details**: Purchase price, bedrooms, bathrooms, square footage, location
- **Financial Assumptions**: Down payment percentage, interest rate, loan term, expected occupancy rate
- **Comparable Data**: Nightly rates and occupancy from similar Airbnb properties in the area

### For Rental Income & Expense Tracking:
- **Comparable Properties**: Airbnb listings data (nightly rates, occupancy rates, reviews)
- **Expense Categories**: Actual or estimated operating expenses
- **Seasonal Factors**: High/low season patterns specific to the market

### For Property Valuation:
- **Property Characteristics**: Size, location, amenities, condition
- **Market Data**: Recent sales comps, current Airbnb rental rates, cap rates in the area
- **Income Projections**: Expected annual rental income and operating expenses

## Output Formats

Results include:

- **Market Analysis Reports**: Detailed breakdown of Airbnb markets within a state, ranked by investment potential with supporting data
- **Financial Models**: Complete pro forma statements showing projected income, expenses, cash flow, and returns (Excel/JSON format)
- **Comparative Analysis Tables**: Side-by-side property comparisons with key metrics and scoring
- **Property Valuations**: Estimated property values with multiple valuation methods and confidence ranges
- **Visual Dashboards**: Charts showing cash flow projections, market trends, and ROI analysis
- **Investment Summaries**: Executive summary with recommendations and risk factors

## How to Use

### Example Invocations:

**Market Research:**
"Analyze the top Airbnb markets in Texas and explain why certain cities are more profitable than others."

**Investment Opportunity:**
"I'm looking at a 3-bedroom house in Austin for $450,000. Can you analyze the investment potential as an Airbnb with comparable rental data?"

**Rental Income Projection:**
"Based on comparable Airbnb properties in downtown Dallas, what's the realistic monthly rental income for a 2-bedroom condo?"

**Property Valuation:**
"Value this property using the income approach based on projected Airbnb rental income of $72,000 annually with a 6% cap rate."

**Expense Tracking:**
"Track my Airbnb expenses for Q4 2024 and calculate my actual vs projected net operating income."

## Scripts

- **`market_analyzer.py`**: Analyzes Airbnb market prevalence, demand factors, and investment potential across regions
- **`investment_calculator.py`**: Calculates investment metrics (ROI, cap rate, cash-on-cash return, payback period, break-even analysis)
- **`rental_income_projector.py`**: Projects rental income based on comparable properties, seasonality, and occupancy modeling
- **`expense_tracker.py`**: Processes and categorizes Airbnb operating expenses with budget variance analysis
- **`property_valuator.py`**: Performs property valuations using multiple approaches (income, sales comparison, GRM)
- **`comparative_analyzer.py`**: Compares multiple properties side-by-side with scoring and ranking
- **`utils.py`**: Shared utility functions for safe calculations and data formatting

## Best Practices

### Data Quality
1. **Use Recent Comps**: Comparable property data should be from the last 3-6 months
2. **Validate Occupancy Rates**: Cross-reference with multiple data sources (AirDNA, AllTheRooms, direct Airbnb research)
3. **Include Seasonal Adjustments**: Account for high/low seasons specific to the market
4. **Conservative Assumptions**: Use realistic occupancy rates (65-75% is typical for well-managed properties)

### Analysis Standards
1. **Consider All Costs**: Include often-overlooked expenses (HOA, property taxes, insurance, platform fees, furnishings)
2. **Account for Vacancy**: Build in vacancy/turnover periods between bookings
3. **Regulatory Awareness**: Check local short-term rental regulations and restrictions
4. **Market Trends**: Consider supply growth and regulatory changes that may affect future returns
5. **Multiple Scenarios**: Run best-case, realistic, and conservative projections

### Investment Decision Framework
1. **Return Thresholds**: Target minimum 12-15% cash-on-cash return for Airbnb investments
2. **Market Diversification**: Don't over-concentrate in a single market or property type
3. **Risk Assessment**: Evaluate regulatory risk, market saturation, and competition
4. **Exit Strategy**: Consider property appreciation and resale potential, not just rental income
5. **Professional Advice**: Consult with local real estate agents, tax advisors, and attorneys

## Assumptions & Limitations

### Assumptions
- **Occupancy Rates**: Based on comparable properties; actual performance may vary based on management quality, marketing, and property condition
- **Operating Expenses**: Estimated at 30-40% of gross rental income (industry standard) unless actual data provided
- **Market Stability**: Projections assume relatively stable market conditions; major economic shifts may significantly impact results
- **Regulatory Environment**: Assumes current regulations remain stable; new restrictions can materially affect viability
- **Cleaning & Turnover**: Assumes $75-150 per turnover depending on property size
- **Property Management**: Assumes 15-25% of gross rental income if using professional management

### Limitations
- **Data Availability**: Analysis quality depends on available comparable property data
- **Market Changes**: Short-term rental markets can shift rapidly due to regulatory changes, supply increases, or economic factors
- **Seasonal Variation**: Some markets have extreme seasonality that requires careful cash flow management
- **Property-Specific Factors**: Unique property features, condition issues, or location factors may not be captured in comps
- **Not Financial Advice**: This tool provides analysis and projections; it is not professional financial, tax, or legal advice
- **Historical Data**: Past performance of comparable properties doesn't guarantee future results

### When NOT to Use This Skill
- **Long-term rental analysis**: This skill is optimized for short-term rentals (Airbnb/VRBO), not traditional 12-month leases
- **Commercial real estate**: Focused on residential short-term rentals, not commercial properties
- **Markets with insufficient data**: Requires comparable property data; very rural or unique markets may lack sufficient comps
- **Complex ownership structures**: Best for direct property ownership; doesn't model partnerships, REITs, or syndications

## Industry Context

### Airbnb Investment Benchmarks
- **Good ROI**: 8-12% cap rate, 12-15% cash-on-cash return
- **Excellent ROI**: 12%+ cap rate, 20%+ cash-on-cash return
- **Typical Occupancy**: 60-75% for well-managed properties in good markets
- **Break-even Occupancy**: Usually 40-50% depending on expenses and mortgage

### Key Success Factors
1. **Location**: Proximity to attractions, downtown areas, universities, medical centers, or business districts
2. **Property Quality**: Well-furnished, clean, modern amenities compete better
3. **Management**: Responsive hosting, 5-star reviews, and optimized pricing drive occupancy
4. **Market Selection**: Choose markets with strong tourism/business travel and favorable regulations
5. **Differentiation**: Unique properties or those filling a market gap perform better

### Common Pitfalls
- **Underestimating expenses**: First-time investors often underestimate maintenance, furnishings, and platform fees
- **Overestimating occupancy**: Using peak-season rates year-round leads to unrealistic projections
- **Ignoring regulations**: Some cities have restricted or banned short-term rentals
- **Poor property management**: Low review scores and slow response times kill occupancy
- **Market saturation**: Entering oversaturated markets with heavy competition
