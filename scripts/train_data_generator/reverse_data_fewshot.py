import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
from Reverse_Prompt import *
from nltk.tokenize import word_tokenize
import random

def get_input_output(vert, input_template, RFlag, AFlag, query_output, Sample_keys):
    input = input_template.format(
        Response=vert["messages"][1]["content"],
        Instruction=vert["messages"][0]["content"],
    )

    if AFlag:
        if "index" in query_output[3]:
            additional_instruction = (
                query_output[2].join(
                    [
                        f"{query_output[3].format(index=i+1, item=vert['Aug_instruction']['Additional_Instruction'][item])}"
                        for i, item in enumerate(Sample_keys)
                    ]
                )
            )
        else:
            additional_instruction = (
                query_output[2].join(
                    [
                        f"{query_output[3].format(item=vert['Aug_instruction']['Additional_Instruction'][item])}"
                        for i, item in enumerate(Sample_keys)
                    ]
                )
            )

    if RFlag and AFlag:
        output = query_output[1].format(
            refined_instruction=vert["Aug_instruction"]["Refined_Instruction"],
            additional_instruction=additional_instruction,
        )
    elif RFlag:
        output = query_output[1].format(
            refined_instruction=vert["Aug_instruction"]["Refined_Instruction"],
        )
    else:
        output = query_output[1].format(
            additional_instruction=additional_instruction,
        )

    return input, output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument("--datasets", type=str, nargs="+")
    parser.add_argument("--input_dir", type=str, default="data/seed_data/")
    parser.add_argument("--output_dir", type=str, default="data/unified_data/")
    parser.add_argument("--output_file", type=str, default="back_data.json")
    parser.add_argument("--min_number", type=int, default=3) # for constraints
    parser.add_argument("--max_number", type=int, default=-1) # for constraints
    parser.add_argument("--shot_num", type=int, default=5)
    args = parser.parse_args()

    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    data = []
    datasets = args.datasets
    print("datasets:",datasets)
    if datasets != ["Null"]:
        for dataset in datasets:
            file = args.input_dir + "/6_" + dataset + "_constraints.json"
            with open(file, "r", encoding="utf-8") as reader:
                d = json.load(reader)
                reader.close()
            for i, vert in enumerate(d):
                data.append(copy.deepcopy(vert))


    out_file = open(output_file, "w")
    
    unified_data = []
    ban = []
    avg_x = 0
    avg_y = 0
    shot_cnt = 0
    for i, vert in enumerate(data):
        idx = str(vert["cnt_id"]) + "_" + vert["source"]
        if idx in ban:
            continue

        # if i > 3:
        #     break

        OFlag = False
        RFlag = False
        AFlag = False
        OFlag = (int)(random.random() > 0.3)
        RFlag = (int)(random.random() > 0.5)
        AFlag = (int)(random.random() > 0.5)
        if RFlag == False:
            AFlag = True

        # if vert["Aug_instruction"]["Additional_Instruction"]["Punctuation"] == "":
        #     del vert["Aug_instruction"]["Additional_Instruction"]["Punctuation"]
        if args.max_number != -1:
            num = random.randint(args.min_number, args.max_number) 
        else:
            num = random.randint(args.min_number, len(vert["Aug_instruction"]["Additional_Instruction"].keys())) 

        Ioverview = ""
        Irefined = ""
        Iadd = ""
        
        if OFlag:
            Ioverview = random.sample(Overview, 1)[0]
        if RFlag:  
            Irefined = random.sample(Refined_Instruction, 1)[0]
        if AFlag:
            Iadd = random.sample(Additional_Instruction, 1)[0]
            
        
        if RFlag and AFlag:
            query_output = random.sample(Combination_Query, 1)[0]
        elif RFlag:
            query_output = random.sample(Refined_Query, 1)[0]
        elif AFlag:
            query_output = random.sample(Add_Instruction_Query, 1)[0]
        
        Sample_keys = []
        if AFlag:
            Sample_keys = random.sample(list(vert["Aug_instruction"]["Additional_Instruction"].keys()), num)
            Constraint_Sentences = []
            for item in Sample_keys:
                Constraint_Sentences.append(random.sample(Constraint_Types[item],1)[0])
            if "index" in query_output[3]:
                Iadditional_instruction = (
                    query_output[2].join(
                        [
                            f"{query_output[3].format(index=i+1, item=item)}"
                            for i, item in enumerate(Constraint_Sentences)
                        ]
                    )
                )
            else:
                Iadditional_instruction = (
                    query_output[2].join(
                        [
                            f"{query_output[3].format(item=item)}"
                            for i, item in enumerate(Constraint_Sentences)
                        ]
                    )
                )

        
        input_template = random.sample(Reverse_Input, 1)[0]

        instruction = ""
        if OFlag:
            instruction += Ioverview + "\n"
        if RFlag:
            instruction += Irefined + "\n" 
        if AFlag:
            instruction += Iadd + "\n" 
            instruction += Iadditional_instruction
        
        prompt = instruction + "\n\n" + query_output[0] +"\n\n"
        # === few-shot ===
        shot_num = random.randint(1, args.shot_num)
        shots = []
        iter_num = 0
        temp_ban = []
        while shot_num and iter_num < 10:
            iter_num += 1
            shot = random.sample(data[i+1:], 1)[0]
            F = False
            for Ckey in Sample_keys:
                if Ckey not in shot["Aug_instruction"]["Additional_Instruction"]:
                    F = True
                    break
            idx = str(shot["cnt_id"]) + "_" + shot["source"]
            if F == False and idx not in ban and idx not in temp_ban:
                temp_ban.append(idx)
                shot_num -= 1
                shots.append(shot)

        if shot_num > 0:
            continue
        else:
            shot_cnt += len(shots)
            icl_template = random.sample(ICL,1)[0]
            for item in shots:
                idx = str(item["cnt_id"]) + "_" + item["source"]
                ban.append(idx)
                iinput, ioutput = get_input_output(item, input_template, RFlag, AFlag, 
                query_output, Sample_keys)
                avg_x += len(word_tokenize(item["messages"][1]["content"])) + len(word_tokenize(item["messages"][0]["content"]))
                # avg_x += len(word_tokenize(item["messages"][1]["content"]))
                avg_y += len(word_tokenize(ioutput))
                prompt += icl_template[0] + iinput + "\n\n" + icl_template[1] + ioutput + "\n\n"
            intput, output = get_input_output(vert, input_template, RFlag, AFlag, query_output, Sample_keys)
            avg_x += len(word_tokenize(vert["messages"][1]["content"])) + len(word_tokenize(vert["messages"][0]["content"]))
            # avg_x += len(word_tokenize(vert["messages"][1]["content"]))
            avg_y += len(word_tokenize(output))
            prompt += icl_template[0] + intput + "\n\n" + icl_template[1]
        
        # print("=============================")
        # print(prompt)
        # print("---------------------------")
        # print(output)
        unified_instance = {
            "id": vert["id"],
            "cnt_id": vert["cnt_id"],
            "source": vert["source"],
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": output},
            ],
            "shots": [str(d["id"]) + "_" + d["source"] for d in shots]
        }
        unified_data.append(unified_instance)


    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    out_file.close()
    print("total_number:", len(unified_data))
    print("avg_x:",avg_x/len(unified_data))
    print("avg_y:",avg_y/len(unified_data))
    print("avg_shot:",shot_cnt/len(unified_data))
