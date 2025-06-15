import streamlit as st
from helpers import calculate_score, determine_risk_level, time_based_projections, generate_detox_plan, get_random_quote
from constants import FREQUENCY_MAP, GENERAL_QUESTIONS, PROFESSION_QUESTIONS, OPTIONS
from ui_elements import display_header, display_donation_section, display_score_history
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta
import json
import time
import random

## Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'

# Custom CSS for immersive experience
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    .stButton>button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 1.2em;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .page-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 20px 0;
        transition: all 0.4s ease;
    }
    .nav-button {
        background: linear-gradient(45deg, #6c5ce7, #a8a4e6);
        color: white;
        border-radius: 15px;
        padding: 10px 20px;
        margin: 5px;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        transform: scale(1.05);
    }
    .content-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .emoji-large {
        font-size: 3em;
        margin: 10px;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for persistent data
if 'user_journey' not in st.session_state:
    st.session_state.user_journey = {
        'reflections': [],
        'milestones': [],
        'goals': [],
        'last_assessment': None
    }

def save_user_journey():
    """Save user journey data to a JSON file"""
    with open('user_journey.json', 'w') as f:
        json.dump(st.session_state.user_journey, f)

def load_user_journey():
    """Load user journey data from JSON file"""
    try:
        with open('user_journey.json', 'r') as f:
            st.session_state.user_journey = json.load(f)
    except FileNotFoundError:
        pass

def add_reflection(reflection, score):
    """Add a user reflection to their journey"""
    st.session_state.user_journey['reflections'].append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'text': reflection,
        'score': score
    })
    save_user_journey()

def add_milestone(milestone):
    """Add a milestone to the user's journey"""
    st.session_state.user_journey['milestones'].append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'text': milestone
    })
    save_user_journey()

def add_goal(goal, target_date):
    """Add a goal to the user's journey"""
    st.session_state.user_journey['goals'].append({
        'text': goal,
        'target_date': target_date,
        'completed': False
    })
    save_user_journey()

def display_journey_timeline():
    """Display an interactive timeline of the user's journey"""
    if not st.session_state.user_journey['reflections']:
        return

    st.markdown("### 🌟 Your Digital Wellness Journey")
    
    # Create timeline data
    timeline_data = []
    for reflection in st.session_state.user_journey['reflections']:
        timeline_data.append({
            'date': reflection['date'],
            'type': 'reflection',
            'content': reflection['text'],
            'score': reflection['score']
        })
    
    for milestone in st.session_state.user_journey['milestones']:
        timeline_data.append({
            'date': milestone['date'],
            'type': 'milestone',
            'content': milestone['text']
        })
    
    # Sort by date
    timeline_data.sort(key=lambda x: x['date'])
    
    # Display timeline
    for item in timeline_data:
        with st.expander(f"📅 {item['date']} - {item['type'].title()}"):
            if item['type'] == 'reflection':
                st.write(f"**Score:** {item['score']}%")
            st.write(item['content'])

def display_goals_progress():
    """Display and manage user goals"""
    st.markdown("### 🎯 Your Digital Wellness Goals")
    
    # Add new goal
    with st.form("new_goal_form"):
        goal = st.text_area("What's your next digital wellness goal?")
        target_date = st.date_input("When do you want to achieve this by?")
        submitted = st.form_submit_button("Add Goal")
        
        if submitted and goal:
            add_goal(goal, target_date.strftime('%Y-%m-%d'))
            st.success("Goal added to your journey!")
    
    # Display existing goals
    if st.session_state.user_journey['goals']:
        for i, goal in enumerate(st.session_state.user_journey['goals']):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.checkbox(
                    goal['text'],
                    value=goal['completed'],
                    key=f"goal_{i}",
                    on_change=lambda: update_goal_status(i)
                )
            with col2:
                st.write(f"Target: {goal['target_date']}")

def update_goal_status(goal_index):
    """Update the completion status of a goal"""
    st.session_state.user_journey['goals'][goal_index]['completed'] = st.session_state[f"goal_{goal_index}"]
    save_user_journey()

