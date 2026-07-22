import React from 'react';

interface InsightsPanelProps {
  forecastData: any;
}

const InsightsPanel: React.FC<InsightsPanelProps> = ({ forecastData }) => {
  const generateInsightTitle = (trend: string): string => {
    return trend === 'up' ? 'Optimize Sales Strategy' : 'Focus on Customer Retention and Upselling';
  };

  const generateInsightDescription = (trend: string): string => {
    return trend === 'up'
      ? 'Increase marketing efforts in high-demand regions.'
      : 'Reduce costs in underperforming regions or product lines.';
  };

  const generateInsights = (): { title: string; description: string }[] => {
    if (!forecastData || !forecastData.salesTrend) return [];

    const trend = forecastData.salesTrend;
    return [
      { title: generateInsightTitle(trend), description: generateInsightDescription(trend) },
      { title: 'Resource Allocation', description: trend === 'up' ? 'Allocate more resources to growing product lines.' : 'Reduce costs in underperforming regions or product lines.' }
    ];
  };

  const insights = generateInsights();

  return (
    <div className="insights-panel p-8">
      <h2 className="text-4xl font-bold mb-10">Actionable Insights</h2>
      {insights.map((insight, index) => (
        <div key={index} className="bg-white shadow-lg rounded-lg p-8 mb-6 hover:bg-gray-50 transition-colors duration-300">
          <h3 className="text-xl font-semibold mb-4">{insight.title}</h3>
          <p className="text-base text-gray-700">{insight.description}</p>
        </div>
      ))}
    </div>
  );
};

export default InsightsPanel;
