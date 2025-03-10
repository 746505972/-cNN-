# 2025/3/10 20:02
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from model import SimpleCNN
from data_preprocessing import load_dataset
import torch.nn as nn

def train_model(data_dir, num_epochs=10, batch_size=32, lr=0.001):
    # 加载数据集
    dataset = load_dataset(data_dir)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # 创建模型
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleCNN(num_classes=len(dataset.classes)).to(device)

    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # 训练循环
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / len(dataloader):.4f}")

    # 保存模型
    torch.save(model.state_dict(), "mahjong_cnn.pth")
    print("训练完成，模型已保存！")


if __name__ == "__main__":
    train_model(data_dir="augmented_dataset")
