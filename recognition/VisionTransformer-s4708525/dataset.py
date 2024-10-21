from torchvision import transforms
from torch.utils.data import DataLoader, Dataset, random_split
import os
from PIL import Image

train_path_local = '/Users/yudahendriawan/Course [LOCAL]/PATTERN/projects/AD_NC/train/'
test_path_local = '/Users/yudahendriawan/Course [LOCAL]/PATTERN/projects/AD_NC/test/'

train_path_server = '/home/groups/comp3710/ADNI/AD_NC/train/'
test_path_server = '/home/groups/comp3710/ADNI/AD_NC/test/'

class ADNI_Dataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        self.category_counts = {'NC': 0, 'AD': 0}  

        for label, sub_dir in enumerate(['NC', 'AD']):
            sub_dir_path = os.path.join(root_dir, sub_dir)
            num_images = len(os.listdir(sub_dir_path))  
            self.category_counts[sub_dir] = num_images  

            for image_name in os.listdir(sub_dir_path):
                self.image_paths.append(os.path.join(sub_dir_path, image_name))
                self.labels.append(label)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert('RGB')
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

    def get_category_counts(self):
        return self.category_counts

transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.CenterCrop(128),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.1155, 0.1155, 0.1155], std=[0.2224, 0.2224, 0.2224])
    ])

transform_test = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(128),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.1155, 0.1155, 0.1155], std=[0.2224, 0.2224, 0.2224])
])

train_dataset = ADNI_Dataset(train_path_server, transform=transform)
test_dataset = ADNI_Dataset(test_path_server, transform=transform_test)

val_split = 0.2 

train_size = int((1 - val_split) * len(train_dataset))
val_size = len(train_dataset) - train_size
train_subset, val_subset = random_split(train_dataset, [train_size, val_size])

train_loader = DataLoader(train_subset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_subset, batch_size=16, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)