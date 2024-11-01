import jsonlines
import json
import argparse
from pathlib import Path
import os
import copy
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from utils import Digit_Format_Max_Min, Keyword_Format, Digit_Format_Min, Digit_Format_Max, Digit_Format_Around, Symbol_Format, Paragraph_Format, Sentence_Format, Word_Format
import random
import yake
from langdetect import detect_langs
from tqdm import tqdm

def detect_language(text):
    try:
        detected_langs = detect_langs(text)
        lang_code = detected_langs[0].lang
    except Exception:
        lang_code = "unknown"
    return lang_code

def get_json_result(text):
    try:
        res = json.loads(text)
    except Exception as Argument:
        try:
            res = text.split("\n\n")[1]
            res = json.loads(res)
        except Exception as Argument2:
            # print("============= Error Extract ===========")
            # print(Argument)
            # print(Argument2)
            return ""
    return res


def refined_Length(content): # min
    min_s = 1000000
    max_w = 0
    max_c = 0
    paragraph = content.split("\n")
    for item in paragraph:
        if item == "":
            continue
        sentences = sent_tokenize(item) 
        min_s = min(len(sentences), min_s)
        for s in sentences:
            words = word_tokenize(s)
            max_w = max(max_w, len(words))
            for w in words:
                max_c = max(max_c, len(w))
    
    if min_s <= 1:
        Pformat = ""
    else:
        min_s = min_s + random.randint(0, 2)
        Pformat = random.sample(Paragraph_Format, 1)[0].format(sentence_number = min_s)

    if max_w <= 5:
        Sformat = ""
    else:
        max_w = int((max_w - 1) / 5 + 1) * 5
        Sformat = random.sample(Sentence_Format, 1)[0].format(word_number = max_w)

    if max_c <= 3:
        Wformat = ""
    else:
        max_c = int((max_c - 1) / 5 + 1) * 5
        Wformat = random.sample(Word_Format, 1)[0].format(character_number = max_c)

    return Pformat, Sformat, Wformat


def refined_number(content):
    # Dformat = random.sample(Digit_Format, 1)[0]
    words = word_tokenize(content)
    number_of_words = len(words)
    num_ten = int(number_of_words / 10)

    if num_ten == 0:
        min_num = 3
        max_num = 20
        around = 10
    else:
        min_num = num_ten * 10 - min(random.randint(0, num_ten - 1), 2) * 10
        max_num = (num_ten + 1) * 10 + random.randint(0, 2) * 10
        around = num_ten * 10

    Flag = random.randint(1, 4)
    if Flag == 1:
        Dformat = random.sample(Digit_Format_Max_Min, 1)[0]
        return Dformat.format(min = min_num, max = max_num)
    elif Flag == 2:
        Dformat = random.sample(Digit_Format_Min, 1)[0]
        return Dformat.format(num = min_num)
    elif Flag == 3:
        Dformat = random.sample(Digit_Format_Max, 1)[0]
        return Dformat.format(num = max_num)
    elif Flag == 4:
        Dformat = random.sample(Digit_Format_Around, 1)[0]
        return Dformat.format(num = around)

def refined_symbol(content):
    for key,value in Symbol_Format.items():
        if key not in content:
            return random.sample(value, 1)[0]
        
    return ""

