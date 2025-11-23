#!/usr/bin/env python
"""
Script to generate stock portfolio visualizations
Run this in your conda environment where packages are installed
"""

import os
import sys

# Change to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("=" * 60)
print("STOCK PORTFOLIO VISUALIZATION GENERATOR")
print("=" * 60)
print(f"Working directory: {script_dir}")
print()

# Check if required packages are available
try:
    import yfinance
    import pandas
    import matplotlib
    import numpy
    print("✓ All required packages are available")
    print()
except ImportError as e:
    print(f"✗ Missing package: {e}")
    print("\nPlease install required packages:")
    print("  conda install yfinance pandas matplotlib numpy")
    print("  OR")
    print("  pip install yfinance pandas matplotlib numpy")
    sys.exit(1)

# Import and run the main script
try:
    from main import main
    print("Running visualization pipeline...")
    print("-" * 60)
    main()
    print()
    print("=" * 60)
    print("SUCCESS! Visualizations generated in 'visualizations/' folder")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check the visualizations/ folder for generated PNG files")
    print("2. Commit the images to git:")
    print("   git add stock_analysis_portfolio/visualizations/*.png")
    print("   git commit -m 'Add stock portfolio visualizations'")
    print("   git push")
except Exception as e:
    print(f"✗ Error running visualization: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)



