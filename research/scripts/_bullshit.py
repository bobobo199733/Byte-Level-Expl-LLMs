import pandas as pd
import opcode

df = pd.read_csv("../test_data/features/processed_bytecode_features.csv")
file ="t41_p1_r2_mistral.py"
# find the row for t41_p1_r1_llama
row = df[df["file_name"] == file].iloc[0]

val = int(row["byte_68"])  # byte_68 is the opcode, byte_69 is the arg
print(f"Analyzing file: {file}")
print(f"byte_68 opname: {opcode.opname[val]}")
print(f"byte_69 raw:    {int(row['byte_69'])}")
