import pandas as pd
def wide_to_long(data:list[dict],
                 id_vars:list[str],
                 var_name:str,
                 value_name:str)->pd.DataFrame:
    
    df = pd.DataFrame(data)
    return df.melt(id_vars=id_vars,var_name=var_name,value_name=value_name).reset_index(drop=True)