def display_reflection_section(score):
    """Display the reflection section after assessment"""
    st.markdown("### 💭 Reflection Time")
    st.write("Take a moment to reflect on your relationship with AI:")
    
    reflection = st.text_area(
        "How do you feel about your AI dependency score? What insights have you gained?",
        height=150
    )
    
    if st.button("Save Reflection"):
        if reflection:
            add_reflection(reflection, score)
            st.success("Thank you for sharing your thoughts! 🌟")
            
            # Check for milestone
            if len(st.session_state.user_journey['reflections']) % 5 == 0:
                st.balloons()
                st.success("🎉 Milestone reached: 5 reflections recorded!")
                add_milestone(f"Completed {len(st.session_state.user_journey['reflections'])} reflections")

def display_insights_dashboard(score, patterns, predictions):
    """Display an insights dashboard with interactive elements"""
    st.markdown("### 🧠 Deep Insights")
    
    # Create tabs for different insights
    tab1, tab2, tab3 = st.tabs(["Pattern Analysis", "Future Projections", "Action Items"])
    
    with tab1:
        st.markdown("#### Your AI Usage Patterns")
        # Create a radar chart for pattern analysis
        categories = ['Critical Areas', 'General Usage', 'Professional Impact', 'Personal Growth']
        values = [
            patterns['critical_score'],
            score / 25,  # Normalize to 0-4 scale
            patterns.get('professional_impact', 2),
            patterns.get('personal_growth', 2)
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current State'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 4]
                )
            ),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### Future Outlook")
        if predictions is not None:
            # Create an interactive prediction chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=predictions,
                mode='lines+markers',
                name='Predicted Trend',
                line=dict(color='red', dash='dash')
            ))
            fig.update_layout(
                title="30-Day Dependency Prediction",
                xaxis_title="Days",
                yaxis_title="Predicted Score",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("#### Personalized Action Plan")
        # Generate action items based on patterns
        action_items = generate_action_items(score, patterns)
        for item in action_items:
            st.write(f"• {item}")

def generate_action_items(score, patterns):
    """Generate personalized action items based on user's patterns"""
    items = []
    
    if patterns['critical_score'] > 2.5:
        items.append("Focus on reducing AI dependency in critical areas")
    if score > 70:
        items.append("Implement a daily digital detox routine")
    if patterns['overall_trend'] == 'increasing':
        items.append("Set specific boundaries for AI tool usage")
    
    return items

def display_gauge_chart(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "AI Dependency Score", "font": {"size": 24}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 30], "color": "lightgreen"},
                {"range": [30, 60], "color": "lightyellow"},
                {"range": [60, 80], "color": "orange"},
                {"range": [80, 100], "color": "red"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": score
            }
        }
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

def predict_future_trends(history, profession):
    if len(history) < 3:
        return None
    
    # Prepare data for prediction
    X = np.array(range(len(history))).reshape(-1, 1)
    y = np.array(history)
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 30 days
    future_days = np.array(range(len(history), len(history) + 30)).reshape(-1, 1)
    predictions = model.predict(future_days)
    
    # Add profession-specific adjustments
    profession_factors = {
        "Developer": 1.2,
        "Writer": 1.1,
        "Student": 1.3,
        "Designer": 1.15,
        "Doctor / Medical Professional": 0.9,
        "Lawyer / Legal Professional": 0.95,
        "Marketer": 1.25,
        "Project Manager": 1.1,
        "Customer Support": 1.2,
        "Entrepreneur / Business Owner": 1.15,
        "General User": 1.0
    }
    
    factor = profession_factors.get(profession, 1.0)
    predictions = np.clip(predictions * factor, 0, 100)
    
    return predictions

def analyze_usage_patterns(responses, profession):
    # Convert responses to numerical values
    numerical_responses = {k: FREQUENCY_MAP[v] for k, v in responses.items()}
    
    # Define critical areas based on profession
    critical_areas = {
        "Developer": ["coding", "debugging"],
        "Writer": ["writing", "grammar"],
        "Student": ["study", "essays"],
        "Designer": ["designing", "editing"],
        "Doctor / Medical Professional": ["diagnosis", "med_research"],
        "Lawyer / Legal Professional": ["legal_research", "legal_docs"],
        "Marketer": ["ads", "market_trends"],
        "Project Manager": ["deadlines", "task_management"],
        "Customer Support": ["chatbots", "sentiment"],
        "Entrepreneur / Business Owner": ["automation", "market_research"],
        "General User": ["decision", "content"]
    }
    
    # Analyze patterns
    critical_scores = [numerical_responses.get(area, 0) for area in critical_areas.get(profession, [])]
    avg_critical = sum(critical_scores) / len(critical_scores) if critical_scores else 0
    
    return {
        "critical_areas": critical_areas.get(profession, []),
        "critical_score": avg_critical,
        "overall_trend": "increasing" if avg_critical > 2.5 else "stable" if avg_critical > 1.5 else "decreasing"
    }

