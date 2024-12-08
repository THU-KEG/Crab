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

    if "Others" in Sample_keys:
        other_keys = []
        for k in vert['Aug_instruction']['Additional_Instruction'].keys():
            if k not in Sample_keys:
                other_keys.append(k)
        key = random.sample(other_keys, 1)[0]
        vert['Aug_instruction']['Additional_Instruction']["Others"] = vert['Aug_instruction']['Additional_Instruction'][key]

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
    parser.add_argument("--min_number", type=int, default=6) # for constraints
    parser.add_argument("--max_number", type=int, default=8) # for constraints
    parser.add_argument("--shot_num", type=int, default=5)
    args = parser.parse_args()

    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    data = dict()
    datasets = args.datasets
    print("datasets:",datasets)
    if datasets != ["Null"]:
        for dataset in datasets:
            file = args.input_dir + "/6_" + dataset + "_filter.json"
            with open(file, "r", encoding="utf-8") as reader:
                d = json.load(reader)
                reader.close()
            for i, vert in enumerate(d):
                data[str(vert["id"]) + "_" + vert["source"]] = copy.deepcopy(vert)

    # load ICL INFO
    file = args.output_dir + "/INFO_forward_ICL.json"
    with open(file, "r", encoding="utf-8") as reader:
        icl = json.load(reader)
        reader.close()
    
    Official_Constraint_Type = Constraint_Types.keys()

    out_file = open(output_file, "w")
    
    unified_data = []
    cnt = 0
    total_words = 0
    for rootidx,iclidx in icl.items():
        cnt += 1
        vert = data[rootidx]
        shots = []
        constraint_types = []
        for idx in iclidx:
            shots.append(data[idx])
        constraint_types = [x for x in vert["Aug_instruction"]["Additional_Instruction"].keys() if (all(x in shot["Aug_instruction"]["Additional_Instruction"].keys() for shot in shots) and x in Official_Constraint_Type)]


        # ==== DEBUG ====
        # if cnt < 10:
        #     print(constraint_types)
        # ===============

        OFlag = False
        RFlag = False
        AFlag = False
        OFlag = (int)(random.random() > 0.3)
        RFlag = (int)(random.random() > 0.7)
        AFlag = (int)(random.random() > 0.5)
        if RFlag == False:
            AFlag = True

        # if vert["Aug_instruction"]["Additional_Instruction"]["Punctuation"] == "":
        #     del vert["Aug_instruction"]["Additional_Instruction"]["Punctuation"]

        Length = len(constraint_types)
        Dflag = (int)(random.random() > 0.3)
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
            Sample_keys = random.sample(constraint_types, num)
            if len(Sample_keys) < len(vert["Aug_instruction"]["Additional_Instruction"].keys()) and all(len(Sample_keys) < len(shot["Aug_instruction"]["Additional_Instruction"].keys()) for shot in shots):
                OtherFlag = (int)(random.random() > 0.7)
                if OtherFlag:
                    Sample_keys.append("Others")

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
        shot_num = len(shots)
        messages = []
        for item in shots:
            iinput, ioutput = get_input_output(item, input_template, RFlag, AFlag, 
                query_output, Sample_keys)
            messages.append({
                "role": "user",
                "content": prompt + iinput,
            })
            messages.append({
                "role": "assistant",
                "content": ioutput,
            })
        input, output = get_input_output(vert, input_template, RFlag, AFlag, query_output, Sample_keys)
        messages.append({
            "role": "user",
            "content": prompt + input,
        })
        messages.append({
            "role": "assistant",
            "content": output,
        })

        # if cnt < 10:
        #     print("==================== ITEM :",cnt, "====================")
        for item in messages:
            # if cnt < 10:
            #     print("--------------------")
            #     print(item["content"])
            total_words += len(item["content"].split(" "))
        
        # print("=============================")
        # print(prompt)
        # print("---------------------------")
        # print(output)
        unified_instance = {
            "id": vert["id"],
            "cnt_id": vert["cnt_id"],
            "source": vert["source"],
            "messages": messages,
        }
        unified_data.append(unified_instance)


    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    out_file.close()
    print("total_number:", len(unified_data))
    print("avg_word:", total_words/len(unified_data))
