# Airbnb Investment Analyzer

A comprehensive Claude Skill for analyzing short-term rental property investment opportunities, with focus on Airbnb properties.

## Overview

The Airbnb Investment Analyzer provides real estate investors with powerful tools to evaluate, compare, and analyze Airbnb property investments. It combines market research, financial modeling, comparative analysis, and property valuation into a single comprehensive skill.

## Version

**v1.0.0** - Initial Release (2025-01-29)

## Capabilities

- **Market Analysis**: Identify high-potential Airbnb markets within a state or region
- **Investment Opportunity Evaluation**: Calculate ROI, cap rate, cash-on-cash return, and other key metrics
- **Rental Income Modeling**: Project income based on comparable properties with seasonal adjustments
- **Expense Tracking**: Process and categorize operating expenses with budget variance analysis
- **Comparative Property Analysis**: Compare multiple properties side-by-side with scoring and ranking
- **Property Valuation**: Estimate property values using multiple valuation approaches

## Use Cases

1. **Analyze property investment opportunities for Airbnb in a given state**
   - Identify top markets by investment potential
   - Understand demand drivers and market dynamics
   - Assess regulatory environment and competition

2. **Identify where Airbnb is most prevalent in a state and explain why**
   - Market prevalence analysis with scoring
   - Key demand driver identification
   - Comparative market insights

3. **Process rental income and expense tracking for a given Airbnb based on comps**
   - Income projections from comparable properties
   - Expense categorization and ratio analysis
   - Budget variance tracking

4. **Create property valuation models in that area**
   - Income approach valuation (cap rate method)
   - Gross Rent Multiplier (GRM) approach
   - Sales comparison approach
   - Airbnb-specific premium valuations

## Installation

### Claude Code (Project-level)

```bash
# Copy skill folder to your project
cp -r airbnb-investment-analyzer /path/to/your/project/.claude/skills/
```

### Claude Code (User-level)

```bash
# Copy skill folder to your user skills directory
cp -r airbnb-investment-analyzer ~/.claude/skills/
```

### Claude Desktop App

1. Compress the skill folder into a ZIP file
2. Drag and drop the ZIP into Claude Desktop
3. The skill will be automatically installed and available

### Verify Installation

After installation, you can verify the skill is available:

```
Hey Claude, can you list my available skills?
```

Or directly invoke it:

```
Hey Claude—I just added the "airbnb-investment-analyzer" skill. Can you help me analyze Airbnb markets in Texas?
```

## File Structure

```
airbnb-investment-analyzer/
├── SKILL.md                                    # Main skill definition
├── README.md                                   # This file
├── HOW_TO_USE.md                              # Usage examples and invocation patterns
├── utils.py                                    # Shared utility functions
├── market_analyzer.py                          # Market analysis and prevalence modeling
├── investment_calculator.py                    # Investment metrics calculations
├── rental_income_projector.py                  # Rental income projections
├── expense_tracker.py                          # Expense tracking and analysis
├── property_valuator.py                        # Property valuation methods
├── comparative_analyzer.py                     # Multi-property comparison
├── sample_input_market_analysis.json           # Sample market analysis input
├── sample_input_investment_analysis.json       # Sample investment analysis input
└── expected_output.json                        # Sample expected output
```

## Python Modules

### Core Modules

1. **utils.py** - Shared utility functions
   - `safe_divide()` - Safe division with zero handling
   - `safe_percentage()` - Safe percentage calculations
   - `format_currency()` - Currency formatting
   - `format_percentage()` - Percentage formatting
   - Input validation functions

2. **market_analyzer.py** - Market analysis
   - `MarketAnalyzer` class
   - Market prevalence analysis
   - Market scoring and ranking
   - Demand driver identification
   - Comparative market analysis

3. **investment_calculator.py** - Investment metrics
   - `InvestmentCalculator` class
   - ROI, cap rate, cash-on-cash return calculations
   - Mortgage payment calculations
   - Break-even occupancy analysis
   - Debt service coverage ratio (DSCR)
   - Sensitivity analysis

4. **rental_income_projector.py** - Income projections
   - `RentalIncomeProjector` class
   - Comparable property analysis
   - Seasonal income modeling
   - Occupancy rate calculations
   - Income range scenarios
   - Comp quality assessment

