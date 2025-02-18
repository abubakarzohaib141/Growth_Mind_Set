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

# LinkedIn-style CSS
st.markdown("""
<style>
    /* General body styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f5;
        color: #333;
    }

    /* Card-like containers */
    .linkedin-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #fff;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
    }

    /* Header styling */
    .linkedin-header {
        color: #0a66c2;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #ddd;
    }

    /* Button styling */
    .stButton>button {
        background-color: #0a66c2;
        color: white;
        border-radius: 30px;
        padding: 12px 24px;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }

    /* Input and Textarea styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 12px;
        font-size: 16px;
        margin-bottom: 15px;
    }

    /* Selectbox styling */
    .stSelectbox>label {
        font-weight: bold;
        margin-bottom: 5px;
    }

    .stSelectbox>div>div>div {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 8px;
        font-size: 16px;
    }

    /* Progress indicators */
    .progress-indicator {
        padding: 12px;
        border-radius: 5px;
        background-color: #e1e9f0;
        margin: 8px 0;
        font-size: 16px;
        color: #555;
    }

    /* Achievement badges */
    .achievement-badge {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background-color: #fff;
        box-shadow: 0 3px 7px rgba(0, 0, 0, 0.1);
        margin: 10px;
    }

    .achievement-badge h3 {
        color: #0a66c2;
        margin-bottom: 5px;
    }

    .achievement-badge h2 {
        color: #28a745;
        margin-top: 0;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        padding: 10px 0;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        color: #0a66c2;
        background-color: #fff;
        border: 1px solid #ddd;
    }

    .stTabs [aria-selected="true"] {
        color: #fff;
        background-color: #0a66c2;
    }

    /* LinkedIn blue color */
    .linkedin-blue {
        color: #0a66c2;
    }

    /* Motivational messages */
    .motivational-message {
        font-style: italic;
        color: #555;
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
                    color: #0a66c2;
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
        
        # Welcome section with LinkedIn-style header
        st.markdown(f"""
        <div class='linkedin-card'>
            <h1 class='linkedin-header'>Welcome {username}! 🎉</h1>
            <p style='font-size: 18px;'>
                Track your progress, reflect on your journey, and grow every day!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs with LinkedIn-style
        tabs = st.tabs(["🎯 Goals", "📝 Reflection", "🛠️ Mistakes", "🚀 Challenges", "🏆 Achievements"])
        
        # Goals Tab
        with tabs[0]:
            st.markdown("<div class='linkedin-header'>Learning Goals</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("<div class='linkedin-card'>", unsafe_allow_html=True)
                new_goal = st.text_input("What do you want to achieve?", placeholder="Enter your learning goal...")
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
                st.markdown("<div class='linkedin-card'>", unsafe_allow_html=True)
                st.markdown("#### Your Current Goals")
                for i, goal in enumerate(goals):
                    if isinstance(goal, dict):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            status_color = "#28a745" if goal.get('status') == 'Completed' else "#ffc107"
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
            st.markdown("<div class='linkedin-header'>Daily Reflection</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("<div class='linkedin-card'>", unsafe_allow_html=True)
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
                        st.success(f"<div class='motivational-message'>{get_motivational_message()}</div>", unsafe_allow_html=True)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Display reflection history
            reflections = load_user_data(username, 'reflections')
            if reflections and len(reflections) > 0:
                st.markdown("<div class='linkedin-card'>", unsafe_allow_html=True)
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
            st.markdown("<div class='linkedin-header'>Mistake Tracker</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("<div class='linkedin-card'>", unsafe_allow_html=True)
                mistake = st.text_area("Describe the mistake or setback:")
                learning = st.text_area("What did you learn from it?")
                
                if st.button("Record Learning 📝"):
                    if mistake and learning:
                        save_user_data(username, 'mistakes', {
                            'mistake': mistake,
                            'learning': learning
                        })
                        st.success("<div class='motivational-message'>Remember: Mistakes are opportunities for growth! 🌱</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # Challenges Tab
        with tabs[3]:
            st.markdown("<div class='linkedin-header'>Daily Challenges</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown("<div class='linkedin-card'>", unsafe_allow_html=True)
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
                        st.success("<div class='motivational-message'>Challenge completed! 🎉</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # Achievements Tab
        with tabs[4]:
            st.markdown("<div class='linkedin-header'>Your Achievements</div>", unsafe_allow_html=True)
            
            user_data = load_user_data(username)
            completed_goals = len([g for g in user_data['goals'] if g.get('status') == 'Completed'])
            reflection_count = len(user_data['reflections'])
            challenge_count = len(user_data['challenges'])
            
            # Display badges with improved styling
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class='achievement-badge'>
                    <h3>🎯 Goal Progress</h3>
                    <h2 style='color: #28a745;'>{completed_goals}/5</h2>
                    <p>Goals Completed</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='achievement-badge'>
                    <h3>📝 Reflection Streak</h3>
                    <h2 style='color: #0a66c2;'>{reflection_count}/7</h2>
                    <p>Days Reflected</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='achievement-badge'>
                    <h3>🚀 Challenge Master</h3>
                    <h2 style='color: #ff6b6b;'>{challenge_count}/3</h2>
                    <p>Challenges Completed</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Progress Chart with improved styling
            st.markdown("<div class='linkedin-card'>", unsafe_allow_html=True)
            progress_data = {
                'Goals': completed_goals,
                'Reflections': reflection_count,
                'Challenges': challenge_count
            }
            
            fig = go.Figure(data=[
                go.Bar(x=list(progress_data.keys()), 
                      y=list(progress_data.values()),
                      marker_color=['#28a745', '#0a66c2', '#ff6b6b'])
            ])
            
            fig.update_layout(
                title="Your Growth Journey",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                title_font=dict(size=24, color='#0a66c2'),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("User not found. Please sign up again.")
        st.session_state['logged_in'] = False
        st.switch_page("main.py")   
