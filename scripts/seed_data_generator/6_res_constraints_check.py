import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
import re
import random


def get_score(text):
    match = re.search(r'Score: (\d+)', text)
    if match:
        return int(match.group(1))
    else:
        return -1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument("--dataset", type=str, default= "")
    parser.add_argument("--original_file", type=str, default="data/seed_data/Long_data/4_alpaca_filter.json")
    parser.add_argument("--input_file", type=str, default="data/seed_data/Long_data/4_alpaca_constraints_check.json")
    parser.add_argument("--output_dir", type=str, default="data/seed_data/Long_data")
    parser.add_argument("--output_file", type=str, default="5_alpaca_constraints.json")
    parser.add_argument("--threshold", type=float, default=0.9)
    args = parser.parse_args()

    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    with open(args.original_file, "r", encoding="utf-8") as reader:
        ori_data = json.load(reader)
        reader.close()

    with open(args.input_file, "r", encoding="utf-8") as reader:
        data = json.load(reader)
        reader.close()


    unified_data = []
    unified_instance = copy.deepcopy(ori_data[0])
    cnt = -1
    count_score = dict()
    Final_count = dict()
    ori_id = 0
    data_id = 0
    for i, vert in enumerate(data):
        assert data_id >= i, print(data_id, i, ori_id, vert["id"], ori_data[ori_id]["id"])
        if data_id != i:
            continue
        if vert["id"] != ori_data[ori_id]["id"]:
            ori_id += 1
            unified_instance["source"] = args.dataset
            unified_data.append(unified_instance)
            for key in unified_instance["Aug_instruction"]["Additional_Instruction"].keys():
                if key not in Final_count:
                    Final_count[key] = 0
                Final_count[key] += 1
            unified_instance = copy.deepcopy(ori_data[ori_id])
        
        if vert["id"] != ori_data[ori_id]["id"]:
            # print("==========")
            # print(data_id, i, ori_id)
            # print(vert["id"], ori_data[ori_id]["id"])
            while data[data_id]["id"] != ori_data[ori_id]["id"]:
                data_id += 1
            continue

        # assert vert["id"] == ori_data[ori_id]["id"]

        data_id += 1
        if vert["request"]["result"]["completions"] == "No":
            if vert["Constraints_Type"] == "Digit" or vert["Constraints_Type"] == "Keyword" or vert["Constraints_Type"] == "Punctuation":
                continue
            Dflag = (int)(random.random() < args.threshold)
            if Dflag:
                continue
            if vert["Constraints_Type"] in unified_instance["Aug_instruction"]["Additional_Instruction"]:
                del unified_instance["Aug_instruction"]["Additional_Instruction"][vert["Constraints_Type"]]
            if vert["Constraints_Type"] not in count_score:
                count_score[vert["Constraints_Type"]] = 0
            count_score[vert["Constraints_Type"]] += 1
        

    out_file = open(output_file, "w", encoding="utf-8")
    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    out_file.close()

    count_score = sorted(count_score.items(), key=lambda item: item[1], reverse=True)
    Final_count = sorted(Final_count.items(), key=lambda item: item[1], reverse=True)

    print("total_number:", len(unified_data))
    print("delete count_score:", count_score)
    print("final count_score:",Final_count)