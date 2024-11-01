import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
from utils import Constraints_Check

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument(
        "--input_file",
        type=str,
        default="data/seed_data/Long_data/3_oasst2_constraints.json",
    )
    parser.add_argument("--output_dir", type=str, default="data/seed_data/Long_data")
    parser.add_argument("--output_file", type=str, default="4_oasst2_check_constraints.json")
    args = parser.parse_args()

    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    with open(args.input_file, "r", encoding="utf-8") as reader:
        data = json.load(reader)
        reader.close()

    out_file = open(output_file, "w")

    unified_data = []
    for i, vert in enumerate(data):
        for key,value in vert["Aug_instruction"]["Additional_Instruction"].items():
            unified_instance = copy.deepcopy(vert)
            prompt = Constraints_Check.format(
                c=value,
                text=vert["messages"][1]["content"],
            )
            unified_instance["messages"] = [
                {"role": "user", "content": prompt},
            ]
            unified_instance["request"] = {
                "result": {"success": False, "completions": ""},
            }
            unified_instance["Constraints_Type"]=key


            unified_data.append(unified_instance)
        # out_file.write(json.dumps(unified_instance) + "\n")

    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    out_file.close()
    print("total_number:", len(unified_data))
