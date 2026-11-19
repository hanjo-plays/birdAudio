import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

from birdaudio.config import PROCESSED_DIR


class BirdDataset(Dataset):
    def __init__(self, file_paths, labels):
        self.file_paths = file_paths
        self.labels = labels

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        # Load spectrogram and add channel dimension (1, 128, 188)
        mel_spec = np.load(self.file_paths[idx])
        mel_spec = torch.FloatTensor(mel_spec).unsqueeze(0)
        label = self.labels[idx]
        return mel_spec, label


def load_dataset(processed_dir=PROCESSED_DIR):
    """Walk through processed folder, collect file paths and labels."""
    file_paths = []
    labels = []
    species_list = sorted([
        d for d in os.listdir(processed_dir)
        if os.path.isdir(os.path.join(processed_dir, d))
    ])

    # Map species name to integer label
    species_to_idx = {name: idx for idx, name in enumerate(species_list)}

    for species in species_list:
        species_dir = os.path.join(processed_dir, species)
        for f in os.listdir(species_dir):
            if f.endswith('.npy'):
                file_paths.append(os.path.join(species_dir, f))
                labels.append(species_to_idx[species])

    return file_paths, labels, species_to_idx


def create_dataloaders(processed_dir=PROCESSED_DIR,batch_size=32, test_size=0.15, val_size=0.15):
    """Create train, val, test dataloaders."""
    file_paths, labels, species_to_idx = load_dataset(processed_dir)

    # First split: separate test set
    train_val_paths, test_paths, train_val_labels, test_labels = train_test_split(
        file_paths, labels, test_size=test_size, stratify=labels, random_state=42
    )

    # Second split: separate validation from training
    val_ratio = val_size / (1 - test_size)
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        train_val_paths, train_val_labels, test_size=val_ratio, stratify=train_val_labels, random_state=42
    )

    train_dataset = BirdDataset(train_paths, train_labels)
    val_dataset = BirdDataset(val_paths, val_labels)
    test_dataset = BirdDataset(test_paths, test_labels)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    print(f"Species: {len(species_to_idx)}")
    print(f"Train: {len(train_dataset)}, Val: {len(val_dataset)}, Test: {len(test_dataset)}")

    return train_loader, val_loader, test_loader, species_to_idx


if __name__ == "__main__":
    train_loader, val_loader, test_loader, species_to_idx = create_dataloaders()
    print(f"\nSpecies mapping:")
    for name, idx in species_to_idx.items():
        print(f"  {idx}: {name}")