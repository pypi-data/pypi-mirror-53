from torchvision import transforms, datasets

from .dataset import ActiveLearningDataset


def active_mnist(
    path="/app/baal/data/mnist",
    *args,
    transform=transforms.Compose([transforms.Grayscale(3), transforms.ToTensor()]),
    test_transform=transforms.Compose([transforms.Grayscale(3), transforms.ToTensor()]),
    **kwargs
):
    """Get active MNIST datasets.

    Arguments:
        path : str
            The root folder for the MNIST dataset
            (default: {"/app/baal/data/mnist"})

    Returns:
        ActiveLearningDataset
            the active learning dataset, training data
        Dataset
            the evaluation dataset
    """

    return (
        ActiveLearningDataset(
            datasets.MNIST(path, train=True, transform=transform, *args, **kwargs),
            eval_transform=test_transform,
        ),
        datasets.MNIST(path, train=False, transform=test_transform, *args, **kwargs),
    )


def active_cifar10(
    path="/app/baal/data/cifar10/",
    *args,
    transform=transforms.ToTensor(),
    test_transform=transforms.ToTensor(),
    **kwargs
):
    """Get active MNIST datasets.

    Arguments:
        path : str
            The root folder for the CIFAR10 dataset
            (default: {"/app/baal/data/cifar10"})

    Returns:
        ActiveLearningDataset
            the active learning dataset, training data
        Dataset
            the evaluation dataset
    """

    return (
        ActiveLearningDataset(
            datasets.CIFAR10(path, train=True, transform=transform, *args, **kwargs),
            eval_transform=test_transform,
        ),
        datasets.CIFAR10(path, train=False, transform=test_transform, *args, **kwargs),
    )


def active_stl10(
    path="/app/baal/data/stl10/",
    *args,
    transform=transforms.ToTensor(),
    test_transform=transforms.ToTensor(),
    **kwargs
):
    """Get active STL10 datasets.

    Arguments:
        path : str
            The root folder for the STL10 dataset
            (default: {"/app/baal/data/cifar10"})

    Returns:
        ActiveLearningDataset
            the active learning dataset, training data
        Dataset
            the evaluation dataset
    """

    return (
        ActiveLearningDataset(
            datasets.STL10(
                path, split='train', transform=transform, download=True, *args, **kwargs
            ),
            eval_transform=test_transform,
        ),
        datasets.STL10(
            path, split='unlabeled', transform=test_transform, *args, **kwargs
        ),
    )


lookup = {'mnist': active_mnist, 'cifar10': active_cifar10, 'stl10': active_stl10}
