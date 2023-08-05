import gpytorch
import torch
from torch.nn import CrossEntropyLoss

from baal.modelwrapper import ModelWrapper


class GaussianProcessWrapper(ModelWrapper):
    def __init__(self, model, likelihood, num_data):
        self.model = model
        self.likelihood = likelihood
        self.mll = gpytorch.mlls.VariationalELBO(likelihood, model.gp_layer, num_data=num_data)
        self.criterion = CrossEntropyLoss()

    def train_on_batch(self, data, target, optimizer, cuda=False):
        if cuda:
            data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        output = self.model(data)
        loss = -self.mll(output, target)
        loss.backward()
        optimizer.step()
        return loss

    def test_on_batch(self, data, target, cuda=False):
        with torch.no_grad():
            if cuda:
                data, target = data.cuda(), target.cuda()
            return self.criterion(self.likelihood(self.model(data)).probs, target)

    def get_params(self, lr):
        return [{'params': self.model.feature_extractor.parameters()},
                {'params': self.model.gp_layer.hyperparameters(), 'lr': lr * 0.01},
                {'params': self.model.gp_layer.variational_parameters()},
                {'params': self.likelihood.parameters()}]

    def state_dict(self):
        return self.model.state_dict(), self.likelihood.state_dict()

    def load_state_dict(self, state_dict):
        self.model.load_state_dict(state_dict[0])
        self.likelihood.load_state_dict(state_dict[1])

    def predict_on_batch(self, data, iterations=1, cuda=False):
        with torch.no_grad():
            if cuda:
                data = data.cuda()
            return torch.stack([self.likelihood(self.model(data)).probs
                                for _ in range(iterations)], dim=-1)

    def train(self):
        self.model.train()
        self.likelihood.train()

    def eval(self):
        self.model.eval()
        self.likelihood.eval()
