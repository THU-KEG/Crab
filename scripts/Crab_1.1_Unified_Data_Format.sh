#========= Unified Data Format: Constraint Bact-Translation ==============
python scripts/seed_data_generator/2_unified_data_refined_instruction.py \
    --input_file data/seed_data/1/1_alpaca.json \
    --output_dir data/seed_data/2 \
    --output_file 2_alpaca_llama_format_refined_instruction.json \
    --num_sample 20000 \

python scripts/seed_data_generator/2_unified_data_refined_instruction.py \
    --input_file data/seed_data/1/1_oasst2.json \
    --output_dir data/seed_data/2 \
    --output_file 2_oasst2_llama_format_refined_instruction.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_refined_instruction.py \
    --input_file data/seed_data/1/1_orca_chat.json \
    --output_dir data/seed_data/2 \
    --output_file 2_orca_chat_llama_format_refined_instruction.json \
    --num_sample 20000 \

python scripts/seed_data_generator/2_unified_data_refined_instruction.py \
    --input_file data/seed_data/1/1_wizardLM.json \
    --output_dir data/seed_data/2 \
    --output_file 2_wizardLM_llama_format_refined_instruction.json \
    --num_sample 20000 


python scripts/seed_data_generator/2_unified_data_additional_global.py \
    --input_file data/seed_data/1/1_alpaca.json \
    --output_dir data/seed_data/2 \
    --output_file 2_alpaca_llama_format_additional_global.json \
    --num_sample 20000 \

python scripts/seed_data_generator/2_unified_data_additional_global.py \
    --input_file data/seed_data/1/1_oasst2.json \
    --output_dir data/seed_data/2 \
    --output_file 2_oasst2_llama_format_additional_global.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_global.py \
    --input_file data/seed_data/1/1_orca_chat.json \
    --output_dir data/seed_data/2 \
    --output_file 2_orca_chat_llama_format_additional_global.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_global.py \
    --input_file data/seed_data/1/1_wizardLM.json \
    --output_dir data/seed_data/2 \
    --output_file 2_wizardLM_llama_format_additional_global.json \
    --num_sample 20000 


python scripts/seed_data_generator/2_unified_data_additional_local.py \
    --input_file data/seed_data/1/1_alpaca.json \
    --output_dir data/seed_data/2 \
    --output_file 2_alpaca_llama_format_additional_local.json \
    --num_sample 20000 \

python scripts/seed_data_generator/2_unified_data_additional_local.py \
    --input_file data/seed_data/1/1_oasst2.json \
    --output_dir data/seed_data/2 \
    --output_file 2_oasst2_llama_format_additional_local.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_local.py \
    --input_file data/seed_data/1/1_orca_chat.json \
    --output_dir data/seed_data/2 \
    --output_file 2_orca_chat_llama_format_additional_local.json \
    --num_sample 20000 

python scripts/seed_data_generator/2_unified_data_additional_local.py \
    --input_file data/seed_data/1/1_wizardLM.json \
    --output_dir data/seed_data/2 \
    --output_file 2_wizardLM_llama_format_additional_local.json \
    --num_sample 20000 
