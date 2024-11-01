import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
from utils import Generate_Refined_Instruction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument(
        "--input_file",
        type=str,
        default="data/seed_data/fewshot/1_wizardLM.json",
    )
    parser.add_argument(
        "--num_sample",
        type=int,
        default=3000,
    )
    parser.add_argument("--output_dir", type=str, default="data/seed_data/fewshot")
    parser.add_argument("--output_file", type=str, default="2_wizardLM_llama_format_3000.json")
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
        if i > args.num_sample:
            break
        unified_instance = copy.deepcopy(vert)
        prompt = Generate_Refined_Instruction.format(
            Response=vert["messages"][1]["content"],
            Instruction=vert["messages"][0]["content"],
        )
        unified_instance["messages"] = [
            {
                "role": "system",
                "content": "You are a helpful and instruction-following linguist with expertise in contextual language nuances.",
            },
            {"role": "user", "content": prompt},
        ]
        unified_instance["request"] = {
            "result": {"success": False, "completions": ""},
        }

        unified_data.append(unified_instance)
        # out_file.write(json.dumps(unified_instance) + "\n")

    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    out_file.close()
    print("total_number:", len(unified_data))
