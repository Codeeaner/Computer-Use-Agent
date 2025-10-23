"""
Test script for See-Think-Act Agent
Run this to verify all components are working
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all required modules can be imported"""
    print("\n" + "=" * 80)
    print("TEST 1: Checking imports...")
    print("=" * 80)
    
    modules = [
        ('mss', 'Screen capture'),
        ('pyautogui', 'GUI automation'),
        ('PIL', 'Image processing'),
        ('ollama', 'Ollama client'),
    ]
    
    all_ok = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name:20s} - {description}")
        except ImportError as e:
            print(f"  ✗ {module_name:20s} - {description} - FAILED: {e}")
            all_ok = False
    
    # Test our custom modules
    custom_modules = [
        ('utils.screenshot_capture', 'Screenshot capture'),
        ('utils.ollama_client', 'Ollama client wrapper'),
        ('utils.action_executor', 'Action executor'),
        ('utils.agent_function_call', 'Function calling'),
    ]
    
    for module_name, description in custom_modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name:30s} - {description}")
        except ImportError as e:
            print(f"  ✗ {module_name:30s} - {description} - FAILED: {e}")
            all_ok = False
    
    return all_ok


def test_screenshot():
    """Test screenshot capture"""
    print("\n" + "=" * 80)
    print("TEST 2: Testing screenshot capture...")
    print("=" * 80)
    
    try:
        from utils.screenshot_capture import ScreenshotCapture
        
        capture = ScreenshotCapture()
        screenshot = capture.capture_screen()
        
        print(f"  ✓ Screenshot captured successfully")
        print(f"    Size: {screenshot.size}")
        print(f"    Mode: {screenshot.mode}")
        
        # Test save
        test_path = "test_screenshot.png"
        capture.capture_and_save(test_path)
        if Path(test_path).exists():
            print(f"  ✓ Screenshot saved: {test_path}")
            Path(test_path).unlink()  # Clean up
            return True
        else:
            print(f"  ✗ Failed to save screenshot")
            return False
            
    except Exception as e:
        print(f"  ✗ Screenshot test failed: {e}")
        return False


def test_ollama_connection():
    """Test Ollama connection"""
    print("\n" + "=" * 80)
    print("TEST 3: Testing Ollama connection...")
    print("=" * 80)
    
    try:
        from utils.ollama_client import OllamaVisionClient
        
        client = OllamaVisionClient(model="qwen3-vl:235b-cloud")
        
        if client.test_connection():
            print(f"  ✓ Ollama connection successful")
            print(f"  ✓ Model 'qwen3-vl:235b-cloud' is available")
            return True
        else:
            print(f"  ✗ Ollama connection failed")
            print(f"  Please ensure:")
            print(f"    1. Ollama is running")
            print(f"    2. Model is pulled: ollama pull qwen3-vl:235b-cloud")
            return False
            
    except Exception as e:
        print(f"  ✗ Ollama test failed: {e}")
        return False


def test_action_executor():
    """Test action executor"""
    print("\n" + "=" * 80)
    print("TEST 4: Testing action executor...")
    print("=" * 80)
    
    try:
        from utils.action_executor import ActionExecutor
        import pyautogui
        
        executor = ActionExecutor()
        
        print(f"  ✓ Action executor initialized")
        print(f"    Screen size: {executor.screen_width}x{executor.screen_height}")
        
        # Test getting current position (doesn't move mouse)
        current_pos = pyautogui.position()
        print(f"  ✓ Current mouse position: {current_pos}")
        
        return True
            
    except Exception as e:
        print(f"  ✗ Action executor test failed: {e}")
        return False


def test_agent_initialization():
    """Test agent initialization"""
    print("\n" + "=" * 80)
    print("TEST 5: Testing agent initialization...")
    print("=" * 80)
    
    try:
        from see_think_act_agent import SeeThinkActAgent
        
        agent = SeeThinkActAgent(
            model="qwen3-vl:235b-cloud",
            max_iterations=5,
            save_screenshots=False,
            log_level="WARNING"
        )
        
        print(f"  ✓ Agent initialized successfully")
        print(f"    Model: {agent.ollama_client.model}")
        print(f"    Max iterations: {agent.max_iterations}")
        print(f"    Screen size: {agent.action_executor.screen_width}x{agent.action_executor.screen_height}")
        
        return True
            
    except Exception as e:
        print(f"  ✗ Agent initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_directories():
    """Test that necessary directories exist or can be created"""
    print("\n" + "=" * 80)
    print("TEST 6: Testing directories...")
    print("=" * 80)
    
    directories = [
        'screenshots',
        'agent_screenshots',
        'logs',
    ]
    
    all_ok = True
    for dir_name in directories:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✓ Directory exists: {dir_name}/")
        else:
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"  ✓ Directory created: {dir_name}/")
            except Exception as e:
                print(f"  ✗ Failed to create directory {dir_name}/: {e}")
                all_ok = False
    
    return all_ok


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("SEE-THINK-ACT AGENT - SYSTEM TEST")
    print("=" * 80)
    print("\nRunning comprehensive system tests...")
    
    tests = [
        ("Import Test", test_imports),
        ("Screenshot Test", test_screenshot),
        ("Ollama Connection Test", test_ollama_connection),
        ("Action Executor Test", test_action_executor),
        ("Agent Initialization Test", test_agent_initialization),
        ("Directory Test", test_directories),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n  ✗ Unexpected error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {status:10s} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED! Agent is ready to use.")
        print("=" * 80)
        print("\nTo get started:")
        print("  1. Run examples: python examples.py")
        print("  2. Run agent: python see_think_act_agent.py")
        print("  3. Open notebook: jupyter notebook see_think_act_demo.ipynb")
        return True
    else:
        print("\n" + "=" * 80)
        print("⚠️  SOME TESTS FAILED - Please fix issues before using agent")
        print("=" * 80)
        print("\nCommon fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Pull Ollama model: ollama pull qwen3-vl:235b-cloud")
        print("  • Start Ollama: ollama serve")
        return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
