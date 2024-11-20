#-------------------------------------------------------------------------------------#
# Project Setup & Development Guidelines: Program_and_Chill
#-------------------------------------------------------------------------------------#
# 
# INITIAL SETUP:
# 1. Create virtual environment:    python -m venv venv
# 2. Activate virtual environment:
#    - Windows:                    .\venv\Scripts\activate
#    - Unix/MacOS:                 source venv/bin/activate
# 3. Install requirements:         pip install -r requirements.txt
# 4. Create .env file:            cp .env.example .env
# 5. Update dependencies:          pip freeze > requirements.txt
#
# PYTHON DEVELOPMENT COMMANDS:
# Package Management:
# 1. List outdated packages:      pip list --outdated
# 2. Show package info:           pip show package_name
# 3. Uninstall package:          pip uninstall package_name
# 4. Install dev dependencies:    pip install -r requirements-dev.txt
# 5. Upgrade pip:                python -m pip install --upgrade pip
# 6. Install package:            pip install package_name==version
#
# Virtual Environment:
# 1. List installed packages:     pip list
# 2. Export dependencies:         pip freeze > requirements.txt
# 3. Deactivate venv:            deactivate
# 4. Remove venv:                rm -rf venv
#
# STREAMLIT COMMANDS:
# Development:
# 1. Run app:                     streamlit run app.py
# 2. Run with custom port:        streamlit run app.py --server.port 8502
# 3. Enable debug mode:           streamlit run app.py --logger.level=debug
# 4. Clear cache:                 streamlit cache clear
# 5. Show all config options:     streamlit config show
# 6. Create new component:        streamlit create my_component
#
# GIT COMMANDS:
# Basic Operations:
# 1. Initialize repository:        git init
# 2. Add files to staging:        git add .
# 3. Commit changes:              git commit -m "your message"
# 4. Push to remote:              git push -u origin branch-name
# 5. Pull latest changes:         git pull origin branch-name
# 
# Branching:
# 1. Create & switch branch:      git checkout -b branch-name
# 2. Switch branches:             git checkout branch-name
# 3. List branches:               git branch
# 4. Delete branch:               git branch -d branch-name
# 5. Merge branch:                git merge branch-name
#
# Advanced Operations:
# 1. Fetch updates:               git fetch origin
# 2. Rebase branch:               git rebase main
# 3. Cherry-pick commit:          git cherry-pick commit-hash
# 4. Reset to commit:             git reset --hard commit-hash
# 5. Clean untracked files:       git clean -fd
#
#-------------------------------------------------------------------------------------#

"""
Program & Chill AI Assistant
---------------------------
A conversational AI assistant using Groq API.

Author: @hams_ollo
Version: 0.0.1
"""

from typing import Dict, List, Optional, Any, Tuple
import streamlit as st
import os
from dotenv import load_dotenv
import logging
import json
from datetime import datetime
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize LLM with better settings
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="mixtral-8x7b-32768",
    temperature=0.7,
    max_tokens=2000
)

# System prompt for better conversation
SYSTEM_PROMPT = """You are a helpful and friendly AI assistant named Program & Chill. Your responses should be:
1. Informative yet conversational
2. Detailed when technical accuracy is needed
3. Concise for simple queries
4. Always helpful and supportive
5. Engaging but professional

Remember to maintain context throughout the conversation and ask for clarification when needed."""

class AgentState:
    """State management for the AI assistant."""
    def __init__(self):
        self.messages: List[Dict[str, str]] = []
        self.context: Dict[str, Any] = {}
        self.conversation_id: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.error: Optional[str] = None
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.messages
    
    def get_last_message(self) -> Optional[Dict[str, str]]:
        """Get the last message in the conversation."""
        return self.messages[-1] if self.messages else None
    
    def set_error(self, error: str) -> None:
        """Set an error state."""
        self.error = error
        logger.error(f"Error in conversation {self.conversation_id}: {error}")
    
    def clear_error(self) -> None:
        """Clear the error state."""
        self.error = None

def chat_node(state: AgentState) -> Tuple[AgentState, str]:
    """Process the user's message and generate a response."""
    try:
        # Build message history for Groq
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend([{
            "role": msg["role"],
            "content": msg["content"]
        } for msg in state.messages])
        
        # Generate response
        response = llm.invoke(messages)
        
        # Add response to state
        state.add_message("assistant", response.content)
        
        # Log successful interaction
        logger.info(f"Successfully processed message in conversation {state.conversation_id}")
        
        return state, "END"
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in chat_node: {error_msg}")
        state.set_error(error_msg)
        state.add_message(
            "assistant",
            "I apologize, but I encountered an error. Could you please try again or rephrase your question?"
        )
        return state, "END"

# Streamlit UI
st.set_page_config(
    page_title="Program & Chill AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Program & Chill AI Assistant v0.0.1"
    }
)

# Add custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --background-color: #0E1117;
        --text-color: #E0E0E0;
        --secondary-background: #262730;
        --border-color: #303236;
        --accent-color: #4CAF50;
    }

    /* Main container */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Chat container */
    .stChat {
        padding: 20px;
        background-color: var(--background-color);
    }

    /* Message bubbles */
    .stChatMessage {
        background-color: var(--secondary-background) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px;
        padding: 15px !important;
        margin: 8px 0;
    }

    /* User message specific */
    .stChatMessage[data-testid="user-message"] {
        background-color: #1E3A8A !important;
    }

    /* Assistant message specific */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #1F2937 !important;
    }

    /* Input box */
    .stChatInputContainer {
        background-color: var(--secondary-background) !important;
        border-color: var(--border-color) !important;
        padding: 10px;
        border-radius: 10px;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: var(--secondary-background);
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--accent-color);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-1px);
    }

    /* Sliders */
    .stSlider {
        padding: 10px 0;
    }

    /* Text elements */
    .stMarkdown {
        color: var(--text-color);
        font-size: 16px;
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--text-color) !important;
    }

    /* Divider */
    hr {
        border-color: var(--border-color);
    }
</style>
""", unsafe_allow_html=True)

# Main title with emoji
st.title("💬 Program & Chill AI Assistant")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # App description
    st.markdown("""
    ### About
    Program & Chill is an advanced AI assistant powered by Groq's API. 
    It offers intelligent conversation with fast, accurate responses.
    
    ---
    """)
    
    # Core Settings
    st.subheader("🎯 Core Settings")
    
    # Model settings
    st.markdown("##### Model Parameters")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="Higher values make responses more creative, lower values make them more focused"
    )
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=4000,
        value=2000,
        help="Maximum length of the response"
    )
    
    # Chat settings
    st.markdown("##### Chat Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm Program & Chill, your AI assistant. How can I help you today?"
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process message
    with st.spinner("Thinking..."):
        try:
            state = AgentState()
            state.messages = [{"role": "user", "content": prompt}]
            result, _ = chat_node(state)
            
            # Get the last message (assistant's response)
            last_message = result.get_last_message()
            if last_message and last_message["role"] == "assistant":
                st.session_state.messages.append(last_message)
                with st.chat_message("assistant"):
                    st.markdown(last_message["content"])
        
        except Exception as e:
            logger.error(f"Error in main chat loop: {str(e)}")
            with st.chat_message("assistant"):
                st.error("I apologize, but something went wrong. Please try again.")