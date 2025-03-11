# 2025/3/10 20:05
import torch
from PIL import Image
from model import SimpleCNN
from data_preprocessing import load_dataset
from torchvision import transforms

def predict_image(image_path, model_path, data_dir):
    # 加载数据集以获取类别信息
    dataset = load_dataset(data_dir)
    class_to_idx = dataset.class_to_idx
    idx_to_class = {v: k for k, v in class_to_idx.items()}

    # 加载模型
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleCNN(num_classes=len(dataset.classes)).to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # 加载并预处理图像
    transform = transforms.Compose([
        transforms.Resize((75, 101)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    # 预测
    with torch.no_grad():
        output = model(image)
        predicted_class = torch.argmax(output, dim=1).item()

    print(f"预测类别: {idx_to_class[predicted_class]}")
# 2025/3/10 20:0500
if __name__ == "__main__":
    predict_image(
        image_path=r"E:\HuaweiMoveData\Users\刘振宸\Documents\Tencent Files\2894044135\nt_qq\nt_data\Pic\2025-03\Ori\5f0136ce5db0dacd629e010cccf7bbde.jpg",
        model_path="mahjong_cnn.pth",
        data_dir="augmented_dataset"
    )