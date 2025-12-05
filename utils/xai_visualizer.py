"""
XAI 可視化模組 - 展示模型如何判斷文本
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import plotly.graph_objects as go
import plotly.express as px

plt.rcParams['font.sans-serif'] = ['Arial', 'SimHei']  # 支持中文
sns.set_style("whitegrid")


class XAIVisualizer:
    """XAI 視覺化工具"""
    
    @staticmethod
    def plot_feature_importance(
        top_features: List[Tuple[str, float]],
        title: str = "Feature Importance for AI Detection"
    ) -> go.Figure:
        """
        繪製特徵重要性圖
        
        Args:
            top_features: [(特徵名, 係數)] 列表
            title: 圖表標題
            
        Returns:
            Plotly Figure
        """
        names = [f[0] for f in top_features]
        values = [f[1] for f in top_features]
        colors = ['red' if v > 0 else 'blue' for v in values]
        
        fig = go.Figure(
            data=go.Bar(
                x=values,
                y=names,
                orientation='h',
                marker=dict(color=colors, opacity=0.7),
                text=values,
                textposition='auto',
            )
        )
        
        fig.update_layout(
            title=title,
            xaxis_title="Coefficient Value",
            yaxis_title="Features",
            height=400,
            template="plotly_white",
            showlegend=False,
        )
        
        return fig
    
    @staticmethod
    def plot_probability_gauge(
        ai_probability: float,
        title: str = "AI Detection Probability"
    ) -> go.Figure:
        """
        繪製概率量表
        
        Args:
            ai_probability: AI 概率 (0-1)
            title: 圖表標題
            
        Returns:
            Plotly Figure
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ai_probability * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "lightblue"},
                    {'range': [50, 75], 'color': "lightyellow"},
                    {'range': [75, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=400, template="plotly_white")
        return fig
    
    @staticmethod
    def plot_feature_distribution(
        features_dict: Dict[str, float],
        top_n: int = 10
    ) -> go.Figure:
        """
        繪製特徵分布
        
        Args:
            features_dict: 特徵字典
            top_n: 顯示前 N 個特徵
            
        Returns:
            Plotly Figure
        """
        # 選擇前 top_n 個特徵
        sorted_features = sorted(
            features_dict.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:top_n]
        
        names = [f[0] for f in sorted_features]
        values = [f[1] for f in sorted_features]
        
        fig = go.Figure(
            data=go.Bar(
                x=names,
                y=values,
                marker=dict(color=values, colorscale='RdBu', showscale=True),
                text=values,
                textposition='auto',
            )
        )
        
        fig.update_layout(
            title="Top Features Distribution",
            xaxis_title="Features",
            yaxis_title="Value",
            height=400,
            template="plotly_white",
            xaxis_tickangle=-45,
        )
        
        return fig
    
    @staticmethod
    def plot_text_token_heatmap(
        tokens: List[str],
        token_scores: List[float],
        title: str = "Token Importance Heatmap"
    ) -> go.Figure:
        """
        繪製 Token 重要性熱力圖
        
        Args:
            tokens: Token 列表
            token_scores: 對應的分數列表
            title: 圖表標題
            
        Returns:
            Plotly Figure
        """
        # 整理成矩陣形狀以方便視覺化
        chunk_size = 20
        heatmap_data = []
        token_labels = []
        
        for i in range(0, len(tokens), chunk_size):
            chunk = tokens[i:i+chunk_size]
            scores = token_scores[i:i+chunk_size]
            heatmap_data.append(scores)
            token_labels.extend(chunk)
        
        fig = go.Figure(
            data=go.Heatmap(
                z=heatmap_data,
                colorscale='RdYlGn',
                colorbar=dict(title="Importance"),
                text=token_labels,
            )
        )
        
        fig.update_layout(
            title=title,
            xaxis_title="Token Position",
            yaxis_title="Text Chunk",
            height=300,
            template="plotly_white",
        )
        
        return fig
    
    @staticmethod
    def plot_prediction_comparison(
        prediction_results: Dict
    ) -> go.Figure:
        """
        繪製 Human vs AI 概率對比
        
        Args:
            prediction_results: 預測結果字典
            
        Returns:
            Plotly Figure
        """
        fig = go.Figure(
            data=[
                go.Bar(
                    name='Human',
                    x=['Probability'],
                    y=[prediction_results['human_probability']],
                    marker=dict(color='lightblue'),
                ),
                go.Bar(
                    name='AI',
                    x=['Probability'],
                    y=[prediction_results['ai_probability']],
                    marker=dict(color='lightcoral'),
                )
            ]
        )
        
        fig.update_layout(
            title="Human vs AI Probability",
            barmode='stack',
            height=400,
            template="plotly_white",
            yaxis_title="Probability",
            showlegend=True,
        )
        
        return fig
    
    @staticmethod
    def plot_feature_radar(
        features_dict: Dict[str, float],
        categories: List[str] = None
    ) -> go.Figure:
        """
        繪製雷達圖
        
        Args:
            features_dict: 特徵字典
            categories: 特徵類別（若為 None 則使用字典的鍵）
            
        Returns:
            Plotly Figure
        """
        if categories is None:
            categories = list(features_dict.keys())[:8]  # 限制為 8 個特徵
        
        values = [features_dict.get(cat, 0) for cat in categories]
        values += values[:1]  # 閉合雷達圖
        
        fig = go.Figure(
            data=go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name='Features',
                line=dict(color='red'),
                fillcolor='rgba(255, 0, 0, 0.3)',
            )
        )
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values)],
                )
            ),
            title="Feature Radar Chart",
            height=500,
            template="plotly_white",
        )
        
        return fig
    
    @staticmethod
    def create_summary_dashboard(
        prediction_results: Dict
    ) -> Dict:
        """
        建立完整儀表板所需的所有圖表
        
        Args:
            prediction_results: 預測結果字典
            
        Returns:
            包含各種圖表的字典
        """
        visualizer = XAIVisualizer()
        
        dashboard = {
            'probability_gauge': visualizer.plot_probability_gauge(
                prediction_results['ai_probability']
            ),
            'feature_importance': visualizer.plot_feature_importance(
                prediction_results['top_features']
            ),
            'prediction_comparison': visualizer.plot_prediction_comparison(
                prediction_results
            ),
        }
        
        # 如果有足夠的特徵，添加特徵分布圖
        if prediction_results['extracted_features']:
            # 只選擇數值特徵
            numeric_features = {
                k: v for k, v in prediction_results['extracted_features'].items()
                if isinstance(v, (int, float))
            }
            if numeric_features:
                dashboard['feature_distribution'] = visualizer.plot_feature_distribution(
                    numeric_features
                )
        
        return dashboard


if __name__ == "__main__":
    # 測試
    test_prediction = {
        'ai_probability': 0.85,
        'human_probability': 0.15,
        'confidence': 0.85,
        'top_features': [
            ('pp_avg_perplexity', 0.42),
            ('style_func_word_ratio', 0.38),
            ('burst_burstiness', -0.35),
            ('pp_log_prob_std', 0.28),
            ('zipf_tail_ratio', -0.25),
        ],
        'extracted_features': {
            'pp_avg_perplexity': 25.3,
            'burst_burstiness': 0.45,
            'style_ttr': 0.65,
        }
    }
    
    visualizer = XAIVisualizer()
    
    # 生成各種圖表
    fig1 = visualizer.plot_probability_gauge(test_prediction['ai_probability'])
    fig1.show()
    
    fig2 = visualizer.plot_feature_importance(test_prediction['top_features'])
    fig2.show()
    
    fig3 = visualizer.plot_prediction_comparison(test_prediction)
    fig3.show()
