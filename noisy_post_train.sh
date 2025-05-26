#!/bin/bash

# define user-specified configs (change these on a new machine)
export BATCH_SIZE=128
export ACCUMULATE=36
export MAX_STEPS=12500
export WARMUP_STEPS=2400
export LOG_STEPS=10
export SAVE_STPES=90
export EVAL_STPES=90

export WANDB_API_KEY=YOUR_KEY
export WANDB_PROJECT=Roberta-pretrain
export prefix=YOUR_PATH_TO_PRETRAIN
export CACHE_DIR=${prefix}"/cache"
export OUTPUT_DIR=${prefix}"/ckpt/pretrain"
export CKPT_TO_RESUME=${prefix}"ckpt/pretrain/checkpoint-90"

export MODEL=configs/roberta_base_128.json
export TOKENIZER=my_custom_tokenizer
export PT_DATASET=JackBAI/bert_pretrain_datasets
export DS_CONFIG=configs/ds_config_stage2.json
export PT_PEAK_LR=1e-3

# define fixed configs (don't change)
export PT_ADAM_EPS=1e-6
export PT_ADAM_BETA1=0.9
export PT_ADAM_BETA2=0.98
export PT_ADAM_WEIGHT_DECAY=0.01
export PT_LR_DECAY=linear

# Set CUDA for 2 GPUs
export CUDA_VISIBLE_DEVICES=0

# uncomment the line below and remove to below 'run_mlm.py' to resume from a checkpoint
      
python run_mlm.py \
    --resume_from_checkpoint $CKPT_TO_RESUME \
    --report_to wandb \
    --config_name $MODEL \
    --tokenizer_name $TOKENIZER \
    --train_file data/noisy_example.txt \
    --max_steps $MAX_STEPS \
    --preprocessing_num_workers 18 \
    --logging_steps $LOG_STEPS \
    --save_strategy steps \
    --save_steps $SAVE_STPES \
    --evaluation_strategy steps \
    --eval_steps $EVAL_STPES \
    --save_total_limit 1 \
    --load_best_model_at_end true \
    --metric_for_best_model loss \
    --greater_is_better false \
    --fp16 \
    --cache_dir $CACHE_DIR \
    --per_device_train_batch_size $BATCH_SIZE \
    --per_device_eval_batch_size $BATCH_SIZE \
    --gradient_accumulation_steps $ACCUMULATE \
    --adam_epsilon $PT_ADAM_EPS \
    --adam_beta1 $PT_ADAM_BETA1 \
    --adam_beta2 $PT_ADAM_BETA2 \
    --weight_decay $PT_ADAM_WEIGHT_DECAY \
    --warmup_steps $WARMUP_STEPS \
    --learning_rate $PT_PEAK_LR \
    --lr_scheduler_type $PT_LR_DECAY \
    --max_seq_length 512 \
    --do_train \
    --do_eval \
    --output_dir $OUTPUT_DIR \
    --overwrite_output_dir