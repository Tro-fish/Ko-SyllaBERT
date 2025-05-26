# SyllaBERT

This project involves generating a synthetic noisy dataset and post-training a model.

---

## 1. Requirements
```
conda create -n syllabert python=3.9
conda activate syllabert
```

You can install the necessary packages using pip:
```bash
pip install -r requirements.txt
```
## 2. Syllable Model Pretraining
### Pretrain
Pretrain the syllable model
```bash
bash ./syllable_pretrain.sh
```

## 3. Noisy Dataset Post-training
### Make noisy dataset
Generate noisy dataset for post-training
```bash
python add_noise.py \
    --input_file data/post_train_example.txt \
    --output_file data/noisy_example.txt \
    --noise_percentage 0.2 \
```
### Post-train model
Post-training to make a noise-robust model
(Modify config settings appropriately)
```bash
bash ./noisy_post_train.sh
```
