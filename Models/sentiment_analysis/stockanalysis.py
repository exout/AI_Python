import typing as t

from pydantic import BaseModel, validator


class StockAnalysis(BaseModel):
    """Result of stock press release sentiment analysis."""

    text: str
    stock_change: t.Optional[float] = None
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

    @validator('stock_change', pre=True)
    def validate_stock_change(cls, value: t.Union[float, str]) -> t.Optional[float]:
        return convert_stock_change(value)

    @classmethod
    def csv_header(cls) -> str:
        """Get CSV header."""
        titles = StockAnalysis.schema().get('required').copy()
        titles.insert(1, 'stock_change')
        return f"{','.join(titles)}\n"


def convert_stock_change(value: t.Union[str, float]):
    """Convert stock change to float."""
    if isinstance(value, str):
        if not value:
            return None
        result = value.replace(',', '.')
        # Exclude sign and % when converting to float.
        result = float(result[1:-1])
        if value.startswith('-'):
            # Result must be negative.
            result *= -1
        return result
    return value


if __name__ == '__main__':
    obj = StockAnalysis(text='abc', stock_change='+3,5%', compound=0.3, neg=0.1, neu=1, pos=0.5)
    print(obj)
    print(StockAnalysis.csv_header())
