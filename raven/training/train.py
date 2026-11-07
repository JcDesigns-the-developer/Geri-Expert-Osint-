from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from models import build_model


def seed_everything(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def run_epoch(model, loader, criterion, device, optimizer=None):
    training = optimizer is not None
    model.train(training)
    total_loss = 0.0
    correct = 0
    count = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        if training:
            optimizer.zero_grad(set_to_none=True)
        with torch.set_grad_enabled(training):
            logits = model(images)
            loss = criterion(logits, labels)
            if training:
                loss.backward()
                optimizer.step()
        total_loss += loss.item() * labels.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
        count += labels.size(0)
    return {"loss": total_loss / max(count, 1), "accuracy": correct / max(count, 1), "samples": count}


def main():
    parser = argparse.ArgumentParser(description="Train a RAVEN geographic scene classifier.")
    parser.add_argument("--data", type=Path, required=True, help="Root with train/, val/, and test/ folders.")
    parser.add_argument("--mode", choices=("scratch", "finetune"), default="scratch")
    parser.add_argument("--pretrained", action="store_true", help="Explicitly download/use torchvision pretrained weights.")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    if args.epochs < 1 or args.batch_size < 1:
        parser.error("--epochs and --batch-size must be positive")
    seed_everything(args.seed)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ])
    datasets_by_split = {}
    for split in ("train", "val", "test"):
        folder = args.data / split
        if not folder.is_dir():
            parser.error(f"Missing dataset split: {folder}")
        datasets_by_split[split] = datasets.ImageFolder(folder, transform=transform)

    classes = datasets_by_split["train"].classes
    if len(classes) < 2:
        parser.error("At least two class folders are required.")
    for split, dataset in datasets_by_split.items():
        if dataset.classes != classes:
            parser.error(f"Class folders in {split}/ must exactly match train/: {classes}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loaders = {
        split: DataLoader(ds, batch_size=args.batch_size, shuffle=(split == "train"),
                          num_workers=0, pin_memory=(device.type == "cuda"))
        for split, ds in datasets_by_split.items()
    }

    model = build_model(len(classes), args.mode, args.pretrained).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    args.output.mkdir(parents=True, exist_ok=True)

    history = []
    best_val = -1.0
    started = time.time()
    for epoch in range(1, args.epochs + 1):
        train_metrics = run_epoch(model, loaders["train"], criterion, device, optimizer)
        val_metrics = run_epoch(model, loaders["val"], criterion, device)
        row = {"epoch": epoch, "train": train_metrics, "validation": val_metrics}
        history.append(row)
        print(json.dumps(row))
        if val_metrics["accuracy"] > best_val:
            best_val = val_metrics["accuracy"]
            torch.save({
                "state_dict": model.state_dict(),
                "classes": classes,
                "mode": args.mode,
                "pretrained": args.pretrained,
                "input_size": [224, 224],
                "normalization": {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]},
            }, args.output / "best_model.pt")

    checkpoint = torch.load(args.output / "best_model.pt", map_location=device, weights_only=False)
    model.load_state_dict(checkpoint["state_dict"])
    test_metrics = run_epoch(model, loaders["test"], criterion, device)
    report = {
        "project": "RAVEN", "mode": args.mode, "pretrained": args.pretrained,
        "classes": classes, "seed": args.seed, "epochs": args.epochs,
        "best_validation_accuracy": best_val, "held_out_test": test_metrics,
        "elapsed_seconds": round(time.time() - started, 2),
        "warning": "Metrics are valid only if geographic areas and near-duplicate sources are disjoint across splits.",
        "history": history,
    }
    (args.output / "evaluation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"test": test_metrics, "report": str(args.output / "evaluation.json")}))


if __name__ == "__main__":
    main()
