# Quick Start Guide - See-Think-Act AI Agent

## Prerequisites Check

Before starting, ensure you have:
- [ ] Windows 11 (or Windows 10)
- [ ] Python 3.9 or higher
- [ ] Ollama installed
- [ ] Internet connection (for model download)

## 5-Minute Setup

### Step 1: Install Ollama (if not installed)

Download and install from: https://ollama.ai

Or use winget:
```powershell
winget install Ollama.Ollama
```

### Step 2: Pull the Model

Open PowerShell and run:
```powershell
ollama pull qwen3-vl:235b-cloud
```

This will download the Qwen3-VL vision model (~13GB). Wait for it to complete.

### Step 3: Install Python Dependencies

In the project directory, run:
```powershell
pip install -r requirements.txt
```

Or use the automated setup script:
```powershell
.\setup.ps1
```

### Step 4: Test the Setup

Run the test:
```powershell
python -c "from utils.ollama_client import OllamaVisionClient; client = OllamaVisionClient(); client.test_connection()"
```

You should see: `✓ Model 'qwen3-vl:235b-cloud' is available`

### Step 5: Run Your First Task

```powershell
python see_think_act_agent.py
```

Or for interactive examples:
```powershell
jupyter notebook see_think_act_demo.ipynb
```

## Your First Task

Try this simple example:

```python
from see_think_act_agent import SeeThinkActAgent

# Initialize the agent
agent = SeeThinkActAgent(
    model="qwen3-vl:235b-cloud",
    max_iterations=20,
    save_screenshots=True
)

# Run a simple task
result = agent.run("Open Notepad and type 'Hello from AI!'")

print(result)
```

## What to Expect

1. **Agent starts**: You'll see log messages indicating the agent is starting
2. **Screenshot capture**: The agent takes a screenshot of your desktop
3. **Thinking**: The model analyzes the screenshot (takes a few seconds)
4. **Action**: The agent performs an action (e.g., clicking, typing)
5. **Repeat**: Steps 2-4 repeat until task completion

## Monitoring

- **Console logs**: Watch the terminal for real-time updates
- **Screenshots**: Check `agent_screenshots/` folder to see what the agent saw
- **Stop anytime**: Press `Ctrl+C` or move mouse to top-left corner

## Common First Tasks

### Task 1: Open an Application
```python
agent.run("Open Calculator")
```

### Task 2: Simple Calculation
```python
agent.run("Open Calculator and calculate 42 + 17")
```

### Task 3: Text Editor
```python
agent.run("Open Notepad and type 'The AI agent is working!'")
```

### Task 4: Web Browser
```python
agent.run("Open Microsoft Edge")
```

## Troubleshooting

### "Model not found"
- Run: `ollama pull qwen3-vl:235b-cloud`
- Verify: `ollama list`

### "Ollama connection error"
- Make sure Ollama is running
- Restart Ollama if needed

### "Agent not clicking correctly"
- Check your screen resolution matches agent settings
- Adjust coordinates in `action_executor.py` if needed

### "Actions too fast/slow"
- Adjust `pyautogui.PAUSE` in `action_executor.py`
- Modify wait times in the agent

## Safety Tips

⚠️ **Important**: The agent can control your computer!

- Start with simple, safe tasks
- Keep important work saved
- Don't leave the agent unattended on complex tasks
- Use a test environment first
- Review the code to understand what it does

## Next Steps

Once comfortable with basic tasks:

1. **Try complex tasks**: Multi-step workflows
2. **Customize the agent**: Adjust parameters and behavior
3. **Add new actions**: Extend the action executor
4. **Create workflows**: Chain multiple tasks together
5. **Review screenshots**: Learn how the agent "sees"

## Getting Help

- Read the full `README.md` for detailed documentation
- Check `see_think_act_demo.ipynb` for examples
- Review saved screenshots to debug issues
- Check console logs for error messages

## Example Session

```
$ python see_think_act_agent.py

================================================================================
Starting task: Open Notepad and type 'Hello from AI!'
================================================================================

Iteration 1/30
================================================================================
Capturing screenshot...
Screenshot saved: agent_screenshots/screenshot_001_20250101_120000.png
Thinking and deciding next action...
Model response: {action: "left_click", coordinate: [50, 950]}
Executing action: left_click at (96, 1026)

Iteration 2/30
================================================================================
Capturing screenshot...
Thinking and deciding next action...
Model response: {action: "type", text: "notepad"}
Executing action: type 'notepad'

...

================================================================================
TASK COMPLETED: Task completed in 8 iterations
Status: success
Time: 45.23 seconds
================================================================================
```

Enjoy using your See-Think-Act AI Agent! 🤖
