import zen
import os
import json
 
# 1. Define our 'Rules' in JDM format (JSON Decision Model)
# This would normally be in a file like 'pii_rules.json'
pii_graph = {
    "contentType": "application/vnd.gorules.decision",
    "nodes": [
    {
        "id": "input_node",
        "type": "inputNode",
        "name": "Request",
        "position": {"x": 0, "y": 0}
    },
    {
        "id": "pii_table",
        "type": "decisionTableNode",
        "name": "PII Detector",
        "position": {"x": 300, "y": 0},
        "content": {
        "hitPolicy": "first",
        "inputs": [
    {
        "id": "c1",
        "name": "Field Name",
        "field": "fieldName"
    }
    ],
    "outputs": [
    {
    "id": "c2",
    "name": "Is PII",
    "field": "isPII"
    }
    ],
    "rules": [
    {
    "_id": "r1",
    "c1": "contains(lower($), \"social\")",
    "c2": "[\"func1\", \"func2\"]"
    },
    {
    "_id": "r2",
    "c1": "contains(lower($), \"credit\")",
    "c2": "true"
    },
    {
    "_id": "r3",
    "c1": "", # Catch-all (anything else)
    "c2": "false"
    }
    ]
    }
    },
    {
    "id": "output_node",
    "type": "outputNode",
    "name": "Response",
    "position": {"x": 600, "y": 0}
    }
    ],
    "edges": [
    {"id": "e1", "sourceId": "input_node", "targetId": "pii_table"},
    {"id": "e2", "sourceId": "pii_table", "targetId": "output_node"}
    ]
}
 
# 2. Setup the Multi-Rule Loader
# This function simulates fetching different rule sets based on a key
def my_loader(key: str):
    print(f"--- Engine is loading: {key} ---")
    if key == "pii_rules.json":
        return json.dumps(pii_graph)
    raise FileNotFoundError(f"Rule {key} not found")

def file_loader(file_name: str):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    print(f"File path: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")
    with open(file_path, "r") as f:
        return f.read()
 
# 3. Initialize the Zen Engine
#engine = zen.ZenEngine({"loader": my_loader})
engine = zen.ZenEngine()
decision = engine.create_decision(file_loader("pii_rules.json"))
# 4. Evaluation Function
def check_field(name):
    #input_data = {"fieldName": name}
    # result returns the output of the 'outputNode'
    result = decision.evaluate(input_data)
    return result
 
# 5. Run Tests
#test_cases = ["Social Security", "CREDIT card number", "Username", "socially awkward"]
input_data = {"data_cls": "social", "ds_ty": "tbl1", "pii": ""}
print(f"Input data: {input_data}")
print("Evaluation Results:")
 
#for test in test_cases:
#    res = check_field(test)
#    print(f"Input: '{test}' -> Result: {res}")
result = check_field(input_data)
print(f"Result: {result}")
