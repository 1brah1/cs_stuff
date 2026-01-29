import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Mock httpx before import
mock_httpx = MagicMock()
class MockHTTPStatusError(Exception):
    def __init__(self, message, request=None, response=None):
        self.response = response
        super().__init__(message)
mock_httpx.HTTPStatusError = MockHTTPStatusError
sys.modules["httpx"] = mock_httpx

# Mock pydantic_settings
mock_pydantic = MagicMock()
sys.modules["pydantic_settings"] = mock_pydantic

# Mock app.core.config
mock_config = MagicMock()
sys.modules["app.core.config"] = mock_config
mock_config.settings = MagicMock()
mock_config.settings.OPENROUTER_API_KEY = "test_key"

# Now import service
from app.services.openrouter_service import OpenRouterService

async def test_service():
    print("Testing OpenRouterService...")
    
    service = OpenRouterService()
    
    # Setup mock for httpx.AsyncClient
    mock_client_instance = AsyncMock()
    mock_httpx.AsyncClient.return_value.__aenter__.return_value = mock_client_instance
    
    # Mock response
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {"message": {"content": "Test response"}}
        ]
    }
    mock_client_instance.post.return_value = mock_response
    
    # Test generate_response
    print("\nTesting generate_response...")
    response = await service.generate_response("Hello")
    print(f"Response: {response}")
    assert response == "Test response"
    print("✅ generate_response passed")
    
    # Verify call arguments
    call_args = mock_client_instance.post.call_args
    # call_args[1] is kwargs
    assert call_args[1]['json']['messages'][0]['content'] == "Hello"
    
    # Test review_document
    print("\nTesting review_document...")
    response = await service.review_document("Doc content")
    print(f"Response: {response}")
    assert response == "Test response"
    print("✅ review_document passed")
    
    # Verify call arguments for review
    call_args = mock_client_instance.post.call_args
    assert "Please review the following document" in call_args[1]['json']['messages'][0]['content']

if __name__ == "__main__":
    asyncio.run(test_service())
