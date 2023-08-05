from gxdltk.header import *

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
    return np.sum(p==l)/len(label)

def sim(a: tensor, b: tensor) -> float:
    """
    calc vector sim
    :param a:
    :param b:
    :return:
    """
    res = th.dot(a, b) / (a.norm()*b.norm())
    return res.item()
