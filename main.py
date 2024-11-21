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

import streamlit as st
import os
import logging
from dotenv import load_dotenv
from app.agents.chat_agent import ChatAgent
from app.agents.document_processor import DocumentProcessor
from datetime import datetime
import pandas as pd
import markdown
from typing import Dict, List, Any, Optional
from langchain.schema import Document

# Must be the first Streamlit command
st.set_page_config(
    page_title="Program & Chill AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_chat_agent():
    """Initialize the chat agent with API key."""
    print("🔑 Initializing chat agent with API key...")
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            st.error("Please set the GROQ_API_KEY in your .env file")
            return None
        return ChatAgent(api_key=groq_api_key)
    except Exception as e:
        st.error(f"Error initializing chat agent: {str(e)}")
        return None

# Initialize session state
if "chat_agent" not in st.session_state:
    print("🤖 Creating new chat agent instance...")
    st.session_state.chat_agent = initialize_chat_agent()
if "messages" not in st.session_state:
    print("💬 Initializing message history...")
    st.session_state.messages = []
if "doc_processor" not in st.session_state:
    st.session_state.doc_processor = DocumentProcessor()

# Streamlit UI

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Chat", "Document Upload"])

if page == "Chat":
    st.title("💬 Program & Chill AI Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "sources" in message:
                with st.expander("View Sources"):
                    for source in message["sources"]:
                        st.write(f"- {source}")
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        print(f"📝 Processing user input at {datetime.now().strftime('%H:%M:%S')}...")
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_agent.process_message(prompt)
                st.write(response["response"])
                
                # Display sources if available
                if response["source_documents"]:
                    with st.expander("View Sources"):
                        for doc in response["source_documents"]:
                            st.write(f"- {doc.metadata.get('source', 'Unknown source')}")
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["response"],
                    "sources": [doc.metadata.get('source', 'Unknown source') for doc in response["source_documents"]]
                })

elif page == "Document Upload":
    st.title("📄 Document Upload")
    st.write("Upload documents to enhance your AI assistant's knowledge.")
    
    uploaded_files = st.file_uploader(
        "Upload your documents",
        accept_multiple_files=True,
        type=["pdf", "txt", "doc", "docx", "md", "csv", "xlsx", "xls"]
    )
    
    if uploaded_files:
        print("📂 Processing uploaded files...")
        for uploaded_file in uploaded_files:
            # Create a unique file ID
            file_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            try:
                print(f"📄 Processing {uploaded_file.name}...")
                
                # Handle different file types
                if file_extension in ['csv', 'xlsx', 'xls']:
                    if file_extension == 'csv':
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    # Convert DataFrame to string representation
                    content = df.to_string()
                    # Create a Document object
                    documents = [Document(
                        page_content=content,
                        metadata={"source": uploaded_file.name}
                    )]
                    print(f"📊 Successfully processed {file_extension.upper()} file: {uploaded_file.name}")
                
                elif file_extension == 'md':
                    content = uploaded_file.read().decode('utf-8')
                    # Convert Markdown to plain text while preserving structure
                    content = markdown.markdown(content)
                    # Create a Document object
                    documents = [Document(
                        page_content=content,
                        metadata={"source": uploaded_file.name}
                    )]
                    print(f"📝 Successfully processed Markdown file: {uploaded_file.name}")
                
                else:
                    # Save the file temporarily
                    with open(file_id, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process the document using existing logic
                    documents = st.session_state.doc_processor.load_document(file_id)
                    # Clean up the temporary file
                    os.remove(file_id)
                
                # Add the processed documents to the chat agent's knowledge base
                st.session_state.chat_agent.add_documents(documents)
                print(f"✅ Successfully added {uploaded_file.name} to knowledge base")
                st.success(f"Successfully processed {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                print(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                continue
    
    # Show document statistics
    with st.expander("Document Statistics"):
        try:
            stats = st.session_state.doc_processor.query_documents("", k=1)
            if stats:
                st.write(f"Number of documents in knowledge base: {len(stats)}")
            else:
                st.write("No documents in knowledge base yet.")
        except Exception:
            st.write("No documents in knowledge base yet.")
            
print("🎨 Rendering chat interface...")