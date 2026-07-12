import numpy as np
import torch
from torch.utils.data import Dataset


class custom_dataset(Dataset):
    def __init__(self, x_files, y_labels, norm=True):
        self.crpa_file_path = "./all_crpa_files.npy"
        self.mean_iq_channel = np.array([5.1587311e-05, 5.5935096e-05, -1.6736331e-06, -3.5345695e-06, 6.1378436e-05, -1.0856257e-06, 3.5265399e-05, -5.1025974e-05])
        self.std_iq_channel = np.array([0.06061232, 0.06058156, 0.05157815, 0.05159907, 0.06074161, 0.06073344, 0.06317467, 0.0631671])
        self.use_norm = norm
        self.indices = np.arange(len(x_files)).astype(int)
        self.labels = y_labels
        self.x_files = x_files
        self.all_data = np.load(self.crpa_file_path).view(np.float32)

    def __getitem__(self, item: int):
        x_data = self.all_data[self.x_files[item]]
        x_data = x_data.reshape((-1, 1024, 2)).transpose((1, 0, 2)).reshape((1024, 8))
        if self.use_norm:
            x_data -= self.mean_iq_channel
            x_data /= self.std_iq_channel
        x_data = x_data.transpose((1, 0))
        y1 = torch.tensor(self.labels[item][0], dtype=torch.long)
        y2 = torch.tensor(self.labels[item][1], dtype=torch.float)
        y3 = torch.tensor(self.labels[item][2], dtype=torch.float)
        return torch.from_numpy(x_data), y1, y2, y3
            
    def __len__(self) -> int:
        return len(self.labels)


def get_dataset(norm=True, train=True, areas=[1,2], use_db_lim=False, db_lim=0):
    """
    norm: If True will norm IQ Values based on mean and std of all train IQ samples
    train: If True will load training data, else will load testing data
    areas: List of areas from which to use data. (only 1 and 2)
    use_db_lim: If True, any samples with a signal strength value below db_lim will be ignored
    db_lim: Samples with a signal strength value below db_lim will be ignored if use_db_lim is True
    """
    data_files = []
    if train:
        for area in areas:
            data_files.append("./splits/train_crpa_%d.txt" % area)
    else:
        for area in areas:
            data_files.append("./splits/test_crpa_%d.txt" % area)
    x_files = []
    y_labels = []
    for di, data_file in enumerate(data_files):
        with open(data_file, "r") as f:
            data_info = f.readlines()
        data_info = np.array([x.split("\n")[0].split("\t") for x in data_info])
        for x in data_info:
            if use_db_lim and float(x[2]) < db_lim:
                continue
            x_files.append(int(x[0]))
            cur_y_labs = [int(x[1]), float(x[2]), float(x[3])]
            y_labels.append(cur_y_labs)
    return custom_dataset(x_files, y_labels, norm=norm)


if __name__ == "__main__":
    # Example Usage #
    from tqdm import tqdm
    from torch.utils.data import DataLoader
    dataset = get_dataset()
    data_loader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=8, pin_memory=True, drop_last=True)
    with tqdm(enumerate(data_loader), total=len(data_loader)) as tqdm_train:
        for episode_index, (x_batch, y1, y2, y3) in tqdm_train:
            # x_batch contains a Tensor of shape (batch_size, 8, 1024) and type torch.float: IQ x data
            # y1 contains a Tensor of shape (batch_size) and type torch.long: Jammer Class Data
            # y2 contains a Tensor of shape (batch_size) and type torch.float: Jammer Signal Strength Data
            # y3 contains a Tensor of shape (batch_size) and type torch.float: Jammer Bandwidth Data
            pass
