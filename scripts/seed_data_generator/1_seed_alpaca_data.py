import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
import random

def sort_key(item):
    source_priority = {
        "gpt4": 1,
        "text-davinci-003": 2,
        "icm-1.3b": 3
    }
    return (-item["score"], source_priority[item["source"]])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument(
        "--input_file",
        type=str,
        default="data/raw_data/GPT-4-LLM-main/data/comparison_data_v2.json",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=36,
    )
    parser.add_argument(
        "--min_length",
        type=int,
        default=300,
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=-1,
    )
    parser.add_argument(
        "--diverse_rate",
        type=float,
        default=0.1,
    )
    parser.add_argument("--output_dir", type=str, default="data/seed_data/fewshot_Short")
    parser.add_argument("--output_file", type=str, default="1_alpaca.json")
    args = parser.parse_args()

    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    
    with open(args.input_file, "r", encoding="utf-8") as reader:
        data = json.load(reader)
        reader.close()

    # print(len(data))
    
    out_file = open(output_file, "w")

    unified_data = []
    total_len = 0
    total_in = 0 
    for i, vert in enumerate(data):
        # if i > 10:
        #     break
        # print("=========== Case ============", i)
        sorted_responses = sorted(vert["responses_and_scores"], key=sort_key)
        
        if sorted_responses[0]["score"] < 9.0:
            continue
        # if len(sorted_responses[0]["response"].split(" ")) < 300:
        #     continue
        # if len(sorted_responses[0]["response"].split(" ")) > 300 or len(sorted_responses[0]["response"].split(" ")) < 100:
        #     continue
        Dflag = (int)(random.random() > args.diverse_rate)
        if Dflag:
            if len(sorted_responses[0]["response"].split(" ")) < args.min_length:
                continue
            if args.max_length != -1:
                if len(sorted_responses[0]["response"].split(" ")) > args.max_length:
                    continue
        try:
            input = vert["user_input"].split("Instruction:\n")[1]
        except:
            input = vert["user_input"]
        unified_instance = {
            "id": i,
            "score": sorted_responses[0]["score"],
            "source": sorted_responses[0]["source"],
            "messages": [
                {"role": "user", "content": input},
                {"role": "assistant", "content": sorted_responses[0]["response"]},
            ],
        }
        # print(unified_instance)
        total_in += len(vert["user_input"].split(" "))
        total_len += len(sorted_responses[0]["response"].split(" "))
        unified_data.append(unified_instance)
    
    random.seed(args.seed)
    random.shuffle(unified_data)
    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    out_file.close()
    print("total_number:", len(unified_data))
    print("avg_len_input:",total_in/len(unified_data))
    print("avg_len_output:",total_len/len(unified_data))
