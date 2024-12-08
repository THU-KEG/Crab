#============================ Get Forword Data ==========================
python scripts/train_data_generator/Forward_data_generate.py \
    --datasets oasst2 alpaca wizardLM orca_chat \
    --min_number 6 \
    --max_number 8 \
    --add_weight 0.0 \
    --diverse_rate 0.3 \
    --ICL_rate 0.5 \
    --input_dir data/seed_data/6/ \
    --output_dir data/unified_data/ \
    --output_file forward_data.json

#============================ Get Reverse Data ==========================

python scripts/train_data_generator/Reverse_data_generate.py \
    --datasets oasst2 alpaca wizardLM orca_chat \
    --min_number 3 \
    --max_number 6 \
    --input_dir data/seed_data/6/ \
    --output_dir data/unified_data/ \
    --output_file reverse_data.json

# #============================ Get Combination Data ==========================

# Mistral-Crab-reconstruction
python scripts/train_data_generator/mix_forward_reverse.py \
    --forward_rate 0.70 \
    --max_num 13500 \
    --sharegpt_num 53000 \
    --forward_file data/unified_data/forward_data.json \
    --reverse_file data/unified_data/reverse_data.json \
    --sharegpt_file data/raw_data/ShareGPT_Vicuna_unfiltered/sharegpt_split.json \
    --word_limit 100000 \
    --dataset_limit 10000 \
    --output_dir data/train_data/Crab_dataset
