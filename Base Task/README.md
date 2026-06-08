# FashionNet — Fashion-MNIST Classifier

A custom branching neural network built from scratch in PyTorch to classify Fashion-MNIST images into 10 clothing categories.

---

## What it does

FashionNet takes 28×28 grayscale images of clothing items and classifies them into one of 10 categories (T-shirt, Trouser, Pullover, etc.). It uses a custom dual-branch architecture where the network splits into two parallel paths after the first hidden layer, then merges the outputs before the final classification.

---

## Architecture

The network is a custom branching MLP (Multi-Layer Perceptron):

```
Input (784) → Trunk (16) → Branch 1: 16 → 8 → 8 (+ skip connection)
                         → Branch 2: 16 → 12 → 8
                         → Concat (16) → Output (10)
```

Branch 1 uses a residual-style skip connection — the output of the first step is added to the output of the second step before merging.

---

## Results

| Metric | Value |
|---|---|
| Validation Accuracy | **86.16%** |
| Epochs | 5 |
| Optimizer | Adam (lr = 0.001) |
| Loss function | CrossEntropyLoss |

---

## Tech Stack

- Python
- PyTorch (`torch`, `torchvision`)
- Matplotlib — loss and accuracy plots
- Pandas — CSV export
- Google Colab — training environment

---

## Dataset

Fashion-MNIST — 70,000 grayscale images (28×28), 10 classes.

| Split | Size |
|---|---|
| Training | 50,000 |
| Validation | 10,000 |
| Test | 10,000 |

Pixel values normalized using mean = 0.2860, std = 0.3530.

---

## Project Structure

```
├── fashionnet.ipynb       # Main notebook (data loading, model, training, evaluation)
├── plots.png              # Training and validation loss/accuracy curves
├── model_weights.pkl      # Saved model weights
└── submission.csv         # Test set predictions (ImageId, label)
```

---

## How it works

1. **Data loading** — Fashion-MNIST is downloaded via `torchvision.datasets`, normalized, and loaded in batches of 64.

2. **Model** — FashionNet is a branching MLP. After the trunk layer, the network splits into two branches of different widths, then their outputs are concatenated and passed to the final output layer.

3. **Training** — Trained for 5 epochs using Adam and CrossEntropyLoss. Training and validation loss/accuracy are tracked each epoch and plotted.

4. **Evaluation** — The model is evaluated on the test set and predictions are exported to `submission.csv`.

5. **Saving weights** — Model weights are saved using `pickle` for later reuse.
