# orchestrator_agent.py
from typing import Dict, Any
from .base_agent import BaseAgent
from .query_understanding_agent import QueryUnderstandingAgent
from .retrieval_agent import RetrievalAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self, datasets_folder: str):
        super().__init__(datasets_folder)
        self.query_agent = QueryUnderstandingAgent(datasets_folder)
        self.retrieval_agent = RetrievalAgent(datasets_folder)
    
    def process_request(self, user_query: str) -> Dict[str, Any]:
        """Main orchestration method - complete pipeline"""
        try:
            # Step 1: Understand the query
            understood_query = self.query_agent.understand_query(user_query)
            
            # Check if query understanding failed
            if "error" in understood_query:
                return {
                    "error": "Failed to understand query",
                    "details": understood_query["error"],
                    "success": False
                }
            
            # Step 2: Extract information from understanding result
            dataset_file = understood_query.get("dataset_file")
            resource_type = understood_query.get("resource_type")
            confidence = understood_query.get("confidence", "unknown")
            
            if not dataset_file:
                return {
                    "error": "Could not determine which dataset to use",
                    "understanding_result": understood_query,
                    "success": False
                }
            
            # Step 3: Retrieve the answer using the retrieval agent
            retrieval_result = self.retrieval_agent.retrieve_answer(
                dataset_file=dataset_file,
                user_query=user_query,
                resource_type=resource_type
            )
            
            # Step 4: Return complete result with metadata
            return {
                "answer": retrieval_result.get("answer"),
                "dataset_used": dataset_file,
                "resource_type": resource_type,
                "confidence": confidence,
                "success": retrieval_result.get("success", False),
                "error": retrieval_result.get("error") if "error" in retrieval_result else None
            }
            
        except Exception as e:
            return {
                "error": f"Orchestration error: {str(e)}",
                "success": False
            }
    
    def get_available_datasets(self) -> Dict[str, Any]:
        """Get list of available datasets for debugging"""
        return {
            "datasets": self.query_agent._get_json_filenames(),
            "datasets_folder": str(self.datasets_folder)
        }