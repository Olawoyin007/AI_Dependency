# ---------------------------
# Configuration & Constants
# ---------------------------

FREQUENCY_MAP = {
    "never": 0,
    "rarely": 1,
    "sometimes": 2,
    "often": 3,
    "always": 4
}

OPTIONS = list(FREQUENCY_MAP.keys())

# General Questions (For All Users)
GENERAL_QUESTIONS = [
    ("How often do you use AI to help with decision-making?", "decision", 4),
    ("How frequently do you consume AI-curated news feeds?", "news", 3),
    ("Do you use AI for writing, summarizing, or generating content?", "content", 3),
    ("How often do you rely on AI for recommendations (movies, music, shopping)?", "recommendations", 3),
    ("Do you use AI-powered virtual assistants (Siri, Alexa, Google Assistant)?", "assistants", 2)
]

# Profession-Specific Questions
PROFESSION_QUESTIONS = {
    "Developer": [
        ("How often do you use AI to generate or refine your code?", "coding", 5),
        ("How much do you rely on AI for debugging?", "debugging", 4),
        ("Do you use AI for system design suggestions?", "design", 3),
        ("How frequently do you use AI-generated scripts or boilerplate code?", "boilerplate", 4)
    ],
    "Writer": [
        ("Do you use AI to generate blog ideas, stories, or article drafts?", "writing", 5),
        ("How frequently do you use AI to correct grammar & improve clarity?", "grammar", 4),
        ("Do you use AI tools for creative writing prompts?", "creativity", 3),
        ("Do you use AI to analyze reader engagement & optimize content?", "seo", 3)
    ],
    "Student": [
        ("Do you rely on AI to summarize or explain study material?", "study", 5),
        ("How often do you use AI to generate research reports or essays?", "essays", 4),
        ("Do you use AI-powered tutoring platforms?", "tutoring", 3),
        ("Do you use AI-generated flashcards or study plans?", "flashcards", 3)
    ],
    "Designer": [
        ("Do you use AI to generate art, logos, or design ideas?", "designing", 5),
        ("How frequently do you rely on AI tools for photo or video editing?", "editing", 4),
        ("Do you use AI-powered tools for UI/UX design?", "ux_design", 3),
        ("Have you used AI to generate complete design mockups?", "mockups", 3)
    ],
    "Doctor / Medical Professional": [
        ("Do you use AI tools for diagnosing or recommending treatments?", "diagnosis", 5),
        ("Do you rely on AI for medical research summaries?", "med_research", 4),
        ("How frequently do you use AI for patient record analysis?", "records", 3),
        ("Do you use AI-powered chatbots for patient interaction?", "chatbots", 3)
    ],
    "Lawyer / Legal Professional": [
        ("Do you use AI for legal research or case analysis?", "legal_research", 5),
        ("How frequently do you rely on AI to draft legal documents?", "legal_docs", 4),
        ("Do you use AI-powered contract review tools?", "contracts", 3),
        ("Have you used AI to predict legal outcomes based on past cases?", "predict_cases", 3)
    ],
    "Marketer": [
        ("Do you use AI for generating social media posts or ad copy?", "ads", 5),
        ("How often do you use AI for market trend analysis?", "market_trends", 4),
        ("Do you use AI for SEO optimization and keyword suggestions?", "seo", 3),
        ("Do you rely on AI-driven chatbots for customer engagement?", "chatbots", 3)
    ],
    "Project Manager": [
        ("Do you use AI to predict project deadlines & resource allocation?", "deadlines", 5),
        ("How often do you rely on AI-powered task management tools?", "task_management", 4),
        ("Do you use AI to analyze team productivity & workflows?", "productivity", 3),
        ("Have you used AI-generated reports for stakeholder communication?", "reports", 3)
    ],
    "Customer Support": [
        ("Do you use AI chatbots to handle customer inquiries?", "chatbots", 5),
        ("How frequently do you rely on AI for sentiment analysis in customer feedback?", "sentiment", 4),
        ("Do you use AI-generated responses for customer support tickets?", "canned_responses", 3),
        ("Have you used AI to automate repetitive customer service tasks?", "automation", 3)
    ],
    "Entrepreneur / Business Owner": [
        ("Do you use AI for automating business decisions & operations?", "automation", 5),
        ("How frequently do you rely on AI-driven market research & competitor analysis?", "market_research", 4),
        ("Do you use AI for optimizing pricing strategies?", "pricing", 3),
        ("Have you used AI-powered financial forecasting tools?", "finance", 3)
    ],
    "General User": []  # Only gets the general questions
}

# Motivational Quotes
MOTIVATIONAL_QUOTES = [
    "Keep your brain active! Every challenge is an opportunity to grow.",
    "Technology is a tool; your mind is your superpower!",
    "Innovation comes from within—balance is key.",
    "Stay curious, stay creative. Your journey never ends!",
    "Let your inner light shine brighter than any digital glow!"
]
