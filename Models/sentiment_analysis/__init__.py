import csv
import typing as t
from pathlib import Path

from .stockanalysis import StockAnalysis, convert_stock_change
from .filtering import filter_on_stock_change_and_compound
from .vader import analyzer, LANGUAGE
from .translation import get_language


csv_file = Path(__file__).parent.parent.parent / 'Data/test/stock-change-title-nov12.csv'
analysis_csv_file = csv_file.parent / 'analysis-stock-change-5-quoted.csv'
filtered_csv_file = analysis_csv_file.parent / f'{analysis_csv_file.stem}-filtered.csv'


def main():
    results = get_sentiment_analysis_results(csv_file, max_limit=None)
    save_results(results, analysis_csv_file)


def get_sentiment_analysis_results(
    source: Path,
    use_lang_detection: bool = True,
    max_limit: t.Optional[int] = None,
) -> t.List[StockAnalysis]:
    """Run sentiment analysis on filtered texts.

    Filter on stock change of 5% or greater and Swedish texts only.
    """
    row_number = 1
    results: t.List[StockAnalysis] = []
    with source.open('r', encoding='utf-8', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        print(
            'Filtering on Swedish press releases where stock change is ±5% or'
            ' more:',
        )
        next(csv_reader)  # Skip CSV headers
        for stock_change_string, text in csv_reader:
            if max_limit is not None and len(results) >= max_limit:
                break
            if row_number % 1000 == 0:
                print(f'Processing row {row_number}... ({len(results)} results)')
            stock_change: float = convert_stock_change(stock_change_string)
            if stock_change is not None and abs(stock_change) >= 5:
                # Update `use_lang_detection` flag based on translation
                #   API status. If rate limit is reached, we don't want
                #   to make another API request.
                detected_lang, use_lang_detection = get_language(text, use_lang_detection)
                if detected_lang == LANGUAGE:
                    polarity_scores = analyzer.polarity_scores(text)
                    result = StockAnalysis(
                        text=text,
                        stock_change=stock_change,
                        **polarity_scores,
                    )
                    results.append(result)
            row_number += 1
    print_results(results, row_number)
    return results


def print_results(results, row_number) -> None:
    """Print found results message."""
    print(f'\nFound {len(results)} matching results in {row_number} rows:\n')
    if results:
        print(repr(results[0]))
    if len(results) > 2:
        print('...')
    if len(results) > 1:
        print(repr(results[-1]))


def save_results(results: t.List[StockAnalysis], target: Path):
    """Save analysis results in target CSV-file."""
    if not target.exists():
        with target.open('a', encoding='utf-8') as f:
            f.write(StockAnalysis.csv_header())
            for result in results:
                f.write(str(result))


if __name__ == "__main__":
    main()
