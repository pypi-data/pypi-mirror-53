from baal import bayesian


def get_model(name, **kwargs):
    return {
        "vgg16": lambda: bayesian.vgg16(True, **kwargs),
        "resnet18": lambda: bayesian.resnet18(pretrained=True, **kwargs),
        "densenet161": lambda: bayesian.densenet161(pretrained=True, **kwargs),
    }[name]()
