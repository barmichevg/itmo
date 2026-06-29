import random
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import accuracy_score, f1_score, classification_report


SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.set_num_threads(1)


class ActivityMLP(nn.Module):
    def __init__(self, input_dim=561, hidden_1=128, hidden_2=64, output_dim=6):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_1),
            nn.ReLU(),
            nn.Linear(hidden_1, hidden_2),
            nn.ReLU(),
            nn.Linear(hidden_2, output_dim)
        )

    def forward(self, x):
        return self.net(x)


def load_data():
    data_path = Path(__file__).resolve().parent / "data" / "har_preprocessed.npz"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Не найден файл: {data_path}\n"
            "Положите har_preprocessed.npz в папку data рядом со скриптом."
        )

    data = np.load(data_path, allow_pickle=True)

    X_train = torch.tensor(data["X_train"], dtype=torch.float32)
    y_train = torch.tensor(data["y_train"], dtype=torch.long)

    X_test = torch.tensor(data["X_test"], dtype=torch.float32)
    y_test = torch.tensor(data["y_test"], dtype=torch.long)

    class_names = data["class_names"].tolist()

    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=len(X_train),
        shuffle=True
    )

    test_loader = DataLoader(
        TensorDataset(X_test, y_test),
        batch_size=len(X_test),
        shuffle=False
    )

    return train_loader, test_loader, class_names


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()

    for X_batch, y_batch in loader:
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)

        optimizer.zero_grad()

        logits = model(X_batch)
        loss = criterion(logits, y_batch)

        loss.backward()
        optimizer.step()

        return loss.item()


def evaluate(model, loader, criterion, device):
    model.eval()

    preds_all = []
    targets_all = []
    total_loss = 0.0

    with torch.no_grad():
        for X_batch, y_batch in loader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)

            logits = model(X_batch)
            loss = criterion(logits, y_batch)

            preds = torch.argmax(logits, dim=1)

            total_loss += loss.item()
            preds_all.append(preds.cpu().numpy())
            targets_all.append(y_batch.cpu().numpy())

    preds_all = np.concatenate(preds_all)
    targets_all = np.concatenate(targets_all)

    accuracy = accuracy_score(targets_all, preds_all)
    macro_f1 = f1_score(targets_all, preds_all, average="macro")

    return total_loss, accuracy, macro_f1, targets_all, preds_all


def plot_history(history, title):
    epochs = [row["epoch"] for row in history]
    train_loss = [row["train_loss"] for row in history]
    test_loss = [row["test_loss"] for row in history]
    accuracy = [row["accuracy"] for row in history]
    macro_f1 = [row["macro_f1"] for row in history]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(epochs, train_loss, marker="o", markersize=3, label="train loss")
    axes[0].plot(epochs, test_loss, marker="o", markersize=3, label="test loss")
    axes[0].set_xlabel("Эпоха")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Функция потерь")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(epochs, accuracy, marker="o", markersize=3, label="accuracy")
    axes[1].plot(epochs, macro_f1, marker="o", markersize=3, label="macro F1")
    axes[1].set_xlabel("Эпоха")
    axes[1].set_ylabel("Значение метрики")
    axes[1].set_title("Качество на тестовой выборке")
    axes[1].grid(True)
    axes[1].legend()

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def main():
    train_loader, test_loader, class_names = load_data()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ActivityMLP().to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adagrad(
        model.parameters(),
        lr=0.1,
        eps=1e-10,
        weight_decay=1e-4
    )

    epochs = 50
    history = []

    print("ЗАДАНИЕ 3 — torch.optim.Adagrad")
    print("Параметры: lr=0.1, eps=1e-10, weight_decay=1e-4")
    print()

    for epoch in range(1, epochs + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        test_loss, acc, f1, _, _ = evaluate(model, test_loader, criterion, device)

        history.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "test_loss": test_loss,
            "accuracy": acc,
            "macro_f1": f1
        })

        if epoch == 1 or epoch % 5 == 0:
            print(
                f"Epoch {epoch:02d}/{epochs}: "
                f"train_loss={train_loss:.4f}, "
                f"test_loss={test_loss:.4f}, "
                f"accuracy={acc:.4f}, "
                f"macro_f1={f1:.4f}"
            )

    test_loss, acc, f1, y_true, y_pred = evaluate(model, test_loader, criterion, device)

    print()
    print("Итоговые результаты:")
    print(f"Test loss: {test_loss:.4f}")
    print(f"Accuracy : {acc:.4f}")
    print(f"Macro F1 : {f1:.4f}")
    print()
    print(classification_report(y_true, y_pred, target_names=class_names, digits=4))

    plot_history(history, "Обучение модели с torch.optim.Adagrad")


if __name__ == "__main__":
    main()