import yaml
import numpy as np
from numpy.random import choice
from os import listdir
from os.path import join


def load_config():
    try:
        with open(join("config.yaml")) as yaml_file:
            doc = yaml.load(yaml_file)
        return doc
    except:
        raise Exception("Can't load config file")


def randomization(n1=6, n2=12):
    grup1 = np.random.choice([f for f in listdir(join("images", "Gr 1"))], n1, replace=False)
    part1_a = grup1[:int(n1/2)]
    part3_a = grup1[int(n1/2):]
    part1_b = [f for f in listdir(join("images", "Gr 2")) if f.split("_")[0] in [e.split("_")[0] for e in part3_a]]
    part3_b = [f for f in listdir(join("images", "Gr 2")) if f.split("_")[0] in [e.split("_")[0] for e in part1_a]]
    part1 = [join("images", "Gr 1", e) for e in part1_a] + [join("images", "Gr 2", e) for e in part1_b]
    np.random.shuffle(part1)
    part3 = [join("images", "Gr 1", e) for e in part3_a] + [join("images", "Gr 2", e) for e in part3_b]
    np.random.shuffle(part3)

    temp = int(n2/2)
    part2_a = list(choice([join("images", "Gr 3", f) for f in listdir(join("images", "Gr 3"))], temp, replace=False))
    part2_b = list(choice([join("images", "Gr 4", f) for f in listdir(join("images", "Gr 4"))], temp, replace=False))
    part2 = part2_a + part2_b
    np.random.shuffle(part2)
    return part1 + part2 + part3


def load_train(n=2):
    return list(choice([join("images", "train", f) for f in listdir(join("images", "train"))], n, replace=False))
