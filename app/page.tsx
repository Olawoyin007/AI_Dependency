'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { calculateScore, determineRiskLevel } from '@/lib/assessment';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

const professions = {
  "Developer": "Code Craftsman",
  "Writer": "Word Weaver",
  "Student": "Knowledge Seeker",
  "Designer": "Visual Artist",
  "Doctor": "Health Guardian",
  "Lawyer": "Justice Keeper",
  "Marketer": "Story Teller",
  "Project Manager": "Harmony Creator",
  "Customer Support": "Connection Builder",
  "Entrepreneur": "Vision Pioneer",
  "General User": "Digital Explorer"
};

const questions = [
  {
    id: "daily_usage",
    text: "How often do you use AI tools in your daily work?",
    options: ["Never", "Rarely", "Sometimes", "Often", "Always"]
  },
  {
    id: "decision_making",
    text: "To what extent do you rely on AI for decision-making?",
    options: ["Never", "Rarely", "Sometimes", "Often", "Always"]
  },
  {
    id: "content_creation",
    text: "How frequently do you use AI for content creation?",
    options: ["Never", "Rarely", "Sometimes", "Often", "Always"]
  }
];

export default function Assessment() {
  const [profession, setProfession] = useState("");
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [score, setScore] = useState<number | null>(null);
  const [showResults, setShowResults] = useState(false);

  const handleResponse = (questionId: string, response: string) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: response
    }));
  };

  const handleSubmit = () => {
    const calculatedScore = calculateScore(responses);
    setScore(calculatedScore);
    setShowResults(true);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          AI Dependency Assessment
        </h1>

        {!showResults ? (
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Select Your Role</h2>
              <select
                value={profession}
                onChange={(e) => setProfession(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a profession</option>
                {Object.entries(professions).map(([key, value]) => (
                  <option key={key} value={key}>{value}</option>
                ))}
              </select>
            </div>

            {profession && (
              <div className="space-y-6">
                {questions.map((question) => (
                  <div key={question.id} className="bg-white rounded-lg shadow-lg p-6">
                    <h3 className="text-lg font-medium mb-4">{question.text}</h3>
                    <div className="grid grid-cols-5 gap-4">
                      {question.options.map((option) => (
                        <button
                          key={option}
                          onClick={() => handleResponse(question.id, option)}
                          className={`p-3 rounded-lg transition-colors ${
                            responses[question.id] === option
                              ? 'bg-blue-500 text-white'
                              : 'bg-gray-100 hover:bg-gray-200'
                          }`}
                        >
                          {option}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}

                <button
                  onClick={handleSubmit}
                  disabled={Object.keys(responses).length !== questions.length}
                  className="w-full bg-blue-500 text-white py-4 rounded-lg font-semibold hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  Calculate Score
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-6">Assessment Results</h2>
            {score !== null && (
              <div className="space-y-6">
                <div className="text-center">
                  <div className="text-6xl font-bold text-blue-500 mb-2">
                    {score}%
                  </div>
                  <p className="text-gray-600">
                    {determineRiskLevel(score)}
                  </p>
                </div>

                <div className="h-96">
                  <Plot
                    data={[
                      {
                        type: 'indicator',
                        mode: 'gauge+number',
                        value: score,
                        title: { text: 'AI Dependency Score' },
                        gauge: {
                          axis: { range: [0, 100] },
                          bar: { color: 'darkblue' },
                          steps: [
                            { range: [0, 30], color: 'lightgreen' },
                            { range: [30, 60], color: 'lightyellow' },
                            { range: [60, 80], color: 'orange' },
                            { range: [80, 100], color: 'red' }
                          ]
                        }
                      }
                    ]}
                    layout={{
                      height: 300,
                      margin: { t: 0, b: 0 }
                    }}
                  />
                </div>

                <button
                  onClick={() => {
                    setShowResults(false);
                    setResponses({});
                    setScore(null);
                  }}
                  className="w-full bg-gray-500 text-white py-4 rounded-lg font-semibold hover:bg-gray-600 transition-colors"
                >
                  Start New Assessment
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
} 