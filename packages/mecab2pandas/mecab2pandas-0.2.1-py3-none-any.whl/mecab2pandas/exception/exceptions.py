"""Defines of exceptions in this library."""


class BaseMecab2PandasError(Exception):
    """Base exception in this library."""


class NotSupportOSError(BaseMecab2PandasError):
    """Exception raised when called a not implemented function on this OS."""
