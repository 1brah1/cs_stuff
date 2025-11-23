"""
Simple Stock Market Analysis
Main script to collect data and create visualizations
"""

from data_collector import collect_all_data
from visualize import create_all_visualizations

def main():
    """Run complete analysis pipeline"""
    print("=" * 60)
    print("STOCK MARKET DATA ANALYSIS & VISUALIZATION")
    print("=" * 60)
    
    # Step 1: Collect data
    print("\n[STEP 1/2] Collecting stock data from yFinance...")
    print("-" * 60)
    collect_all_data()
    
    # Step 2: Create visualizations
    print("\n[STEP 2/2] Creating visualizations...")
    print("-" * 60)
    create_all_visualizations()
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\nCheck the 'visualizations' folder for all generated charts.")
    print("Check 'stock_data.db' for the SQL database.")

if __name__ == "__main__":
    main()
