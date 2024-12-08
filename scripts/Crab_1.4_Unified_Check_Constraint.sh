#============================ Check Constraints ==========================

python scripts/seed_data_generator/4_constraints_check.py \
    --input_file data/seed_data/3/3_oasst2_constraints.json \
    --output_dir data/seed_data/4 \
    --output_file 4_oasst2_check.json

python scripts/seed_data_generator/4_constraints_check.py \
    --input_file data/seed_data/3/3_alpaca_constraints.json \
    --output_dir data/seed_data/4 \
    --output_file 4_alpaca_check.json

python scripts/seed_data_generator/4_constraints_check.py \
    --input_file data/seed_data/3/3_orca_chat_constraints.json \
    --output_dir data/seed_data/4 \
    --output_file 4_orca_chat_check.json

python scripts/seed_data_generator/4_constraints_check.py \
    --input_file data/seed_data/3/3_wizardLM_constraints.json \
    --output_dir data/seed_data/4 \
    --output_file 4_wizardLM_check.json

