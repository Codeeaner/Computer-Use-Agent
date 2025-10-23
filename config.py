"""
Configuration file for See-Think-Act Agent
Customize these settings to adjust agent behavior
"""

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# Ollama model to use
MODEL_NAME = "qwen3-vl:235b-cloud"

# Ollama server URL (default: local)
OLLAMA_BASE_URL = "http://localhost:11434"

# ============================================================================
# AGENT BEHAVIOR
# ============================================================================

# Maximum number of actions before stopping
MAX_ITERATIONS = 30

# Time to wait between iterations (seconds)
ITERATION_DELAY = 0.5

# Time to wait after each action for UI to update (seconds)
POST_ACTION_DELAY = 1.0

# ============================================================================
# SCREENSHOT SETTINGS
# ============================================================================

# Save screenshots for debugging
SAVE_SCREENSHOTS = True

# Directory to save screenshots
SCREENSHOT_DIR = "agent_screenshots"

# Screenshot format (PNG, JPEG)
SCREENSHOT_FORMAT = "PNG"

# Monitor to capture (1 = primary monitor)
MONITOR_NUMBER = 1

# ============================================================================
# ACTION EXECUTOR SETTINGS
# ============================================================================

# Default pause between pyautogui actions (seconds)
PYAUTOGUI_PAUSE = 0.5

# Enable pyautogui failsafe (move mouse to corner to abort)
PYAUTOGUI_FAILSAFE = True

# Mouse movement duration (seconds)
MOUSE_MOVE_DURATION = 0.5

# Typing interval between characters (seconds)
TYPING_INTERVAL = 0.05

# Drag duration (seconds)
DRAG_DURATION = 0.5

# ============================================================================
# COORDINATE SYSTEM
# ============================================================================

# Normalized coordinate range (used by model)
NORMALIZED_WIDTH = 1000
NORMALIZED_HEIGHT = 1000

# ============================================================================
# LOGGING
# ============================================================================

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = "INFO"

# Log format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Save logs to file
SAVE_LOGS = True

# Log file directory
LOG_DIR = "logs"

# Log file name pattern
LOG_FILE_NAME = "agent_{timestamp}.log"

# ============================================================================
# SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """You are a helpful AI assistant that can see, think, and act on a Windows 11 computer.

Your capabilities:
1. SEE: You receive screenshots of the current desktop state
2. THINK: You analyze what you see and plan the next action
3. ACT: You can control the mouse, keyboard, and perform various actions

When given a task:
1. First, look at the screenshot to understand the current state
2. Think about what needs to be done to accomplish the task
3. Take ONE action at a time
4. After each action, you'll get a new screenshot to see the result
5. Continue until the task is complete

Important guidelines:
- Be precise with mouse coordinates - aim for the center of buttons/links
- Wait after actions that might take time (opening apps, loading pages)
- If an action fails, try adjusting your approach
- When the task is complete, use the 'terminate' action with status 'success'
- If the task cannot be completed, use 'terminate' with status 'failure'

You have access to a 'computer' tool that allows you to:
- Click (left, right, double, middle)
- Type text
- Press keys
- Move mouse
- Scroll
- Wait for changes
- Terminate when done
"""

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Retry failed actions
RETRY_FAILED_ACTIONS = False

# Maximum retries for failed actions
MAX_RETRIES = 3

# Use vision grounding for precise clicking
USE_VISION_GROUNDING = True

# Minimum confidence for action execution (0-1)
MIN_CONFIDENCE = 0.7

# Enable multi-monitor support
MULTI_MONITOR_SUPPORT = False

# Screenshot compression quality (1-100, higher = better quality)
SCREENSHOT_QUALITY = 95

# ============================================================================
# SAFETY SETTINGS
# ============================================================================

# Dangerous actions to block (list of action types)
BLOCKED_ACTIONS = []

# Require confirmation for sensitive actions
REQUIRE_CONFIRMATION = False

# Maximum task duration (seconds, 0 = no limit)
MAX_TASK_DURATION = 600  # 10 minutes

# Auto-abort if no progress after N iterations
AUTO_ABORT_THRESHOLD = 10

# ============================================================================
# DEBUGGING
# ============================================================================

# Print detailed debug information
DEBUG_MODE = False

# Save model responses
SAVE_MODEL_RESPONSES = True

# Model response save directory
MODEL_RESPONSE_DIR = "model_responses"

# Visualize actions on screenshots (draw click points, etc.)
VISUALIZE_ACTIONS = True

# Color for visualization (RGB)
VISUALIZATION_COLOR = (0, 255, 0)  # Green

# ============================================================================
# PERFORMANCE
# ============================================================================

# Use faster screenshot method (may reduce quality)
FAST_SCREENSHOT = False

# Compress screenshots before sending to model
COMPRESS_SCREENSHOTS = True

# Maximum screenshot resolution (width, height)
MAX_SCREENSHOT_RESOLUTION = (1920, 1080)

# Cache model responses (not recommended for dynamic tasks)
CACHE_RESPONSES = False
