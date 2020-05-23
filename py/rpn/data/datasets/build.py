# -*- coding: utf-8 -*-

"""
@date: 2020/5/14 上午11:33
@file: build.py
@author: zj
@description: 
"""

from torch.utils.data import ConcatDataset

from rpn.data.datasets.path_catalog import DatasetCatalog
from .voc import VOCDataset

_DATASETS = {
    'VOCDataset': VOCDataset,
}


def build_dataset(dataset_list, transform=None, target_transform=None, is_train=True):
    assert len(dataset_list) > 0
    datasets = []
    for dataset_name in dataset_list:
        data = DatasetCatalog.get(dataset_name)
        args = data['args']
        factory = _DATASETS[data['factory']]
        args['transform'] = transform
        args['target_transform'] = target_transform
        if factory == VOCDataset:
            args['keep_difficult'] = not is_train
        dataset = factory(**args)
        datasets.append(dataset)
    # for testing, return a list of datasets
    if not is_train:
        return datasets
    dataset = datasets[0]
    if len(datasets) > 1:
        dataset = ConcatDataset(datasets)

    return [dataset]
