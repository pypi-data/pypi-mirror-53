import torch


class Average(object):
    """computes the average of and stores the current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        """reset all the parameters to zero"""
        self.val = torch.Tensor([0]).float()
        self.sum = torch.Tensor([0]).float()
        self.count = 0

    def update(self, value, num_vals=1):
        """calculates the average at each step and stores the current value"""
        self.val = value
        self.sum += value * num_vals
        self.count += num_vals

    @property
    def avg(self):
        return (self.sum / self.count).cpu().numpy().item()

    def __str__(self):
        return f"{self.avg:.3f}"


def accuracy(output, target, topk=(1,)):
    """ computes the top first and top five accuracy for the model batch by
    batch.
    Args:
        output (np.array): output data of the model
        target (np.array): data labels
        topk (tuple): the value of k for calculating the topk accuracy.
    Returns:
        result (list): topk accuracies for each k sorted in ascending mode.
    """
    batch_size = target.shape[0]
    maxk = max(topk)
    dim = 1
    _, pred = output.topk(maxk, dim, True, True)
    pred = pred.t()

    # expand the dimension of target and copy it's elements to compare with
    # each of the topk probabelities of pred
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    # topk accuracies
    result = []

    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
        result.append(float(correct_k.mul_(100.0 / batch_size)))

    return result
