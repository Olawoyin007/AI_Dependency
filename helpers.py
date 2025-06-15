import random
from constants import FREQUENCY_MAP, GENERAL_QUESTIONS, PROFESSION_QUESTIONS
from constants import MOTIVATIONAL_QUOTES


# Function to calculate AI Dependency Score
def calculate_score(responses, questions):
    total_score = 0
    breakdown = []
    
    for question, key, weight in questions:  # Use dynamically provided question set
        response_value = FREQUENCY_MAP.get(responses.get(key, "never"), 0)
        score_contrib = response_value * weight
        breakdown.append((question, responses.get(key, "never"), weight, response_value, score_contrib))
        total_score += score_contrib
    
    max_score = sum(4 * weight for _, _, weight in questions) if questions else 1  # Prevent division by zero
    normalized_score = int((total_score / max_score) * 100)
    
    return normalized_score, breakdown


# Function to determine dependency level
def determine_risk_level(score):
    if score < 30:
        return "Low Dependency", "Your inner genius is fully in control!"
    elif score < 60:
        return "Moderate Dependency", "AI is a tool, but don't forget your mind!"
    elif score < 80:
        return "High Dependency", "Time to flex those mental muscles!"
    else:
        return "Critical Dependency", "Heavy AI reliance! Try a digital detox."

# Time-based projections for increased dependency
def time_based_projections(score):
    return {
        '6 months': min(100, int(score + score * 0.10)),
        '1 year': min(100, int(score + score * 0.25)),
        '2 years': min(100, int(score + score * 0.50))
    }

# Personalized Detox Plan
def generate_detox_plan(score):
    if score < 30:
        return [
            "Keep up the great work—challenge yourself with new problems!",
            "Try a weekly 'no-AI day' to celebrate your independent thinking!"
        ]
    elif score < 60:
        return [
            "Schedule time to work without AI assistance.",
            "Experiment with brain teasers and creative problem-solving games."
        ]
    elif score < 80:
        return [
            "Implement a gradual AI detox—start with one day a week.",
            "Join a hackathon or coding dojo for creativity."
        ]
    else:
        return [
            "Adopt a strict detox: one full day without AI, then increase.",
            "Engage in brainstorming sessions without digital tools.",
            "Try mindfulness exercises and journaling to track progress."
        ]

# Get a random motivational quote
def get_random_quote():
    return random.choice(MOTIVATIONAL_QUOTES)
