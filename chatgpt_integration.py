"""
ChatGPT Integration Module
Fallback layer untuk responses yang tidak cocok dengan patterns lokal
"""

import os
from pathlib import Path
from typing import Optional, List, Dict
import json
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class ChatGPTFallback:
    """Fallback ke ChatGPT untuk respons yang tidak cocok dengan patterns lokal"""
    
    def __init__(self, enable: bool = True, model: str = "gpt-3.5-turbo", max_history: int = 10):
        """
        Inisialisasi ChatGPT fallback
        
        Args:
            enable: Enable/disable ChatGPT fallback
            model: Model ChatGPT yang digunakan
            max_history: Jumlah conversation history untuk context
        """
        self.enable = enable
        self.model = model
        self.max_history = max_history
        self.client = None
        self.conversation_history = []
        self.history_file = Path("data") / "chatgpt_history.json"
        
        # Load API key dari .env atau environment
        self.api_key = self._load_api_key()
        
        if self.api_key and enable:
            try:
                if OpenAI is None:
                    print("⚠ OpenAI library not installed. Install with: pip install openai")
                    self.enable = False
                else:
                    self.client = OpenAI(api_key=self.api_key)
                    self._load_conversation_history()
                    print("✓ ChatGPT fallback initialized")
            except Exception as e:
                print(f"⚠ Failed to initialize ChatGPT: {e}")
                self.enable = False
        elif enable and not self.api_key:
            print("⚠ OpenAI API key not found in .env or environment")
            self.enable = False
    
    def _load_api_key(self) -> Optional[str]:
        """Load API key dari .env file atau environment variable"""
        from dotenv import load_dotenv
        
        # Load dari .env file
        try:
            env_path = Path(__file__).parent / ".env"
            load_dotenv(env_path)
        except Exception:
            pass
        
        # Try OS environment
        api_key = os.getenv("OPENAI_API_KEY")
        return api_key
    
    def _load_conversation_history(self):
        """Load conversation history dari file untuk context"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('history', [])[-self.max_history:]
        except Exception:
            self.conversation_history = []
    
    def _save_conversation_history(self):
        """Save conversation history ke file"""
        try:
            self.history_file.parent.mkdir(exist_ok=True)
            data = {
                'last_updated': datetime.now().isoformat(),
                'history': self.conversation_history[-self.max_history:]
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠ Failed to save history: {e}")
    
    def get_response(self, user_input: str, user_name: Optional[str] = None) -> Optional[str]:
        """
        Get response dari ChatGPT
        
        Args:
            user_input: Input dari user
            user_name: Nama user (untuk personalisasi)
        
        Returns:
            Response dari ChatGPT atau None jika failed
        """
        if not self.enable or not self.client:
            return None
        
        try:
            # Build system prompt
            system_prompt = self._build_system_prompt(user_name)
            
            # Build messages dengan history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history untuk context
            for hist_msg in self.conversation_history:
                messages.append({
                    "role": hist_msg.get("role"),
                    "content": hist_msg.get("content")
                })
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Call ChatGPT API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=300,
                timeout=10
            )
            
            # Extract response
            assistant_response = response.choices[0].message.content.strip()
            
            # Save to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            self._save_conversation_history()
            
            return assistant_response
        
        except Exception as e:
            print(f"⚠ ChatGPT error: {e}")
            return None
    
    def _build_system_prompt(self, user_name: Optional[str] = None) -> str:
        """Build system prompt untuk ChatGPT context"""
        prompt = """Anda adalah Mentis, asisten chatbot yang cerdas dan ramah. 
Anda membantu menjawab pertanyaan pengguna dalam bahasa Indonesia dengan jelas dan informatif.

Perilaku:
- Ramah dan sopan dalam setiap interaksi
- Jawab dengan singkat dan padat (max 3 paragraf)
- Jika tidak tahu, akui dengan jujur
- Hindari informasi sensitif atau berbahaya
- Gunakan emoji untuk membuat respons lebih menarik

Konteks:
- Ini adalah fallback response untuk pertanyaan yang tidak cocok dengan knowledge lokal
- User mungkin sudah bertanya ke vocabulary, Wikipedia, atau patterns sebelumnya
- Hindari mengulang informasi yang sudah diberikan"""
        
        if user_name:
            prompt += f"\n- Nama user: {user_name}"
        
        return prompt
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        try:
            if self.history_file.exists():
                self.history_file.unlink()
        except Exception:
            pass
    
    def get_stats(self) -> Dict:
        """Get statistics tentang ChatGPT fallback"""
        return {
            'enabled': self.enable,
            'model': self.model,
            'history_length': len(self.conversation_history),
            'api_key_set': bool(self.api_key),
            'history_file': str(self.history_file)
        }
