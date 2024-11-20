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
A multi-agent AI system for content creation and brand management using LangGraph,
Streamlit, and Groq API.

Author: @hams_ollo
Version: 0.0.1
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import END, StateGraph
from typing import Dict, List, Tuple, Any, Optional
import os
from dotenv import load_dotenv
from database_manager import DatabaseManager
import logging
import json
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database
db = DatabaseManager(persist_directory="./chroma_db")

# Initialize LLM
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="mixtral-8x7b-32768"
)

class AgentState:
    def __init__(self):
        self.messages: List[Dict] = []
        self.current_plan: Optional[Dict] = None
        self.current_post: Optional[Dict] = None
        self.error: Optional[str] = None

def understand_request(state: AgentState) -> Tuple[AgentState, str]:
    """Process the user's request and determine the next action."""
    try:
        messages = [
            SystemMessage(content="You are a helpful AI assistant for content creation and social media management."),
            *[HumanMessage(content=msg["content"]) for msg in state.messages]
        ]
        response = llm.invoke(messages)
        
        # Update state with the response
        state.messages.append({"role": "assistant", "content": response.content})
        
        # Determine next action
        if "create plan" in response.content.lower():
            return state, "plan_execution"
        elif "create post" in response.content.lower():
            return state, "execute_task"
        else:
            return state, "generate_response"
    except Exception as e:
        state.error = str(e)
        logger.error(f"Error in understand_request: {e}")
        return state, END

def plan_execution(state: AgentState) -> Tuple[AgentState, str]:
    """Create and store a content plan."""
    try:
        # Generate content plan
        plan_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="Create a detailed content plan based on the user's request."),
            MessagesPlaceholder(variable_name="history"),
            HumanMessage(content="Generate a content plan with specific goals and timeline.")
        ])
        
        chain = plan_prompt | llm
        
        # Create plan
        plan_response = chain.invoke({"history": state.messages})
        plan_data = {
            "id": str(uuid.uuid4()),
            "content": plan_response.content,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Store in database
        db.add_content_plan(plan_data["id"], plan_data)
        
        # Update state
        state.current_plan = plan_data
        state.messages.append({"role": "assistant", "content": f"Content plan created: {plan_data['id']}"})
        
        return state, "generate_response"
    except Exception as e:
        state.error = str(e)
        logger.error(f"Error in plan_execution: {e}")
        return state, END

def execute_task(state: AgentState) -> Tuple[AgentState, str]:
    """Execute specific tasks like creating social media posts."""
    try:
        # Generate social media post
        post_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="Create an engaging social media post based on the content plan and user request."),
            MessagesPlaceholder(variable_name="history"),
            HumanMessage(content="Generate a social media post.")
        ])
        
        chain = post_prompt | llm
        
        # Create post
        post_response = chain.invoke({"history": state.messages})
        post_data = {
            "id": str(uuid.uuid4()),
            "content": post_response.content,
            "created_at": datetime.now().isoformat(),
            "plan_id": state.current_plan["id"] if state.current_plan else None,
            "status": "draft"
        }
        
        # Store in database
        db.add_social_post(post_data["id"], post_data)
        
        # Update state
        state.current_post = post_data
        state.messages.append({"role": "assistant", "content": f"Social post created: {post_data['id']}"})
        
        return state, "generate_response"
    except Exception as e:
        state.error = str(e)
        logger.error(f"Error in execute_task: {e}")
        return state, END

def generate_response(state: AgentState) -> Tuple[AgentState, str]:
    """Generate a final response to the user."""
    try:
        response_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="Generate a helpful response summarizing the actions taken."),
            MessagesPlaceholder(variable_name="history"),
            HumanMessage(content="Summarize what has been done and provide next steps.")
        ])
        
        chain = response_prompt | llm
        
        # Generate response
        final_response = chain.invoke({"history": state.messages})
        state.messages.append({"role": "assistant", "content": final_response.content})
        
        return state, END
    except Exception as e:
        state.error = str(e)
        logger.error(f"Error in generate_response: {e}")
        return state, END

# Create workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("understand_request", understand_request)
workflow.add_node("plan_execution", plan_execution)
workflow.add_node("execute_task", execute_task)
workflow.add_node("generate_response", generate_response)

# Add edges
workflow.add_edge("understand_request", "plan_execution")
workflow.add_edge("understand_request", "execute_task")
workflow.add_edge("understand_request", "generate_response")
workflow.add_edge("plan_execution", "generate_response")
workflow.add_edge("execute_task", "generate_response")

# Set entry point
workflow.set_entry_point("understand_request")

# Compile workflow
app = workflow.compile()

# Streamlit UI
st.set_page_config(page_title="Program & Chill", page_icon="🎯", layout="wide")

# Apply dark theme
st.markdown("""
    <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stTextInput > div > div > input {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
        .stButton > button {
            background-color: #0078D4;
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Program & Chill")
    st.markdown("---")
    
    # View selection
    view = st.radio("Select View", ["Chat", "Content Calendar", "Analytics"])
    
    # Settings and tools
    st.markdown("### Settings")
    temperature = st.slider("AI Temperature", 0.0, 1.0, 0.7)
    
    # Update LLM temperature
    llm.temperature = temperature

# Main content area
if view == "Chat":
    st.header("AI Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process with workflow
        state = AgentState()
        state.messages = st.session_state.messages.copy()
        result = app.invoke(state)
        
        # Update chat history with assistant's response
        if result.messages:
            for message in result.messages[len(st.session_state.messages):]:
                st.session_state.messages.append(message)
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

elif view == "Content Calendar":
    st.header("Content Calendar")
    
    # Query recent content plans
    recent_plans = db.query_content_plans("", n_results=10)
    
    # Display content plans
    for plan in recent_plans:
        with st.expander(f"Plan: {plan['created_at']}"):
            st.write(plan['content'])
            st.button("Edit", key=f"edit_{plan['id']}")
            st.button("Delete", key=f"delete_{plan['id']}")

elif view == "Analytics":
    st.header("Analytics Dashboard")
    
    # Placeholder for analytics
    st.markdown("Analytics dashboard coming soon!")