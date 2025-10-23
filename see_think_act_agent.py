"""
See-Think-Act Agent for Windows 11
Autonomous agent that captures screenshots, analyzes with Qwen3-VL via Ollama, and performs actions
"""
import time
import json
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

from utils.screenshot_capture import ScreenshotCapture
from utils.ollama_client import OllamaVisionClient
from utils.action_executor import ActionExecutor
from utils.agent_function_call import ComputerUse


class SeeThinkActAgent:
    """
    Autonomous AI Agent that can See, Think, and Act
    - See: Captures screenshots of the desktop
    - Think: Analyzes with Qwen3-VL model via Ollama
    - Act: Executes actions based on model's decisions
    """
    
    def __init__(self,
                 model: str = "qwen3-vl:235b-cloud",
                 max_iterations: int = 50,
                 save_screenshots: bool = True,
                 screenshot_dir: str = "screenshots",
                 log_level: str = "INFO"):
        """
        Initialize the See-Think-Act Agent
        
        Args:
            model: Ollama model name
            max_iterations: Maximum number of iterations before stopping
            save_screenshots: Whether to save screenshots
            screenshot_dir: Directory to save screenshots
            log_level: Logging level
        """
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.screenshot_capture = ScreenshotCapture()
        self.ollama_client = OllamaVisionClient(model=model)
        
        # Get actual screen size
        screen_width, screen_height = self.screenshot_capture.get_screen_size()
        self.action_executor = ActionExecutor(
            screen_width=screen_width,
            screen_height=screen_height
        )
        
        # Configuration
        self.max_iterations = max_iterations
        self.save_screenshots = save_screenshots
        self.screenshot_dir = Path(screenshot_dir)
        
        # Create screenshot directory
        if self.save_screenshots:
            self.screenshot_dir.mkdir(exist_ok=True)
        
        # Initialize computer use tool
        self.computer_use = ComputerUse(
            cfg={
                "display_width_px": 1000,  # Normalized coordinates
                "display_height_px": 1000
            }
        )
        
        # State tracking
        self.iteration_count = 0
        self.task_completed = False
        self.task_status = None
        self.conversation_history = []
        
        self.logger.info(f"Agent initialized with model: {model}")
        self.logger.info(f"Screen size: {screen_width}x{screen_height}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent"""
        return """You are a helpful AI assistant that can see, think, and act on a Windows 11 computer.

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
    
    def _prepare_tools(self) -> List[Dict[str, Any]]:
        """Prepare tool definitions for Ollama"""
        # Convert ComputerUse function to Ollama tool format
        computer_function = self.computer_use.function
        
        tool = {
            "type": "function",
            "function": {
                "name": computer_function["name"],
                "description": computer_function["description"],
                "parameters": computer_function["parameters"]
            }
        }
        
        return [tool]
    
    def _save_screenshot(self, image, prefix: str = "screenshot") -> str:
        """Save screenshot with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{self.iteration_count:03d}_{timestamp}.png"
        filepath = self.screenshot_dir / filename
        image.save(filepath)
        self.logger.info(f"Screenshot saved: {filepath}")
        return str(filepath)
    
    def _capture_current_state(self):
        """Capture current screenshot"""
        self.logger.info("Capturing screenshot...")
        screenshot = self.screenshot_capture.capture_screen()
        
        if self.save_screenshots:
            self._save_screenshot(screenshot)
        
        return screenshot
    
    def _think_and_decide(self, task: str, screenshot) -> Dict[str, Any]:
        """
        Send screenshot to model and get decision
        
        Args:
            task: The user's task
            screenshot: PIL Image of current screen
            
        Returns:
            Response from the model
        """
        self.logger.info("Thinking and deciding next action...")
        
        # Build the prompt
        if self.iteration_count == 0:
            user_prompt = f"Task: {task}\n\nThis is the current state of the desktop. What should I do first to accomplish this task?"
        else:
            user_prompt = f"Task: {task}\n\nThis is the current state after the previous action. What should I do next?"
        
        # Prepare tools
        tools = self._prepare_tools()
        
        # Get response from model
        try:
            response = self.ollama_client.chat_with_image(
                user_query=user_prompt,
                image=screenshot,
                system_prompt=self._get_system_prompt(),
                tools=tools
            )
            
            self.logger.info(f"Model response: {response}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error in model inference: {e}")
            raise
    
    def _execute_action(self, response: Dict[str, Any]) -> bool:
        """
        Execute the action decided by the model
        
        Args:
            response: Response from the model
            
        Returns:
            True if action executed successfully
        """
        # Parse the action from response
        action = self.ollama_client.parse_computer_use_action(response)
        
        if not action:
            self.logger.warning("No action found in response")
            # Check if the model just wants to observe
            if 'message' in response and 'content' in response['message']:
                content = response['message']['content']
                self.logger.info(f"Model response: {content}")
                
                # Check for termination signal in text
                if 'terminate' in content.lower() or 'complete' in content.lower():
                    self.logger.info("Task appears to be complete (textual indication)")
                    self.task_completed = True
                    self.task_status = 'success'
                    return True
            
            return False
        
        # Extract action details
        if 'function' in action:
            action_details = action['function']
            action_name = action_details.get('name')
            
            if isinstance(action_details.get('arguments'), str):
                arguments = json.loads(action_details['arguments'])
            else:
                arguments = action_details.get('arguments', {})
        else:
            arguments = action.get('arguments', {})
            action_name = action.get('name', 'computer')
        
        # Check for termination
        if arguments.get('action') == 'terminate':
            self.task_completed = True
            self.task_status = arguments.get('status', 'success')
            self.logger.info(f"Task terminated with status: {self.task_status}")
            return True
        
        # Check for answer action (just observation)
        if arguments.get('action') == 'answer':
            answer_text = arguments.get('text', '')
            self.logger.info(f"Model's answer: {answer_text}")
            return True
        
        # Execute the action
        self.logger.info(f"Executing action: {arguments}")
        success = self.action_executor.execute_computer_use_action({
            'name': action_name,
            'arguments': arguments
        })
        
        # Wait a bit after action for UI to update
        if success and arguments.get('action') != 'wait':
            time.sleep(1)
        
        return success
    
    def run(self, task: str) -> Dict[str, Any]:
        """
        Run the agent to complete the given task
        
        Args:
            task: The task to complete
            
        Returns:
            Dictionary with results including success status and message
        """
        self.logger.info(f"=" * 80)
        self.logger.info(f"Starting task: {task}")
        self.logger.info(f"=" * 80)
        
        # Reset state
        self.iteration_count = 0
        self.task_completed = False
        self.task_status = None
        self.conversation_history = []
        
        start_time = time.time()
        
        try:
            while self.iteration_count < self.max_iterations and not self.task_completed:
                self.iteration_count += 1
                self.logger.info(f"\n{'=' * 80}")
                self.logger.info(f"Iteration {self.iteration_count}/{self.max_iterations}")
                self.logger.info(f"{'=' * 80}")
                
                # Step 1: SEE - Capture screenshot
                screenshot = self._capture_current_state()
                
                # Step 2: THINK - Analyze and decide
                response = self._think_and_decide(task, screenshot)
                
                # Store in conversation history
                self.conversation_history.append({
                    'iteration': self.iteration_count,
                    'response': response
                })
                
                # Step 3: ACT - Execute action
                success = self._execute_action(response)
                
                if not success:
                    self.logger.warning("Action execution failed, but continuing...")
                
                # Small delay between iterations
                time.sleep(0.5)
            
            # Task completion
            elapsed_time = time.time() - start_time
            
            if self.task_completed:
                result = {
                    'success': self.task_status == 'success',
                    'status': self.task_status,
                    'message': f'Task completed in {self.iteration_count} iterations',
                    'iterations': self.iteration_count,
                    'elapsed_time': elapsed_time
                }
                self.logger.info(f"\n{'=' * 80}")
                self.logger.info(f"TASK COMPLETED: {result['message']}")
                self.logger.info(f"Status: {self.task_status}")
                self.logger.info(f"Time: {elapsed_time:.2f} seconds")
                self.logger.info(f"{'=' * 80}\n")
            else:
                result = {
                    'success': False,
                    'status': 'timeout',
                    'message': f'Task did not complete within {self.max_iterations} iterations',
                    'iterations': self.iteration_count,
                    'elapsed_time': elapsed_time
                }
                self.logger.warning(f"\n{'=' * 80}")
                self.logger.warning(f"TASK TIMEOUT: {result['message']}")
                self.logger.warning(f"{'=' * 80}\n")
            
            return result
            
        except KeyboardInterrupt:
            self.logger.info("\nTask interrupted by user")
            return {
                'success': False,
                'status': 'interrupted',
                'message': 'Task interrupted by user',
                'iterations': self.iteration_count,
                'elapsed_time': time.time() - start_time
            }
        
        except Exception as e:
            self.logger.error(f"Error during task execution: {e}", exc_info=True)
            return {
                'success': False,
                'status': 'error',
                'message': f'Error: {str(e)}',
                'iterations': self.iteration_count,
                'elapsed_time': time.time() - start_time
            }


def main():
    """Example usage of the agent"""
    # Initialize agent
    agent = SeeThinkActAgent(
        model="qwen3-vl:235b-cloud",
        max_iterations=30,
        save_screenshots=True
    )
    
    # Test connection
    if not agent.ollama_client.test_connection():
        print("\n⚠️  WARNING: Could not connect to Ollama or model not found")
        print("Make sure Ollama is running and the model is pulled:")
        print("  ollama run qwen3-vl:235b-cloud")
        return
    
    # Example task
    task = "Open Notepad and type 'Hello from AI Agent!'"
    
    print(f"\nTask: {task}")
    print("Starting agent... (Press Ctrl+C to stop)\n")
    
    # Run the agent
    result = agent.run(task)
    
    # Print results
    print("\n" + "=" * 80)
    print("FINAL RESULT:")
    print(json.dumps(result, indent=2))
    print("=" * 80)


if __name__ == "__main__":
    main()
