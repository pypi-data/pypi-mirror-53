# MIT License
#
# Copyright (c) 2018 Haoxintong
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""This module provides popular face recognition datasets."""

from .dataset import *


datasets = {"lfw": FRValDataset,
            "calfw": FRValDataset,
            "cplfw": FRValDataset,
            "cfp_fp": FRValDataset,
            "agedb_30": FRValDataset,
            "cfp_ff": FRValDataset,
            "vgg2_fp": FRValDataset,
            "emore": FRTrainRecordDataset,
            "vgg": FRTrainRecordDataset,
            "webface": FRTrainRecordDataset,
            "asian_celeb": FRTrainRecordDataset,
            "deep_glint": FRTrainRecordDataset
            }


def get_recognition_dataset(name, **kwargs):
    return datasets[name](name, **kwargs)
