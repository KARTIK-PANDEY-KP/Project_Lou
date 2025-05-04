import os
import json

def main():
    # Try different directories
    test_dirs = [
        ".",
        os.path.expanduser("~"),
        os.path.dirname(os.path.abspath(__file__))
    ]
    
    test_data = {"test": "data"}
    
    print("Current working directory:", os.getcwd())
    print("\nTrying to write test files:")
    
    for d in test_dirs:
        try:
            full_path = os.path.join(d, "test_oauth.json")
            print(f"\nTrying to write to: {full_path}")
            with open(full_path, "w") as f:
                json.dump(test_data, f)
            print("Success!")
            # Clean up
            os.remove(full_path)
        except Exception as e:
            print(f"Failed: {str(e)}")

if __name__ == "__main__":
    main() 