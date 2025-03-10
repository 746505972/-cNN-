# 2025/3/10 19:19
import os
from PIL import Image
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torchvision.utils import save_image


def augment_data(input_dir, output_dir, num_augmented=50):
    """
    对数据集进行数据增强
    :param input_dir: 原始数据集路径
    :param output_dir: 增强后数据集路径
    :param num_augmented: 每张图片生成的增强图片数量
    """
    transform = transforms.Compose([
        transforms.RandomRotation(degrees=15),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomResizedCrop(size=(75, 101), scale=(0.8, 1.0)),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.GaussianBlur(kernel_size=3),
        transforms.ToTensor(),
    ])

    os.makedirs(output_dir, exist_ok=True)

    for class_name in os.listdir(input_dir):
        class_dir = os.path.join(input_dir, class_name)
        if os.path.isdir(class_dir):
            output_class_dir = os.path.join(output_dir, class_name)
            os.makedirs(output_class_dir, exist_ok=True)

            for image_name in os.listdir(class_dir):
                image_path = os.path.join(class_dir, image_name)
                image = Image.open(image_path).convert("RGB")

                for i in range(num_augmented):
                    augmented_image = transform(image)
                    save_image(augmented_image, os.path.join(output_class_dir, f"{class_name}_aug_{i}.png"))

    print("数据增强完成！")


def load_dataset(data_dir):
    """
    加载数据集
    :param data_dir: 数据集路径
    :return: 数据集对象
    """
    transform = transforms.Compose([
        transforms.Resize((75, 101)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    dataset = ImageFolder(root=data_dir, transform=transform)
    return dataset


if __name__ == "__main__":
    augment_data('dataset', 'augmented_dataset', num_augmented=50)
