import typing as t
from dataclasses import dataclass


@dataclass
class StockAnalysis:
    """Result of stock press release sentiment analysis."""

    text: str
    stock_change: float
    compound: float
    neg: float
    neu: float
    pos: float
    debug: t.Optional[t.Dict[str, t.Any]] = None

    def __repr__(self) -> str:
        """Get repr string representation."""
        text = f'{self.text[:40]}...'
        return (
            f'{type(self).__name__}('
            f'{self.stock_change=}, '
            f'{text=}, '
            f'{self.compound=}, '
            f'{self.neg=}, '
            f'{self.neu=}, '
            f'{self.pos=}, '
            f'{self.debug=}'
            f')'
        ).replace('self.', '')

    def __str__(self) -> str:
        """Get CSV string representation, ignoring debug."""
        return (
            f'|{self.text}|,{self.stock_change},{self.compound},{self.neg},'
            f'{self.neu},{self.pos}\n'
        )

    @staticmethod
    def get_stock_change(string: str) -> float:
        """Get stock change as float from string."""
        string = string.replace(',', '.')
        # Exclude sign and % when converting to float.
        result = float(string[1:-1])
        if string.startswith('-'):
            # Result must be negative.
            result *= -1
        return result

    @staticmethod
    def csv_header() -> str:
        """Get CSV header."""
        return 'text,stock_change,compound,neg,neu,pos\n'
