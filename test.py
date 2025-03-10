# 2025/3/10 20:23
import torch
from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data import DataLoader
from model import SimpleCNN

def evaluate_model(model, test_loader, device):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    return accuracy

if __name__ == "__main__":
    # 定义数据预处理
    transform = transforms.Compose([
        transforms.Resize((75, 101)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # 加载测试集
    test_dataset = ImageFolder(root="dataset", transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # 加载模型
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleCNN(num_classes=len(test_dataset.classes)).to(device)
    model.load_state_dict(torch.load("mahjong_cnn.pth"))

    # 评估模型
    accuracy = evaluate_model(model, test_loader, device)
    print(f"测试集准确率: {accuracy:.2f}%")