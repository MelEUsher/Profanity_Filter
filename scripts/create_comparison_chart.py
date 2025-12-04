#!/usr/bin/env python3
"""
Create visual comparison chart of Regex vs LLM performance metrics.

This script generates a high-quality bar chart comparing:
- Accuracy
- Precision
- Recall
- F1 Score

for both Regex and LLM approaches.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def create_comparison_chart():
    """Create and save comparison chart."""

    # Metrics from comparison results
    # These values come from running compare_approaches.py
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    regex_values = [0.600, 0.857, 0.240, 0.375]
    llm_values = [0.800, 0.759, 0.880, 0.815]

    # Set up the bar chart
    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))

    # Create bars
    bars1 = ax.bar(x - width/2, regex_values, width, label='Regex',
                   color='steelblue', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, llm_values, width, label='LLM',
                   color='coral', edgecolor='black', linewidth=1.2)

    # Customize chart
    ax.set_xlabel('Metric', fontsize=14, fontweight='bold')
    ax.set_ylabel('Score', fontsize=14, fontweight='bold')
    ax.set_title('Regex vs LLM Profanity Filter Performance\n(Same 50-Message Sample)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=12)
    ax.set_ylim(0, 1.0)
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # Add value labels on bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')

    add_value_labels(bars1)
    add_value_labels(bars2)

    # Adjust layout and save
    plt.tight_layout()

    output_file = Path('results/comparison_chart.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_file}")
    plt.close()


if __name__ == '__main__':
    create_comparison_chart()
