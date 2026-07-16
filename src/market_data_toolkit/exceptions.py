"""Custom exceptions raised by Market Data Toolkit."""

class MarketDataToolkitError(Exception):
    """Base exception for all package-specific failures."""


class NormalizationError(MarketDataToolkitError):
    """Raised when a vendor payload cannot be normalized."""


class ValidationError(MarketDataToolkitError):
    """Raised when invalid market data blocks an operation."""


class AggregationError(MarketDataToolkitError):
    """Raised when tick ordering or aggregation inputs are invalid."""
