"""
ChIP-nexus dataset in Mouse embryonic stem cells (MESCs) to train BPNet from https://doi.org/10.1101/737981

It involves
"""
from kipoi_datasets.core import Dataset
from kipoiseq.dataclasses import Interval
from kipoi_utils.utils import map_nested
from kipoi_utils.external.flatten_json import flatten
from kipoi_utils.external.torchvision.dataset_utils import download_and_extract_archive, download_url, check_integrity
# TODO - implement the bigwig extractor in kipoiseq
from genomelake.extractors import FastaExtractor, BigwigExtractor
import pandas as pd
import random
import os
import numpy as np


valid_chr = ['chr2', 'chr3', 'chr4']
test_chr = ['chr1', 'chr8', 'chr9']


def map_nested(dd, fn):
    """Map a function to a nested data structure (containing lists or dictionaries

    Args:
      dd: nested data structure
      fn: function to apply to each leaf
    """
    if isinstance(dd, dict):
        return {key: map_nested(dd[key], fn) for key in dd}
    elif isinstance(dd, list):
        return [map_nested(x, fn) for x in dd]
    else:
        return fn(dd)


class IntervalAugmentor:
    """Randomly shift and swap strands

    Args:
      max_shift: Inteval shift is sampled uniformly from [-max_shift, max_shift]
      flip_strand: if True, strand is randomly sampled
    """

    def __init__(self, max_shift, flip_strand=True):
        self.max_shift = max_shift
        self.flip_strand = flip_strand

    def __call__(self, interval: Interval):
        # Generate the random shift
        interval = interval.copy()
        if self.flip_strand:
            # randomly assign the strand
            interval._strand = ['+', '-'][random.randint(0, 1)]

        shift = random.randint(-self.max_shift, self.max_shift)
        return interval.shift(shift, use_strand=False)


MD5SUMS = {
    'patchcap/counts.neg.bw': 'f82c66ee5e5a0471846db35191fe481a',
    'patchcap/counts.pos.bw': '98d336de48cbdcd89a0e5a4c0dd43633',
    'Sox2/counts.pos.bw': 'd88d3af721a2fb9ed1356a68c0400313',
    'Sox2/counts.neg.bw': 'e61c408a9c39efe37892d13d440bef2d',
    'Klf4/counts.pos.bw': '238b2400d36ce1c5d5bba9aeb378a545',
    'Klf4/counts.neg.bw': '9b4259a13aed4d72529ec4d390f4387e',
    'Nanog/counts.pos.bw': '57adcc51ef400742869979bf021c6b50',
    'Nanog/counts.neg.bw': '3d7b6d1d2ecfd7192f9884d14897cd5b',
    'Oct4/counts.pos.bw': 'd7b0458fd622842a96fb7b72a4a01af5',
    'Oct4/counts.neg.bw': '70e1f8307583509214cb72260aab6d5b',
    'ranges.tsv': 'b8a42c9c437ef84c7be0ed6347d3323d',
    'mm10.fa.gz': '96a6ea89d77e1aed39eaf51d760f015d',
}


