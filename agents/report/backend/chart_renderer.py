"""
Chart rendering utilities for the Report Agent.
Generates actual PNG/JPG charts using matplotlib and saves them to the `generated` directory.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class ChartRenderer:
    """
    Renders visualization data as actual chart images.
    """
    
    def __init__(self, output_dir: str = "api_server/public"):
        """
        Initialize the chart renderer.
        
        Args:
            output_dir: Directory to save chart images
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_unique_filename(self, user_session_id: str, chart_type: str = "dashboard") -> str:
        """
        Generate a unique filename for a chart.
        
        Args:
            user_session_id: User's session ID
            chart_type: Type of chart (dashboard, progress, etc.)
            
        Returns:
            Unique filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"report_{user_session_id}_{chart_type}_{timestamp}_{unique_id}.png"
    
    def render_dashboard(
        self,
        viz_data: Dict[str, Any],
        user_session_id: str,
        days: int = 14
    ) -> str:
        """
        Render a complete dashboard with all charts.
        
        Args:
            viz_data: Visualization data from generate_all_visualizations
            user_session_id: User's session ID
            days: Number of days covered in the report
            
        Returns:
            Relative path to the saved chart file
        """
        try:
            # Create figure with subplots
            fig = plt.figure(figsize=(20, 12))
            gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
            
            # Create subplots
            ax1 = fig.add_subplot(gs[0, :])  # Top row - full width
            self._plot_progress_over_time(viz_data['progress_over_time'], ax1)
            
            ax2 = fig.add_subplot(gs[1, 0])  # Middle-left
            self._plot_difficulty_breakdown(viz_data['difficulty_breakdown'], ax2)
            
            ax3 = fig.add_subplot(gs[1, 1])  # Middle-center
            self._plot_quiz_performance(viz_data['quiz_performance_trend'], ax3)
            
            ax4 = fig.add_subplot(gs[1, 2])  # Middle-right
            self._plot_learning_time(viz_data['learning_time'], ax4)
            
            ax5 = fig.add_subplot(gs[2, :2])  # Bottom-left, wide
            self._plot_topic_mastery(viz_data['topic_mastery'], ax5)
            
            ax6 = fig.add_subplot(gs[2, 2])   # Bottom-right
            self._plot_topic_distribution(viz_data['topic_distribution'], ax6)
            
            # Add main title
            fig.suptitle(f'Learning Progress Dashboard - Last {days} Days', 
                         fontsize=18, fontweight='bold')
            
            # Save the figure
            filename = self.generate_unique_filename(user_session_id, "dashboard")
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close(fig)
            
            logger.info(f"✅ Dashboard chart saved: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ Error rendering dashboard: {e}")
            raise
    
    def _plot_progress_over_time(self, chart_data: Dict[str, Any], ax):
        """Plot progress over time."""
        if not chart_data.get('labels'):
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return
            
        labels = chart_data['labels']
        for dataset in chart_data['datasets']:
            ax.plot(labels, dataset['data'], label=dataset['label'], 
                   marker='o', linewidth=2, markersize=6)
        
        ax.set_title(chart_data['title'], fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Score (%)', fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)
    
    def _plot_difficulty_breakdown(self, chart_data: Dict[str, Any], ax):
        """Plot difficulty breakdown."""
        if not chart_data.get('labels'):
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return
            
        labels = chart_data['labels']
        data = chart_data['datasets'][0]['data']
        colors = ['#4BC0C0', '#FFCE56', '#FF6384']
        
        ax.bar(labels, data, color=colors, alpha=0.7, edgecolor='black')
        ax.set_title(chart_data['title'], fontsize=14, fontweight='bold')
        ax.set_ylabel('Accuracy (%)', fontsize=10)
        ax.set_ylim(0, 100)
        ax.grid(True, axis='y', alpha=0.3)
    
    def _plot_topic_mastery(self, chart_data: Dict[str, Any], ax):
        """Plot topic mastery."""
        if not chart_data.get('labels'):
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return
            
        labels = chart_data['labels']
        datasets = chart_data['datasets']
        x = np.arange(len(labels))
        width = 0.35
        
        for i, dataset in enumerate(datasets):
            offset = width * (i - len(datasets)/2 + 0.5)
            ax.barh(x + offset, dataset['data'], width, 
                   label=dataset['label'], alpha=0.7)
        
        ax.set_yticks(x)
        ax.set_yticklabels(labels, fontsize=9)
        ax.set_xlabel('Score (%)', fontsize=10)
        ax.set_title(chart_data['title'], fontsize=14, fontweight='bold')
        ax.legend(fontsize=9)
        ax.set_xlim(0, 100)
        ax.grid(True, axis='x', alpha=0.3)
    
    def _plot_quiz_performance(self, chart_data: Dict[str, Any], ax):
        """Plot quiz performance trend."""
        if not chart_data.get('labels'):
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return
            
        labels = chart_data['labels']
        for dataset in chart_data['datasets']:
            linestyle = '--' if 'Average' in dataset['label'] else '-'
            marker = 'o' if 'Score' in dataset['label'] else ''
            ax.plot(labels, dataset['data'], label=dataset['label'], 
                   marker=marker, linestyle=linestyle, linewidth=2, markersize=6)
        
        ax.set_title(chart_data['title'], fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Score (%)', fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)
    
    def _plot_learning_time(self, chart_data: Dict[str, Any], ax):
        """Plot learning time."""
        if not chart_data.get('labels'):
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return
            
        labels = chart_data['labels']
        data = chart_data['datasets'][0]['data']
        
        ax.bar(labels, data, color='#9966FF', alpha=0.7, edgecolor='black')
        ax.set_title(chart_data['title'], fontsize=14, fontweight='bold')
        ax.set_ylabel('Minutes', fontsize=10)
        ax.grid(True, axis='y', alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)
    
    def _plot_topic_distribution(self, chart_data: Dict[str, Any], ax):
        """Plot topic distribution pie chart."""
        if not chart_data.get('labels'):
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return
            
        labels = chart_data['labels']
        data = chart_data['datasets'][0]['data']
        
        # Convert CSS colors to matplotlib colors
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
                 '#9966FF', '#FF9F40', '#C7C7C7', '#5366FF'][:len(labels)]
        
        wedges, texts, autotexts = ax.pie(data, labels=labels, colors=colors,
                                            autopct='%1.1f%%', startangle=90)
        ax.set_title(chart_data['title'], fontsize=14, fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(8)
        
        for text in texts:
            text.set_fontsize(8)
    
    def render_single_chart(
        self,
        chart_data: Dict[str, Any],
        user_session_id: str,
        chart_type: str
    ) -> str:
        """
        Render a single chart.
        
        Args:
            chart_data: Chart data for a specific visualization
            user_session_id: User's session ID
            chart_type: Type of chart (progress, difficulty, etc.)
            
        Returns:
            Relative path to the saved chart file
        """
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Route to appropriate plot function
            plot_functions = {
                'progress_over_time': self._plot_progress_over_time,
                'difficulty_breakdown': self._plot_difficulty_breakdown,
                'topic_mastery': self._plot_topic_mastery,
                'quiz_performance_trend': self._plot_quiz_performance,
                'learning_time': self._plot_learning_time,
                'topic_distribution': self._plot_topic_distribution,
            }
            
            plot_func = plot_functions.get(chart_type)
            if plot_func:
                plot_func(chart_data, ax)
            else:
                ax.text(0.5, 0.5, f'Unknown chart type: {chart_type}', 
                       ha='center', va='center')
            
            # Save the figure
            filename = self.generate_unique_filename(user_session_id, chart_type)
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close(fig)
            
            logger.info(f"✅ Single chart saved: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ Error rendering single chart: {e}")
            raise
