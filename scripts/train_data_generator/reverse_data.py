import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
from Reverse_Prompt import *
from nltk.tokenize import word_tokenize
import random


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument("--datasets", type=str, nargs="+")
    parser.add_argument("--input_dir", type=str, default="data/seed_data/")
    parser.add_argument("--output_dir", type=str, default="data/unified_data/")
    parser.add_argument("--output_file", type=str, default="back_data.json")
    parser.add_argument("--min_number", type=int, default=3)
    parser.add_argument("--max_number", type=int, default=-1)
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
    avg_x = 0
    avg_y = 0
    for i, vert in enumerate(data):
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
            # print("==========")
            # print(vert["Aug_instruction"]["Additional_Instruction"])
        if args.max_number != -1:
            num = random.randint(args.min_number, args.max_number) 
        else:
            if args.min_number > len(vert["Aug_instruction"]["Additional_Instruction"].keys()):
                num = len(vert["Aug_instruction"]["Additional_Instruction"].keys())
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

        
        input_template = random.sample(Reverse_Input, 1)[0]

        # ================== Combination ==================
        input = input_template.format(
            Response=vert["messages"][1]["content"],
            Instruction=vert["messages"][0]["content"],
        )
        
        instruction = ""
        if OFlag:
            instruction += Ioverview + "\n"
        if RFlag:
            instruction += Irefined + "\n" 
        if AFlag:
            instruction += Iadd + "\n" 
            instruction += Iadditional_instruction
        
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

        prompt = random.sample(Combination, 1)[0].format(
            input=input, instruction=instruction, query=query_output[0]
        )
        
        # print("=============================")
        # print(prompt)
        # print("---------------------------")
        # print(output)
        avg_x += len(word_tokenize(vert["messages"][1]["content"])) + len(word_tokenize(vert["messages"][0]["content"]))
        # avg_x += len(word_tokenize(vert["messages"][1]["content"]))
        avg_y +=  len(word_tokenize(output))

        unified_instance = {
            "id": vert["id"],
            "cnt_id": vert["cnt_id"],
            "source": vert["source"],
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": output},
            ],
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
