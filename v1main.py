import zen
import os

def file_loader(key):
    with open(key, 'r') as f:
        return f.read()

engine = zen.ZenEngine({"loader": file_loader})

def run_evaluation(field_val, class_type_val):
    payload = {
        "field": field_val,
        "dataClassType": class_type_val
    }
    
    try:
        response = engine.evaluate("v1graph.json", payload)
        # Note: Your JSON output field is 'dateClassType'
        result = response.get("result", {}).get("dateClassType", "ERROR")
        print(response)
        print(f"[{field_val or 'None':^15}] | [{class_type_val or 'None':^15}] => Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(f"{'Field':^17} | {'dataClassType':^17} | Status")
    print("-" * 60)
    
    # Test cases
    run_evaluation("t_orders", "Confidential") # Rule 1: len > 0 (Passes through)
    run_evaluation("t_orders", "")             # Rule 2: startsWith t_
    run_evaluation("v_users", None)            # Rule 3: startsWith v_
    run_evaluation("social_name", "")          # Rule 4: Catch-all NA
