import csv
from pathlib import Path

from .stockanalysis import StockAnalysis


def filter_on_stock_change_and_compound(source_file: Path, target_file: Path):
    """Exclude results where stock change and compound don't correlate."""
    if target_file.exists():
        raise FileExistsError
    with source_file.open('r', encoding='utf-8', newline='') as source:
        with target_file.open('a', encoding='utf-8') as target:
            target.write(StockAnalysis.csv_header())
            source_reader = csv.DictReader(
                source,
                delimiter=',',
                quotechar='|',
            )
            for data in source_reader:
                result = StockAnalysis(**data)
                if is_true_positive(result) or is_true_negative(result):
                    target.write(str(result))


def is_true_positive(result: StockAnalysis) -> bool:
    """Check if result is true positive.

    True positive means that both stock change and compound is positive.
    """
    return result.stock_change > 0 and result.compound > 0.2


def is_true_negative(result: StockAnalysis) -> bool:
    """Check if result is true negative.

    True negative means that both stock change and compound is negative.
    """
    return result.stock_change < 0 and result.compound < -0.2
