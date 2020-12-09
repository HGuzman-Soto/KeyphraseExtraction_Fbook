import json
import pandas as pd
import ast

# with open('fbook_data.json') as f:
#     df = pd.read_json(f)

# df.to_csv("fbook_data.csv", index=False)


df = pd.read_csv('fbook_data.csv')
df["Post"] = ""
df["threads"] = ""
for row in range(len(df)):
    data = df['json_obj'][row]
    test = ast.literal_eval(data)
    df["threads"][row] = " ".join(test["comments"])

    try:
        df["Post"][row] = " ".join(test["post"])
    except:
        df["Post"][row] = ""

df.to_csv("fbook_data.csv", index=False)