5. **expense_tracker.py** - Expense management
   - `ExpenseTracker` class
   - Expense categorization
   - Budget variance analysis
   - Expense ratio calculations
   - NOI calculations
   - Monthly averaging

6. **property_valuator.py** - Property valuation
   - `PropertyValuator` class
   - Income approach valuation
   - Gross Rent Multiplier (GRM) method
   - Sales comparison approach
   - Airbnb-specific valuations
   - Multi-approach reconciliation

7. **comparative_analyzer.py** - Property comparison
   - `ComparativeAnalyzer` class
   - Multi-property scoring and ranking
   - Financial performance scoring
   - Market strength assessment
   - Risk factor analysis
   - Operational ease scoring

## Key Metrics Calculated

### Investment Metrics
- **Cap Rate**: Net Operating Income / Purchase Price
- **Cash-on-Cash Return**: Annual Cash Flow / Total Cash Invested
- **ROI**: Return on Investment (Year 1)
- **DSCR**: Debt Service Coverage Ratio
- **Payback Period**: Years to recover initial investment
- **Break-Even Occupancy**: Minimum occupancy to cover expenses

### Market Metrics
- **Market Score**: Weighted score (0-100) based on demand, financial, regulatory, and competition factors
- **Investment Potential**: Rating from Poor to Excellent
- **Demand Drivers**: Tourism, business travel, education, events, medical

### Property Scores
- **Overall Property Score**: Composite score from financial, market, risk, and operational factors
- **Investment Recommendation**: Strong Buy, Buy, Consider, Pass, or Avoid
- **Risk Level**: Low, Medium, or High

## Sample Usage

See [HOW_TO_USE.md](HOW_TO_USE.md) for detailed usage examples.

### Quick Example: Investment Analysis

```
Hey Claude—I just added the "airbnb-investment-analyzer" skill.

I'm looking at a 3-bedroom house in Austin for $450,000 with:
- 25% down payment
- 7% interest rate
- 30-year mortgage

Based on these comparable Airbnb properties in the area:
- Property 1: $195/night, 75% occupancy, 87 reviews, 4.8 rating
- Property 2: $175/night, 70% occupancy, 52 reviews, 4.6 rating
- Property 3: $210/night, 78% occupancy, 134 reviews, 4.9 rating

Can you analyze the investment potential and projected returns?
```

## Assumptions & Best Practices

### Default Assumptions
- **Operating Expenses**: 30-40% of gross rental income (if not provided)
- **Occupancy Rate**: 65-75% for well-managed properties
- **Cleaning Costs**: $75-150 per turnover (property size dependent)
- **Property Management**: 15-25% of gross rental income (if using professional management)

### Best Practices
1. Use recent comparable data (last 3-6 months)
2. Include 5-10 comparable properties for reliable projections
3. Account for seasonality specific to the market
4. Use conservative assumptions for risk management
5. Check local short-term rental regulations before investing
6. Include all costs (furnishings, renovation, platform fees, etc.)
7. Run multiple scenarios (conservative, realistic, optimistic)

## Limitations

- **Data Quality**: Analysis quality depends on comparable property data availability and accuracy
- **Market Changes**: Short-term rental markets can shift rapidly due to regulations or economic factors
- **Not Financial Advice**: This tool provides analysis; it is not professional financial, tax, or legal advice
- **Historical Performance**: Past performance of comparables doesn't guarantee future results
- **Regulatory Risk**: New STR restrictions can materially affect investment viability

## Industry Benchmarks

### Good Performance
- Cap Rate: 8-12%
- Cash-on-Cash Return: 12-15%
- Occupancy: 65-75%
- DSCR: 1.25+

### Excellent Performance
- Cap Rate: 12%+
- Cash-on-Cash Return: 20%+
- Occupancy: 75%+
- DSCR: 1.5+

## Support & Feedback

This skill is part of the Claude Code Skills Factory project. For issues, feature requests, or contributions:

- Repository: https://github.com/yourusername/claude-code-skill-factory
- Issues: Submit via GitHub Issues
- Documentation: See `/documentation` folder in repository

## License

MIT License - See repository for full license text

## Changelog

### v1.0.0 (2025-01-29)
- Initial release
- Market analysis capabilities
- Investment calculator with sensitivity analysis
- Rental income projector with seasonality
- Expense tracker with budget variance
- Property valuator with multiple approaches
- Comparative analyzer for multi-property evaluation

---

**Built with Claude Code Skill Factory** 🏭
