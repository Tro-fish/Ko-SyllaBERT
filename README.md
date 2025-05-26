# Ko-SyllaBERT

A official implementation of **generating a synthetic noisy dataset** and **post-training a model**, as introduced in our paper:

> **Ko-SyllaBERT: A Syllable-Based Efficient and Robust Korean Language Model for Real-World Noise and Typographical Errors** 
---

## Methodology Overview

<div align="center">
<img src="https://github.com/user-attachments/assets/fb773a60-5bb3-4ef3-8172-6a9308355f3f" width="100%" alt="Framework overview"/>
</div>

Overview of the Ko-SyllaBERT training pipeline. The model is trained in two stages. In Stage 1 (Pre-training), an efficient syllable vocabulary is constructed and used to train a lightweight BERT model with reduced token embedding and hidden sizes. In Stage 2 (Post-training), the model is further trained on synthetically generated Korean noisy data with typographical errors to enhance robustness in real-world settings.

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
To pretrain the syllable-based model, prepare a single .txt file containing your training data (e.g., data/pretrain_example.txt).

Run the following script to start pretraining:
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