class BPNetDataset(Dataset):

    BASE_URL = 'http://mitra.stanford.edu/kundaje/avsec/chipnexus/paper/data/'

    TFS = ['Oct4', 'Sox2', 'Nanog', 'Klf4']
    tasks = TFS
    CONTROL = 'patchcap'

    SPLITS = {
        "train": {
            "incl_chromosomes": None,
            "excl_chromosomes": valid_chr + test_chr,
        },
        "valid": {
            "incl_chromosomes": valid_chr,
            "excl_chromosomes": None,
        },
        "test": {
            "incl_chromosomes": test_chr,
            "excl_chromosomes": None,
        },
        "all": {
            "incl_chromosomes": None,
            "excl_chromosomes": None,
        },

    }

    def __init__(self, root,
                 split='train',
                 peak_width=1000,
                 seq_width=1000,
                 shuffle=True,
                 interval_transform=None,
                 track_transform=None,
                 total_count_transform=lambda x: np.log(1 + x)):
        """Dataset for loading the bigwigs and fastas

        Args:
          ds (bpnet.dataspecs.DataSpec): data specification containing the
            fasta file, bed files and bigWig file paths
          chromosomes (list of str): a list of chor
          seq_width: resize the bed file to a certain width
          peak_width: resize the bed file to a certain width
          shuffle: shuffle the interval order
          track_transform: function to be applied to transform the tracks (shape=(batch, seqlen, channels))
          total_count_transform: transform to apply to the total counts

        output_schema:
          inputs:
            seq:
              shape: (seq_width, 4)
              doc: One-hot encoded DNA sequence (A, C, G, T) channels
            bias/{task}/profile:
              shape: (peak_width, 2)
              doc: bias

          targets:
            {task}/profile:
              shape: (peak_width, 2)
              doc:  5-prime end read counts for the positive and negative strand (0's and 1st channel correspondingly)
            {task}/counts:
              shape: (2, )
              doc: Total number of count transformed with `total_count_transform`

          metadata:
            range:
              type: GenomicRanges
              doc: ranges describing the target interval
            interval_from_task:
              doc: TF name of the peak (example Oct, Sox2, Nanog, ...)
        """

        self.root = root
        self.split = split
        self.peak_width = peak_width
        self.seq_width = seq_width
        self.track_transform = track_transform
        self.interval_transform = interval_transform
        self.total_count_transform = total_count_transform
        self.shuffle = shuffle

        # setup files:
        self.files = {"signal_tracks": {tf: [f'{tf}/counts.{strand}.bw' for strand in ['pos', 'neg']]
                                        for tf in self.TFS},
                      "peaks": 'ranges.tsv',
                      "patchcap_controls": [f'patchcap/counts.{strand}.bw' for strand in ['pos', 'neg']]}

        self.fasta_file = os.path.join(self.root, 'mm10.fa')

        # 1. download the data
        self._download()

        self.incl_chromosomes = self.SPLITS[self.split]['incl_chromosomes']
        self.excl_chromosomes = self.SPLITS[self.split]['excl_chromosomes']

        # use absolute file pat
        self.files = map_nested(self.files, lambda v: os.path.join(self.root, v))

        # get the intervals. Columns: chrom, start, end, strand, interval_from_task, idx
        self.dfm = pd.read_csv(self.files['peaks'], sep='\t', index_col=False)
        if self.incl_chromosomes is not None:
            self.dfm = self.dfm[self.dfm.chrom.isin(self.incl_chromosomes)]
        if self.excl_chromosomes is not None:
            self.dfm = self.dfm[~self.dfm.chrom.isin(self.excl_chromosomes)]
        if self.shuffle:
            self.dfm = self.dfm.sample(frac=1)

        self.fasta_extractor = None

    def _download(self):
        all_files = list(flatten(self.files).values())
        # bigwig files and fasta
        for file_path in all_files:
            file_dir = os.path.join(self.root, os.path.dirname(file_path))
            os.makedirs(file_dir, exist_ok=True)
            download_url(os.path.join(self.BASE_URL, 'chip-nexus', file_path),
                         root=file_dir,
                         filename=os.path.basename(file_path),
                         md5=MD5SUMS[file_path])

        # download and extract the fasta file
        if not check_integrity(self.fasta_file, 'ce8b0b14cff41f9dc49e3e98792dc7fd'):
            print("mm10.fa doesn't exist. Downloading.")
            download_and_extract_archive(os.path.join(self.BASE_URL, 'mm10.fa.gz'),
                                         download_root=self.root,
                                         remove_finished=True,  # so that we can validate the md5file and not re-download
                                         md5=MD5SUMS['mm10.fa.gz'])

    def __len__(self):
        return len(self.dfm)

    def __getitem__(self, idx):
        if self.fasta_extractor is None:
            # first call
            # Use normal fasta/bigwig extractors
            self.fasta_extractor = FastaExtractor(self.fasta_file, use_strand=True)

            self.bw_extractors = {task: [BigwigExtractor(track) for track in tracks]
                                  for task, tracks in self.files['signal_tracks'].items()}
            self.patchcap_bias_extractor = [BigwigExtractor(track) for track in self.files['patchcap_controls']]

        # Get the genomic interval for that particular datapoint
        interval = Interval(chrom=self.dfm.iat[idx, 0],  # chrom
                            start=self.dfm.iat[idx, 1],  # start
                            end=self.dfm.iat[idx, 2])  # end
        interval_from_task = self.dfm.iat[idx, 3]

        # Transform the input interval (for say augmentation...)
        if self.interval_transform is not None:
            interval = self.interval_transform(interval)

        # resize the intervals to the desired widths
        target_interval = interval.resize(self.peak_width)
        seq_interval = interval.resize(self.seq_width)

        # extract DNA sequence + one-hot encode it
        sequence = self.fasta_extractor([seq_interval])[0]

        # extract the profile counts from the bigwigs
        def _run_extractors(extractors, interval):
            out = np.stack([np.abs(extractor([interval], nan_as_zero=True))
                            for extractor in extractors], axis=-1)[0]
            if interval.strand == '-':  # Take the strand into account
                out[:, :] = out[::-1, ::-1]
            return out
        targets = {f"{task}/profile": _run_extractors(self.bw_extractors[task], target_interval)
                   for task in self.tasks}

        for task in self.tasks:
            # Add total number of counts
            targets[f'{task}/counts'] = self.total_count_transform(targets[f'{task}/profile'].sum(0))
        if self.track_transform is not None:
            # custom profile track transform
            for task in self.tasks:
                targets[f'{task}/profile'] = self.track_transform(targets[f'{task}/profile'])

        # Extract the bias tracks
        patchcap_bias = _run_extractors(self.patchcap_bias_extractor, target_interval)
        task_biases = {f"bias/{task}/profile": patchcap_bias for task in self.tasks}  # all tasks have the same bias
        for task in self.tasks:
            task_biases[f'bias/{task}/counts'] = self.total_count_transform(task_biases[f'bias/{task}/profile'].sum(0))
        if self.track_transform is not None:
            for task in self.tasks:
                task_biases[f'bias/{task}/profile'] = self.track_transform(task_biases[f'bias/{task}/profile'])

        return {
            "inputs": {"seq": sequence, **task_biases},
            "targets": targets,
            "metadata": {"range": dict(chr=target_interval.chrom,
                                       start=target_interval.start,
                                       end=target_interval.stop,
                                       id=idx,
                                       strand=target_interval.strand),
                         "interval_from_task": interval_from_task}
        }
