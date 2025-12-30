"""
Utility functions for Airbnb Investment Analyzer.
Provides shared helper functions for safe calculations and data formatting.
"""

from typing import Union, Optional


def safe_divide(
    numerator: Union[int, float],
    denominator: Union[int, float],
    default: Union[int, float] = 0.0
) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.

    Args:
        numerator: The numerator value
        denominator: The denominator value
        default: Value to return if denominator is zero (default: 0.0)

    Returns:
        Result of division or default value
    """
    if denominator == 0 or denominator is None:
        return default
    return numerator / denominator


def safe_percentage(
    value: Union[int, float],
    total: Union[int, float],
    default: float = 0.0
) -> float:
    """
    Safely calculate percentage, handling zero total.

    Args:
        value: The value to convert to percentage
        total: The total value (denominator)
        default: Value to return if total is zero (default: 0.0)

    Returns:
        Percentage as decimal (e.g., 0.15 for 15%)
    """
    return safe_divide(value, total, default)


def format_currency(amount: Union[int, float]) -> str:
    """
    Format number as currency string.

    Args:
        amount: Numeric amount to format

    Returns:
        Formatted currency string (e.g., "$1,250.50")
    """
    return f"${amount:,.2f}"


def format_percentage(decimal: float, decimals: int = 2) -> str:
    """
    Format decimal as percentage string.

    Args:
        decimal: Decimal value (e.g., 0.15 for 15%)
        decimals: Number of decimal places (default: 2)

    Returns:
        Formatted percentage string (e.g., "15.00%")
    """
    return f"{decimal * 100:.{decimals}f}%"


def validate_positive(value: Union[int, float], name: str) -> None:
    """
    Validate that a value is positive.

    Args:
        value: Value to validate
        name: Name of the value for error message

    Raises:
        ValueError: If value is not positive
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_percentage(value: float, name: str) -> None:
    """
    Validate that a value is a valid percentage (0-1).

    Args:
        value: Value to validate (as decimal, e.g., 0.15 for 15%)
        name: Name of the value for error message

    Raises:
        ValueError: If value is not between 0 and 1
    """
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1, got {value}")


def calculate_annual_from_monthly(monthly_amount: float) -> float:
    """
    Convert monthly amount to annual.

    Args:
        monthly_amount: Monthly amount

    Returns:
        Annual amount (monthly * 12)
    """
    return monthly_amount * 12


def calculate_monthly_from_annual(annual_amount: float) -> float:
    """
    Convert annual amount to monthly.

    Args:
        annual_amount: Annual amount

    Returns:
        Monthly amount (annual / 12)
    """
    return annual_amount / 12
