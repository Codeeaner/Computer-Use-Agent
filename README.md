# See-Think-Act AI Agent for Windows 11

An autonomous AI Agent that can **See**, **Think**, and **Act** to perform any task on Windows 11 using Ollama with Qwen3-VL vision-language model.

## 🎯 Features

- **👁️ See**: Captures screenshots of your desktop using efficient Windows APIs
- **🧠 Think**: Analyzes screenshots with Qwen3-VL model via Ollama to understand the UI and plan actions
- **🎯 Act**: Executes mouse clicks, keyboard input, and system actions autonomously
- **🔄 Loop**: Continues until the task is complete or max iterations reached
- **📸 Screenshot History**: Saves all screenshots for debugging and analysis
- **🛡️ Safe Operation**: Includes failsafe mechanisms to prevent runaway automation

## 🚀 Quick Start

### Prerequisites

1. **Windows 11** (or Windows 10)
2. **Python 3.9+**
3. **Ollama** installed and running
4. **Qwen3-VL model** pulled in Ollama

### Installation

1. **Install Ollama** (if not already installed):
   ```powershell
   # Download from https://ollama.ai and install
   # Or use winget:
   winget install Ollama.Ollama
   ```

2. **Pull the Qwen3-VL model**:
   ```powershell
   ollama pull qwen3-vl:235b-cloud
   ```

3. **Clone this repository**:
   ```powershell
   git clone <repository-url>
   cd Computer-Use-Agent
   ```

4. **Install Python dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Agent

#### Option 1: Command Line

```powershell
python see_think_act_agent.py
```

You can also run custom tasks programmatically:

```python
from see_think_act_agent import SeeThinkActAgent

# Initialize agent
agent = SeeThinkActAgent(
    model="qwen3-vl:235b-cloud",
    max_iterations=30,
    save_screenshots=True
)

# Run a task
result = agent.run("Open Notepad and type 'Hello World'")
print(result)
```

#### Option 2: Jupyter Notebook

Open and run `see_think_act_demo.ipynb` for interactive examples:

```powershell
jupyter notebook see_think_act_demo.ipynb
```

## 📁 Project Structure

```
STC/
├── see_think_act_agent.py       # Main agent implementation
├── see_think_act_demo.ipynb     # Demo notebook with examples
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── utils/
│   ├── __init__.py
│   ├── screenshot_capture.py    # Screen capture utility
│   ├── ollama_client.py         # Ollama API wrapper
│   ├── action_executor.py       # Action execution (mouse/keyboard)
│   └── agent_function_call.py   # Function calling definitions
├── screenshots/                  # Default screenshot directory
└── agent_screenshots/           # Agent execution screenshots
```

## 🎮 How It Works

The agent operates in a continuous **See-Think-Act** loop:

### 1. SEE 👁️
- Captures a screenshot of the current desktop state
- Uses `mss` library for efficient, low-latency screen capture
- Encodes image for transmission to the model

### 2. THINK 🧠
- Sends screenshot to Qwen3-VL model via Ollama
- Model analyzes the visual state and understands the UI
- Uses function calling to structure the next action
- Considers task progress and decides next step

### 3. ACT 🎯
- Executes the action decided by the model
- Uses `pyautogui` for precise mouse and keyboard control
- Actions include:
  - Mouse clicks (left, right, double, middle)
  - Mouse movement and dragging
  - Keyboard typing and key presses
  - Scrolling
  - Waiting for UI updates
  - Task termination

### 4. REPEAT 🔄
- Captures new screenshot to see the result
- Loop continues until task completion or max iterations
- Agent adapts based on what it sees

## 🛠️ Configuration

### Agent Parameters

```python
agent = SeeThinkActAgent(
    model="qwen3-vl:235b-cloud",    # Ollama model name
    max_iterations=30,               # Maximum action loops
    save_screenshots=True,           # Save screenshots for debugging
    screenshot_dir="screenshots",    # Screenshot save directory
    log_level="INFO"                 # Logging verbosity
)
```

### Action Executor Settings

Edit `utils/action_executor.py` to adjust:
- Mouse movement speed
- Typing speed
- Wait times between actions
- Failsafe settings

## 📝 Example Tasks

### Simple Tasks
```python
# Open an application
agent.run("Open Notepad")

# Type text
agent.run("Open Notepad and type 'Hello World'")

# Use calculator
agent.run("Open Calculator and calculate 123 + 456")
```

### Complex Tasks
```python
# Web browsing
agent.run("Open Microsoft Edge and search for 'Ollama AI'")

# File management
agent.run("Open File Explorer and create a new folder named 'AI_Projects'")

# Multi-step tasks
agent.run("Open Notepad, type a grocery list, and save it as groceries.txt on Desktop")
```

## 🔒 Safety Features

- **Failsafe**: Move mouse to top-left corner to abort (pyautogui feature)
- **Max Iterations**: Prevents infinite loops
- **Keyboard Interrupt**: Press Ctrl+C to stop
- **Screenshot History**: Review what the agent did
- **Logging**: Full activity logs for debugging

## 🐛 Troubleshooting

### Model Not Found
```powershell
# Pull the model
ollama pull qwen3-vl:235b-cloud

# Verify it's available
ollama list
```

### Ollama Connection Error
```powershell
# Check if Ollama is running
ollama serve

# Or restart Ollama service
```

### Screen Capture Issues
- Ensure Python has screen capture permissions
- Try running with administrator privileges
- Check antivirus/security software settings

### Mouse Control Problems
- Verify screen resolution in agent initialization
- Adjust coordinate scaling if needed
- Check for display scaling settings in Windows

### Actions Too Fast/Slow
- Adjust `pyautogui.PAUSE` in `action_executor.py`
- Modify wait times after actions
- Increase iteration delays

## 🎯 Best Practices

1. **Start Simple**: Begin with simple tasks and build up complexity
2. **Clear Desktop**: Minimize visual clutter for better recognition
3. **Specific Instructions**: Give clear, specific task descriptions
4. **Monitor Progress**: Watch the agent work to understand its decisions
5. **Review Screenshots**: Check saved screenshots to debug issues
6. **Reasonable Scope**: Keep tasks focused and achievable

## 🧪 Testing

Test individual components:

```powershell
# Test screenshot capture
python utils/screenshot_capture.py

# Test Ollama client
python utils/ollama_client.py

# Test action executor
python utils/action_executor.py
```

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    See-Think-Act Agent                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  SEE Module  │    │ THINK Module │    │  ACT Module  │
│              │    │              │    │              │
│  Screenshot  │───▶│    Ollama    │───▶│  PyAutoGUI   │
│   Capture    │    │   Qwen3-VL   │    │   Control    │
│   (mss)      │    │  Vision LLM  │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                      ┌─────▼─────┐
                      │  Windows  │
                      │    OS     │
                      └───────────┘
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional action types
- Better error handling
- Multi-monitor support
- Task planning and optimization
- Integration with more models

## 🙏 Acknowledgments

- **Qwen Team**: For the amazing Qwen3-VL model
- **Ollama**: For making local LLM inference easy
- **PyAutoGUI**: For GUI automation capabilities
- **MSS**: For efficient screen capture

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

---

**⚠️ Warning**: This agent has the ability to control your computer. Use responsibly and monitor its actions, especially when testing new tasks.
