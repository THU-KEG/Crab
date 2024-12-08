
#============================ Generate Check Constraints ==========================

LLM_Path='/data3/MODELS/Meta-Llama-3-70B-Instruct' # Your Llama-3-70B-Instruct Local Path
CUDA='1,2,5,7'

CUDA_VISIBLE_DEVICES=${CUDA} python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/4/test.json \
    --output_file data/seed_data/4/test.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=${CUDA} python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/4/4_oasst2_check.json \
    --output_file data/seed_data/4/4_oasst2_check.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=${CUDA} python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/4/4_alpaca_check.json \
    --output_file data/seed_data/4/4_alpaca_check.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=${CUDA} python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/4/4_orca_chat_check.json \
    --output_file data/seed_data/4/4_orca_chat_check.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=${CUDA} python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/4/4_wizardLM_check.json \
    --output_file data/seed_data/4/4_wizardLM_check.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

