from gxdltk.header import *



def batch_provider_th(*data: list, batch_size: int = 1, shuffle: bool = True) \
        -> \
        tdata.DataLoader:
    """
    convert list type data to a dataloader
    :param data: your data, tensor
    :return: data loader
    """
    dtensors = tuple(map(tensor, data))  # tensor tuple
    dataset = tdata.TensorDataset(*dtensors)
    loader = tdata.DataLoader(dataset=dataset, batch_size=batch_size,
                              shuffle=shuffle)
    return loader

def batch_provider_mx(*data: list, batch_size: int = 1, shuffle: bool = True) -> gdata.DataLoader:
    dataset = gdata.ArrayDataset(data)
    data_iter = gdata.DataLoader(dataset,batch_size,shuffle=shuffle)
    return data_iter

def batch_provider(*data: list, batch_size: int = 1, shuffle: bool = True):
    if os.environ["GXBACKEND"] == 'torch':
        return batch_provider_th(*data, batch_size= 1,shuffle= True)
    else:
        return batch_provider_mx(*data, batch_size= 1,shuffle= True)
