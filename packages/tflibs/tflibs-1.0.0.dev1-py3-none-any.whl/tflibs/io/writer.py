"""
    Writer
"""
import os
from typing import Callable, Iterable
from itertools import cycle

import tensorflow as tf
from tqdm import tqdm

from tflibs.dataset.enums import Split
from tflibs.io.utils import build_tfrecord_basepath
from tflibs.utils.multiprocessing import async_map


class Writer:
    def __init__(self, dataset_dir: str, filename: str, split: Split = None):
        self._dataset_dir = dataset_dir
        self._filename = filename
        self._split = split

        os.makedirs(dataset_dir, exist_ok=True)

    @property
    def dataset_dir(self):
        return self._dataset_dir

    @property
    def filename(self):
        return self._filename

    @property
    def split(self):
        return self._split

    @property
    def tfrecord_basepath(self):
        return build_tfrecord_basepath(self.dataset_dir, self.filename, split=self.split)

    def write(self, collection: Iterable, map_fn: Callable = None, num_shards: int = 32, num_parallel_calls: int = 32):
        try:
            num_examples = len(collection)
        except TypeError:
            num_examples = None

        if num_shards == 1:
            writers = [tf.io.TFRecordWriter(self.tfrecord_basepath)]
        else:
            fname, ext = os.path.splitext(self.tfrecord_basepath)

            postfix_format = '{shard_idx:03d}-of-{num_shards:03d}'
            tfrecord_paths = ['_'.join([fname, postfix_format.format(shard_idx=shard_idx, num_shards=num_shards)]) + ext
                              for shard_idx in range(num_shards)]
            writers = list(map(tf.io.TFRecordWriter, tfrecord_paths))

        if callable(map_fn):
            collection = async_map(map_fn, collection, num_parallel_calls=num_parallel_calls)

        writer_iterator = cycle(writers)

        for i, example in tqdm(enumerate(collection), total=num_examples):
            writer = next(writer_iterator)
            writer.write(example)

        for writer in writers:
            writer.close()
