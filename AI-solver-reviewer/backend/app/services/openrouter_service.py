import httpx
from app.core.config import settings
from typing import Dict, Any


class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-r1:free"
    
    async def review_document(self, content: str) -> str:
        """
        Send document content to DeepSeek R1T2 for review via OpenRouter
        """
        prompt = f"""Please review the following document and provide comprehensive feedback. 
        
Focus on:
1. Content quality and clarity
2. Grammar and spelling
3. Structure and organization
4. Suggestions for improvement
5. Overall assessment

Document Content:
{content}

Please provide a detailed review with actionable feedback."""
        return await self._call_openrouter(prompt)

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response for chat interactions
        """
        return await self._call_openrouter(prompt)

    async def _call_openrouter(self, prompt: str) -> str:
        """
        Internal method to make the API call
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/ai-solver-reviewer",
            "X-Title": "AI Document Reviewer"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                # Extract the review text from the response
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    raise Exception("No response from AI model")
                    
            except httpx.HTTPStatusError as e:
                error_msg = f"HTTP error: {e.response.status_code}"
                if e.response.text:
                    error_msg += f" - {e.response.text}"
                raise Exception(error_msg)
            except Exception as e:
                raise Exception(f"Error calling OpenRouter API: {str(e)}")

    async def generate_response(self, content: str) -> str:
        """
        Generate a general chat response
        """
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]
        return await self._call_api(messages)

    async def review_document(self, content: str) -> str:
        """
        Send document content to DeepSeek R1T2 for review via OpenRouter
        """
        prompt = f"""Please review the following document and provide comprehensive feedback. 
        
Focus on:
1. Content quality and clarity
2. Grammar and spelling
3. Structure and organization
4. Suggestions for improvement
5. Overall assessment

Document Content:
{content}

Please provide a detailed review with actionable feedback."""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        return await self._call_api(messages)






