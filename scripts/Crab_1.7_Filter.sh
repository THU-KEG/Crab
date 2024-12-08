#============================ Part5 Filter Similar Data and Constraints ==========================

python scripts/seed_data_generator/6_mix_filter.py \
    --datasets oasst2 \
    --input_dir data/seed_data/5 \
    --output_dir data/seed_data/6 \
    --output_file 6_oasst2_filter.json


python scripts/seed_data_generator/6_mix_filter.py \
    --datasets alpaca \
    --input_dir data/seed_data/5 \
    --output_dir data/seed_data/6 \
    --output_file 6_alpaca_filter.json

python scripts/seed_data_generator/6_mix_filter.py \
    --datasets orca_chat \
    --input_dir data/seed_data/5 \
    --output_dir data/seed_data/6 \
    --output_file 6_orca_chat_filter.json

python scripts/seed_data_generator/6_mix_filter.py \
    --datasets wizardLM \
    --input_dir data/seed_data/5 \
    --output_dir data/seed_data/6 \
    --output_file 6_wizardLM_filter.json
