# base_agent.py
import json
import os
from typing import Dict, List, Any
from pathlib import Path

class BaseAgent:
    def __init__(self, datasets_folder: str):
        self.datasets_folder = Path(datasets_folder)
        self.datasets = self._load_datasets()
    
    def _load_datasets(self) -> Dict[str, Any]:
        """Load all JSON datasets from folder"""
        datasets = {}
        
        if not self.datasets_folder.exists():
            print(f"Warning: Datasets folder {self.datasets_folder} does not exist")
            return datasets
        
        try:
            for file_path in self.datasets_folder.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        datasets[file_path.name] = json.load(f)
                except Exception as e:
                    print(f"Error loading {file_path.name}: {str(e)}")
                    
        except Exception as e:
            print(f"Error scanning datasets folder: {str(e)}")
        
        return datasets
    
    def search_dataset(self, dataset_name: str) -> Dict[str, Any]:
        """Find specific dataset by name"""
        if dataset_name in self.datasets:
            return self.datasets[dataset_name]
        
        # Try with different extensions if exact match not found
        if not dataset_name.endswith('.json'):
            json_name = f"{dataset_name}.json"
            if json_name in self.datasets:
                return self.datasets[json_name]
        
        return None
    
    def get_dataset_names(self) -> List[str]:
        """Get list of all available dataset names"""
        return list(self.datasets.keys())
    
    def reload_datasets(self) -> None:
        """Reload all datasets from folder"""
        self.datasets = self._load_datasets()