#================= Unified Format of Generated Constraints ==========================

python scripts/seed_data_generator/3_llama3_unified_constraints.py \
    --origin_file data/seed_data/1/1_oasst2.json \
    --refined_instruction_file data/seed_data/2/2_oasst2_llama_format_refined_instruction.json \
    --global_instruction_file data/seed_data/2/2_oasst2_llama_format_additional_global.json \
    --local_instruction_file data/seed_data/2/2_oasst2_llama_format_additional_local.json \
    --output_dir data/seed_data/3 \
    --output_file 3_oasst2_constraints.json

python scripts/seed_data_generator/3_llama3_unified_constraints.py \
    --origin_file data/seed_data/1/1_alpaca.json \
    --refined_instruction_file data/seed_data/2/2_alpaca_llama_format_refined_instruction.json \
    --global_instruction_file data/seed_data/2/2_alpaca_llama_format_additional_global.json \
    --local_instruction_file data/seed_data/2/2_alpaca_llama_format_additional_local.json \
    --output_dir data/seed_data/3 \
    --output_file 3_alpaca_constraints.json


python scripts/seed_data_generator/3_llama3_unified_constraints.py \
    --origin_file data/seed_data/1/1_orca_chat.json \
    --refined_instruction_file data/seed_data/2/2_orca_chat_llama_format_refined_instruction.json \
    --global_instruction_file data/seed_data/2/2_orca_chat_llama_format_additional_global.json \
    --local_instruction_file data/seed_data/2/2_orca_chat_llama_format_additional_local.json \
    --output_dir data/seed_data/3 \
    --output_file 3_orca_chat_constraints.json

python scripts/seed_data_generator/3_llama3_unified_constraints.py \
    --origin_file data/seed_data/1/1_wizardLM.json \
    --refined_instruction_file data/seed_data/2/2_wizardLM_llama_format_refined_instruction.json \
    --global_instruction_file data/seed_data/2/2_wizardLM_llama_format_additional_global.json \
    --local_instruction_file data/seed_data/2/2_wizardLM_llama_format_additional_local.json \
    --output_dir data/seed_data/3 \
    --output_file 3_wizardLM_constraints.json
