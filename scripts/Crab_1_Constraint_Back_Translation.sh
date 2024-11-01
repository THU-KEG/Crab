#============================ Part2 Unified Data Format: Constraint Bact-Translation ==========================
python scripts/seed_data_generator/2_unified_data_refined_instruction.py \
    --input_file data/seed_data/1_alpaca.json \
    --output_dir data/seed_data \
    --output_file 2_alpaca_llama_format_refined_instruction.json \
    --num_sample 20000 \

python scripts/seed_data_generator/2_unified_data_refined_instruction.py \
    --input_file data/seed_data/1_oasst2.json \
    --output_dir data/seed_data \
    --output_file 2_oasst2_llama_format_refined_instruction.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_refined_instruction.py \
    --input_file data/seed_data/1_orca_chat.json \
    --output_dir data/seed_data \
    --output_file 2_orca_chat_llama_format_refined_instruction.json \
    --num_sample 20000 \

python scripts/seed_data_generator/2_unified_data_refined_instruction.py \
    --input_file data/seed_data/1_wizardLM.json \
    --output_dir data/seed_data \
    --output_file 2_wizardLM_llama_format_refined_instruction.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_global.py \
    --input_file data/seed_data/1_alpaca.json \
    --output_dir data/seed_data \
    --output_file 2_alpaca_llama_format_additional_global.json \
    --num_sample 20000 \

python scripts/seed_data_generator/2_unified_data_additional_global.py \
    --input_file data/seed_data/1_oasst2.json \
    --output_dir data/seed_data \
    --output_file 2_oasst2_llama_format_additional_global.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_global.py \
    --input_file data/seed_data/1_orca_chat.json \
    --output_dir data/seed_data \
    --output_file 2_orca_chat_llama_format_additional_global.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_global.py \
    --input_file data/seed_data/1_wizardLM.json \
    --output_dir data/seed_data \
    --output_file 2_wizardLM_llama_format_additional_global.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_local.py \
    --input_file data/seed_data/1_alpaca.json \
    --output_dir data/seed_data \
    --output_file 2_alpaca_llama_format_additional_local.json \
    --num_sample 20000 \

python scripts/seed_data_generator/2_unified_data_additional_local.py \
    --input_file data/seed_data/1_oasst2.json \
    --output_dir data/seed_data \
    --output_file 2_oasst2_llama_format_additional_local.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_local.py \
    --input_file data/seed_data/1_orca_chat.json \
    --output_dir data/seed_data \
    --output_file 2_orca_chat_llama_format_additional_local.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_local.py \
    --input_file data/seed_data/1_wizardLM.json \
    --output_dir data/seed_data \
    --output_file 2_wizardLM_llama_format_additional_local.json \
    --num_sample 20000 


#============================ Part3 Constraint Bact-Translation ==========================

LLM_Path='' # Your Llama-3-70B-Instruct Local Path

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_alpaca_llama_format_refined_instruction.json \
    --output_file data/seed_data/2_alpaca_llama_format_refined_instruction.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_oasst2_llama_format_refined_instruction.json \
    --output_file data/seed_data/2_oasst2_llama_format_refined_instruction.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_orca_chat_llama_format_refined_instruction.json \
    --output_file data/seed_data/2_orca_chat_llama_format_refined_instruction.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_wizardLM_llama_format_refined_instruction.json \
    --output_file data/seed_data/2_wizardLM_llama_format_refined_instruction.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format


CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_alpaca_llama_format_additional_global.json \
    --output_file data/seed_data/2_alpaca_llama_format_additional_global.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_oasst2_llama_format_additional_global.json \
    --output_file data/seed_data/2_oasst2_llama_format_additional_global.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format


CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_orca_chat_llama_format_additional_global.json \
    --output_file data/seed_data/2_orca_chat_llama_format_additional_global.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format


CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_wizardLM_llama_format_additional_global.json \
    --output_file data/seed_data/2_wizardLM_llama_format_additional_global.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_oasst2_llama_format_additional_local.json \
    --output_file data/seed_data/2_oasst2_llama_format_additional_local.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format


CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_alpaca_llama_format_additional_local.json \
    --output_file data/seed_data/2_alpaca_llama_format_additional_local.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format


CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_orca_chat_llama_format_additional_local.json \
    --output_file data/seed_data/2_orca_chat_llama_format_additional_local.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format


CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/2_wizardLM_llama_format_additional_local.json \
    --output_file data/seed_data/2_wizardLM_llama_format_additional_local.json \
    --batch_size 8 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format
    
#============================ Part4 Unified Format of Generated Constraints ==========================

python scripts/seed_data_generator/3_llama3_unified_constraints.py \
    --origin_file data/seed_data/1_oasst2.json \
    --refined_instruction_file data/seed_data/2_oasst2_llama_format_refined_instruction.json \
    --global_instruction_file data/seed_data/2_oasst2_llama_format_additional_global.json \
    --local_instruction_file data/seed_data/2_oasst2_llama_format_additional_local.json \
    --output_dir data/seed_data \
    --output_file 3_oasst2_constraints.json

