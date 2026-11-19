import torch
import torch.nn as nn

class BirdCNN(nn.Module):
    """
    Lightweight CNN for bird audio classification.
    Input: mel spectrogram (1, 128, 188) — 1 channel, 128 mel bins, 188 time steps
    Output: one score per class (pass len(species_to_idx) from the dataset)
    """
    def __init__(self, num_classes):
        super().__init__()
        self.features = nn.Sequential(
            
            # Conv → BatchNorm → ReLU → Pool → repeat with more filters
            # Layer 1
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            # Block 4
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
    
if __name__ == "__main__":
    from birdaudio.config import SPECIES
    model = BirdCNN(num_classes=len(SPECIES))
    dummy = torch.randn(1, 1, 128, 188)
    output = model(dummy)
    print(f"Input: {dummy.shape}")
    print(f"Output: {output.shape}")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")