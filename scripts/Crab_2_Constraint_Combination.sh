#============================ Get Forword Data ==========================
python scripts/train_data_generator/forward_generate.py \
    --datasets oasst2 alpaca wizardLM orca_chat \
    --min_number 6 \
    --max_number 8 \
    --add_weight 0.0 \
    --diverse_rate 0.3 \
    --ICL_rate 0.5 \
    --input_dir data/seed_data/ \
    --output_dir data/unified_data/ \
    --output_file forward_data.json

#============================ Get Reverse Data ==========================


python scripts/train_data_generator/reverse_data.py \
    --datasets oasst2 alpaca wizardLM orca_chat \
    --min_number 3 \
    --max_number -1 \
    --output_dir data/unified_data/ \
    --output_file reverse_data.json

python scripts/train_data_generator/reverse_data_fewshot.py \
    --datasets oasst2 alpaca wizardLM orca_chat \
    --min_number 3 \
    --max_number -1 \
    --output_dir data/unified_data/ \
    --output_file fewshot_reverse_data.json

#============================ Get Combination Data ==========================

python scripts/train_data_generator/mix_forward_reverse_o.py \
    --forward_rate 0.75 \
    --max_num 13000 \
    --fewshot_num 500 \
    --sharegpt_num 53000 \
    --forward_file data/unified_data/forward_data.json \
    --reverse_file data/unified_data/reverse_data.json \
    --fewshot_file data/unified_data/fewshot_reverse_data.json \
    --sharegpt_file data/raw_data/ShareGPT_Vicuna_unfiltered/sharegpt_split.json \
    --forward_shuffle \
    --word_limit 100000 \
    --dataset_limit 4500 \
    --output_dir data/train_data/Crab_dataset.json
