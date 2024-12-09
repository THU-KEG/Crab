import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
import re
import random
from rouge import Rouge
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util

def calculate_rouge_l(reference, hypothesis):
    rouge = Rouge()
    try:
        scores = rouge.get_scores(hypothesis, reference)
        return scores[0]['rouge-l']["f"]
    except:
        return 1.0


def check_length(messages, word_limit):
    cur_word = 0
    for vert in messages:
        cur_word += len(vert["content"].split(" "))
    if cur_word > word_limit:
        return False
    return True


def slice_list(data, n):
    return [data[i:i + n] for i in range(0, len(data), n)]

def filter(data, args, num_c, unified_data):
    # =============== First Filter: Calculate the similarity between the constraint and the refined instruction. ===============
    Ban_instance = []
    count_first = 0
    for i, vert in enumerate(tqdm(data)):
        data[i]["overlap"] = 0
        if vert["Aug_instruction"]["Refined_Instruction"] == "":
            continue
        for key, value in vert["Aug_instruction"]["Additional_Instruction"].items():
            if value == "":
                continue
            try:
                score = calculate_rouge_l(vert["Aug_instruction"]["Refined_Instruction"], value)
            except:
                Ban_instance.append(i)
                break
            if score > args.threshold:
                data[i]["overlap"] += 1
                count_first += 1
    print(f"After first stage, there are {count_first} items overlap.")            
    # print(f"After first stage, filtering {len(Ban)/len(data) * 100:.2f} %, there are {len(data) - len(Ban)} items left.")

    delete_key = dict()
    Ban = dict()
    for i, vert in enumerate(tqdm(data)):
        Ban.clear()
        keys = list(vert["Aug_instruction"]["Additional_Instruction"].keys())
        for j in range(len(keys)):
            for k in range(j + 1, len(keys)):
                score = calculate_rouge_l(vert["Aug_instruction"]["Additional_Instruction"][keys[j]], vert["Aug_instruction"]["Additional_Instruction"][keys[k]])
                if score > args.threshold:
                    if k not in Ban:
                        Ban[k] = []
                    if j not in Ban:
                        Ban[j] = []
                    Ban[k].append(j)
                    Ban[j].append(k)
        sorted_Ban = dict(sorted(Ban.items(), key=lambda item: len(item[1]), reverse=True))
        # print("========")
        # print(sorted_Ban)
        for key, value in sorted_Ban.items():
            if len(sorted_Ban[key]) == 0:
                continue
            # print("+++++++++")
            # print(keys[key])
            del data[i]["Aug_instruction"]["Additional_Instruction"][keys[key]]
            if keys[key] not in delete_key:
                delete_key[keys[key]] = 0
            delete_key[keys[key]] += 1
            for item in value:
                sorted_Ban[item].remove(key)

    print("After the second phase, the number of deleted constraints of different types is:",delete_key)

    for i, vert in enumerate(data):
        if i in Ban_instance:
            continue
        num_c += len(vert["Aug_instruction"]["Additional_Instruction"])
        unified_data.append(copy.deepcopy(vert))
    
    return num_c, unified_data



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument("--datasets", type=str, nargs="+")
    parser.add_argument("--word_limit", type=int, default=1500)
    parser.add_argument("--Pool_size", type=int, default=5000)
    parser.add_argument("--threshold", type=float, default=0.6)
    parser.add_argument("--input_dir", type=str, default="data/seed_data/Long_data")
    parser.add_argument("--output_dir", type=str, default="data/seed_data/Long_data")
    parser.add_argument("--output_file", type=str, default="filter.json")
    args = parser.parse_args()


    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    datasets = args.datasets
    word_limit = args.word_limit

    data = []
    print("datasets:",datasets)
    if datasets != ["Null"]:
        for dataset in datasets:
            file = args.input_dir + "/5_" + dataset + "_constraints.json"
            with open(file, "r", encoding="utf-8") as reader:
                d = json.load(reader)
                reader.close()
            for i, vert in enumerate(d):
                vert["source"] = dataset
                data.append(copy.deepcopy(vert))
    

    num_c = 0
    unified_data = []

    data = slice_list(data, args.Pool_size)

    for i, d in enumerate(data):
        num_c, unified_data = filter(d, args, num_c, unified_data)
        print(f"Pool {i}: there are {len(unified_data)} items.")
      

    out_file = open(output_file, "w")

    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    # for vert in unified_data:
    #     # vert["id"] = str(vert["id"])
    #     out_file.write(json.dumps(vert) + "\n")

    out_file.close()
    print("total_number:", len(unified_data))
    print("avg_constraints:", num_c/len(unified_data))

    constraint_type={}
    for vert in unified_data:
        for key in vert["Aug_instruction"]["Additional_Instruction"].keys():
            if key not in constraint_type:
                constraint_type[key] = 0
            constraint_type[key] += 1
    
    out_file = open(os.path.join(output_folder, "_".join(datasets)+"_constraint_type.json"), "w", encoding="utf-8")
    json.dump(
        constraint_type,
        out_file,
        indent=4,
    )
    out_file.close()