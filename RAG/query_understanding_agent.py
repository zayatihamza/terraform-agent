# query_understanding_agent.py
from typing import Dict, Any
import os
import requests
from .base_agent import BaseAgent

class QueryUnderstandingAgent(BaseAgent):
    def __init__(self, datasets_folder: str):
        super().__init__(datasets_folder)
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "mistral"
    
    def understand_query(self, user_query: str) -> Dict[str, Any]:
        """Parse user query and determine which dataset to use"""
        # Get all JSON file names from parsed_docs folder
        json_files = self._get_json_filenames()
        
        # Create prompt for Mistral
        prompt = self._create_mistral_prompt(user_query, json_files)
        
        # Send to Ollama Mistral
        mistral_response = self._query_ollama_mistral(prompt)
        
        return mistral_response
    
    def _get_json_filenames(self) -> list:
        """Get all JSON file names from the datasets folder"""
        json_files = []
        if os.path.exists(self.datasets_folder):
            for file in os.listdir(self.datasets_folder):
                if file.endswith('.json'):
                    json_files.append(file)
        return json_files
    
    def _create_mistral_prompt(self, user_query: str, json_files: list) -> str:
        """Create prompt for Mistral to understand query and match dataset"""
        prompt = f"""
You are a CloudStack resource expert. Analyze the user query and determine which JSON dataset contains the answer.

User Query: "{user_query}"

Available JSON datasets in the folder:
{chr(10).join([f"- {file}" for file in json_files])}

Based on the user's request, determine:
1. Which JSON file likely contains the information to answer this query
2. What type of CloudStack resource the user wants

Return your response in this exact JSON format:
{{
    "dataset_file": "exact_filename.json",
    "resource_type": "cloudstack_resource_name", 
    "confidence": "high/medium/low"
}}
"""
        return prompt
    
    def _query_ollama_mistral(self, prompt: str) -> Dict[str, Any]:
        """Send prompt to local Ollama Mistral"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result.get("response", "")
            
            # Parse JSON response from Mistral
            import json
            return json.loads(content)
            
        except Exception as e:
            return {
                "error": f"Ollama Mistral error: {str(e)}",
                "dataset_file": None,
                "resource_type": None
            }
    
    def extract_intent(self, query: str) -> str:
        """Extract the main intent/resource type from query"""
        # TODO: Keep for later use if needed
        pass
    
    def extract_properties(self, query: str) -> Dict[str, Any]:
        """Extract mentioned properties from the query"""
        # TODO: Keep for later use if needed  
        pass