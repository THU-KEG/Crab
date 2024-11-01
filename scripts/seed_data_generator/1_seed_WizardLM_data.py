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
        default="data/raw_data/WizardLM/WizardLM_evol_instruct_V2_143k.json",
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
    parser.add_argument("--output_file", type=str, default="1_wizardLM.json")
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
        # if i > 2:
        #     break
        # print("=========== Case ============", i)
        # print(vert)
        
        if vert["conversations"]==[]:
            continue
        try:
            input=vert["conversations"][0]["value"]
            output=vert["conversations"][1]["value"]
        except:
            print("=========== Case ============", i)
            print(vert)
            break
        # if len(output.split(" ")) < 300:
        #     continue
        # if len(output.split(" ")) > 300 or len(output.split(" ")) < 100:
        #     continue
        Dflag = (int)(random.random() > args.diverse_rate)
        if Dflag:
            if len(output.split(" ")) < args.min_length:
                continue
            if args.max_length != -1:
                if len(output.split(" ")) > args.max_length:
                    continue
            if len(input.split(" ")) > 70:
                continue
        

        unified_instance = {
            "id": i,
            "idx": vert["idx"],
            "messages": [
                {"role": "user", "content": input},
                {"role": "assistant", "content": output},
            ],
        }
        # print(unified_instance)
        total_in += len(input.split(" "))
        total_len += len(output.split(" "))
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