python scripts/seed_data_generator/3_llama3_unified_constraints.py \
    --origin_file data/seed_data/1_alpaca.json \
    --refined_instruction_file data/seed_data/2_alpaca_llama_format_refined_instruction.json \
    --global_instruction_file data/seed_data/2_alpaca_llama_format_additional_global.json \
    --local_instruction_file data/seed_data/2_alpaca_llama_format_additional_local.json \
    --output_dir data/seed_data \
    --output_file 3_alpaca_constraints.json


python scripts/seed_data_generator/3_llama3_unified_constraints.py \
    --origin_file data/seed_data/1_orca_chat.json \
    --refined_instruction_file data/seed_data/2_orca_chat_llama_format_refined_instruction.json \
    --global_instruction_file data/seed_data/2_orca_chat_llama_format_additional_global.json \
    --local_instruction_file data/seed_data/2_orca_chat_llama_format_additional_local.json \
    --output_dir data/seed_data \
    --output_file 3_orca_chat_constraints.json

python scripts/seed_data_generator/3_llama3_unified_constraints.py \
    --origin_file data/seed_data/1_wizardLM.json \
    --refined_instruction_file data/seed_data/2_wizardLM_llama_format_refined_instruction.json \
    --global_instruction_file data/seed_data/2_wizardLM_llama_format_additional_global.json \
    --local_instruction_file data/seed_data/2_wizardLM_llama_format_additional_local.json \
    --output_dir data/seed_data \
    --output_file 3_wizardLM_constraints.json

#============================ Part5 Filter Similar Data and Constraints ==========================

python scripts/seed_data_generator/4_mix_filter.py \
    --datasets oasst2 \
    --input_dir data/seed_data \
    --output_dir data/seed_data \
    --output_file 4_oasst2_filter.json


python scripts/seed_data_generator/4_mix_filter.py \
    --datasets wizardLM \
    --input_dir data/seed_data \
    --output_dir data/seed_data \
    --output_file 4_wizardLM_filter.json

python scripts/seed_data_generator/4_mix_filter.py \
    --datasets alpaca \
    --input_dir data/seed_data \
    --output_dir data/seed_data \
    --output_file 4_alpaca_filter.json

python scripts/seed_data_generator/4_mix_filter.py \
    --datasets orca_chat \
    --input_dir data/seed_data \
    --output_dir data/seed_data \
    --output_file 4_orca_chat_filter.json

#============================ Part6 Check Constraints ==========================

python scripts/seed_data_generator/5_constraints_check.py \
    --input_file data/seed_data/4_oasst2_filter.json \
    --output_dir data/seed_data \
    --output_file 5_oasst2_check.json

python scripts/seed_data_generator/5_constraints_check.py \
    --input_file data/seed_data/4_alpaca_filter.json \
    --output_dir data/seed_data \
    --output_file 5_alpaca_check.json

python scripts/seed_data_generator/5_constraints_check.py \
    --input_file data/seed_data/4_orca_chat_filter.json \
    --output_dir data/seed_data \
    --output_file 5_orca_chat_check.json

python scripts/seed_data_generator/5_constraints_check.py \
    --input_file data/seed_data/4_wizardLM_filter.json \
    --output_dir data/seed_data \
    --output_file 5_wizardLM_check.json

#============================ Part7 Generate Check Constraints ==========================

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/5_oasst2_check.json \
    --output_file data/seed_data/5_oasst2_check.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/5_alpaca_check.json \
    --output_file data/seed_data/5_alpaca_check.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/5_orca_chat_check.json \
    --output_file data/seed_data/5_orca_chat_check.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

CUDA_VISIBLE_DEVICES=0,1,2,3 python eval/predict.py \
    --model_name_or_path ${LLM_Path} \
    --input_files data/seed_data/5_wizardLM_check.json \
    --output_file data/seed_data/5_wizardLM_check.json \
    --batch_size 4 \
    --use_vllm \
    --top_p 0.3 \
    --temperature 0.4 \
    --do_sample \
    --use_chat_format \
    --chat_formatting_function eval.templates.create_prompt_with_llama3_chat_format

#============================ Part8 Unified Check Constraints ==========================

python scripts/seed_data_generator/6_res_constraints_check.py \
    --dataset oasst2 \
    --original_file data/seed_data/4_oasst2_filter.json \
    --input_file data/seed_data/5_oasst2_check.json \
    --output_dir data/seed_data \
    --output_file 6_oasst2_constraints.json

python scripts/seed_data_generator/6_res_constraints_check.py \
    --dataset alpaca \
    --original_file data/seed_data/4_alpaca_filter.json \
    --input_file data/seed_data/5_alpaca_check.json \
    --output_dir data/seed_data \
    --output_file 6_alpaca_constraints.json

python scripts/seed_data_generator/6_res_constraints_check.py \
    --dataset orca_chat \
    --original_file data/seed_data/4_orca_chat_filter.json \
    --input_file data/seed_data/5_orca_chat_check.json \
    --output_dir data/seed_data \
    --output_file 6_orca_chat_constraints.json

python scripts/seed_data_generator/6_res_constraints_check.py \
    --dataset wizardLM \
    --original_file data/seed_data/4_wizardLM_filter.json \
    --input_file data/seed_data/5_wizardLM_check.json \
    --output_dir data/seed_data \
    --output_file 6_wizardLM_constraints.json

#============================ Congratulations! You have obtained the complete list of constraints. ==========================