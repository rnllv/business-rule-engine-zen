import zen
import os
#import pdb

def file_loader(file_name: str):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    print(f"File path: {file_path}")
    if not os.path.exists(file_path):
       raise FileNotFoundError("File not found")
    with open(file_path, "r") as f:
        return f.read()

engine = zen.ZenEngine()
decision = engine.create_decision(file_loader("v1graph2.json"))

#lookup vars
lkp_clmn_data = {"T_TEST": {"pii": "yes", "wi": "no"}}

def run_evaluation(payload: dict):
    try:
        updated_payload = {"data": payload} | {"lkp_clmn_data": lkp_clmn_data}
        print(f"Updated payload: {updated_payload}")
        response = decision.evaluate(updated_payload, {"trace": True})
        #print(f"Full response: {response}")
        #pdb.set_trace()
        # Note: Your JSON output field is 'd_cls_out'
        result = response.get("result", {})
        print(f"Evaluated result: {result}")

        for match_attrbt, match_val in result.items():
            tgt_key = match_attrbt.replace("_out", "")
            # match key in input_data and update val
            if tgt_key in payload:
                payload[tgt_key] = match_val

        print(f"Final result: {payload}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    
    # Test
    #input_data = {"d_cls": "  ", "ds_type": "tbl1", "pii": "social"}
    #missing input field is considered as null
    input_data = {"tbl": "T_TEST", "d_cls": " ", "ds_type": "", "pii": ""}
    print(f"Input data: {input_data}")
    print("-" * 60)
    run_evaluation(input_data)
