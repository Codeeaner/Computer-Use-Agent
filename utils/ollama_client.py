"""
Ollama client for Qwen3-VL model with function calling support
"""
import ollama
import json
import base64
from typing import List, Dict, Any, Optional
from PIL import Image
import io


class OllamaVisionClient:
    """Client for interacting with Qwen3-VL via Ollama"""
    
    def __init__(self, model: str = "qwen3-vl:235b-cloud"):
        """
        Initialize Ollama client
        
        Args:
            model: Model name to use (default: qwen3-vl:235b-cloud)
        """
        self.model = model
        self.client = ollama
        
    def encode_image_to_base64(self, image: Image.Image, format: str = 'PNG') -> str:
        """
        Encode PIL Image to base64 string
        
        Args:
            image: PIL Image object
            format: Image format (PNG, JPEG, etc.)
            
        Returns:
            Base64 encoded string
        """
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')
    
    def chat(self, 
             messages: List[Dict[str, Any]], 
             stream: bool = False,
             tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Send chat request to Ollama with vision support
        
        Args:
            messages: List of message dictionaries
            stream: Whether to stream the response
            tools: Optional list of tool definitions for function calling
            
        Returns:
            Response dictionary from Ollama
        """
        try:
            # Prepare the request
            request_params = {
                'model': self.model,
                'messages': messages,
                'stream': stream
            }
            
            # Add tools if provided
            if tools:
                request_params['tools'] = tools
            
            # Make the request
            response = self.client.chat(**request_params)
            
            return response
            
        except Exception as e:
            print(f"Error in Ollama chat: {e}")
            raise
    
    def chat_with_image(self,
                       user_query: str,
                       image: Image.Image,
                       system_prompt: Optional[str] = None,
                       tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Chat with image input
        
        Args:
            user_query: User's text query
            image: PIL Image object
            system_prompt: Optional system prompt
            tools: Optional list of tool definitions
            
        Returns:
            Response from the model
        """
        # Build messages
        messages = []
        
        # Add system message if provided
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        
        # Encode image to base64
        image_base64 = self.encode_image_to_base64(image, format='PNG')
        
        # Add user message with image
        messages.append({
            'role': 'user',
            'content': user_query,
            'images': [image_base64]
        })
        
        # Make the request
        response = self.chat(messages=messages, tools=tools)
        
        return response
    
    def extract_tool_calls(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract tool calls from model response
        
        Args:
            response: Response from Ollama
            
        Returns:
            List of tool call dictionaries
        """
        tool_calls = []
        
        if 'message' in response:
            message = response['message']
            
            # Check for tool_calls in the message
            if 'tool_calls' in message:
                tool_calls = message['tool_calls']
        
        return tool_calls
    
    def parse_computer_use_action(self, response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse computer use action from model response
        
        Args:
            response: Response from Ollama
            
        Returns:
            Parsed action dictionary or None
        """
        # Try to extract tool calls
        tool_calls = self.extract_tool_calls(response)
        
        if tool_calls:
            return tool_calls[0]
        
        # Fallback: try to parse from content
        if 'message' in response and 'content' in response['message']:
            content = response['message']['content']
            
            # Look for tool_call markers
            if '<tool_call>' in content and '</tool_call>' in content:
                try:
                    json_str = content.split('<tool_call>')[1].split('</tool_call>')[0].strip()
                    action = json.loads(json_str)
                    return action
                except (json.JSONDecodeError, IndexError) as e:
                    print(f"Error parsing tool call: {e}")
        
        return None
    
    def test_connection(self) -> bool:
        """
        Test connection to Ollama and model availability
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to list models
            models = self.client.list()
            
            # Check if our model is available
            model_names = [m['name'] for m in models.get('models', [])]
            
            if self.model in model_names or any(self.model in name for name in model_names):
                print(f"✓ Model '{self.model}' is available")
                return True
            else:
                print(f"✗ Model '{self.model}' not found")
                print(f"Available models: {model_names}")
                return False
                
        except Exception as e:
            print(f"✗ Error connecting to Ollama: {e}")
            return False


if __name__ == "__main__":
    # Test the Ollama client
    client = OllamaVisionClient()
    
    print("Testing Ollama connection...")
    if client.test_connection():
        print("\n✓ Ollama client initialized successfully")
    else:
        print("\n✗ Failed to initialize Ollama client")
        print("Make sure Ollama is running and the model is pulled:")
        print("  ollama run qwen3-vl:235b-cloud")
