# coding: utf-8

# # Deep Kernel Learning (DenseNet + GP) on CIFAR10/100
# 
# In this notebook, we'll demonstrate the steps necessary to train a medium sized DenseNet
# (https://arxiv.org/abs/1608.06993) on either of two popularly used benchmark dataset in
# computer vision (CIFAR10 and CIFAR100). We'll be training the DKL model entirely end to
# end using the standard 300 Epoch training schedule and SGD.
# 
# This notebook is largely for tutorial purposes. If your goal is just to get (for example
# ) a trained DKL + CIFAR100 model, we __recommend__ that you move this code to a simple python
# script and run that, rather than training directly out of a python notebook. We find that training
# is just a bit faster out of a python notebook. We also of course recommend that you increase the
# size of the DenseNet used to a full sized model if you would like to achieve state of
# the art performance.
# 
# Furthermore, because this notebook involves training an actually reasonably large neural
# network, it is __strongly recommended__ that you have a decent GPU available for this,
# as with all large deep learning models.

# In[1]:


import math

import gpytorch
import torch
import torch.nn.functional as F
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.optim import SGD
from torch.optim.lr_scheduler import MultiStepLR

# In[2]:
from baal.gaussian import DenseNet

# ## Set up data augmentation
#
# The first thing we'll do is set up some data augmentation transformations
# to use during training, as well as some basic normalization to use during both
# training and testing. We'll use random crops and flips to train the model, and do basic
# normalization at both training time and test time. To accomplish these transformations,
# we use standard `torchvision` transforms.

normalize = transforms.Normalize(mean=[0.5071, 0.4867, 0.4408], std=[0.2675, 0.2565, 0.2761])
aug_trans = [transforms.RandomCrop(32, padding=4), transforms.RandomHorizontalFlip()]
common_trans = [transforms.ToTensor(), normalize]
train_compose = transforms.Compose(aug_trans + common_trans)
test_compose = transforms.Compose(common_trans)

# ## Create DataLoaders
# 
# Next, we create dataloaders for the selected dataset using the built in torchvision datasets.
# The cell below will download either the cifar10 or cifar100 dataset, depending on which
# is made. The default here is cifar10, however training is just as fast on either dataset.
# 
# After downloading the datasets, we create standard `torch.utils.data.DataLoader`s for each
# dataset that we will be using to get minibatches of augmented data.

# In[3]:


dataset = 'cifar10'
batch_size = 1

if dataset == 'cifar10':
    d_func = dset.CIFAR10
    train_set = dset.CIFAR10('data', train=True, transform=train_compose, download=True)
    test_set = dset.CIFAR10('data', train=False, transform=test_compose)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=False)
    num_classes = 10
elif dataset == 'cifar100':
    d_func = dset.CIFAR100
    train_set = dset.CIFAR100('data', train=True, transform=train_compose, download=True)
    test_set = dset.CIFAR100('data', train=False, transform=test_compose)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=False)
    num_classes = 100
else:
    raise RuntimeError('dataset must be one of "cifar100" or "cifar10"')


# ## Creating the DenseNet Model
# 
# With the data loaded, we can move on to defining our DKL model. A DKL model consists of three
# components: the neural network, the Gaussian process layer used after the neural network
# , and the Softmax likelihood.
# 
# The first step is defining the neural network architecture. To do this, we use a slightly
# modified version of the DenseNet available in the standard PyTorch package.
# Specifically, we modify it to remove the softmax layer, since we'll only be needing the
# final features extracted from the neural network.

class DenseNetFeatureExtractor(DenseNet):
    def forward(self, x):
        features = self.features(x)
        out = F.relu(features, inplace=True)
        out = F.avg_pool2d(out, kernel_size=self.avgpool_size).view(features.size(0), -1)
        return out


feature_extractor = DenseNetFeatureExtractor(block_config=(6, 6, 6), num_classes=num_classes).cuda()
num_features = feature_extractor.classifier.in_features


# ## Creating the GP Layer
# 
# In the next cell, we create the layer of Gaussian process models that are called after the
# neural network. In this case, we'll be using one GP per feature, as in the SV-DKL paper.
# The outputs of these Gaussian processes will the be mixed in the softmax likelihood.

# In[5]:


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


# ## Creating the DKL Model
# 
# With both the DenseNet feature extractor and GP layer defined, we can put them together
# in a single module that simply calls one and then the other, much like building any Sequential
# neural network in PyTorch. This completes defining our DKL model.

# In[6]:


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


model = DKLModel(feature_extractor, num_dim=num_features).cuda()
likelihood = gpytorch.likelihoods.SoftmaxLikelihood(num_features=model.num_dim,
                                                    n_classes=num_classes).cuda()

# ## Defining Training and Testing Code
# 
# Next, we define the basic optimization loop and testing code. This code is entirely analogous
# to the standard PyTorch training loop. We create a `torch.optim.SGD` optimizer with the
# parameters of the neural network on which we apply the standard amount of weight decay suggested
# from the paper, the parameters of the Gaussian process (from which we omit weight decay,
# as L2 regualrization on top of variational inference is not necessary), and the mixing parameters
# of the Softmax likelihood.
# 
# We use the standard learning rate schedule from the paper, where we decrease the learning
# rate by a factor of ten 50% of the way through training, and again at 75% of the way
# training.

# In[7]:


n_epochs = 300
lr = 0.1
optimizer = SGD([
    {'params': model.feature_extractor.parameters()},
    {'params': model.gp_layer.hyperparameters(), 'lr': lr * 0.01},
    {'params': model.gp_layer.variational_parameters()},
    {'params': likelihood.parameters()},
], lr=lr, momentum=0.9, nesterov=True, weight_decay=0)
scheduler = MultiStepLR(optimizer, milestones=[0.5 * n_epochs, 0.75 * n_epochs], gamma=0.1)


def train(epoch):
    model.train()
    likelihood.train()

    mll = gpytorch.mlls.VariationalELBO(likelihood, model.gp_layer,
                                        num_data=len(train_loader.dataset))

    train_loss = 0.
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        output = model(data)
        loss = -mll(output, target)
        loss.backward()
        optimizer.step()
        if (batch_idx + 1) % 25 == 0:
            print('Train Epoch: %d [%03d/%03d], Loss: %.6f' % (
                epoch, batch_idx + 1, len(train_loader), loss.item()))


def test():
    import torch
    model.eval()
    likelihood.eval()

    correct = 0
    for data, target in test_loader:
        data, target = data.cuda(), target.cuda()
        with torch.no_grad():
            output = likelihood(model(data))
            pred = output.probs.argmax(1)
            correct += pred.eq(target.view_as(pred)).cpu().sum()
    print('Test set: Accuracy: {}/{} ({}%)'.format(
        correct, len(test_loader.dataset), 100. * correct / float(len(test_loader.dataset))
    ))


# ## Train the Model
# 
# We are now ready to train the model.
# At the end of each Epoch we report the current test loss and accuracy,
# and we save a checkpoint model out to a file.

# In[8]:


for epoch in range(1, n_epochs + 1):
    scheduler.step()
    with gpytorch.settings.use_toeplitz(False), gpytorch.settings.max_preconditioner_size(0):
        train(epoch)
        test()
    state_dict = model.state_dict()
    likelihood_state_dict = likelihood.state_dict()
    torch.save({'model': state_dict, 'likelihood': likelihood_state_dict},
               'dkl_cifar_checkpoint.dat')
