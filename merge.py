import argparse
import csv
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Объединение CSV-файлов без дубликатов")
    parser.add_argument("files", nargs="+", type=Path, help="исходные CSV-файлы")
    parser.add_argument("-o", "--output", required=True, type=Path, help="итоговый CSV-файл")
    args = parser.parse_args()

    rows = []
    seen = set()
    columns = None

    try:
        for path in args.files:
            with path.open(encoding="utf-8-sig", newline="") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                if not header:
                    raise ValueError(f"Файл пустой: {path}")
                if columns is None:
                    columns = header
                elif header != columns:
                    raise ValueError(f"Столбцы не совпадают: {path}")

                for row in reader:
                    if not row:
                        continue
                    if len(row) != len(columns):
                        raise ValueError(f"Неверное число столбцов в файле {path}, строка {reader.line_num}")
                    item = tuple(row)
                    if item not in seen:
                        seen.add(item)
                        rows.append(row)

        with args.output.open("x", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(rows)

        print(f"Готово: {args.output}. Строк: {len(rows)}")
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        parser.exit(1, f"Ошибка: {error}\n")


if __name__ == "__main__":
    main()
