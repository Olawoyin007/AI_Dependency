const FREQUENCY_MAP = {
  "Never": 0,
  "Rarely": 25,
  "Sometimes": 50,
  "Often": 75,
  "Always": 100
};

export const calculateScore = (responses: Record<string, string>): number => {
  const values = Object.values(responses).map(response => FREQUENCY_MAP[response as keyof typeof FREQUENCY_MAP]);
  const average = values.reduce((sum, value) => sum + value, 0) / values.length;
  return Math.round(average);
};

export const determineRiskLevel = (score: number): string => {
  if (score < 30) {
    return "Low Risk: You maintain a healthy balance with AI tools";
  } else if (score < 60) {
    return "Moderate Risk: Consider setting boundaries for AI usage";
  } else if (score < 80) {
    return "High Risk: Significant dependency on AI tools detected";
  } else {
    return "Critical Risk: Immediate attention needed to reduce AI dependency";
  }
};

export const analyzePatterns = (responses: Record<string, string>) => {
  const patterns = {
    dailyUsage: FREQUENCY_MAP[responses.daily_usage as keyof typeof FREQUENCY_MAP],
    decisionMaking: FREQUENCY_MAP[responses.decision_making as keyof typeof FREQUENCY_MAP],
    contentCreation: FREQUENCY_MAP[responses.content_creation as keyof typeof FREQUENCY_MAP]
  };

  return {
    ...patterns,
    highestDependency: Object.entries(patterns).reduce((a, b) => a[1] > b[1] ? a : b)[0],
    lowestDependency: Object.entries(patterns).reduce((a, b) => a[1] < b[1] ? a : b)[0]
  };
}; 