def display_meditation_session():
    """Display a guided meditation session"""
    st.markdown("""
        <div class="meditation-card">
            <h2>🧘‍♂️ Digital Detox Meditation</h2>
            <p>Take a moment to center yourself and reflect on your digital habits.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Meditation Session"):
        with st.spinner("Preparing your meditation space..."):
            time.sleep(1)
            
        st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <h3>Breathe in... Breathe out...</h3>
                <p>Focus on your breath for the next 30 seconds.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Animated breathing circle
        for i in range(3):
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        width: {100 + i*20}px;
                        height: {100 + i*20}px;
                        background: rgba(76, 175, 80, 0.2);
                        border-radius: 50%;
                        margin: 20px auto;
                        animation: breathe 4s infinite;
                    "></div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(4)

def display_digital_garden():
    """Display a virtual digital garden representing user's progress"""
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2>🌱 Your Digital Garden</h2>
            <p>Watch your digital wellness grow!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create a garden visualization
    garden_elements = []
    if st.session_state.user_journey['reflections']:
        garden_elements.append("🌸 Reflection Flowers")
    if st.session_state.user_journey['milestones']:
        garden_elements.append("🌳 Milestone Trees")
    if st.session_state.user_journey['goals']:
        garden_elements.append("🌺 Goal Gardens")
    
    # Display garden elements
    cols = st.columns(len(garden_elements))
    for i, element in enumerate(garden_elements):
        with cols[i]:
            st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.9); border-radius: 15px;">
                    <h3>{element}</h3>
                    <p style="font-size: 2em;">{element.split()[0]}</p>
                </div>
            """, unsafe_allow_html=True)

def display_achievements():
    """Display user achievements and badges"""
    achievements = [
        {"name": "First Reflection", "icon": "🌟", "condition": lambda: len(st.session_state.user_journey['reflections']) > 0},
        {"name": "Goal Setter", "icon": "🎯", "condition": lambda: len(st.session_state.user_journey['goals']) > 0},
        {"name": "Milestone Master", "icon": "🏆", "condition": lambda: len(st.session_state.user_journey['milestones']) > 0},
        {"name": "Digital Balance", "icon": "⚖️", "condition": lambda: any(r['score'] < 50 for r in st.session_state.user_journey['reflections'])},
    ]
    
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2>🏆 Your Achievements</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Display achievements
    cols = st.columns(4)
    for i, achievement in enumerate(achievements):
        with cols[i]:
            if achievement['condition']():
                st.markdown(f"""
                    <div class="achievement-badge">
                        <h3>{achievement['icon']} {achievement['name']}</h3>
                    </div>
                """, unsafe_allow_html=True)

def display_question_with_emotion(question, key, options):
    """Display a question with emotional context and interactive elements"""
    with st.container():
        st.markdown(f"""
            <div class="question-card">
                <h3 style="color: #2c3e50;">{question}</h3>
                <p style="color: #7f8c8d;">How does this make you feel?</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Enhanced emotion selector
        emotions = ["😊", "😐", "😔", "😤", "🤔"]
        selected_emotion = st.radio("", emotions, horizontal=True, key=f"emotion_{key}")
        
        # Response with emotion context
        response = st.radio("", options, horizontal=True, key=key)
        
        # Add a small delay for smooth transitions
        time.sleep(0.1)
        
        return response, selected_emotion

