"""Core code
"""
from tqdm import tqdm
from kipoi_utils.external.torch.data import DataLoader
from kipoi_utils.data_utils import (numpy_collate, numpy_collate_concat, get_dataset_item,
                                    DataloaderIterable, batch_gen, get_dataset_lens, iterable_cycle)
import abc


class Dataset:
    """An abstract class representing a Dataset.

    All other datasets should subclass it. All subclasses should override
    ``__len__``, that provides the size of the dataset, and ``__getitem__``,
    supporting integer indexing in range from 0 to len(self) exclusive.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __getitem__(self, index):
        """Return one sample

        index: {0, ..., len(self)-1}
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self):
        """Return the number of all samples
        """
        raise NotImplementedError

    def _batch_iterable(self, batch_size=32, shuffle=False, num_workers=0, drop_last=False, **kwargs):
        """Return a batch-iteratrable

        See batch_iter docs

        Returns:
            Iterable
        """
        dl = DataLoader(self,
                        batch_size=batch_size,
                        collate_fn=numpy_collate,
                        shuffle=shuffle,
                        num_workers=num_workers,
                        drop_last=drop_last,
                        **kwargs)
        return dl

    def batch_iter(self, batch_size=32, shuffle=False, num_workers=0, drop_last=False, **kwargs):
        """Return a batch-iterator

        Arguments:
            dataset (Dataset): dataset from which to load the data.
            batch_size (int, optional): how many samples per batch to load
                (default: 1).
            shuffle (bool, optional): set to ``True`` to have the data reshuffled
                at every epoch (default: False).
            num_workers (int, optional): how many subprocesses to use for data
                loading. 0 means that the data will be loaded in the main process
                (default: 0)
            drop_last (bool, optional): set to ``True`` to drop the last incomplete batch,
                if the dataset size is not divisible by the batch size. If False and
                the size of dataset is not divisible by the batch size, then the last batch
                will be smaller. (default: False)

        Returns:
            iterator
        """
        dl = self._batch_iterable(batch_size=batch_size,
                                  shuffle=shuffle,
                                  num_workers=num_workers,
                                  drop_last=drop_last,
                                  **kwargs)
        return iter(dl)

    def batch_train_iter(self, cycle=True, **kwargs):
        """Returns samples directly useful for training the model:
        (x["inputs"],x["targets"])

        Args:
          cycle: when True, the returned iterator will run indefinitely go through the dataset
            Use True with `fit_generator` in Keras.
          **kwargs: Arguments passed to self.batch_iter(**kwargs)
        """
        if cycle:
            return ((x["inputs"], x["targets"])
                    for x in iterable_cycle(self._batch_iterable(**kwargs)))
        else:
            return ((x["inputs"], x["targets"]) for x in self.batch_iter(**kwargs))

    def batch_predict_iter(self, **kwargs):
        """Returns samples directly useful for prediction x["inputs"]

        Args:
          **kwargs: Arguments passed to self.batch_iter(**kwargs)
        """
        return (x["inputs"] for x in self.batch_iter(**kwargs))

    def load_all(self, batch_size=32, **kwargs):
        """Load the whole dataset into memory
        Arguments:
            batch_size (int, optional): how many samples per batch to load
                (default: 1).
        """
        return numpy_collate_concat([x for x in tqdm(self.batch_iter(batch_size, **kwargs))])
