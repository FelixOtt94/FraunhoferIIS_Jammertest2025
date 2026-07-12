import numpy as np
import torch
from torch.utils.data import Dataset
import h5py


class custom_dataset(Dataset):
    def __init__(self, x_files, norm=True, iq_len=1024, shift=10220):
        self.iq_len = iq_len
        self.shift = shift
        self.mean_iq_channel = np.array([-0.00085627, -0.00819987])
        self.std_iq_channel = np.array([2.3488201, 2.3562662])
        self.use_norm = norm
        self.indices = np.arange(len(x_files)).astype(int)
        self.x_files = x_files

    def __getitem__(self, item: int):
        if self.x_files[item][2] == 1:
            if self.x_files[item][0] == 1475000:
                h5_file = h5py.File("./dataset/Sample_Area%d_%07d_1486589.h5" % (self.x_files[item][2], self.x_files[item][0]), "r")
            else:
                h5_file = h5py.File("./dataset/Sample_Area%d_%07d_%07d.h5" % (self.x_files[item][2], self.x_files[item][0], self.x_files[item][0] + 24999), "r")
        else:
            if self.x_files[item][0] == 625000:
                h5_file = h5py.File("./dataset/Sample_Area%d_%07d_0646510.h5" % (self.x_files[item][2], self.x_files[item][0]), "r")
            else:
                h5_file = h5py.File("./dataset/Sample_Area%d_%07d_%07d.h5" % (self.x_files[item][2], self.x_files[item][0], self.x_files[item][0] + 24999), "r")
        y_data = h5_file["label"][self.x_files[item][1]]
        x_data = (h5_file["data"][self.x_files[item][1]]).astype(np.float32)[self.shift:self.shift + self.iq_len * 2]
        x_data = x_data.reshape((self.iq_len, 2))
        if self.use_norm:
            x_data -= self.mean_iq_channel
            x_data /= self.std_iq_channel
        x_data = x_data.transpose((1, 0))
        y1 = torch.tensor(int(y_data[0]), dtype=torch.long)
        y2 = torch.tensor(y_data[1], dtype=torch.float)
        y3 = torch.tensor(np.minimum(y_data[2], 40.), dtype=torch.float)
        return torch.from_numpy(x_data), y1, y2, y3
            
    def __len__(self) -> int:
        return len(self.x_files)


def get_dataset(norm=True, train=True, iq_len=1024, shift=10120, areas=[1,2], use_db_lim=False, db_lim=0, bands=[1,5], ignore_files_without_antenna_power=True):
    """
    norm: If True will norm IQ Values based on mean and std of all train IQ samples
    train: If True will load training data, else will load testing data
    iq_len: Number of IQ samples to return in the shape of (2, iq_len), where the 2 channels correspond to I and Q
    shift: The original IQ Length size is 263120. This script is intended to be used for time series classification, so using the entire sample length will be very slow.
           This value offsets the starting point. So shift=10120 means: IQ_Data[shift: shift+iq_len] 
    areas: List of areas from which to use data. (only 1 and 2)
    use_db_lim: If True, any samples with a signal strength value below db_lim will be ignored
    db_lim: Samples with a signal strength value below db_lim will be ignored if use_db_lim is True
    bands: List of Bands to include in the dataset. (only 1 and 5, 1 corresponds to E1 and 5 corrseponds to E5a)
    ignore_files_without_antenna_power: If True, any samples where the antenna power was not set correctly will be ignored. (Recommendation: Set to True)
    """
    data_files = []
    if train:
        for area in areas:
            data_files.append("./splits/train_%d.txt" % area)
    else:
        for area in areas:
            data_files.append("./splits/test_%d.txt" % area)
    x_files = []
    for di, data_file in enumerate(data_files):
        cur_area = areas[di]
        with open(data_file, "r") as f:
            data_info = f.readlines()
        data_info = np.array([x.split("\n")[0].split("\t") for x in data_info])
        for x in data_info:
            if use_db_lim and float(x[2]) < db_lim:
                continue
            if int(x[3]) not in bands:
                continue
            if ignore_files_without_antenna_power and int(x[4]) == 0:
                continue
            x_files.append([int(x[0]), int(x[1]), cur_area])
    return custom_dataset(x_files, norm=norm, iq_len=iq_len, shift=shift)


if __name__ == "__main__":
    # Example Usage #
    from tqdm import tqdm
    from torch.utils.data import DataLoader
    dataset = get_dataset()
    data_loader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=8, pin_memory=True, drop_last=True)
    with tqdm(enumerate(data_loader), total=len(data_loader)) as tqdm_train:
        for episode_index, (x_batch, y1, y2, y3) in tqdm_train:
            # x_batch contains a Tensor of shape (batch_size, 2, iq_length) and type torch.float: IQ x data
            # y1 contains a Tensor of shape (batch_size) and type torch.long: Jammer Class Data
            # y2 contains a Tensor of shape (batch_size) and type torch.float: Jammer Signal Strength Data
            # y3 contains a Tensor of shape (batch_size) and type torch.float: Jammer Bandwidth Data
            pass
