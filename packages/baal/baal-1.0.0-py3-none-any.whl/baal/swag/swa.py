import torch
from torch.optim import SGD
from torch.optim.optimizer import required


class StochasticWeightAveraging(SGD):
    """Optimise a model using stochastic weight averaging.

    This class optimises using standard SGD intially, but when you call
    optimiser.swa(), your model parameters are converted to the average of
    some recent points along the gradient descent path.

    You can call optimiser.sgd() to reset the parameters to the most recent
    gradient descent point.

    Parameters
    ----------
    params (iterable):
        iterable of parameters to optimize or dicts defining parameter groups
    lr (float):
        learning rate
    momentum (float, optional):
        momentum factor (default: 0)
    weight_decay (float, optional):
        weight decay (L2 penalty) (default: 0)
    dampening (float, optional):
        dampening for momentum (default: 0)
    nesterov (bool, optional):
        enables Nesterov momentum (default: False)
    swa_burn_in : int
        The number of steps to take before beginning to average. Often, this is
        some multiple of the steps in an epoch, so that you train for N epochs
        before beginning to average.
    swa_steps : int
        The number of steps between each stochastic weight average update. This
        is often one epoch, e.g. epoch_size // batch_size.
    n_deviations : int
        How many deviations from the mean to store. These will be used to
        estimate the covariance between weights.
    """

    def __init__(
        self,
        params,
        lr=required,
        momentum=0,
        dampening=0,
        weight_decay=0,
        nesterov=False,
        swa_burn_in=required,
        swa_steps=required,
        n_deviations=20,
    ):

        super().__init__(
            params,
            lr=lr,
            momentum=momentum,
            dampening=dampening,
            weight_decay=weight_decay,
            nesterov=nesterov,
        )
        if swa_steps is required:
            raise ValueError(
                "You need to pass a number of steps after which averaging "
                "occurs, e.g. swa_steps=epoch_size // batch_size."
            )
        elif swa_steps == 0:
            raise ValueError("swa_steps needs to be a positive integer.")
        self.swa_steps = swa_steps
        if swa_burn_in is required:
            raise ValueError(
                "You need to pass a number of steps for which no averaging "
                "happens, e.g. swa_burn_in=100 * epoch_size // batch_size."
            )
        elif swa_burn_in < swa_steps:
            raise ValueError("swa_burn_in needs to be at least equal to swa_steps.")
        self.swa_burn_in = swa_burn_in

        self.state['n_steps'] = 0
        self.state['n_deviations'] = max((n_deviations, 1))

    def step(self, closure=None):
        # first, execute a standard gradient descent step
        super().step(closure=closure)
        self.state['n_steps'] += 1
        # check if n_steps indicates we need to update averages
        if (
            self.state['n_steps'] >= self.swa_burn_in
            and self.state['n_steps'] % self.swa_steps == 0
        ):
            self._update_means()

    def _update_means(self):
        # update our estimates of the means
        average_updates = (self.state['n_steps'] - self.swa_burn_in) // self.swa_steps
        for group in self.param_groups:
            for p in group["params"]:
                p_state = self.state[p]
                values = p.data.cpu()  # all the following values should be on CPU
                # update the mean (first moment)
                p_state["mean"] = (
                    p_state.get("mean", 0) * (average_updates) + values
                ) / (average_updates + 1)
                # update the square mean (second moment)
                p_state["square_mean"] = (
                    p_state.get("square_mean", 0) * average_updates + values ** 2
                ) / (average_updates + 1)
                # update the deviation matrix
                if "deviations" not in p_state:
                    p_state["deviations"] = (values - p_state["mean"]).unsqueeze(0)
                else:
                    p_state["deviations"] = torch.cat(
                        (p_state["deviations"], (values - p_state["mean"]).unsqueeze(0))
                    )
                # trim the matrix if needed
                if average_updates > self.state["n_deviations"]:
                    p_state["deviations"] = p_state["deviations"][1:, ...]

    def swa(self):
        """Apply the stochastic weight averaging to the model."""
        if (self.state['n_steps'] - self.swa_burn_in) // self.swa_steps > 0:
            for group in self.param_groups:
                for p in group["params"]:
                    p.data.copy_(self.state[p]["mean"])

    def sgd(self):
        """
        Un-apply the stochastic weight averaging to the model.

        Note that this only resets to the last point at which you did a SWA
        update, which is not necessarily the most recent stochastic gradient
        descent point.
        """
        if (self.state['n_steps'] - self.swa_burn_in) // self.swa_steps > 0:
            for group in self.param_groups:
                for p in group["params"]:
                    p.data.copy_(
                        self.state[p]["mean"] + self.state[p]["deviations"][-1, ...]
                    )

    def sample(self, scale=1.0):
        """
        Sample parameters and apply to the model being optimised.

        NB: Currently this only draws a diagonal sample and does not implement
        covariance between weights.

        Parameters
        ----------
        scale : float
            The amount by which to scale the variance of the distribution from
            which to draw samples. If zero, only the mean gets drawn. If more
            than 1.0, the distribution is broadened.
        """
        if (self.state['n_steps'] - self.swa_burn_in) // self.swa_steps > 0:
            for group in self.param_groups:
                for p in group["params"]:
                    param_state = self.state[p]
                    p.data.copy_(
                        param_state["mean"]
                        + torch.randn_like(param_state["mean"])
                        * (scale ** 0.5)
                        * (
                            (param_state["square_mean"] - param_state["mean"] ** 2)
                            .clamp(1e-30)
                            .sqrt()
                        )
                    )
