# retrieval_agent.py
from typing import Dict, Any, List
import json
import os
import requests
from .base_agent import BaseAgent

class RetrievalAgent(BaseAgent):
    def __init__(self, datasets_folder: str):
        super().__init__(datasets_folder)
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "mistral"
    
    def retrieve_answer(self, dataset_file: str, user_query: str, resource_type: str) -> Dict[str, Any]:
        """
        Retrieve answer from the specified dataset file based on user query
        
        Args:
            dataset_file: Name of the JSON file to search
            user_query: Original user question
            resource_type: Type of CloudStack resource
            
        Returns:
            Dict containing the answer and metadata
        """
        try:
            # Load the specific dataset
            dataset_content = self._load_dataset_file(dataset_file)
            
            if not dataset_content:
                return {
                    "error": f"Could not load dataset file: {dataset_file}",
                    "answer": None
                }
            
            # Use Mistral to find and format the answer from the dataset
            answer = self._query_dataset_with_mistral(dataset_content, user_query, resource_type)
            
            return {
                "answer": answer,
                "dataset_used": dataset_file,
                "resource_type": resource_type,
                "success": True
            }
            
        except Exception as e:
            return {
                "error": f"Retrieval error: {str(e)}",
                "answer": None,
                "success": False
            }
    
    def _load_dataset_file(self, filename: str) -> Dict[str, Any]:
        """Load specific JSON dataset file"""
        file_path = os.path.join(self.datasets_folder, filename)
        
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            return None
    
    def _query_dataset_with_mistral(self, dataset: Dict[str, Any], user_query: str, resource_type: str) -> str:
        """Use Mistral to extract relevant information from dataset"""
        
        # Convert dataset to a readable format for the prompt
        dataset_text = json.dumps(dataset, indent=2)
        
        prompt = f"""
You are a CloudStack expert assistant. Use the provided dataset to answer the user's question accurately.

User Question: "{user_query}"
Resource Type: "{resource_type}"

Dataset Content:
{dataset_text}

Instructions:
1. Search through the dataset for information relevant to the user's question
2. Provide a clear, comprehensive answer based ONLY on the information in the dataset
3. If the dataset contains specific examples, include them in your response
4. If the information is not found in the dataset, clearly state that
5. Format your response in a user-friendly way

Answer:"""

        return self._query_ollama_mistral(prompt)
    
    def _query_ollama_mistral(self, prompt: str) -> str:
        """Send prompt to local Ollama Mistral and get response"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "Sorry, I couldn't generate an answer.")
            
        except Exception as e:
            return f"Error querying Mistral: {str(e)}"
    
    def _format_response(self, raw_answer: str, dataset_file: str) -> Dict[str, Any]:
        """Format the final response with metadata"""
        return {
            "answer": raw_answer,
            "source": f"Dataset: {dataset_file}",
            "timestamp": "2025-07-25",  # You might want to use actual timestamp
            "success": True
        }