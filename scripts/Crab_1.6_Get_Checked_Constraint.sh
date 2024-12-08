
# #============================ Unified Check Constraints ==========================

python scripts/seed_data_generator/5_res_constraints_check.py \
    --dataset oasst2 \
    --original_file data/seed_data/3/3_oasst2_constraints.json \
    --input_file data/seed_data/4/4_oasst2_check.json \
    --output_dir data/seed_data/5 \
    --output_file 5_oasst2_constraints.json

python scripts/seed_data_generator/5_res_constraints_check.py \
    --dataset alpaca \
    --original_file data/seed_data/3/3_alpaca_constraints.json \
    --input_file data/seed_data/4/4_alpaca_check.json \
    --output_dir data/seed_data/5 \
    --output_file 5_alpaca_constraints.json

python scripts/seed_data_generator/5_res_constraints_check.py \
    --dataset orca_chat \
    --original_file data/seed_data/3/3_orca_chat_constraints.json \
    --input_file data/seed_data/4/4_orca_chat_check.json \
    --output_dir data/seed_data/5 \
    --output_file 5_orca_chat_constraints.json

python scripts/seed_data_generator/5_res_constraints_check.py \
    --dataset wizardLM \
    --original_file data/seed_data/3/3_wizardLM_constraints.json \
    --input_file data/seed_data/4/4_wizardLM_check.json \
    --output_dir data/seed_data/5 \
    --output_file 5_wizardLM_constraints.json
