import sys
from RAG.orchestrator_Agent import OrchestratorAgent

def main():
    # Initialize the OrchestratorAgent with the datasets folder
    datasets_folder = "parsed_docs"  # Path relative to project root
    orchestrator = OrchestratorAgent(datasets_folder)
    
    print("CloudStack Chatbot - Type your query or 'exit' to quit")
    print("=" * 50)
    
    while True:
        # Get user input from terminal
        user_query = input("\nEnter your query: ").strip()
        
        # Check for exit condition
        if user_query.lower() in ['exit', 'quit']:
            print("Exiting chatbot...")
            break
        
        if not user_query:
            print("Please enter a valid query.")
            continue
        
        # Process the query using the orchestrator
        try:
            print("\nProcessing your query...")
            response = orchestrator.process_request(user_query)
            
            print("\n" + "=" * 50)
            print("RESPONSE:")
            print("=" * 50)
            
            if response.get("success"):
                # Display the actual answer
                print(f"Answer: {response.get('answer', 'No answer provided')}")
                print(f"\nMetadata:")
                print(f"  - Dataset Used: {response.get('dataset_used', 'N/A')}")
                print(f"  - Resource Type: {response.get('resource_type', 'N/A')}")
                print(f"  - Confidence: {response.get('confidence', 'N/A')}")
            else:
                # Display error information
                print(f"❌ Error: {response.get('error', 'Unknown error occurred')}")
                
                # Show additional details if available
                if response.get('details'):
                    print(f"Details: {response['details']}")
                if response.get('understanding_result'):
                    print(f"Understanding Result: {response['understanding_result']}")
                    
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {str(e)}")
            print("Please try again with a different query.")

def show_available_datasets(orchestrator):
    """Helper function to show available datasets"""
    try:
        datasets_info = orchestrator.get_available_datasets()
        print(f"\nAvailable datasets in '{datasets_info['datasets_folder']}':")
        for dataset in datasets_info['datasets']:
            print(f"  - {dataset}")
    except Exception as e:
        print(f"Could not retrieve dataset information: {str(e)}")

if __name__ == "__main__":
    main()