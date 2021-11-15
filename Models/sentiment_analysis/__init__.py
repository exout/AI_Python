import csv
import time
import typing as t
from pathlib import Path

from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .stockanalysis import StockAnalysis





csv_file = Path('../../Data/test/stock-change-title-nov12.csv')
analysis_csv_file = csv_file.parent / 'analysis-stock-change-5.csv'


def main():
    max_limit: int = 10
    row_number = 1
    results: t.List[StockAnalysis] = []
    detector = Translator()
    # Google translation allows for 5 calls/s and maximum 200k per day.
    use_lang_detection = False

    with csv_file.open('r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        print(
            'Filtering on Swedish press releases where stock change is ±5% or'
            ' more:',
        )
        for stock_change_string, text in csv_reader:
            row_number += 1
            if row_number % 1000 == 0:
                print(f'Processing row {row_number}... ({len(results)} results)')
            try:
                # Filter on Swedish texts with a stock change value.
                stock_change: float = StockAnalysis.get_stock_change(stock_change_string)
            except Exception:
                continue
            else:
                # Filter on stock change of 5% or greater.
                if abs(stock_change) >= 5:
                    detected_lang = 'sv' if any(char in text.lower() for char in {'å', 'ä', 'ö'}) else None
                    try:
                        if use_lang_detection:
                            detected_lang = detector.detect(text).lang
                            time.sleep(1)
                    except Exception:
                        pass  # Use vowel fallback
                    if detected_lang == 'sv':
                        analyzer = SentimentIntensityAnalyzer()
                        polarity_scores = analyzer.polarity_scores(text)
                        result = StockAnalysis(
                            text=text,
                            stock_change=stock_change,
                            **polarity_scores,
                        )
                        results.append(result)
    print(f'\nFound {len(results)} matching results in {row_number} rows:\n')
    if results:
        print(repr(results[0]))
    if len(results) > 2:
        print('...')
    if len(results) > 1:
        print(repr(results[-1]))
    # Save analysis results.
    if not analysis_csv_file.exists():
        with analysis_csv_file.open('a', encoding='utf-8') as f:
            f.write(StockAnalysis.csv_header())
            for result in results:
                f.write(str(result))


if __name__ == "__main__":
    main()
