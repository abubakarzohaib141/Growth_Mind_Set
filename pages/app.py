import streamlit as st
import json
import os
import plotly.graph_objects as go
from datetime import datetime
import random

# Configure the app (must be the first Streamlit command)
st.set_page_config(
    page_title="Growth Mind Set - Dashboard",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for better styling
st.markdown("""
<style>
    /* General body styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f5;
        color: #333;
    }

    /* Card-like containers */
    .styledDiv {
        padding: 20px;
        border-radius: 10px;
        background-color: #fff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Custom header styling */
    .custom-header {
        color: #283593; /* A deeper, more professional blue */
        font-size: 28px; /* Slightly larger for emphasis */
        font-weight: 600; /* Semi-bold for a modern look */
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e0e0e0; /* Lighter border for subtlety */
    }

    /* Button styling */
    .stButton>button {
        background-color: #1976D2; /* A more vibrant blue */
        color: white;
        border-radius: 25px; /* More rounded corners */
        padding: 12px 24px;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* Slightly stronger shadow */
    }

    .stButton>button:hover {
        background-color: #1565C0; /* Darker shade on hover */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* Stronger shadow on hover */
    }

    /* Input and Textarea styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px; /* More rounded corners */
        border: 1.5px solid #bdbdbd; /* Slightly thicker border */
        padding: 12px;
        font-size: 16px;
        margin-bottom: 15px;
        transition: border-color 0.3s ease; /* Smooth transition for focus */
    }

    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #1976D2; /* Highlight color on focus */
        outline: none; /* Remove default focus outline */
    }

    /* Selectbox styling */
    .stSelectbox>label {
        font-weight: 500; /* Semi-bold for the label */
        margin-bottom: 5px;
        color: #424242; /* Darker text for the label */
    }

    .stSelectbox>div>div>div {
        border-radius: 8px; /* More rounded corners */
        border: 1.5px solid #bdbdbd; /* Slightly thicker border */
        padding: 8px;
        font-size: 16px;
    }

    /* Progress indicators */
    .progress-indicator {
        padding: 12px;
        border-radius: 8px; /* More rounded corners */
        background-color: #e0e0e0; /* A softer background color */
        margin: 8px 0;
        font-size: 16px;
        color: #546E7A; /* A more subtle text color */
    }

    /* Achievement badges */
    .achievement-badge {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background-color: #fff;
        box-shadow: 0 3px 7px rgba(0, 0, 0, 0.1);
        margin: 10px;
        transition: transform 0.3s ease; /* Add a subtle scaling effect */
    }

    .achievement-badge:hover {
        transform: scale(1.05); /* Slightly scale up on hover */
    }

    .achievement-badge h3 {
        color: #283593; /* A deeper, more professional blue */
        margin-bottom: 5px;
        font-weight: 600; /* Semi-bold for the heading */
    }

    .achievement-badge h2 {
        color: #2E7D32; /* A richer green */
        margin-top: 0;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        padding: 10px 0;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px; /* More rounded corners */
        font-size: 16px;
        color: #283593; /* A deeper, more professional blue */
        background-color: #fff;
        border: 1.5px solid #bdbdbd; /* Slightly thicker border */
        transition: background-color 0.3s ease, color 0.3s ease; /* Smooth transition */
    }

    .stTabs [aria-selected="true"] {
        color: #fff;
        background-color: #283593; /* A deeper, more professional blue */
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e8eaf6; /* Lighter background on hover */
        color: #1A237E; /* Darker text on hover */
    }

    /* LinkedIn blue color */
    .linkedin-blue {
        color: #283593;
    }

    /* Motivational messages */
    .motivational-message {
        font-style: italic;
        color: #546E7A; /* A more subtle text color */
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

def check_user_exists(username):
    return os.path.exists(f'users/{username}.json')

def save_user_data(username, data_type, content):
    file_path = f'users/{username}_data.json'
    try:
        with open(file_path, 'r') as f:
            user_data = json.load(f)
    except:
        user_data = {
            'goals': [],
            'reflections': [],
            'mistakes': [],
            'challenges': [],
            'achievements': []
        }
    
    # Add timestamp to content
    content['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_data[data_type].append(content)
    
    with open(file_path, 'w') as f:
        json.dump(user_data, f)

def load_user_data(username, data_type=None):
    file_path = f'users/{username}_data.json'
    try:
        with open(file_path, 'r') as f:
            user_data = json.load(f)
            if data_type:
                return user_data.get(data_type, [])
            return user_data
    except:
        # Return empty dictionary instead of empty list
        return {
            'goals': [],
            'reflections': [],
            'mistakes': [],
            'challenges': [],
            'achievements': []
        }

def get_motivational_message():
    messages = [
        "You're making great progress! 🚀",
        "Keep pushing forward! 💪",
        "Every mistake is a step toward success! 🎯",
        "Your effort is inspiring! ✨",
        "Growth mindset in action! 🌱"
    ]
    return random.choice(messages)

# Create navigation bar with logout button
def create_navbar():
    navbar = st.container()
    with navbar:
        cols = st.columns([8, 2])
        with cols[0]:
            st.markdown("""
                <h3 style='
                    font-size: 28px;
                    font-weight: bold;
                    color: #283593;
                    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
                    letter-spacing: 0.5px;
                '>
                    Growth Mind Set
                </h3>
            """, unsafe_allow_html=True)
        with cols[1]:
            if st.button("🚪 Logout", key="logout"):
                st.session_state['logged_in'] = False
                st.session_state['username'] = None
                st.switch_page("main.py")
    st.markdown("---")

# Main app logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.error("Please sign up first!")
    st.switch_page("main.py")
else:
    username = st.session_state.get('username')
    if username and check_user_exists(username):
        create_navbar()
        
        # Welcome section with gradient background
        st.markdown(f"""
        <div style='background: linear-gradient(120deg, #283593, #1976D2);
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 30px;'>
            <h1 style='color: white;'>Welcome {username}! 🎉</h1>
            <p style='color: white; font-size: 18px;'>
                Track your progress, reflect on your journey, and grow every day!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs with improved styling
        tabs = st.tabs(["🎯 Goals", "📝 Daily Reflection", "🔍 Mistake Tracker", "💪 Challenges", "🏆 Achievements"])
        
        # Goals Tab
        with tabs[0]:
            st.markdown("<div class='custom-header'>Learning Goals</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("<div class='styledDiv'>", unsafe_allow_html=True)
                new_goal = st.text_input("What would you like to achieve?", placeholder="Enter your learning goal here...")
                if st.button("Add Goal ✨"):
                    if new_goal:
                        save_user_data(username, 'goals', {
                            'goal': new_goal,
                            'status': 'In Progress'
                        })
                        st.success("Goal added successfully!")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Display existing goals
            goals = load_user_data(username, 'goals')
            if goals:
                st.markdown("<div class='styledDiv'>", unsafe_allow_html=True)
                st.markdown("#### Your Current Goals")
                for i, goal in enumerate(goals):
                    if isinstance(goal, dict):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            status_color = "#2E7D32" if goal.get('status') == 'Completed' else "#FFB300"
                            st.markdown(f"""
                            <div class='progress-indicator' style='border-left: 4px solid {status_color};'>
                                {goal.get('goal', 'Unnamed Goal')}
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if goal.get('status') != 'Completed':
                                if st.button("Complete ✅", key=f"goal_{i}"):
                                    goals[i]['status'] = 'Completed'
                                    user_data = load_user_data(username)
                                    user_data['goals'] = goals
                                    save_user_data(username, 'goals', user_data['goals'])
                                    st.success("Goal marked as completed!")
                                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        # Daily Reflection Tab
        with tabs[1]:
            st.markdown("<div class='custom-header'>Daily Reflection</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("<div class='styledDiv'>", unsafe_allow_html=True)
                reflection = st.text_area("What did you learn today?", 
                                        placeholder="Share your thoughts and experiences...",
                                        height=100)
                col1, col2 = st.columns(2)
                with col1:
                    challenges = st.text_area("What challenges did you face?",
                                            placeholder="Describe any obstacles...",
                                            height=100)
                with col2:
                    solutions = st.text_area("How did you overcome them?",
                                           placeholder="Share your solutions...",
                                           height=100)
                
                if st.button("Save Reflection 💭"):
                    if reflection:
                        save_user_data(username, 'reflections', {
                            'reflection': reflection,
                            'challenges': challenges,
                            'solutions': solutions
                        })
                        st.success(get_motivational_message())
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Display reflection history
            reflections = load_user_data(username, 'reflections')
            if reflections:
                st.markdown("<div class='styledDiv'>", unsafe_allow_html=True)
                st.markdown("#### Previous Reflections")
                recent_reflections = reflections[-min(5, len(reflections)):]
                for ref in reversed(recent_reflections):
                    with st.expander(f"📅 {ref['timestamp']}"):
                        st.markdown(f"**Reflection:**\n{ref['reflection']}")
                        if ref.get('challenges'):
                            st.markdown(f"**Challenges:**\n{ref['challenges']}")
                        if ref.get('solutions'):
                            st.markdown(f"**Solutions:**\n{ref['solutions']}")
                st.markdown("</div>", unsafe_allow_html=True)

        # Mistake Tracker Tab
        with tabs[2]:
            st.markdown("<div class='custom-header'>Mistake Tracker</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("<div class='styledDiv'>", unsafe_allow_html=True)
                mistake = st.text_area("Describe the mistake or setback:")
                learning = st.text_area("What did you learn from it?")
                
                if st.button("Record Learning 📝"):
                    if mistake and learning:
                        save_user_data(username, 'mistakes', {
                            'mistake': mistake,
                            'learning': learning
                        })
                        st.success("Remember: Mistakes are opportunities for growth! 🌱")
                st.markdown("</div>", unsafe_allow_html=True)

        # Challenges Tab
        with tabs[3]:
            st.markdown("<div class='custom-header'>Daily Challenges</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("<div class='styledDiv'>", unsafe_allow_html=True)
                challenges = [
                    "Learn a new programming concept today",
                    "Read an article about Growth Mindset",
                    "Help someone else learn something new",
                    "Practice problem-solving for 30 minutes",
                    "Write code documentation for better understanding"
                ]
                
                selected_challenge = st.selectbox("Select a challenge:", challenges)
                completion_notes = st.text_area("Notes on completion:")
                
                if st.button("Complete Challenge 🎉"):
                    if completion_notes:
                        save_user_data(username, 'challenges', {
                            'challenge': selected_challenge,
                            'notes': completion_notes
                        })
                        st.success("Challenge completed! 🎉")
                st.markdown("</div>", unsafe_allow_html=True)

        # Achievements Tab
        with tabs[4]:
            st.markdown("<div class='custom-header'>Your Achievements</div>", unsafe_allow_html=True)
            
            user_data = load_user_data(username)
            completed_goals = len([g for g in user_data['goals'] if g.get('status') == 'Completed'])
            reflection_count = len(user_data['reflections'])
            challenge_count = len(user_data['challenges'])
            
            # Display badges with improved styling
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div class='achievement-badge'>
                    <h3>🎯 Goal Progress</h3>
                    <h2 style='color: #4CAF50;'>{}/5</h2>
                    <p>Goals Completed</p>
                </div>
                """.format(completed_goals), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class='achievement-badge'>
                    <h3>📝 Reflection Streak</h3>
                    <h2 style='color: #1f4287;'>{}/7</h2>
                    <p>Days Reflected</p>
                </div>
                """.format(reflection_count), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class='achievement-badge'>
                    <h3>💪 Challenge Master</h3>
                    <h2 style='color: #ff6b6b;'>{}/3</h2>
                    <p>Challenges Completed</p>
                </div>
                """.format(challenge_count), unsafe_allow_html=True)
            
            # Progress Chart with improved styling
            st.markdown("<div class='styledDiv'>", unsafe_allow_html=True)
            progress_data = {
                'Goals': completed_goals,
                'Reflections': reflection_count,
                'Challenges': challenge_count
            }
            
            fig = go.Figure(data=[
                go.Bar(x=list(progress_data.keys()), 
                      y=list(progress_data.values()),
                      marker_color=['#4CAF50', '#1f4287', '#ff6b6b'])
            ])
            
            fig.update_layout(
                title="Your Growth Journey",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                title_font=dict(size=24, color='#1f4287'),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("User not found. Please sign up again.")
        st.session_state['logged_in'] = False
        st.switch_page("main.py")   
