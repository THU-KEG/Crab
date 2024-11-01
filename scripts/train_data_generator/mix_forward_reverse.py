import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
import re
import random


def check_length(messages, word_limit):
    cur_word = 0
    for vert in messages:
        cur_word += len(vert["content"].split(" "))
    if cur_word > word_limit:
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument(
        "--forward_file",
        type=str,
        default="",
    )
    parser.add_argument(
        "--forward_shuffle",
        action='store_true',
    )
    parser.add_argument(
        "--max_num",
        type=int,
        default=13500,
    )
    parser.add_argument(
        "--reverse_file",
        type=str,
        default="",
    )
    parser.add_argument(
        "--fewshot_file",
        type=str,
        default="",
    )
    parser.add_argument(
        "--sharegpt_file",
        type=str,
        default="data/raw_data/ShareGPT_Vicuna_unfiltered/sharegpt_clean_en_reduce_rep.json",
    )
    parser.add_argument(
        "--forward_rate",
        type=float,
        default=0.667,
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=36,
    )
    parser.add_argument(
        "--sharegpt_num",
        type=int,
        default=48000,
    )
    parser.add_argument(
        "--fewshot_num",
        type=int,
        default=150,
    )
    parser.add_argument(
        "--word_limit",
        type=int,
        default=1500,
    )
    parser.add_argument(
        "--dataset_limit",
        type=int,
        default=3500,
    )
    parser.add_argument("--output_dir", type=str, default="data/train_data/")
    parser.add_argument("--output_file", type=str, default="train.jsonl")
    args = parser.parse_args()


    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    word_limit = args.word_limit

    forward_data = []
    reverse_data = []
    fewshot_data = []

    if args.forward_file != "":
        with open(args.forward_file, "r", encoding="utf-8") as reader:
            forward_data = json.load(reader)
            reader.close()

    if args.reverse_file != "":
        with open(args.reverse_file, "r", encoding="utf-8") as reader:
            reverse_data = json.load(reader)
            reader.close()
    
    if args.fewshot_file != "":
        with open(args.fewshot_file, "r", encoding="utf-8") as reader:
            fewshot_data = json.load(reader)
            reader.close()

    if args.sharegpt_file != "":
        with open(args.sharegpt_file, "r", encoding="utf-8") as reader:
            otherdata = json.load(reader)
            reader.close()

    out_file = open(output_file, "w")

    random.seed(args.seed)
    print(len(otherdata))
    sample_sharegpt = random.sample(
        otherdata,
        args.sharegpt_num,
    )

    unified_data = []
    if args.forward_shuffle == True:
        print("forward_shuffle",args.forward_shuffle)    
        random.shuffle(forward_data)
    random.shuffle(reverse_data)
    random.shuffle(fewshot_data)

    total_word = 0

    BanID = []
    limit = min(args.max_num, len(forward_data)) * args.forward_rate
    Cnt = 0
    num_of_Cons = 0
    last_num = dict()
    source_count = dict()
    print("len_forward_data:",len(forward_data))
    for i, vert in enumerate(forward_data):
        if Cnt >= limit:
            break
        if check_length(vert["messages"], word_limit) == False:
            continue
        if str(vert["id"]) + "_" + vert["source"]  in BanID:
            continue
        
        if vert["source"] not in source_count:
            source_count[vert["source"]] = 0
            
        if source_count[vert["source"]] < args.dataset_limit:
            source_count[vert["source"]] += 1
        else:
            continue

        unified_instance = {
            "id": str(vert["id"]) + "_forward",
            "cnt_id": str(vert["cnt_id"]),
            "source": vert["source"],
            "messages": vert["messages"],
        }
        unified_data.append(unified_instance)

        for item in vert["messages"]:
            total_word += len(item["content"].split(" "))
        if "Num_Cons" in vert:
            num_of_Cons += vert["Num_Cons"]
            if vert["Num_Cons"] not in last_num:
                last_num[vert["Num_Cons"]] = 0
            last_num[vert["Num_Cons"]] += 1
        Cnt += 1
        BanID.append(str(vert["id"]) + "_" + vert["source"])
        if "shots" in vert:
            for item in vert["shots"]:
                BanID.append(item)
    print("total_number:", len(unified_data))
    if len(unified_data) != 0:
        last_num_s = {key: last_num[key] for key in sorted(last_num.keys())}
        print("avg_cons:",num_of_Cons/(len(unified_data)-args.conifer_num), last_num_s)
        print("dataset_num:",source_count)

    for i, vert in enumerate(reverse_data):
        if Cnt >= args.max_num:
            break
        if check_length(vert["messages"], word_limit) == False:
            continue
        if str(vert["id"]) + "_" + vert["source"] in BanID:
            continue
        
        unified_instance = {
            "id": str(vert["id"]) + "_reverse",
            "cnt_id": str(vert["cnt_id"]),
            "source": vert["source"],
            "messages": vert["messages"],
        }
        unified_data.append(unified_instance)
        for item in vert["messages"]:
            total_word += len(item["content"].split(" "))
        Cnt += 1
        BanID.append(str(vert["id"]) + "_" + vert["source"])
        if "shots" in vert:
            for item in vert["shots"]:
                BanID.append(item)
    print("total_number:", len(unified_data))

    FCnt = 0
    for i, vert in  enumerate(fewshot_data):
        if FCnt >= args.fewshot_num:
            break
        if check_length(vert["messages"], word_limit) == False:
            continue
        if str(vert["id"]) + "_" + vert["source"]  in BanID:
            continue
        unified_instance = {
            "id": str(vert["id"]) + "_fewshot",
            "cnt_id": str(vert["cnt_id"]),
            "source": vert["source"],
            "messages": vert["messages"],
        }
        unified_data.append(unified_instance)
        for item in vert["messages"]:
            total_word += len(item["content"].split(" "))
        FCnt += 1
        BanID.append(str(vert["id"]) + "_" + vert["source"])
        if "shots" in vert:
            for item in vert["shots"]:
                BanID.append(item)
    print("total_number:", len(unified_data))
    if len(unified_data) != 0:
        print("avg_word:",total_word/len(unified_data))

    for i, vert in enumerate(sample_sharegpt):
        if vert["conversations"] == []:
            continue
        messages = []
        for c in vert["conversations"]:
            content = c["value"]
            if c["from"] == "human" or c["from"] == "user":
                messages.append(
                    {
                        "role": "user",
                        "content": content,
                    }
                )
            elif (
                c["from"] == "gpt"
                or c["from"] == "chatgpt"
                or c["from"] == "bing"
                or c["from"] == "bard"
            ):
                messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                    }
                )
            elif c["from"] == "system":
                messages.append(
                    {
                        "role": "system",
                        "content": content,
                    }
                )
            else:
                print("Error 'from': ", c["from"])
        assert messages != [], print(vert["conversations"])

        if check_length(messages, word_limit) == False:
            continue
        
        unified_instance = {
            "id": str(vert["id"]),
            "cnt_id": str(i),
            "source": "sharegpt",
            "messages": messages,
        }
        unified_data.append(unified_instance)


    for vert in unified_data:
        out_file.write(json.dumps(vert) + "\n")

    out_file.close()
    print("file:",output_file)
    print("total_number:", len(unified_data))
    