def display_profession_selector():
    """Display an interactive profession selector"""
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2 style="color: #2c3e50;">What's Your Digital Identity?</h2>
            <p style="color: #7f8c8d;">Select the role that best describes your relationship with technology</p>
        </div>
    """, unsafe_allow_html=True)
    
    professions = {
        "Developer": "💻 Code Craftsman",
        "Writer": "✍️ Word Weaver",
        "Student": "📚 Knowledge Seeker",
        "Designer": "🎨 Visual Artist",
        "Doctor / Medical Professional": "⚕️ Health Guardian",
        "Lawyer / Legal Professional": "⚖️ Justice Keeper",
        "Marketer": "📢 Story Teller",
        "Project Manager": "📋 Harmony Creator",
        "Customer Support": "🤝 Connection Builder",
        "Entrepreneur / Business Owner": "🚀 Vision Pioneer",
        "General User": "🌐 Digital Explorer"
    }
    
    selected = st.selectbox("", list(professions.keys()), format_func=lambda x: f"{professions[x]}")
    return selected

def display_welcome_animation():
    """Display a welcoming animation"""
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h1 style="color: #2c3e50; font-size: 2.5em;">Welcome to Your Digital Wellness Sanctuary</h1>
            <p style="color: #7f8c8d; font-size: 1.2em;">Let's begin your journey to digital balance and mindfulness</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Animated progress bar
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.01)

def display_results_with_animation(score, patterns, predictions):
    """Display results with engaging animations"""
    # Animated score reveal
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2 style="color: #2c3e50;">Your Digital Wellness Score</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Animated gauge chart
    display_gauge_chart(score)
    
    # Animated insights reveal
    with st.spinner("Analyzing your digital patterns..."):
        time.sleep(1)
        display_insights_dashboard(score, patterns, predictions)
    
    # Celebration animation for good scores
    if score < 50:
        st.balloons()
        st.success("🎉 You're maintaining a healthy balance with AI!")

def personal_mode(user_name):
    st.subheader(f"Welcome, {user_name}! 🌟 Let's begin your digital wellness journey")
    
    # Display welcome animation
    display_welcome_animation()
    
    # Display meditation session
    display_meditation_session()
    
    # Load user journey data
    load_user_journey()
    
    # Display digital garden
    display_digital_garden()
    
    # Display achievements
    display_achievements()
    
    # Display journey timeline if available
    if st.session_state.user_journey['reflections']:
        display_journey_timeline()
    
    # Display goals section
    display_goals_progress()
    
    # Interactive profession selector
    profession = display_profession_selector()
    
    questions = GENERAL_QUESTIONS + PROFESSION_QUESTIONS.get(profession, [])
    responses = {}
    emotions = {}

    st.markdown("<hr style='border-top: 1px solid #ddd;'>", unsafe_allow_html=True)

    # Display questions with emotional context
    for question, key, _ in questions:
        response, emotion = display_question_with_emotion(question, key, OPTIONS)
        responses[key] = response
        emotions[key] = emotion

    if st.button("🌟 Begin Your Digital Wellness Journey", use_container_width=True):
        with st.spinner("Analyzing your digital patterns..."):
            score, breakdown = calculate_score(responses, questions)
            predictions = predict_future_trends(st.session_state.get("personal_history", []), profession)
            patterns = analyze_usage_patterns(responses, profession)
            
            # Display results with animations
            display_results_with_animation(score, patterns, predictions)
            
            # Display reflection section
            display_reflection_section(score)
            
            # Update session state
            if "personal_history" not in st.session_state:
                st.session_state.personal_history = []
            st.session_state.personal_history.append(score)
            st.session_state.user_journey['last_assessment'] = datetime.now().strftime('%Y-%m-%d')
            save_user_journey()
            
            display_score_history(st.session_state.personal_history)

def display_navigation():
    """Display navigation buttons"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = 'welcome'
    with col2:
        if st.button("🧘‍♂️ Meditation", use_container_width=True):
            st.session_state.current_page = 'meditation'
    with col3:
        if st.button("🌱 Garden", use_container_width=True):
            st.session_state.current_page = 'garden'
    with col4:
        if st.button("📊 Assessment", use_container_width=True):
            st.session_state.current_page = 'assessment'

