"""
Action executor for Windows 11
Performs mouse, keyboard, and other computer actions
"""
import pyautogui
import time
import subprocess
from typing import Tuple, Optional, List
import logging

# Configure pyautogui
pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
pyautogui.PAUSE = 0.5  # Small pause between actions


class ActionExecutor:
    """Executes computer actions on Windows 11"""
    
    def __init__(self, screen_width: int = 1920, screen_height: int = 1080):
        """
        Initialize action executor
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = logging.getLogger(__name__)
        
        # Get actual screen size
        actual_width, actual_height = pyautogui.size()
        self.logger.info(f"Screen size: {actual_width}x{actual_height}")
    
    def click(self, x: int, y: int, button: str = 'left', clicks: int = 1) -> bool:
        """
        Click at specified coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            button: Mouse button ('left', 'right', 'middle')
            clicks: Number of clicks (1 for single, 2 for double)
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Clicking at ({x}, {y}) with {button} button, {clicks} times")
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
            return True
        except Exception as e:
            self.logger.error(f"Error clicking: {e}")
            return False
    
    def click_relative(self, x_ratio: float, y_ratio: float, 
                      button: str = 'left', clicks: int = 1) -> bool:
        """
        Click at coordinates specified as ratios (0-1) of screen size
        
        Args:
            x_ratio: X coordinate as ratio (0-1) where 0.5 is 500 on a 1000px scale
            y_ratio: Y coordinate as ratio (0-1) where 0.5 is 500 on a 1000px scale
            button: Mouse button
            clicks: Number of clicks
            
        Returns:
            True if successful
        """
        # Convert from 0-1 ratio to actual pixels
        x = int(x_ratio * self.screen_width)
        y = int(y_ratio * self.screen_height)
        
        return self.click(x, y, button, clicks)
    
    def click_normalized(self, x_norm: float, y_norm: float,
                        button: str = 'left', clicks: int = 1) -> bool:
        """
        Click at normalized coordinates (0-1000 scale)
        
        Args:
            x_norm: X coordinate on 0-1000 scale
            y_norm: Y coordinate on 0-1000 scale
            button: Mouse button
            clicks: Number of clicks
            
        Returns:
            True if successful
        """
        # Convert from 0-1000 scale to actual pixels
        x = int((x_norm / 1000.0) * self.screen_width)
        y = int((y_norm / 1000.0) * self.screen_height)
        
        return self.click(x, y, button, clicks)
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Move mouse to specified coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Time to take for movement (seconds)
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Moving mouse to ({x}, {y})")
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            self.logger.error(f"Error moving mouse: {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """
        Type text using keyboard
        
        Args:
            text: Text to type
            interval: Interval between key presses (seconds)
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Typing text: {text[:50]}...")
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            self.logger.error(f"Error typing text: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """
        Press a single key
        
        Args:
            key: Key name (e.g., 'enter', 'escape', 'tab')
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Pressing key: {key}")
            pyautogui.press(key)
            return True
        except Exception as e:
            self.logger.error(f"Error pressing key: {e}")
            return False
    
    def hotkey(self, *keys) -> bool:
        """
        Press a combination of keys
        
        Args:
            *keys: Keys to press together (e.g., 'ctrl', 'c')
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Pressing hotkey: {'+'.join(keys)}")
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            self.logger.error(f"Error pressing hotkey: {e}")
            return False
    
    def scroll(self, clicks: int) -> bool:
        """
        Scroll the mouse wheel
        
        Args:
            clicks: Number of clicks (positive = up, negative = down)
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Scrolling {clicks} clicks")
            pyautogui.scroll(clicks)
            return True
        except Exception as e:
            self.logger.error(f"Error scrolling: {e}")
            return False
    
    def drag(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Drag mouse to specified coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Time to take for drag (seconds)
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Dragging to ({x}, {y})")
            pyautogui.drag(x, y, duration=duration)
            return True
        except Exception as e:
            self.logger.error(f"Error dragging: {e}")
            return False
    
    def wait(self, seconds: float) -> bool:
        """
        Wait for specified seconds
        
        Args:
            seconds: Time to wait
            
        Returns:
            True
        """
        self.logger.info(f"Waiting {seconds} seconds")
        time.sleep(seconds)
        return True
    
    def execute_computer_use_action(self, action: dict) -> bool:
        """
        Execute a computer use action from the model
        
        Args:
            action: Action dictionary with 'name' and 'arguments'
            
        Returns:
            True if successful
        """
        try:
            action_name = action.get('name') or action.get('function', {}).get('name')
            arguments = action.get('arguments') or action.get('function', {}).get('arguments', {})
            
            if isinstance(arguments, str):
                import json
                arguments = json.loads(arguments)
            
            self.logger.info(f"Executing action: {action_name} with args: {arguments}")
            
            if action_name in ['computer', 'computer_use']:
                return self._execute_computer_action(arguments)
            else:
                self.logger.warning(f"Unknown action: {action_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error executing action: {e}")
            return False
    
    def _execute_computer_action(self, args: dict) -> bool:
        """
        Execute a computer action
        
        Args:
            args: Action arguments with 'action' and other parameters
            
        Returns:
            True if successful
        """
        action_type = args.get('action')
        
        if action_type == 'left_click':
            coordinate = args.get('coordinate', [500, 500])
            return self.click_normalized(coordinate[0], coordinate[1], button='left', clicks=1)
        
        elif action_type == 'left_click_drag':
            coordinate = args.get('coordinate', [500, 500])
            x = int((coordinate[0] / 1000.0) * self.screen_width)
            y = int((coordinate[1] / 1000.0) * self.screen_height)
            return self.drag(x, y)
        
        elif action_type == 'right_click':
            coordinate = args.get('coordinate', [500, 500])
            return self.click_normalized(coordinate[0], coordinate[1], button='right', clicks=1)
        
        elif action_type == 'double_click':
            coordinate = args.get('coordinate', [500, 500])
            return self.click_normalized(coordinate[0], coordinate[1], button='left', clicks=2)
        
        elif action_type == 'middle_click':
            coordinate = args.get('coordinate', [500, 500])
            return self.click_normalized(coordinate[0], coordinate[1], button='middle', clicks=1)
        
        elif action_type == 'mouse_move':
            coordinate = args.get('coordinate', [500, 500])
            x = int((coordinate[0] / 1000.0) * self.screen_width)
            y = int((coordinate[1] / 1000.0) * self.screen_height)
            return self.move_mouse(x, y)
        
        elif action_type == 'type':
            text = args.get('text', '')
            return self.type_text(text)
        
        elif action_type == 'key':
            key = args.get('text', 'enter')
            return self.press_key(key)
        
        elif action_type == 'scroll':
            scroll_amount = args.get('scroll_amount', 0)
            return self.scroll(scroll_amount)
        
        elif action_type == 'screenshot':
            # Screenshot is handled externally
            self.logger.info("Screenshot action requested (handled externally)")
            return True
        
        elif action_type == 'cursor_position':
            # Get current cursor position
            x, y = pyautogui.position()
            self.logger.info(f"Current cursor position: ({x}, {y})")
            return True
        
        else:
            self.logger.warning(f"Unknown computer action: {action_type}")
            return False


if __name__ == "__main__":
    # Test the action executor
    logging.basicConfig(level=logging.INFO)
    
    executor = ActionExecutor()
    
    print("Testing action executor...")
    print("Screen size:", pyautogui.size())
    print("\nMove your mouse to the top-left corner to abort any action")
    
    time.sleep(2)
    
    # Test getting current position
    print("\nCurrent mouse position:", pyautogui.position())
