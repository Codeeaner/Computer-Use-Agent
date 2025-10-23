"""
Screenshot capture utility for Windows 11
Uses mss for efficient screen capture
"""
import mss
import mss.tools
from PIL import Image
import io
import base64
from typing import Tuple, Optional


class ScreenshotCapture:
    """Captures screenshots on Windows 11 using mss library"""
    
    def __init__(self):
        self.sct = mss.mss()
        
    def capture_screen(self, monitor_number: int = 1) -> Image.Image:
        """
        Capture screenshot of specified monitor
        
        Args:
            monitor_number: Monitor to capture (1 = primary monitor)
            
        Returns:
            PIL Image object
        """
        monitor = self.sct.monitors[monitor_number]
        screenshot = self.sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img
    
    def capture_and_save(self, output_path: str, monitor_number: int = 1) -> str:
        """
        Capture screenshot and save to file
        
        Args:
            output_path: Path to save screenshot
            monitor_number: Monitor to capture
            
        Returns:
            Path to saved screenshot
        """
        img = self.capture_screen(monitor_number)
        img.save(output_path)
        return output_path
    
    def capture_to_base64(self, monitor_number: int = 1, format: str = 'PNG') -> str:
        """
        Capture screenshot and encode as base64
        
        Args:
            monitor_number: Monitor to capture
            format: Image format (PNG, JPEG, etc.)
            
        Returns:
            Base64 encoded string
        """
        img = self.capture_screen(monitor_number)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format=format)
        img_bytes = buffer.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        return img_base64
    
    def get_screen_size(self, monitor_number: int = 1) -> Tuple[int, int]:
        """
        Get the size of the specified monitor
        
        Args:
            monitor_number: Monitor number
            
        Returns:
            Tuple of (width, height)
        """
        monitor = self.sct.monitors[monitor_number]
        return monitor['width'], monitor['height']
    
    def list_monitors(self) -> list:
        """
        List all available monitors
        
        Returns:
            List of monitor information dictionaries
        """
        return self.sct.monitors
    
    def __del__(self):
        """Cleanup mss instance"""
        if hasattr(self, 'sct'):
            self.sct.close()


if __name__ == "__main__":
    # Test the screenshot capture
    capture = ScreenshotCapture()
    
    print("Available monitors:")
    for i, monitor in enumerate(capture.list_monitors()):
        print(f"Monitor {i}: {monitor}")
    
    # Capture and save screenshot
    output_path = "test_screenshot.png"
    capture.capture_and_save(output_path)
    print(f"\nScreenshot saved to: {output_path}")
    
    # Get screen size
    width, height = capture.get_screen_size()
    print(f"Screen size: {width}x{height}")
