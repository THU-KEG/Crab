import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
import re
import random
import transformers
from Forward_Prompt import *

num_CType = dict()
ICL_List = dict()

def get_input_output(vert, num_cons, weighted, Com, Symbol, args):

    instruction = vert["messages"][0]["content"]
    if vert["Aug_instruction"]["Refined_Instruction"] != "":
        Iflag = (int)(random.random() > vert["overlap"] * 0.1 + args.diverse_rate)
        if Iflag: 
            instruction = vert["Aug_instruction"]["Refined_Instruction"]
            try:
                if len(vert["Aug_instruction"]["Refined_Instruction"].split(" ")) < len(vert["messages"][0]["content"].split(" ")):
                    instruction = vert["messages"][0]["content"]
            except:
                instruction = vert["messages"][0]["content"]
        else:
            instruction = vert["messages"][0]["content"]
    
    # mostly long story in the instruction:
    Long_Flag = False
    if len(vert["Aug_instruction"]["Refined_Instruction"].split(" ")) < len(vert["messages"][0]["content"].split(" ")):
        Long_Flag = True
        Com = random.sample(Long_Combination, 1)[0]


    Sample_keys = []
    w = dict()
    for key in vert["Aug_instruction"]["Additional_Instruction"].keys():
        if key in weighted:
            w[key] = random.random() - weighted[key]
        else:
            w[key] = random.random() - args.add_weight
    sorted_w = sorted(w.items(), key=lambda item: item[1], reverse = True)
    for j, item in enumerate(sorted_w):
        if j == num_cons:
            break
        Sample_keys.append(item[0])
    
    Constraints = []
    for item in Sample_keys:
        if item not in num_CType:
            num_CType[item] = 0
        num_CType[item] += 1
        Constraints.append(vert["Aug_instruction"]["Additional_Instruction"][item])

    random.shuffle(Constraints)

    if Symbol == " ":
        additional_instruction = " ".join(Constraints)
    else:
        if Long_Flag ==  False:
            additional_instruction = "\n"
        else:
            additional_instruction = ""
        Symbol = Com[1] + Symbol
        if "index" in Symbol:
            additional_instruction += (
                "\n".join(
                    [
                        f"{Symbol.format(index=i+1, item=item)}"
                        for i, item in enumerate(Constraints)
                    ]
                )
            )
        else:
            additional_instruction += (
                "\n".join(
                    [
                        f"{Symbol.format(item=item)}"
                        for i, item in enumerate(Constraints)
                    ]
                )
            )

    Prompt = Com[0].format(
        instruction = instruction,
        additional = additional_instruction,
    )

    return Prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument("--datasets", type=str, nargs="+")
    parser.add_argument("--min_number", type=int, default=6)
    parser.add_argument("--max_number", type=int, default=8)
    parser.add_argument("--weight", type=int, default=1)
    parser.add_argument("--add_weight", type=float, default=0.0)
    parser.add_argument("--diverse_rate", type=float, default=0.3)
    parser.add_argument("--base_rate", type=float, default=0.85)
    parser.add_argument("--ICL_rate", type=float, default=0.2)
    parser.add_argument("--shot_num", type=int, default=3)
    parser.add_argument("--input_dir", type=str, default="data/seed_data/Long_data_N/")
    parser.add_argument("--output_dir", type=str, default="data/unified_data/Long_data_N/")
    parser.add_argument("--output_file", type=str, default="random_shuffle_W_6_ICL.json")
    args = parser.parse_args()


    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    data = []
    datasets = args.datasets
    print("datasets:",datasets)
    if datasets != ["Null"]:
        for dataset in datasets:
            file = args.input_dir + "/6_" + dataset + "_filter.json"
            print("input_dir:",args.input_dir)
            print("file:",file)
            with open(file, "r", encoding="utf-8") as reader:
                d = json.load(reader)
                reader.close()
            for i, vert in enumerate(d):
                vert["source"] = dataset
                data.append(copy.deepcopy(vert))

    constraint_num = dict()
    if datasets != ["Null"]:
        for dataset in datasets:
            file = args.input_dir + "/" + dataset + "_constraint_type.json"
            with open(file, "r", encoding="utf-8") as reader:
                c = json.load(reader)
                reader.close()
            for k,v in c.items():
                if k not in constraint_num:
                    constraint_num[k] = 0
                constraint_num[k] += v
    
    weighted = dict()
    for k, v in constraint_num.items():
        weighted[k] = max((v) / len(data) , 0.5)

    # ===== DEBUG =====
    out_file = open(os.path.join(output_folder, "INFO_forward_weighted.json"), "w", encoding="utf-8")
    json.dump(
        weighted,
        out_file,
        indent=4,
    )
    out_file.close()
    # ===== ===== =====

    out_file = open(output_file, "w")

    unified_data = []
    cnt = -1
    total_num = 0
    shot_instance = 0
    total_shots = 0
    total_words = 0
    ban = []
    for i, vert in enumerate(data):
        # if i > 3:
        #     break
        # print("==========")
        # print(vert)

        idx = str(vert["cnt_id"]) + "_" + vert["source"]
        if idx in ban:
            continue
        
        # =========== MAX and MIN to GET KEY ================
        Length = len(list(vert["Aug_instruction"]["Additional_Instruction"].keys()))
        Dflag = (int)(random.random() > args.diverse_rate)
        if Dflag:
            min_number = min(args.min_number, Length)
            if args.max_number != -1:
                max_number = min(args.max_number, Length)
            else:
                max_number = Length
        else:
            min_number = 1
            max_number = Length
        

        num = random.randint(min_number, max_number)  
        Bflag = (int)(random.random() < args.base_rate)
        if Bflag:
            Com = random.sample(Base_Combination, 1)[0]
            Symbol = random.sample(Base_Connectors, 1)[0]
        else:
            Com = random.sample(Combination, 1)[0]
            Symbol = random.sample(Connectors, 1)[0]

        # =========== Fewshot ================
        SFlag = (int)(random.random() < args.ICL_rate)
        if SFlag:
            shot_num = random.randint(1, args.shot_num)
        else:
            shot_num = 0
        if i + 1 >= len(data):
            shot_num = 0
        shots = []
        iter_num = 0
        while shot_num and iter_num < 10:
            iter_num += 1
            end = min(i + iter_num * 50 , len(data))
            shot = random.sample(data[i+1:end], 1)[0]
            idx = str(shot["cnt_id"]) + "_" + shot["source"]
            if idx not in ban:
                ban.append(idx)
                shot_num -= 1
                shots.append(shot)

        messages = []
        min_num = 0
        shot_cnt = len(shots)
        if shot_cnt != 0:
            shot_instance += 1
            num = max(num, args.shot_num)
            num = min(num, Length)
            total_shots += shot_cnt
        for item in shots:
            num_cons = random.randint(min_num, num - shot_cnt)  
            Prompt = get_input_output(item, num_cons, weighted, Com, Symbol, args)
            messages.append({
                    "role": "user",
                    "content": Prompt,
                })
            messages.append({
                    "role": "assistant",
                    "content": item["messages"][1]["content"],
                })
            shot_cnt -= 1
            min_num = num_cons
        total_num += num
        Prompt = get_input_output(vert, num, weighted, Com, Symbol, args)
        messages.append({
                "role": "user",
                "content": Prompt,
            })
        messages.append({
                "role": "assistant",
                "content": vert["messages"][1]["content"],
            })

        unified_instance = {
            "id": vert["id"],
            "cnt_id": vert["cnt_id"],
            "source": vert["source"],
            "messages": messages,
            "Num_Cons": num,
            "shots": [str(d["id"]) + "_" + d["source"] for d in shots]
        }
        ICL_List[str(vert["id"]) + "_" + vert["source"]] = unified_instance["shots"]
        # print("====================")
        # print(unified_instance)
        for item in messages:
            # print("--------------------")
            # print(item["content"])
            total_words += len(item["content"].split(" "))

        unified_data.append(unified_instance)

    # unified_data = sorted(unified_data, key=lambda x: x['Num_Cons'], reverse=True)
                             
    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    out_file.close()
    print("total_number:", len(unified_data))
    print("avg_constraint:", total_num/len(unified_data))
    print("avg_shots:",total_shots/shot_instance)
    print("avg_word:", total_words/len(unified_data))

    # ===== DEBUG =====
    sorted_CType = dict(sorted(num_CType.items(), key=lambda item: item[1], reverse = True))
    out_file = open(os.path.join(output_folder, "INFO_forward_constraint_type.json"), "w", encoding="utf-8")
    json.dump(
        sorted_CType,
        out_file,
        indent=4,
    )
    out_file.close()

    out_file = open(os.path.join(output_folder, "INFO_forward_ICL.json"), "w", encoding="utf-8")
    json.dump(
        ICL_List,
        out_file,
        indent=4,
    )
    out_file.close()
    # ===== ===== =====