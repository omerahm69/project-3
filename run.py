"""
Project 3 - Survey Data Analysis Tool.

A four-step data analysis application:
    1. Import data   (CSV, Excel or Google Sheets)
    2. Parse & analyze (auto-detects numeric vs categorical columns)
    3. Visualize      (saves PNG charts and plots to /plots)
    4. Export         (saves a report and the clean data to /reports)

Usage:
    python run.py                 # interactive menu
    python run.py data.csv        # one-shot: import -> analyze -> plot -> export
    python run.py data.xlsx       # one-shot with an Excel file
    python run.py --quick <file>  # same as above
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import gspread
    from google.oauth2.service_account import Credentials
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

DATA_FILE = Path("data.pkl")
IMPORTED_FILE = Path("imported_data.csv")
PLOTS_DIR = Path("plots")
REPORTS_DIR = Path("reports")

MISSING_TOKENS = {"na", "n/a", "nan", "null", "none", "?"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slug(name):
    """Turn a column name into a safe filename (lowercase, underscores)."""
    # Keep only letters and digits; everything else becomes an underscore.
    return re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_") or "column"


def split_columns(df):
    """Return (numeric_columns, categorical_columns)."""
    # select_dtypes(include=[np.number]) picks the numeric types (int/float/date).
    # Everything else (strings, booleans, objects) is treated as categorical.
    numeric = list(df.select_dtypes(include=[np.number]).columns)
    categorical = [c for c in df.columns if c not in numeric]
    return numeric, categorical


def prepare_df(df):
    """Clean a raw dataframe so it is ready for analysis.

    Treats common missing-value tokens (NA, ?, blank cells, ...) as real
    missing values and auto-converts columns that are mostly numeric.
    Survey exports often store missing cells as text such as "NA", so we
    normalise those before any statistics are calculated.
    """
    # Copy so the caller's dataframe is never modified in place.
    df = df.copy()
    # Strip whitespace around column names (e.g. "Age " -> "Age").
    df.columns = [str(c).strip() for c in df.columns]
    for col in df.columns:
        series = df[col]
        # Only object/text columns need this cleaning - numbers are already fine.
        if pd.api.types.is_object_dtype(series):
            # Lowercase + strip so "na", " NA ", "N/A" are all recognised.
            stripped = series.astype(str).str.strip()
            missing_mask = stripped.str.lower().isin(MISSING_TOKENS)
            # Replace those tokens with real NaN values (pandas' missing marker).
            series = series.where(~missing_mask)
            # Try to read the column as numbers; incorrect cells become NaN.
            numeric = pd.to_numeric(series, errors="coerce")
            # Only convert if the majority (80%) of non-empty cells are numeric.
            if numeric.notna().sum() >= 0.8 * series.notna().sum():
                df[col] = numeric
    return df


def load_data(source):
    """Load a dataframe from a file path by extension."""
    path = Path(source)
    if not path.exists():
        return None, f"File not found: {source}"
    try:
        # Dispatch on the file extension so the user does not have to
        # remember the right pandas reader function.
        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        elif path.suffix.lower() in (".xls", ".xlsx"):
            df = pd.read_excel(path)
        elif path.suffix.lower() == ".pkl":
            df = pd.read_pickle(path)
        else:
            return None, f"Unsupported file type: {path.suffix or '(none)'}"
    except Exception as exc:
        return None, f"Could not read file: {exc}"
    if df.empty:
        return None, f"The file contains no data: {source}"
    return df, None


def store_data(df):
    """Persist the cleaned dataframe for later steps.

    data.pkl keeps the full Python dataframe (types preserved); the CSV copy
    gives the user a human-readable mirror of what was imported.
    """
    df.to_pickle(DATA_FILE)
    df.to_csv(IMPORTED_FILE, index=False)


def load_or_import():
    """Return the stored dataframe, or ask the user to import data."""
    if DATA_FILE.exists():
        return pd.read_pickle(DATA_FILE)
    print("No imported data found. Let's import some data first.")
    return import_data()


# ---------------------------------------------------------------------------
# STEP 1: Data import
# ---------------------------------------------------------------------------

def import_from_google():
    """STEP 1 (option 3): pull survey data straight from a Google Sheet."""
    if not HAS_GOOGLE:
        print("Google Sheets support needs 'gspread' and 'google-auth' "
              "(both are in requirements.txt).")
        return None
    creds_file = Path("creds.json")
    if not creds_file.exists():
        print("creds.json not found. Place your Google service-account "
              "credentials in this file.")
        return None
    try:
        # Authenticate with the service-account JSON downloaded from Google.
        creds = Credentials.from_service_account_file(str(creds_file), scopes=SCOPE)
        client = gspread.authorize(creds)
        # Accept either a full sheet URL or just its title.
        ref = input("Enter the Google Sheets title or URL: ").strip()
        sheet = client.open_by_url(ref) if ref.startswith("http") else client.open(ref)
        # sheet1 = first tab; get_all_records() reads rows into dicts.
        records = sheet.sheet1.get_all_records()
    except Exception as exc:
        print(f"Could not open the spreadsheet: {exc}")
        return None
    if not records:
        print("The spreadsheet is empty.")
        return None
    return pd.DataFrame(records)


def import_data():
    """STEP 1: ask the user for a source and turn it into a cleaned dataframe."""
    print("\nChoose the data source:")
    print("  1. CSV file")
    print("  2. Excel file")
    print("  3. Google Sheets")
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        df, err = load_data(input("Enter the path to the CSV file: ").strip())
    elif choice == "2":
        df, err = load_data(input("Enter the path to the Excel file: ").strip())
    elif choice == "3":
        df = import_from_google()
        err = None if df is not None else "Google Sheets import failed."
    else:
        print("Invalid choice. Please try again.")
        return None

    # Abort the import and keep the previous data if anything went wrong.
    if err or df is None:
        print(err or "Import failed - no data was saved.")
        return None

    # Clean + persist so the Analyse/Visualise/Export steps can use it later.
    df = prepare_df(df)
    store_data(df)
    print(f"Data imported successfully: {df.shape[0]:,} rows x {df.shape[1]:,} columns.")
    data_overview(df)
    return df


# ---------------------------------------------------------------------------
# STEP 2: Data parse and analysis
# ---------------------------------------------------------------------------

def data_overview(df):
    """Print a quick orientation: size, column types and missing values."""
    numeric, categorical = split_columns(df)
    print(f"\nDataset overview: {df.shape[0]:,} rows, {df.shape[1]:,} columns")
    print(f"  Numeric columns     ({len(numeric)}): "
          f"{', '.join(numeric) if numeric else 'none'}")
    print(f"  Categorical columns ({len(categorical)}): "
          f"{', '.join(categorical) if categorical else 'none'}")
    missing = int(df.isna().sum().sum())
    print(f"  Missing values      : {missing:,}"
          f" ({missing / df.size * 100:.1f}% of all cells)")


def analyze_data(df):
    """Print summary statistics and return a list of plain-language insights."""
    numeric, categorical = split_columns(df)

    print("\n" + "=" * 60)
    print("STEP 2: DATA ANALYSIS")
    print("=" * 60)

    if numeric:
        # describe() gives count/mean/std/min/quartiles/max; we add the
        # median and a missing-value counter to round it out.
        stats = df[numeric].describe().transpose()
        stats.insert(len(stats.columns) - 1, "median", df[numeric].median())
        stats.insert(0, "missing", df[numeric].isna().sum().astype(int))
        print("\n[NUMERIC COLUMNS] summary statistics")
        print(stats.round(2).to_string())

        # Correlation matrix reveals which numeric columns move together.
        corr = df[numeric].corr(numeric_only=True)
        if corr.shape[0] > 1:
            print("\n[NUMERIC COLUMNS] correlation matrix")
            print(corr.round(2).to_string())

    if categorical:
        print("\n[CATEGORICAL COLUMNS] most common values")
        for col in categorical:
            s = df[col].dropna()
            if s.empty:
                continue
            counts = s.value_counts()
            table = pd.DataFrame({
                "count": counts,
                "share_%": (counts / len(s) * 100).round(1),
            })
            print(f"\n  '{col}'")
            print(table.head(5).to_string())

    # The insights are the "so what?" part - human-readable takeaways.
    insights = build_insights(df)
    print("\n[INSIGHTS]")
    for i, insight in enumerate(insights, 1):
        print(f"  {i}. {insight}")
    return insights


def build_insights(df):
    """Turn the data into short, human-readable takeaways."""
    numeric, categorical = split_columns(df)
    insights = []

    # 1. Strongest correlation: scan every unique pair of numeric columns
    #    and keep the one with the largest absolute correlation value.
    if len(numeric) > 1:
        corr = df[numeric].corr()
        pairs = []
        for i in range(len(corr)):
            for j in range(i + 1, len(corr)):
                value = corr.iloc[i, j]
                if pd.notna(value):
                    pairs.append((abs(value), value, corr.index[i], corr.columns[j]))
        pairs.sort(key=lambda t: -t[0])
        if pairs:
            _, value, a, b = pairs[0]
            direction = "positive" if value > 0 else "negative"
            insights.append(
                f"Strongest relationship: '{a}' and '{b}' change together "
                f"({direction} correlation, r = {value:.2f})."
            )

    # 2. Distribution shape for each numeric column: if the mean sits well
    #    above the median the data is right-skewed (a few big values), and
    #    the opposite means left-skewed.
    for col in numeric:
        s = df[col].dropna()
        if s.empty:
            insights.append(f"'{col}' has no usable values - consider dropping it.")
            continue
        mean, median = s.mean(), s.median()
        if median != 0 and abs(mean - median) / abs(median) < 0.05:
            insights.append(
                f"'{col}': fairly balanced distribution "
                f"(average {mean:.2f} vs midpoint {median:.2f})."
            )
        elif mean > median:
            ratio = mean / median if median else float("inf")
            insights.append(
                f"'{col}': right-skewed - the average ({mean:.2f}) is "
                f"{ratio:.1f}x the midpoint ({median:.2f}), so a minority "
                f"with high values pulls the average up."
            )
        else:
            insights.append(
                f"'{col}': left-skewed - the average ({mean:.2f}) sits below "
                f"the midpoint ({median:.2f}), so low values pull it down."
            )

    # 3. Dominant category for each categorical column, with the runner-up.
    for col in categorical:
        s = df[col].dropna()
        if s.empty:
            continue
        counts = s.value_counts()
        top = counts.index[0]
        share = counts.iloc[0] / len(s) * 100
        if counts.shape[0] > 1:
            second = counts.index[1]
            insights.append(
                f"'{col}': '{top}' dominates ({counts.iloc[0]:,} of {len(s):,}, "
                f"{share:.1f}%), followed by '{second}'."
            )
        else:
            insights.append(
                f"'{col}': single value '{top}' across all {len(s):,} loaded rows."
            )

    # 4. Data quality: report the column with the most missing cells.
    missing = int(df.isna().sum().sum())
    if missing == 0:
        insights.append("Dataset is complete - no missing values to clean.")
    else:
        most_missing = df.isna().mean().idxmax()
        insights.append(
            f"Missing data: '{most_missing}' is the least complete "
            f"({df[most_missing].isna().mean() * 100:.1f}% of its cells empty)."
        )

    return insights


# ---------------------------------------------------------------------------
# STEP 3: Visualization
# ---------------------------------------------------------------------------

def visualize_data(df):
    """Save distribution plots for every column; return the file paths."""
    PLOTS_DIR.mkdir(exist_ok=True)
    numeric, categorical = split_columns(df)
    saved = []

    # "whitegrid" gives the charts a light grid so trends are easier to read.
    sns.set_theme(style="whitegrid")

    # One combined heatmap is enough to see every numeric relationship at once.
    if len(numeric) > 1:
        corr = df[numeric].corr(numeric_only=True)
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                    square=True, cbar_kws={"shrink": 0.8})
        plt.title("Correlation Heatmap - Numerical Columns")
        path = PLOTS_DIR / "correlation_heatmap.png"
        plt.tight_layout()
        plt.savefig(path, dpi=120)
        plt.close()
        saved.append(path)

    # Histogram + smooth density curve (kde) for each numeric column.
    for col in numeric:
        s = df[col].dropna()
        if s.empty:
            continue
        plt.figure(figsize=(8, 5))
        # Choose between 10 and 30 bars depending on how many rows there are.
        bins = min(30, max(10, len(s) // 10))
        sns.histplot(s, bins=bins, kde=True, color="#1f77b4")
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        path = PLOTS_DIR / f"numeric_{slug(col)}.png"
        plt.tight_layout()
        plt.savefig(path, dpi=120)
        plt.close()
        saved.append(path)

    # Horizontal bar chart of value counts for each categorical column.
    # head(15) stops huge value lists from making the chart unreadable.
    for col in categorical:
        counts = df[col].dropna().value_counts()
        if counts.empty:
            continue
        counts = counts.head(15)
        plt.figure(figsize=(max(8, len(counts) * 0.8), 5))
        sns.barplot(x=counts.values, y=counts.index, color="#2ca02c")
        plt.title(f"Count of {col}")
        plt.xlabel("Count")
        plt.ylabel(col)
        path = PLOTS_DIR / f"categorical_{slug(col)}.png"
        plt.tight_layout()
        plt.savefig(path, dpi=120)
        plt.close()
        saved.append(path)

    return saved


# ---------------------------------------------------------------------------
# STEP 4: Data export
# ---------------------------------------------------------------------------

def export_data(df, insights=None):
    """Write a per-column report, the clean dataset and the insights."""
    if df is None:
        df = load_or_import()
        if df is None:
            return None
    REPORTS_DIR.mkdir(exist_ok=True)

    numeric, categorical = split_columns(df)
    # Build one row per column so the report is easy to scan in Excel/CSV:
    # - numeric columns get average/median/std/min/max
    # - categorical columns get number of unique values + the top choice.
    rows = []
    for col in df.columns:
        s = df[col]
        missing = int(s.isna().sum())
        type_col = "numeric" if col in numeric else "categorical"
        rec = {
            "column": col,
            "type": type_col,
            "missing": missing,
            "missing_pct": round(missing / len(df) * 100, 1),
        }
        non_null = s.dropna()
        if col in numeric:
            if not non_null.empty:
                rec.update({
                    "n_unique": "",
                    "count": int(non_null.shape[0]),
                    "mean": round(non_null.mean(), 2),
                    "median": round(non_null.median(), 2),
                    "std": round(non_null.std(ddof=1), 2),
                    "min": round(non_null.min(), 2),
                    "max": round(non_null.max(), 2),
                    "most_common": "",
                    "most_common_share_pct": "",
                })
        else:
            if not non_null.empty:
                counts = non_null.value_counts()
                rec.update({
                    "n_unique": int(counts.shape[0]),
                    "count": int(non_null.shape[0]),
                    "mean": "",
                    "median": "",
                    "std": "",
                    "min": "",
                    "max": "",
                    "most_common": str(counts.index[0]),
                    "most_common_share_pct": round(counts.iloc[0] / len(non_null) * 100, 1),
                })
        rows.append(rec)

    report = pd.DataFrame(rows)
    report_path = REPORTS_DIR / "analysis_results.csv"
    report.to_csv(report_path, index=False)

    # The cleaned dataset as a usable CSV for external tools.
    data_path = REPORTS_DIR / "analysis_export.csv"
    df.to_csv(data_path, index=False)

    # Excel report is a bonus - skip silently if openpyxl is not installed.
    xlsx_path = REPORTS_DIR / "analysis_results.xlsx"
    try:
        report.to_excel(xlsx_path, index=False)
    except Exception:
        xlsx_path = None

    insight_path = None
    if insights:
        # Save the numbered takeaways so they survive outside the terminal.
        insight_path = REPORTS_DIR / "insights.txt"
        insight_path.write_text(
            "DATA ANALYSIS INSIGHTS\n" + "=" * 30 + "\n\n"
            + "\n".join(f"{i}. {text}" for i, text in enumerate(insights, 1))
            + "\n",
            encoding="utf-8",
        )

    written = [p for p in (report_path, data_path, xlsx_path, insight_path) if p]
    print("\n[FILES EXPORTED]")
    for path in written:
        print(f"  {path}")
    return written


# ---------------------------------------------------------------------------
# One-shot pipeline and menu
# ---------------------------------------------------------------------------

def run_full_pipeline(df, resume=False):
    """Analyze, visualize, and export an already-imported dataframe."""
    if df is None:
        return
    if not resume:
        # In one-shot mode the overview is printed here; in menu mode the
        # import step already showed it, so resume=True skips the repeat.
        data_overview(df)
    insights = analyze_data(df)
    plots = visualize_data(df)
    export_data(df, insights)
    print(f"\n[PLOTS SAVED] {len(plots)} chart(s) in '{PLOTS_DIR}':")
    for path in plots:
        print(f"  {path}")
    print("\nDone. You can now open the charts and the report to review the insights.")


def quick_report(target):
    """One-shot mode: import a file, analyze it, plot it, and export a report."""
    print("Quick analysis mode")
    print("=" * 60)
    # Allow both "python run.py file.csv" and "python run.py --quick file.csv".
    if target in ("--quick", "-q") and len(sys.argv) > 2:
        target = sys.argv[2]

    # A URL is treated as a Google Sheet; anything else is a local file.
    if target.lower().startswith("http"):
        df = import_from_google()
    else:
        df, err = load_data(target)
        if err:
            print(err)
            return
        df = prepare_df(df)

    if df is None:
        print("Nothing to analyze - aborting.")
        return

    store_data(df)
    print(f"Data imported successfully: {df.shape[0]:,} rows x {df.shape[1]:,} columns.")
    run_full_pipeline(df)


def main():
    """Interactive menu mode."""
    df = None
    while True:
        print("\n" + "=" * 60)
        print("DATA ANALYSIS TOOL - PYTHON")
        print("=" * 60)
        print("  1. Import Data")
        print("  2. Analyze Data")
        print("  3. Visualize Data")
        print("  4. Export Data")
        print("  5. Run Full Pipeline")
        print("  6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            df = import_data()
        elif choice == "2":
            # If data was already imported this session, use it in memory;
            # otherwise fall back to the last imported file on disk.
            if df is None:
                df = load_or_import()
            if df is not None:
                analyze_data(df)
        elif choice == "3":
            if df is None:
                df = load_or_import()
            if df is not None:
                plots = visualize_data(df)
                print(f"\n[PLOTS SAVED] {len(plots)} chart(s) in '{PLOTS_DIR}':")
                for path in plots:
                    print(f"  {path}")
        elif choice == "4":
            export_data(df)
        elif choice == "5":
            if df is None:
                df = import_data()
            run_full_pipeline(df, resume=True)
        elif choice == "6":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Entry point: a file argument runs the whole pipeline, otherwise the menu.
    if len(sys.argv) > 1:
        quick_report(sys.argv[1])
    else:
        main()