def display_welcome_page():
    """Display the welcome page with rich content"""
    st.markdown("""
        <div class="page-container fade-in">
            <h1 style="text-align: center; color: #2c3e50;">Welcome to Your Digital Wellness Sanctuary</h1>
            <div style="text-align: center; margin: 20px 0;">
                <span class="emoji-large">🌿</span>
                <span class="emoji-large">🧘‍♀️</span>
                <span class="emoji-large">✨</span>
            </div>
            <div class="content-card">
                <h2>🌟 Begin Your Journey</h2>
                <p>Welcome to a space dedicated to your digital wellbeing. Here, we'll explore:</p>
                <ul>
                    <li>🧘‍♂️ Mindful technology usage</li>
                    <li>🌱 Growing your digital wellness</li>
                    <li>🎯 Setting meaningful goals</li>
                    <li>✨ Celebrating your progress</li>
                </ul>
            </div>
            <div class="content-card">
                <h2>🌈 What to Expect</h2>
                <p>Your journey includes:</p>
                <ul>
                    <li>🎯 Personalized assessments</li>
                    <li>🧘‍♀️ Guided meditation sessions</li>
                    <li>🌱 A growing digital garden</li>
                    <li>🏆 Achievement tracking</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_meditation_page():
    """Display the meditation page with rich content"""
    st.markdown("""
        <div class="page-container fade-in">
            <h1 style="text-align: center; color: #2c3e50;">Digital Detox Meditation</h1>
            <div style="text-align: center; margin: 20px 0;">
                <span class="emoji-large">🧘‍♂️</span>
                <span class="emoji-large">🌿</span>
                <span class="emoji-large">✨</span>
            </div>
            <div class="content-card">
                <h2>🌟 Guided Meditation</h2>
                <p>Take a moment to center yourself and reflect on your digital habits.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Begin Meditation Session", use_container_width=True):
        with st.spinner("Creating your peaceful space..."):
            time.sleep(1)
        
        st.markdown("""
            <div class="content-card">
                <h3 style="text-align: center;">Breathe in... Breathe out...</h3>
                <p style="text-align: center;">Focus on your breath for the next 30 seconds.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Animated breathing circle
        for i in range(3):
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        width: {100 + i*20}px;
                        height: {100 + i*20}px;
                        background: rgba(76, 175, 80, 0.2);
                        border-radius: 50%;
                        margin: 20px auto;
                        animation: breathe 4s infinite;
                    "></div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(4)

def display_garden_page():
    """Display the digital garden page with rich content"""
    st.markdown("""
        <div class="page-container fade-in">
            <h1 style="text-align: center; color: #2c3e50;">Your Digital Garden</h1>
            <div style="text-align: center; margin: 20px 0;">
                <span class="emoji-large">🌱</span>
                <span class="emoji-large">🌸</span>
                <span class="emoji-large">🌳</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create a garden visualization
    garden_elements = []
    if st.session_state.user_journey['reflections']:
        garden_elements.append("🌸 Reflection Flowers")
    if st.session_state.user_journey['milestones']:
        garden_elements.append("🌳 Milestone Trees")
    if st.session_state.user_journey['goals']:
        garden_elements.append("🌺 Goal Gardens")
    
    # Display garden elements
    cols = st.columns(len(garden_elements))
    for i, element in enumerate(garden_elements):
        with cols[i]:
            st.markdown(f"""
                <div class="content-card">
                    <h3 style="text-align: center;">{element}</h3>
                    <p style="text-align: center; font-size: 2em;">{element.split()[0]}</p>
                </div>
            """, unsafe_allow_html=True)

def display_assessment_page():
    """Display the assessment page with rich content"""
    st.markdown("""
        <div class="page-container fade-in">
            <h1 style="text-align: center; color: #2c3e50;">Digital Wellness Assessment</h1>
            <div style="text-align: center; margin: 20px 0;">
                <span class="emoji-large">📊</span>
                <span class="emoji-large">🎯</span>
                <span class="emoji-large">✨</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display profession selector
    profession = display_profession_selector()
    
    questions = GENERAL_QUESTIONS + PROFESSION_QUESTIONS.get(profession, [])
    responses = {}
    emotions = {}

    for question, key, _ in questions:
        response, emotion = display_question_with_emotion(question, key, OPTIONS)
        responses[key] = response
        emotions[key] = emotion

    if st.button("Begin Assessment", use_container_width=True):
        with st.spinner("Analyzing your digital patterns..."):
            score, breakdown = calculate_score(responses, questions)
            predictions = predict_future_trends(st.session_state.get("personal_history", []), profession)
            patterns = analyze_usage_patterns(responses, profession)
            
            display_results_with_animation(score, patterns, predictions)
            display_reflection_section(score)
            
            if "personal_history" not in st.session_state:
                st.session_state.personal_history = []
            st.session_state.personal_history.append(score)
            st.session_state.user_journey['last_assessment'] = datetime.now().strftime('%Y-%m-%d')
            save_user_journey()
            
            display_score_history(st.session_state.personal_history)

def main():
    """Main application function with page navigation"""
    display_header()
    
    # Display navigation
    display_navigation()
    
    # Display current page
    if st.session_state.current_page == 'welcome':
        display_welcome_page()
    elif st.session_state.current_page == 'meditation':
        display_meditation_page()
    elif st.session_state.current_page == 'garden':
        display_garden_page()
    elif st.session_state.current_page == 'assessment':
        display_assessment_page()

if __name__ == "__main__":
    main()
