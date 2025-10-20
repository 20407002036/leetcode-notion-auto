import re
# from Models.LeetMdl import LeetMdl  # TODO: Fix import path

def parse_leet_data_from_extracted_text(file_text):
    # More flexible patterns
    leet_no_re = re.compile(r'no\.?\s*(\d+)', flags=re.IGNORECASE)
    leet_func_name_re = re.compile(r'def\s+([A-Za-z_]\w*)', flags=re.IGNORECASE)
    
    try:
        no_match = leet_no_re.search(file_text)
        fn_match = leet_func_name_re.search(file_text)
        
        if not no_match:
            raise ValueError("Leet number not found")
        if not fn_match:
            raise ValueError("Function name not found")
        
        int_leetNo = int(no_match.group(1))  # Use captured group
        leetFuncName = fn_match.group(1)     # Use captured group
        
        # Create and save the model
        # TODO: Uncomment when Models are available
        # leet_mdl = LeetMdl(int_leetNo, leetFuncName)
        # leet_mdl.save_leet()
        
        return int_leetNo
    except Exception as e:
        print(f"Exception: {e}")
        return None