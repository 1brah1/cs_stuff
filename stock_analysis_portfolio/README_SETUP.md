# Quick Setup Guide - Generate Stock Portfolio Visualizations

## Using Your Conda Environment

Since you have miniconda with the packages already installed:

1. **Open Anaconda Prompt** (or activate your conda environment)

2. **Navigate to the project directory**:
   ```bash
   cd cs_stuff/stock_analysis_portfolio
   ```

3. **Run the visualization script**:
   ```bash
   python run_visualizations.py
   ```
   
   Or use the main script directly:
   ```bash
   python main.py
   ```

4. **After images are generated, commit them to git**:
   ```bash
   cd ../..  # Go back to CODE directory
   git add cs_stuff/stock_analysis_portfolio/visualizations/*.png
   git commit -m "Add generated stock portfolio visualizations"
   git push
   ```

## What Gets Generated

The script will create 6 visualization images in the `visualizations/` folder:
- `price_trends.png` - Individual stock price charts
- `volume_analysis.png` - Trading volume analysis
- `price_comparison.png` - Normalized price comparison
- `daily_changes.png` - Daily price changes
- `price_range.png` - High-low price ranges
- `summary_stats.png` - Summary statistics dashboard

## Troubleshooting

If you get import errors, make sure your conda environment is activated and has the packages:
```bash
conda activate base  # or your environment name
conda list | grep -E "yfinance|pandas|matplotlib|numpy"
```

If packages are missing:
```bash
conda install yfinance pandas matplotlib numpy
```



