import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument(
        "--input_file",
        type=str,
        default="data/raw_data/oasst2/2023-11-05_oasst2_ready.messages.jsonl",
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
    parser.add_argument("--output_dir", type=str, default="data/seed_data/fewshot")
    parser.add_argument("--output_file", type=str, default="1_oasst2.json")
    args = parser.parse_args()

    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    data = []
    with open(args.input_file, "r", encoding="utf-8") as reader:
        for item in jsonlines.Reader(reader):
            data.append(item)

    out_file = open(output_file, "w")

    unified_data = []
    Flag = -1
    user = dict()
    total_len = 0
    total_in = 0
    for i, vert in enumerate(data):
        # if i > 10:
        #     break
        # print("=========== Case ============", i)
        # print(vert)
        if vert["parent_id"] == None:
            # if vert["lang"] == "en":
            user = vert
            Flag = i
        

        if Flag != -1:
            if (
                vert["role"] == "assistant"
                and vert["parent_id"] == user["message_id"]
                and vert["rank"] == 0
            ):
                Dflag = (int)(random.random() > args.diverse_rate)
                if Dflag:
                    if len(vert["text"].split(" ")) < args.min_length:
                        continue
                    if args.max_length != -1:
                        if len(vert["text"].split(" ")) > args.max_length:
                            continue
                
                unified_instance = {
                    "id": Flag,
                    "user_id": user["message_id"],
                    "assistant_id": vert["message_id"],
                    "messages": [
                        {"role": "user", "content": user["text"]},
                        {"role": "assistant", "content": vert["text"]},
                    ],
                    # "request": {
                    #     "result": {"success": False, "completions": ""},
                    # },
                }
                total_in += len(user["text"].split(" "))
                total_len += len(vert["text"].split(" "))
                unified_data.append(unified_instance)

                Flag = -1
                user.clear()
                # out_file.write(json.dumps(unified_instance) + "\n")

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