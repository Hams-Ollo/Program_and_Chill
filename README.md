# Program & Chill AI Assistant

## Overview

Program & Chill is an intelligent conversational AI assistant built with Groq's Mixtral-8x7B model and Streamlit. It features a modern dark-themed UI and provides fast, accurate responses in a user-friendly chat interface.

## 🌟 Features

- **Advanced Language Model**: Powered by Groq's Mixtral-8x7B model
- **Modern Dark Theme UI**: Clean, responsive interface with customized styling
- **Intelligent Conversations**: Natural and context-aware responses
- **Configurable Settings**: Adjustable temperature and response length
- **Error Handling**: Robust error management and logging
- **State Management**: Efficient conversation history tracking

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Groq API (Mixtral-8x7B)
- **Language**: Python 3.8+
- **Key Libraries**:
  - `streamlit`: Web interface
  - `langchain-groq`: Groq API integration
  - `python-dotenv`: Environment management
  - `logging`: Error tracking and debugging

## 📋 Prerequisites

- Python 3.8+
- Groq API key
- Git (for version control)

## 🚀 Quick Start

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Hams-Ollo/Program_and_Chill.git
   cd Program_and_Chill
   ```

2. **Set up virtual environment**:

   ```bash
   python -m venv venv
   # For Windows:
   .\venv\Scripts\activate
   # For Unix/MacOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Create a `.env` file in the project root
   - Add your Groq API key:

     ```curl
     GROQ_API_KEY=your_api_key_here
     ```

5. **Run the application**:

   ```bash
   streamlit run main.py
   ```

## 📁 Project Structure

```curl
Program_and_Chill/
├── main.py              # Main application file
├── .env                 # Environment variables
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## ⚙️ Core Components

### Main Application (`main.py`)

- Streamlit UI configuration
- Chat interface implementation
- Groq API integration
- State management
- Error handling
- Logging setup

### Environment Configuration (`.env`)

- API key storage
- Configuration settings

## 🎨 UI Features

- **Dark Theme**: Modern, eye-friendly dark mode
- **Responsive Design**: Adapts to different screen sizes
- **Chat Interface**: Clean message bubbles with distinct styling
- **Settings Sidebar**: Easy access to model parameters
- **Error Feedback**: Clear error messages and status indicators

## 🔧 Configuration Options

### Model Parameters

- **Temperature**: Controls response creativity (0.0 - 1.0)
- **Max Tokens**: Adjusts response length (100 - 4000)

### Chat Settings

- Clear chat history
- View conversation timestamps
- Error state tracking

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📝 License

[MIT License](LICENSE)

## 👤 Author

@hams_ollo

## 🔄 Version

Current Version: 0.0.1
