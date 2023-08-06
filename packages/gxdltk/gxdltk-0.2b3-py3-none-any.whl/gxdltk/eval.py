from gxdltk.header import *
from gxdltk.errors.error import NoBackendError

def calc_acc(pred: list, label: list) -> float:
    """
    calc accuracy
    :param pred:
    :param label:
    :return:
    """
    assert len(pred) == len(label), "length of arg#1 must be equal to arg#2"
    p = np.array(pred)
    l = np.array(label)
    return np.sum(p == l) / len(label)


def sim(a, b) -> float:
    if os.environ["GXBACKEND"] == 'torch':
        return sim_th(a, b)
    else:
        # default use mxnet
        return sim_mx(a, b)


def sim_th(a: tensor, b: tensor) -> float:
    """
    calc vector sim
    :param a:
    :param b:
    :return:
    """
    res = th.dot(a, b) / (a.norm() * b.norm())
    return res.item()


def sim_mx(a: nd.NDArray, b: nd.NDArray) -> float:
    """
    calc vector sim in mxnet
    :param a: vec a
    :param b: vec b
    :return: similarity of a and b
    """
    res = nd.dot((a, b)) / (a.norm() * b.norm())
    return res
