
#============================ Part1 Filter Seed Data ==========================
python scripts/seed_data_generator/1_seed_alpaca_data.py \
    --output_dir data/seed_data \
    --min_length 200 \
    --diverse_rate 0.1

python scripts/seed_data_generator/1_seed_oasst2_data.py \
    --output_dir data/seed_data \
    --min_length 200 \
    --diverse_rate 0.1

python scripts/seed_data_generator/1_seed_orca-chat_data.py \
    --output_dir data/seed_data \
    --min_length 200 \
    --diverse_rate 0.1

python scripts/seed_data_generator/1_seed_WizardLM_data.py \
    --output_dir data/seed_data \
    --min_length 200 \
    --diverse_rate 0.1
