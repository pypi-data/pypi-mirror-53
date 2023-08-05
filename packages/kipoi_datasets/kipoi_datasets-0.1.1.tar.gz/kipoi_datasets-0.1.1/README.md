# Kipoi datasets

Datasets for regulatory genomics formatted in the similar fasion as https://github.com/pytorch/vision/tree/master/torchvision/datasets.

<!-- <a href='https://circleci.com/gh/kipoi/kipoiseq'> -->
<!-- 	<img alt='CircleCI' src='https://circleci.com/gh/kipoi/kipoiseq.svg?style=svg' style="max-height:20px;width:auto"> -->
<!-- </a> -->
<!-- <a href=https://coveralls.io/github/kipoi/kipoiseq?branch=master> -->
<!-- 	<img alt='Coverage status' src=https://coveralls.io/repos/github/kipoi/kipoiseq/badge.svg?branch=master style="max-height:20px;width:auto;"> -->
<!-- </a> -->

## Installation

```bash
conda install genomelake -c bioconda
pip install git@github.com:kipoi/datasets.git
```

## Getting started


```python
from kipoi_datasets.bpnet_oskn import BPNetOSKNDataset

# downloads the data
train = BPNetOSKNDataset(root='/tmp/data', split='train')

# training iterator. Returning (x,targets) tuples
it = train.batch_train_iter(num_workers=10)

# setup keras model
model = Sequential(...)
model.fit(it)

# or 
for x,targets in it:
    model.fit_on_batch(x, targets)
	...

```
