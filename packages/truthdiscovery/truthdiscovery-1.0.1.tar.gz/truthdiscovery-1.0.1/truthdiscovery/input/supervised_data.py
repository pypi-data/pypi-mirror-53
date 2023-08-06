import random

import numpy.ma as ma

from truthdiscovery.input.matrix_dataset import (
    csv_to_masked_array,
    MatrixDataset
)


class SupervisedData:
    """
    A class to store a dataset for which the true values of a subset of the
    variables is known
    """
    def __init__(self, dataset, true_values):
        """
        :param dataset:     a :any:`Dataset` (or sub-class) object
        :param true_values: dict of the form ``{var_label: true_value, ...}``
                            pairs for the known true values
        """
        self.data = dataset
        self.values = true_values

    def get_accuracy(self, results):
        """
        Calculate the accuracy of truth discovery results, computed as the
        frequency of cases where the most believed value for a variable is the
        correct one, ignoring cases where only one value for a variable is
        claimed across all sources (in this case all algorithms will predict
        the same value).

        :param results: a :any:`Result` object
        :return: accuracy as a number in [0, 1]: 1 is best accuracy, 0 is worst
        :raises ValueError: if no true values are known, or if all variables
                            have only one claimed value
        """
        if not self.values:
            raise ValueError("No known true values")
        total = 0
        count = 0

        for var_label, true_value in self.values.items():
            # Skip if there is only one claimed value
            try:
                if len(results.belief[var_label]) == 1:
                    continue
            except KeyError:
                continue

            total += 1
            # Note: select value randomly if more than one most-believed value
            # exists
            most_believed = random.choice(
                list(results.get_most_believed_values(var_label))
            )
            if most_believed == true_value:
                count += 1
        if total == 0:
            raise ValueError(
                "No known variables where more than one claimed value exists"
            )
        return count / total

    @classmethod
    def from_csv(cls, fileobj):
        """
        Load a matrix from a CSV file along with true values. The format is the
        same as for loading an unsupervised matrix dataset, but the first row
        contains the true values.

        :param fileobj: file object to read from
        :return:        a :any:`SupervisedData` object representing the matrix
                        encoded by the CSV
        """
        # Load the whole thing as a matrix
        temp = csv_to_masked_array(fileobj)
        # Get true values from first row
        true_values = {i: v for i, v in enumerate(temp[0, :])
                       if not ma.is_masked(v)}
        sv_mat = temp[1:, :]
        return cls(MatrixDataset(sv_mat), true_values)
