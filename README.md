# National Parks and Societal Change

A data science project by **The Correlators** (Anvi Mehta, Jamal Moussa, Katie Bakkonnen, Mia George) exploring how periods of societal change and disturbance influence visitation patterns in U.S. National Parks.

## Research Question

**How do periods of societal change and disturbance influence patterns of visitation in national parks?**

We examine correlations between major events—political elections, public health crises (e.g., COVID-19), economic downturns, and other shocks—and park usage. The goal is to understand how human behavior under stress and uncertainty shows up in visitation data and to clarify the interplay between society and the environment.

## Repository Overview

| Component | Description |
|-----------|-------------|
| **Datasets/** | Park visitation data (yearly 1904–2024, monthly 1979–present), world/US events, president winners; raw NPS reports by month (e.g., jan 25, feb 25, april 25). |
| **Data cleaning/** | Scripts to parse, clean, and merge NPS reports: `parse_monthly_data.py`, `parse_march_april_data.py`, `parse_may_june_data.py`, `merge_park_data.py`, `clean_national_parks.py`, `organize_historic_park_data.py`, `process_president_winners.py`. |
| **EDA/** | Exploratory outputs (e.g., park seasonality, monthly averages, state voting–visitation correlation). |
| **models/** | Time series (SARIMA), multi-period analysis, year-over-year and anomaly outputs. See [Model files](#model-files) below. |
| **Notebooks** | Main analysis and reporting. |

## Key Data Sources

- **National Park Service (NPS)**  
  [Query Builder for Public Use Statistics (1979 – Last Calendar Year)](https://irma.nps.gov/Stats/SSRSReports/National%20Reports/Query%20Builder%20for%20Public%20Use%20Statistics%20(1979%20-%20Last%20Calendar%20Year))  
  Monthly and annual visitation by park.

- **Historic data (1904–1979)**  
  Combined with summed monthly data to form a continuous yearly series (1904–2024).

- **World & US events**  
  Manually compiled list (`world_event.csv`) used to map anomalies to specific years and events (pandemics, recessions, policy changes, etc.).

## Model files

| File | Description |
|------|--------------|
| [models/sarima.ipynb](models/sarima.ipynb) | SARIMA time series modeling. |
| [models/yoy.ipynb](models/yoy.ipynb) | Year-over-year analysis. |
| [models/multi_period_analysis_asymmetric.csv](models/multi_period_analysis_asymmetric.csv) | Multi-period analysis results (asymmetric). |
| [models/multi_period_analysis_asymmetric_excl.csv](models/multi_period_analysis_asymmetric_excl.csv) | Multi-period analysis results (asymmetric, excluded). |
| [models/park_anomalies.csv](models/park_anomalies.csv) | Park-level anomaly outputs. |

## Key Scripts

- **`Data cleaning/parse_monthly_data.py`** — Parses monthly NPS reports for 2025. Update and run this script each month as new reports (e.g., Jan 25, Feb 25) are added to `Datasets/` to keep the analysis up to date.

## Analysis & Insights

The project includes:

- **Data exploration** — Patterns, summary statistics, and notable shifts (e.g., sharp drop in 2020 due to COVID-19).
- **Anomaly detection** — Linear regression residuals, z-scores, KNN-based anomaly detection, and majority voting across methods.
- **Event mapping** — Linking detected anomalies to entries in the world/US events dataset.
- **Modeling** — Linear regression (yearly and monthly), SARIMA, and multi-period comparisons.

Main narrative and results are in **`report.ipynb`**.

## Setup

```bash
pip install -r requirments.txt
```

Dependencies include: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`. Additional packages (e.g., `statsmodels`, `plotly`) are used in the notebooks and may need to be installed if you run them.

## Notebooks at a Glance

| Notebook | Purpose |
|----------|---------|
| `report.ipynb` | Main report: intro, datasets, EDA, preprocessing, and findings. |
| `linear_regression.ipynb` / `linear_regression year.ipynb` | Linear regression on visitation. |
| `linear_regression_anomalies.ipynb` | Anomaly detection via regression residuals (yearly and monthly). |
| `knn_anomaly_detection.ipynb` | KNN-based anomaly detection. |
| `majority_voting.ipynb` | Combining anomaly detection methods (majority voting). |
| `models/sarima.ipynb` | SARIMA time series modeling. |
| `models/yoy.ipynb` | Year-over-year analysis. |
| `demo.ipynb` | Demo or supplementary visualizations. |

---

*Data exploration focuses on key patterns, statistics, and insights from NPS visitation data and their relationship to societal change.*
