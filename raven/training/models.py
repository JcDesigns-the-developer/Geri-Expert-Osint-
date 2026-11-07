from __future__ import annotations

import torch
from torch import nn


class GeoSceneCNN(nn.Module):
    """Small RAVEN-owned CNN trained from random initialization (track A)."""

    def __init__(self, num_classes: int, width: int = 32):
        super().__init__()
        self.features = nn.Sequential(
            self._block(3, width),
            self._block(width, width * 2),
            self._block(width * 2, width * 4),
            self._block(width * 4, width * 6),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.25),
            nn.Linear(width * 6, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.15),
            nn.Linear(256, num_classes),
        )

    @staticmethod
    def _block(in_channels: int, out_channels: int) -> nn.Sequential:
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def build_model(num_classes: int, mode: str, pretrained: bool = False) -> nn.Module:
    if mode == "scratch":
        if pretrained:
            raise ValueError("The from-scratch track cannot use pretrained weights.")
        return GeoSceneCNN(num_classes)

    if mode == "finetune":
        from torchvision.models import ResNet18_Weights, resnet18

        weights = ResNet18_Weights.DEFAULT if pretrained else None
        model = resnet18(weights=weights)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model

    raise ValueError(f"Unknown training mode: {mode}")
