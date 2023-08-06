from collections import defaultdict
from typing import DefaultDict, List, Any, Dict, SupportsFloat, Union, TYPE_CHECKING
import copy
import pickle
import os
import warnings

from pennpaper.metric.cached_parameters_mixin import CachedParamMixin
from pennpaper.metric.interpolate import missing_value

default_folder = "_ez_metrics"

if TYPE_CHECKING:
    from numpy import ndarray


class Metric(CachedParamMixin):
    def __init__(self, name="unknown", x_label="x", y_label="y", style_kwargs=None):
        super().__init__()
        self.name = name
        self.x_label = x_label
        self.y_label = y_label
        self.data = defaultdict(list)
        self.style_kwargs = style_kwargs or {}

    @property
    def samples(self):
        # assert len(set( len(x) for x in self.data.values() )) == 1
        if not self.data:
            return 0
        return len(next(iter(self.data.values())))

    def _sort(self):
        temp = self.data
        self.data = defaultdict(list)
        self.data.update({k: v for k, v in sorted(temp.items())})

    def add_record(self, x: SupportsFloat, y: SupportsFloat):
        self.data[x].append(y)
        self.dirty()

    def add_ys(self, x: SupportsFloat, ys: List[SupportsFloat]):
        self.data[x].extend(ys)
        self.dirty()

    def add_arrays(
        self,
        xs: Union["ndarray", List[SupportsFloat]],
        ys: Union["ndarray", List[SupportsFloat]],
        new_sample=False,
    ):
        """
        Add a list of measurements to the metric. xs and ys must be arrays of same length.

        :param new_sample: If the arrays are to be considered a separate experiment,
        or a part of current experiment.
        """
        assert len(xs) == len(ys)
        self.add_dict({x: y for x, y in zip(xs, ys)}, new_sample)

    def add_dict(
        self, dictionary: Dict[SupportsFloat, SupportsFloat], new_sample=False
    ):
        """
        :param dictionary: the dictionary to add to the metric
        :param new_sample: If the arrays are to be considered a separate experiment,
        or a part of current experiment.
        """
        if new_sample and self.samples:
            new = Metric()
            for x, y in dictionary.items():
                new.add_record(x, y)
            new = self.__add__(new)
            self.data = new.data

        else:
            for x, y in dictionary.items():
                self.add_record(x, y)

    def save(self, folder=default_folder):
        os.makedirs(folder, exist_ok=True)

        with open(os.path.join(folder, f"{self.name}.ezm"), "wb") as f:
            pickle.dump(self, file=f)

    def discard_warmup(self, part: float):
        assert 0 < part < 1
        self._sort()

        keys = list(self.data.keys())
        d_min, d_max = keys[0], keys[-1]

        span = d_max - d_min

        to_delete = [k for k in self.data if k < d_min + part * span]

        for k in to_delete:
            del self.data[k]

    @staticmethod
    def load_all(folder=default_folder) -> List["Metric"]:
        if not os.path.isdir(folder):
            raise FileNotFoundError(folder)

        metrics = []
        for file in os.listdir(folder):
            if file[-4:] == ".ezm":
                with open(os.path.join(folder, file), "rb") as f:
                    metrics.append(pickle.load(f))

        return metrics

    def _merge_equal(self, b: "Metric") -> "Metric":
        """ Modifies metric data a and b looking for keys not shared between the two,
         and inserting interpolated values"""

        all_keys = set(self.data.keys()) | set(b.data.keys())
        a, b = copy.deepcopy(self), copy.deepcopy(b)

        for md in [a, b]:
            missing = {}

            for k in all_keys:
                if k not in md.data:
                    missing[k] = [missing_value(md, k)]

            md.data.update(missing)

        result = Metric(a.name, a.x_label, a.y_label)
        result.data.update({k: v for k, v in sorted(a.data.items())})
        for k, v in b.data.items():
            result.add_ys(x=k, ys=v)

        return result

    def _merge_in(self, small_other: "Metric") -> "Metric":

        assert small_other.samples == 1

        result = Metric(self.name, self.x_label, self.y_label)
        result.data.update(self.data)

        for k in result.data.keys():
            result.add_record(x=k, y=missing_value(small_other, k))

        return result

    def __add__(self, other: "Metric") -> "Metric":
        if self.samples == 0:
            return other
        elif other.samples == 0:
            return self

        self._sort()
        other._sort()

        if self.samples == other.samples:
            result = self._merge_equal(other)
        else:
            smaller = min([self, other], key=lambda x: x.samples)
            bigger = max([self, other], key=lambda x: x.samples)

            result = bigger._merge_in(smaller)

        if self.name != other.name:
            warnings.warn(
                f"\nMerging two metrics with different names: '{self.name}' and '{other.name}'."
                f" Resulting metric is assigned name '{result.name}'"
            )

        return result

    def __radd__(self, other):
        # support sum
        assert other == 0
        return self
