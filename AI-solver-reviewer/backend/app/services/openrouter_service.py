import httpx
from app.core.config import settings
from typing import Dict, Any


class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-chat"
    
    async def _call_api(self, messages: list[Dict[str, Any]], temperature: float = 0.7) -> str:
        """
        Internal method to call OpenRouter API
        """
        if not self.api_key:
            raise Exception("OpenRouter API key is not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/1brah1/cs_stuff",
            "X-Title": "AI Document Reviewer"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                elif "error" in data:
                    raise Exception(f"OpenRouter error: {data['error'].get('message', 'Unknown error')}")
                else:
                    raise Exception("No response from AI model")
                    
            except httpx.HTTPStatusError as e:
                error_msg = f"HTTP error: {e.response.status_code}"
                try:
                    error_data = e.response.json()
                    if "error" in error_data and "message" in error_data["error"]:
                        error_msg += f" - {error_data['error']['message']}"
                except:
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
