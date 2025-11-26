import pandas as pd
import os
try:
    import openpyxl
    print(f"openpyxl version: {openpyxl.__version__}")
except ImportError:
    print("openpyxl not found")


file_path = 'Fichas tecnicas (1).xlsx'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    try:
        xl = pd.ExcelFile(file_path)
        with open('excel_analysis.txt', 'w', encoding='utf-8') as f:
            f.write(f"Sheet names: {xl.sheet_names}\n")
            
            for sheet in xl.sheet_names:
                f.write(f"\n--- Sheet: {sheet} ---\n")
                df = xl.parse(sheet)
                f.write(df.to_string())
                f.write("\n" + "-" * 20 + "\n")

    except Exception as e:
        print(f"Error reading excel: {e}")