def refined_keyword(content):

    language = detect_language(content)
    # max_ngram_size = 3
    # deduplication_threshold = 0.9
    # deduplication_algo = "seqm"
    # windowSize = 1
    number_of_words = len(content)
    num_ten = int(number_of_words / 10)

    numOfKeywords = min(num_ten, 3)

    assert numOfKeywords != 0

    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        # n=max_ngram_size,
        # dedupLim=deduplication_threshold,
        # dedupFunc=deduplication_algo,
        # windowsSize=windowSize,
        top=numOfKeywords,
        features=None,
    )
    keywords = custom_kw_extractor.extract_keywords(content)

    key = []
    for kw in keywords:
        if kw[1] < 0.07:
            key.append(kw[0])
    quoted = [f'"{k}"' for k in key]

    assert len(quoted) != []
    
    result = ", ".join(quoted)

    assert result != ""

    Kformat = random.sample(Keyword_Format, 1)[0].format(keywords=result)
    return Kformat



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="generate")
    parser.add_argument(
        "--num_sample",
        type=int,
        default=10000,
    )
    parser.add_argument(
        "--origin_file",
        type=str,
        default="data/seed_data/1_wizardLM.json",
    )
    parser.add_argument(
        "--refined_instruction_file",
        type=str,
        default="",
    )
    parser.add_argument(
        "--global_instruction_file",
        type=str,
        default="",
    )
    parser.add_argument(
        "--local_instruction_file",
        type=str,
        default="",
    )
    parser.add_argument("--output_dir", type=str, default="data/seed_data/")
    parser.add_argument("--output_file", type=str, default="3_wizardLM_constraints.json")
    args = parser.parse_args()


    output_folder = Path(args.output_dir)
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = os.path.join(output_folder, args.output_file)

    data = []
    Rdata = []
    Gdata = []
    Ldata = []

    with open(args.origin_file, "r", encoding="utf-8") as reader:
        data = json.load(reader)
        reader.close()

    if args.refined_instruction_file != "":
        with open(args.refined_instruction_file, "r", encoding="utf-8") as reader:
            Rdata = json.load(reader)
            reader.close()

    if args.global_instruction_file != "":
        with open(args.global_instruction_file, "r", encoding="utf-8") as reader:
            Gdata = json.load(reader)
            reader.close()

    if args.local_instruction_file != "":
        with open(args.local_instruction_file, "r", encoding="utf-8") as reader:
            Ldata = json.load(reader)
            reader.close()


    out_file = open(output_file, "w")

    unified_data = []
    count_constraints = dict()
    for i, d in enumerate(tqdm(data)):
        if i > args.num_sample:
            break
        unified_instance = copy.deepcopy(d)
        unified_instance["Aug_instruction"] = {
            "Refined_Instruction" : "",
            "Additional_Instruction" : dict()
        }
        constraint = refined_number(d["messages"][1]["content"])
        unified_instance["Aug_instruction"]["Additional_Instruction"]["Digit"] = constraint

        Pconstraint, Sconstraint, Wconstraint = refined_Length(d["messages"][1]["content"])

        if Pconstraint != "":
            unified_instance["Aug_instruction"]["Additional_Instruction"]["Paragraph"] = Pconstraint

        if Sconstraint != "":    
            unified_instance["Aug_instruction"]["Additional_Instruction"]["Sentence"] = Sconstraint
        
        if Wconstraint != "":
            unified_instance["Aug_instruction"]["Additional_Instruction"]["Word"] = Wconstraint

        try:
            constraint = refined_keyword(d["messages"][1]["content"])
            unified_instance["Aug_instruction"]["Additional_Instruction"]["Keyword"] = constraint
        except:
            print("Warning: Keyword Extraction")

        constraint = refined_symbol(d["messages"][1]["content"])
        if constraint != "":
            unified_instance["Aug_instruction"]["Additional_Instruction"]["Punctuation"] = constraint

        for k in unified_instance["Aug_instruction"]["Additional_Instruction"].keys():
            if k not in count_constraints:
                count_constraints[k] = 0
            count_constraints[k] += 1

        unified_instance["cnt_id"] = i
        unified_data.append(unified_instance)

    print("Initialization completed.")

    for i,d in enumerate(tqdm(Rdata)):
        assert d["id"] == unified_data[i]["id"], print(d["id"], i, unified_data[i]["id"])
        assert d["request"]["result"]["success"] == True
        try:
            unified_data[i]["Aug_instruction"]["Refined_Instruction"] = eval(d["request"]["result"]["completions"])
        except:
            unified_data[i]["Aug_instruction"]["Refined_Instruction"] = d["request"]["result"]["completions"]

    print("Get refined_instruction.")

    for i,d in enumerate(Gdata):
        assert d["id"] == unified_data[i]["id"], print(d["id"], i, unified_data[i]["id"])
        assert d["request"]["result"]["success"] == True
        json_output = get_json_result(d["request"]["result"]["completions"])
        if json_output != "":
            for k,v in json_output.items():
                if v == "NULL":
                    continue
                # if k == "Desired_Writing_Style":
                #     continue
                if k not in count_constraints:
                    count_constraints[k] = 0
                count_constraints[k] += 1
                unified_data[i]["Aug_instruction"]["Additional_Instruction"][k] = v

    print("Get global_instruction.")

    symbols = ["******", "**", "*", "•", "1.", "-"]
    for i,d in enumerate(tqdm(Ldata)):
        assert d["id"] == unified_data[i]["id"], print(d["id"], i, unified_data[i]["id"])
        assert d["request"]["result"]["success"] == True
        json_output = get_json_result(d["request"]["result"]["completions"])
        if json_output != "":
            for k,v in json_output.items():
                Flag = True
                if v == "NULL":
                    continue
                if k == "Key_Formatting" or k == "Item_Listing_Details" or k == "Paragraphs_Constraints":
                    for s in symbols:
                        if s in v and s not in unified_data[i]["messages"][1]["content"]:
                            Flag = False
                            break
                if k == "Key_Formatting" and "no use of CAPITAL LETTERS" in v:
                    v = ",".join(v.split(",")[:-1]) + "."
                if Flag == False:
                    continue
                if k not in count_constraints:
                    count_constraints[k] = 0
                count_constraints[k] += 1
                unified_data[i]["Aug_instruction"]["Additional_Instruction"][k] = v

    print("Get local_instruction.")

    json.dump(
        unified_data,
        out_file,
        indent=4,
    )
    out_file.close()
    print("total_number:", len(unified_data))
    print("count_constraints:",count_constraints)
