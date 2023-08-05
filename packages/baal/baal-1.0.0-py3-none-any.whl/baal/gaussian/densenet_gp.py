import math

import gpytorch
import torch
import torch.nn.functional as F

from baal.gaussian.densenet import DenseNet


class DenseNetFeatureExtractor(DenseNet):
    def forward(self, x):
        features = self.features(x)
        out = F.relu_(features)
        out = F.avg_pool2d(out, kernel_size=self.avgpool_size).view(features.size(0), -1)
        return out


class GaussianProcessLayer(gpytorch.models.AdditiveGridInducingVariationalGP):
    def __init__(self, num_dim, grid_bounds=(-10., 10.), grid_size=64):
        super(GaussianProcessLayer, self).__init__(grid_size=grid_size, grid_bounds=[grid_bounds],
                                                   num_dim=num_dim, mixing_params=False,
                                                   sum_output=False)
        self.covar_module = gpytorch.kernels.ScaleKernel(
            gpytorch.kernels.RBFKernel(
                lengthscale_prior=gpytorch.priors.SmoothedBoxPrior(
                    math.exp(-1), math.exp(1), sigma=0.1, transform=torch.exp
                )
            )
        )
        self.mean_module = gpytorch.means.ConstantMean()
        self.grid_bounds = grid_bounds

    def forward(self, x):
        mean = self.mean_module(x)
        covar = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean, covar)


class DKLModel(gpytorch.Module):
    def __init__(self, feature_extractor, num_dim, grid_bounds=(-10., 10.)):
        super(DKLModel, self).__init__()
        self.feature_extractor = feature_extractor
        self.gp_layer = GaussianProcessLayer(num_dim=num_dim, grid_bounds=grid_bounds)
        self.grid_bounds = grid_bounds
        self.num_dim = num_dim

    def forward(self, x):
        features = self.feature_extractor(x)
        features = gpytorch.utils.grid.scale_to_bounds(features, self.grid_bounds[0],
                                                       self.grid_bounds[1])
        res = self.gp_layer(features)
        return res


def get_model(num_classes, use_cuda=False):
    """Get a Deep Kernel Learning model based on DenseNet."""
    def cuda(x):
        if use_cuda:
            x = x.cuda()
        return x

    feature_extractor = cuda(
        DenseNetFeatureExtractor(block_config=(6, 6, 6), num_classes=num_classes))
    num_features = feature_extractor.classifier.in_features
    model = cuda(DKLModel(feature_extractor, num_dim=num_features))
    likelihood = cuda(
        gpytorch.likelihoods.SoftmaxLikelihood(num_features=model.num_dim, n_classes=num_classes))
    return model, likelihood
