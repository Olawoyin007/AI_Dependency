import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def display_header():
    st.markdown(
        """
        <h1 style="text-align: center; font-size: 50px;">🤖 AI Dependency Risk Calculator</h1>
        <p style="text-align: center; font-size: 18px;">
            Welcome! This tool helps you assess your AI reliance and 
            maintain a healthy balance. Let's get started! 🚀
        </p>
        <hr style="border-top: 2px solid #bbb;">
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center;">
            <h3>📌 How It Works:</h3>
            <ul>
                <li>📝 Answer some quick questions about your AI usage.</li>
                <li>📊 Get an AI Dependency Score & risk level.</li>
                <li>🛠 Receive a personalized AI detox plan.</li>
                <li>💖 Support Hallel Hodia by donating if you find this helpful!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

    st.write("")

def display_donation_section():
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>💖 Support Our Cause</h2>
            <p style="font-size: 18px;">
                If you found this tool helpful, consider donating to **Hallel Hodia**. 
                Your contribution helps keep this project **free and accessible for all**. 💡
            </p>
            <a href="www.Youtube.com" target="_blank">
                <button style="background-color: #ff7f50; color: white; padding: 10px 20px;
                        font-size: 20px; border-radius: 8px; border: none;">
                    ❤️ Donate Now
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True
    )


def display_score_history(history):
    if history:
        st.markdown("### 📊 Your Score History")
        
        # Create a DataFrame with dates
        dates = [datetime.now() - timedelta(days=len(history)-i-1) for i in range(len(history))]
        df = pd.DataFrame({
            "Date": dates,
            "Score": history
        })
        
        # Display line chart with improved styling
        st.line_chart(
            df.set_index("Date"),
            use_container_width=True
        )
        
        # Show statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Latest Score", f"{history[-1]}%")
        with col2:
            st.metric("Average Score", f"{sum(history)/len(history):.1f}%")
        with col3:
            trend = history[-1] - history[0]
            st.metric("Score Trend", f"{trend:+.1f}%", 
                     delta_color="inverse" if trend > 0 else "normal")
