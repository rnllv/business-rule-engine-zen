import zen
import json

def file_loader(key):
    with open(key, 'r') as f:
        return f.read()

engine = zen.ZenEngine({"loader": file_loader})

def run_batch_evaluation():
    # We wrap our items in a "rows" key as defined in the JSON's inputField
    payload = {
        "rows": [
            {"field": "t_social_security", "dataClassType": "Confidential"},
            {"field": "v_user_list", "dataClassType": ""},
            {"field": "account_name", "dataClassType": None}
        ]
    }
    
    try:
        response = engine.evaluate("graph.json", payload)
        result = response.get("result", {})
        
        # In Loop Mode, these are now lists!
        classes = result.get("classifications", [])
        pii_checks = result.get("pii_results", [])
        
        print(f"{'Field':<20} | {'Class':<15} | {'Is PII'}")
        print("-" * 50)
        
        for i in range(len(payload["rows"])):
            field_name = payload["rows"][i]["field"]
            cls = classes[i].get("dateClassType")
            pii = pii_checks[i].get("isPii")
            print(f"{field_name:<20} | {cls:<15} | {pii}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_batch_evaluation()
