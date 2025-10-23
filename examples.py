"""
Example scripts for See-Think-Act Agent
Run these examples to test the agent with different tasks
"""

from see_think_act_agent import SeeThinkActAgent
import json


def example_1_simple_notepad():
    """Example 1: Open Notepad and type text"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Open Notepad and Type Text")
    print("=" * 80)
    
    agent = SeeThinkActAgent(
        model="qwen3-vl:235b-cloud",
        max_iterations=20,
        save_screenshots=True
    )
    
    task = "Open Notepad and type 'Hello from the See-Think-Act AI Agent!'"
    print(f"\nTask: {task}\n")
    
    result = agent.run(task)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))
    

def example_2_calculator():
    """Example 2: Use Calculator"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Use Calculator")
    print("=" * 80)
    
    agent = SeeThinkActAgent(
        model="qwen3-vl:235b-cloud",
        max_iterations=30,
        save_screenshots=True
    )
    
    task = "Open Calculator and calculate 10 + 15"
    print(f"\nTask: {task}\n")
    
    result = agent.run(task)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))


def example_3_file_explorer():
    """Example 3: Open File Explorer"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Open File Explorer")
    print("=" * 80)
    
    agent = SeeThinkActAgent(
        model="qwen3-vl:235b-cloud",
        max_iterations=15,
        save_screenshots=True
    )
    
    task = "Open File Explorer"
    print(f"\nTask: {task}\n")
    
    result = agent.run(task)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))


def example_4_web_browser():
    """Example 4: Open Web Browser"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Open Web Browser")
    print("=" * 80)
    
    agent = SeeThinkActAgent(
        model="qwen3-vl:235b-cloud",
        max_iterations=25,
        save_screenshots=True
    )
    
    task = "Open Google Chrome browser. Open new tab and go to chatgpt.com. Ask it 'What is the capital of France?'"
    print(f"\nTask: {task}\n")
    
    result = agent.run(task)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))


def example_5_custom_task():
    """Example 5: Custom Task (modify as needed)"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Custom Task")
    print("=" * 80)
    
    agent = SeeThinkActAgent(
        model="qwen3-vl:235b-cloud",
        max_iterations=30,
        save_screenshots=True
    )
    
    # Customize your task here
    task = "Open Settings"
    print(f"\nTask: {task}\n")
    
    result = agent.run(task)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))


def run_all_examples():
    """Run all examples sequentially"""
    print("\n" + "=" * 80)
    print("RUNNING ALL EXAMPLES")
    print("=" * 80)
    print("\nThis will run all example tasks sequentially.")
    print("Press Ctrl+C at any time to stop.\n")
    
    input("Press Enter to continue...")
    
    examples = [
        example_1_simple_notepad,
        example_2_calculator,
        example_3_file_explorer,
        example_4_web_browser,
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n\n{'=' * 80}")
        print(f"Running Example {i}/{len(examples)}")
        print('=' * 80)
        
        try:
            example()
        except KeyboardInterrupt:
            print("\n\nExecution interrupted by user.")
            break
        except Exception as e:
            print(f"\n\nError in example: {e}")
            continue
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 80)


def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("SEE-THINK-ACT AI AGENT - EXAMPLES")
    print("=" * 80)
    print("\nAvailable Examples:")
    print("  1. Open Notepad and type text")
    print("  2. Use Calculator")
    print("  3. Open File Explorer")
    print("  4. Open Web Browser")
    print("  5. Custom task")
    print("  6. Run all examples")
    print("  0. Exit")
    
    while True:
        print("\n" + "-" * 80)
        choice = input("\nSelect an example (0-6): ").strip()
        
        if choice == "0":
            print("\nGoodbye!")
            break
        elif choice == "1":
            example_1_simple_notepad()
        elif choice == "2":
            example_2_calculator()
        elif choice == "3":
            example_3_file_explorer()
        elif choice == "4":
            example_4_web_browser()
        elif choice == "5":
            example_5_custom_task()
        elif choice == "6":
            run_all_examples()
        else:
            print("\nInvalid choice. Please select 0-6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user. Goodbye!")
