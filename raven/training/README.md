# RAVEN model training

RAVEN deliberately separates two learning tracks:

1. **From-scratch models (A):** small CNNs trained from random initialization to classify broad, non-sensitive geographic scene attributes such as terrain class, road environment, vegetation zone, and built-environment style.
2. **Custom-trained vision models (B):** permitted pretrained visual backbones adapted to RAVEN's labeled feature tasks. Pretrained weights are optional and must be documented in each model card.

Do not train on private-person tracking data, private residences, or scraped personal photo collections. Use public-place imagery with documented provenance and usage rights.

## Dataset layout

Use ImageFolder-compatible labels with geographic leakage controls:

```text
dataset/
  train/
    rural_flat/
    coastal_urban/
    forested_hills/
  val/
    rural_flat/
    coastal_urban/
    forested_hills/
  test/
    rural_flat/
    coastal_urban/
    forested_hills/
```

The split must be made by geographic area or source collection, not random neighboring photos. Near-duplicate images and images from the same panorama/session must never cross splits.

## Install and train

```powershell
pip install -r training\requirements.txt
python training\train.py --data dataset --mode scratch --epochs 25
```

For transfer learning, install compatible torchvision weights and explicitly opt in:

```powershell
python training\train.py --data dataset --mode finetune --pretrained --epochs 10
```

The pretrained option may download ResNet-18 weights. Training from scratch requires no model download. A resulting classifier is only as reliable as its labels, coverage, and held-out evaluation.
