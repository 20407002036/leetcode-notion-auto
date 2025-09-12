import re
from Models.LeetMdl import LeetMdl

def parse_leet_data_from_extracted_text(file_text):
    leet_no_re = re.compile(r'no. ?\d{4}', flags=re.IGNORECASE)
    leet_func_name = re.compile(r'def [a-z]+', flags=re.IGNORECASE)
    try:
        leetNo = leet_no_re.search(file_text).group()
        leetFuncName = leet_func_name.search(file_text).group()

        if type(leetNo) == str and type(leetFuncName) == str:
            int_leetNo = leetNo.split(".")[-1]
            leetFuncName = leetFuncName.split(" ")[-1]
            print(int(int_leetNo), leetFuncName)
            leet_mdl = LeetMdl(int_leetNo, leetFuncName)
            leet_mdl.save_leet()
    except Exception as e:
        print(f"Exception: {e}")