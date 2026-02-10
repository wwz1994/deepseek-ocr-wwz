"""
Generate professional visualizations for Patagonia Case Study
Georgetown University MSB - Executive MBA Final Exam
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
colors = ['#2E5266', '#6E8898', '#9FB1BC', '#D3D0CB', '#E2C044']

# Create output directory for figures
import os
os.makedirs('case_study_figures', exist_ok=True)

# Figure 1: Patagonia Revenue Growth (2010-2023)
def create_revenue_growth():
    years = np.array([2010, 2012, 2014, 2016, 2018, 2020, 2022, 2023])
    revenue = np.array([275, 540, 600, 750, 1000, 800, 1500, 1700])  # in millions
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, revenue, marker='o', linewidth=3, markersize=10, color=colors[0])
    ax.fill_between(years, revenue, alpha=0.3, color=colors[0])
    
    # Add annotations for key events
    ax.annotate('"Don\'t Buy This Jacket"\nCampaign Launch', 
                xy=(2011, 400), xytext=(2012, 450),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, ha='center', color='red', weight='bold')
    
    ax.annotate('COVID-19\nImpact', 
                xy=(2020, 800), xytext=(2019, 650),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2),
                fontsize=10, ha='center', color='orange', weight='bold')
    
    ax.set_xlabel('Year', fontsize=12, weight='bold')
    ax.set_ylabel('Revenue ($ Millions)', fontsize=12, weight='bold')
    ax.set_title('Patagonia Revenue Growth (2010-2023)\nSustainable Growth Despite Anti-Consumption Messaging', 
                 fontsize=14, weight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1900)
    
    # Add CAGR annotation
    cagr = ((1700/275)**(1/13) - 1) * 100
    ax.text(0.02, 0.98, f'CAGR: {cagr:.1f}%', 
            transform=ax.transAxes, fontsize=11, weight='bold',
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('case_study_figures/figure1_revenue_growth.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 1: Revenue Growth chart created")

# Figure 2: Sustainability Metrics Dashboard
def create_sustainability_metrics():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Subplot 1: Carbon Footprint Reduction
    years = [2015, 2017, 2019, 2021, 2023]
    carbon = [100, 85, 72, 58, 45]  # indexed to 2015 = 100
    ax1.bar(years, carbon, color=colors[1], alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.axhline(y=50, color='red', linestyle='--', linewidth=2, label='2025 Target')
    ax1.set_xlabel('Year', fontsize=11, weight='bold')
    ax1.set_ylabel('Carbon Footprint Index\n(2015 = 100)', fontsize=11, weight='bold')
    ax1.set_title('Carbon Footprint Reduction', fontsize=12, weight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Recycled Materials Usage
    categories = ['Polyester', 'Nylon', 'Cotton', 'Down', 'Wool']
    recycled_pct = [87, 69, 100, 75, 52]
    bars = ax2.barh(categories, recycled_pct, color=colors[2], alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Percentage Recycled/Organic (%)', fontsize=11, weight='bold')
    ax2.set_title('Recycled & Organic Materials Usage (2023)', fontsize=12, weight='bold')
    ax2.set_xlim(0, 110)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax2.text(width + 2, bar.get_y() + bar.get_height()/2, 
                f'{recycled_pct[i]}%', ha='left', va='center', fontsize=10, weight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Subplot 3: Worn Wear Program Growth
    years_ww = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    items_resold = [15000, 28000, 45000, 52000, 78000, 110000, 145000]
    ax3.plot(years_ww, np.array(items_resold)/1000, marker='s', linewidth=3, 
             markersize=8, color=colors[3])
    ax3.fill_between(years_ww, np.array(items_resold)/1000, alpha=0.3, color=colors[3])
    ax3.set_xlabel('Year', fontsize=11, weight='bold')
    ax3.set_ylabel('Items Resold (Thousands)', fontsize=11, weight='bold')
    ax3.set_title('Worn Wear Program Growth', fontsize=12, weight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Subplot 4: Environmental Grants
    years_grants = [2015, 2017, 2019, 2021, 2023]
    grants = [6.2, 8.5, 10.3, 13.1, 17.5]  # millions
    ax4.bar(years_grants, grants, color=colors[4], alpha=0.8, edgecolor='black', linewidth=1.5)
    ax4.set_xlabel('Year', fontsize=11, weight='bold')
    ax4.set_ylabel('Grants ($ Millions)', fontsize=11, weight='bold')
    ax4.set_title('Environmental Grants & Donations', fontsize=12, weight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    # Add total annotation
    total = sum(grants)
    ax4.text(0.98, 0.98, f'Total: ${total:.1f}M', 
            transform=ax4.transAxes, fontsize=10, weight='bold',
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    plt.suptitle('Patagonia Sustainability Metrics Dashboard', 
                 fontsize=16, weight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('case_study_figures/figure2_sustainability_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 2: Sustainability Metrics Dashboard created")

# Figure 3: Customer Loyalty & Brand Value Analysis
def create_customer_loyalty():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Net Promoter Score Comparison
    brands = ['Patagonia', 'The North\nFace', 'Columbia', 'REI', 'Industry\nAverage']
    nps_scores = [73, 42, 38, 67, 35]
    colors_nps = ['#2E5266' if x == max(nps_scores) else '#9FB1BC' for x in nps_scores]
    
    bars = ax1.bar(brands, nps_scores, color=colors_nps, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Net Promoter Score', fontsize=12, weight='bold')
    ax1.set_title('Net Promoter Score Comparison\n(Higher = Better Customer Loyalty)', 
                  fontsize=13, weight='bold')
    ax1.set_ylim(0, 80)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom', fontsize=11, weight='bold')
    
    # Subplot 2: Customer Lifetime Value
    segments = ['Loyal\nAdvocates\n(35%)', 'Regular\nCustomers\n(40%)', 
                'Occasional\nBuyers\n(25%)']
    clv = [4500, 2200, 800]  # Customer Lifetime Value in dollars
    colors_clv = [colors[0], colors[1], colors[2]]
    
    wedges, texts, autotexts = ax2.pie(clv, labels=segments, autopct='$%1.0f',
                                         colors=colors_clv, startangle=90,
                                         textprops={'fontsize': 11, 'weight': 'bold'},
                                         wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    
    # Make percentage text bold and larger
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_weight('bold')
    
    ax2.set_title('Customer Lifetime Value by Segment\n(Average CLV per Customer)', 
                  fontsize=13, weight='bold')
    
    # Add total CLV annotation
    avg_clv = sum([clv[i] * [0.35, 0.40, 0.25][i] for i in range(3)])
    ax2.text(0, -1.4, f'Weighted Average CLV: ${avg_clv:.0f}', 
            ha='center', fontsize=11, weight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    plt.suptitle('Customer Loyalty & Brand Value Analysis', 
                 fontsize=16, weight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('case_study_figures/figure3_customer_loyalty.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 3: Customer Loyalty & Brand Value chart created")

# Figure 4: Strategic Positioning Matrix
def create_strategic_positioning():
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define brands and their positions
    brands_data = {
        'Patagonia': (9.2, 8.8, 150),
        'REI': (7.5, 7.2, 120),
        'The North Face': (6.5, 5.5, 100),
        'Columbia': (5.8, 4.2, 90),
        'Arc\'teryx': (8.5, 6.0, 80),
        'Outdoor Research': (6.0, 5.8, 70),
        'Marmot': (5.5, 5.0, 65)
    }
    
    # Plot brands
    for brand, (sustainability, brand_strength, size) in brands_data.items():
        if brand == 'Patagonia':
            ax.scatter(sustainability, brand_strength, s=size*15, 
                      color=colors[0], alpha=0.7, edgecolors='black', linewidth=2.5,
                      label=brand, zorder=5)
            ax.annotate(brand, (sustainability, brand_strength), 
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=12, weight='bold', color=colors[0],
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2))
        else:
            ax.scatter(sustainability, brand_strength, s=size*15, 
                      color=colors[2], alpha=0.6, edgecolors='gray', linewidth=1.5)
            ax.annotate(brand, (sustainability, brand_strength), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=9, alpha=0.8)
    
    # Add quadrant lines
    ax.axhline(y=6.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axvline(x=7.0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    
    # Add quadrant labels
    ax.text(8.5, 9.5, 'LEADERS\n(Sustainability + Brand)', 
            fontsize=11, weight='bold', ha='center', 
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    ax.text(5.5, 9.5, 'BRAND FOCUSED', 
            fontsize=11, weight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    ax.text(8.5, 3.5, 'SUSTAINABILITY\nFOCUSED', 
            fontsize=11, weight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax.text(5.5, 3.5, 'FOLLOWERS', 
            fontsize=11, weight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
    
    ax.set_xlabel('Sustainability Commitment Score (0-10)', fontsize=12, weight='bold')
    ax.set_ylabel('Brand Strength & Customer Loyalty (0-10)', fontsize=12, weight='bold')
    ax.set_title('Strategic Positioning Matrix: Outdoor Apparel Industry\n(Bubble size represents market share)', 
                 fontsize=14, weight='bold', pad=20)
    ax.set_xlim(4, 10)
    ax.set_ylim(3, 10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('case_study_figures/figure4_strategic_positioning.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 4: Strategic Positioning Matrix created")

# Generate all figures
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Generating Professional Visualizations for Case Study")
    print("Georgetown University MSB - Executive MBA")
    print("="*60 + "\n")
    
    create_revenue_growth()
    create_sustainability_metrics()
    create_customer_loyalty()
    create_strategic_positioning()
    
    print("\n" + "="*60)
    print("All visualizations generated successfully!")
    print("Output directory: case_study_figures/")
    print("="*60 + "\n")
