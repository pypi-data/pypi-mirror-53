import torch
from torch.autograd import Variable

from ..modelwrapper import ModelWrapper
from .swa import StochasticWeightAveraging


class SwagModelWrapper(ModelWrapper):
    def predict_on_batch(self, data, optimizer, iterations=1, cuda=False):
        """
        Get the model's prediction on a batch.
        Args:
            data: Tensor, the model input
            iterations: int, number of prediction to perform.
            cuda: bool, use cuda or not

        Returns:
            Tensor, the loss computed from the criterion.
                    shape = {batch_size, nclass, n_iteration}
        """

        if not isinstance(optimizer, StochasticWeightAveraging):
            raise ValueError("This only works with a SWA optimizer")

        data = Variable(data)
        if cuda:
            data = data.cuda()
        predictions = []
        for _ in range(iterations):
            optimizer.sample()  # this samples a model
            predictions.append(self.model(data))  # make a list of predictions
        optimizer.sgd()  # this returns to the SGD state
        return torch.stack(predictions, dim=2)
