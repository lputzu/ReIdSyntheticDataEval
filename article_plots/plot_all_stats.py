import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import copy, joblib
import os
import argparse

from statistics import ClonedPerson
from statistics import finegpr
from statistics import personx
from statistics import unrealperson
from statistics import syri
from statistics import randperso2
from statistics import weperson

names = ["UnrealPerson","PersonX","ClonedPerson","SyRI","RandPerson","FineGPR","WePerson"]

min_img_per_pid_v, mean_img_per_pid_v, max_img_per_pid_v = list(), list(), list()
min_pid_per_camid_v, mean_pid_per_camid_v, max_pid_per_camid_v = list(), list(), list()

def get_store_stats(img_per_pid_v, pid_per_camid_v):
    global min_img_per_pid_v
    global mean_img_per_pid_v
    global max_img_per_pid_v
    global min_pid_per_camid_v
    global mean_pid_per_camid_v
    global max_pid_per_camid_v

    min_img_per_pid_v.append(min(img_per_pid_v))
    mean_img_per_pid_v.append(sum(img_per_pid_v)/len(img_per_pid_v))
    max_img_per_pid_v.append(max(img_per_pid_v))
    min_pid_per_camid_v.append(min(pid_per_camid_v))
    mean_pid_per_camid_v.append(sum(pid_per_camid_v)/len(pid_per_camid_v))
    max_pid_per_camid_v.append(max(pid_per_camid_v))


def plot_v1():

    global min_img_per_pid_v
    global mean_img_per_pid_v
    global max_img_per_pid_v
    global min_pid_per_camid_v
    global mean_pid_per_camid_v
    global max_pid_per_camid_v

    N = 7
    ind = np.arange(N)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    min_img_per_pid_v = np.array(min_img_per_pid_v)
    max_img_per_pid_v = np.array(max_img_per_pid_v)

    p1 = plt.bar(ind, min_img_per_pid_v, width)

    p2 = plt.bar(ind, max_img_per_pid_v-min_img_per_pid_v, width, bottom=min_img_per_pid_v)

    p3 = plt.plot(ind, mean_img_per_pid_v, marker='o', c='r')
    for i in range(len(ind)):
        plt.text(i, int(mean_img_per_pid_v[i]), int(mean_img_per_pid_v[i]), ha = 'center')

    plt.xticks(ind, names, rotation=30, ha='right')
    plt.ylim(top=1850)
    plt.legend((p1[0], p3[0], p2[0]), ('min', 'avg', 'max'))
    plt.ylabel("#images per ID", size=12)
    plt.tight_layout()
    plt.savefig('imagesXID_plot.png')


    plt.clf()
    min_pid_per_camid_v = np.array(min_pid_per_camid_v)
    max_pid_per_camid_v = np.array(max_pid_per_camid_v)

    p1 = plt.bar(ind, min_pid_per_camid_v, width)

    p2 = plt.bar(ind, max_pid_per_camid_v-min_pid_per_camid_v, width, bottom=min_pid_per_camid_v)

    p3 = plt.plot(ind, mean_pid_per_camid_v, marker='o', c='r')
    for i in range(len(ind)):
        plt.text(i, int(mean_pid_per_camid_v[i]), int(mean_pid_per_camid_v[i]), ha = 'center')

    plt.xticks(ind, names, rotation=30, ha='right')
    plt.ylim(top=8100)
    plt.legend((p1[0], p3[0], p2[0]), ('min', 'avg', 'max'))
    plt.ylabel("#IDs per camera", size=12)
    plt.tight_layout()
    plt.savefig('PidXcamim_plot.png')


def plot_v2():

    global min_img_per_pid_v
    global mean_img_per_pid_v
    global max_img_per_pid_v
    global min_pid_per_camid_v
    global mean_pid_per_camid_v
    global max_pid_per_camid_v

    base_colors = {"min": "blue", "avg": "orange", "max": "green"}
    N = 7
    sep = 4

    width = 0.4       # the width of the bars: can also be len(x) sequence
    min_img_per_pid_v = np.array(min_img_per_pid_v)
    max_img_per_pid_v = np.array(max_img_per_pid_v)
    mean_img_per_pid_v = np.array(mean_img_per_pid_v)

    ind1 = np.array(list(range(1,sep*(N),sep)))
    p1 = plt.bar(ind1, min_img_per_pid_v, width, color = mcolors.to_rgba("blue", 1.0), edgecolor="darkslategray")

    ind2 = np.array(list(range(2,sep*(N),sep)))
    p2 = plt.bar(ind2, mean_img_per_pid_v, width, color = mcolors.to_rgba("orange", 1.0), edgecolor="darkslategray")

    ind3 = np.array(list(range(3,sep*(N),sep)))
    p3 = plt.bar(ind3, max_img_per_pid_v, width, color = mcolors.to_rgba("green", 1.0), edgecolor="darkslategray")

    plt.xticks(ind2, names, rotation=30, ha='right')
    plt.ylim(top=1850)
    plt.legend((p1[0], p2[0], p3[0]), ('min', 'avg', 'max'))
    plt.ylabel("#images per ID", size=12)
    plt.tight_layout()
    plt.savefig('imagesXID_plot.png')


    plt.clf()
    min_pid_per_camid_v = np.array(min_pid_per_camid_v)
    max_pid_per_camid_v = np.array(max_pid_per_camid_v)
    mean_pid_per_camid_v = np.array(mean_pid_per_camid_v)

    ind1 = np.array(list(range(1,sep*(N),sep)))
    p1 = plt.bar(ind1, min_pid_per_camid_v, width, color = mcolors.to_rgba("blue", 1.0), edgecolor="darkslategray")

    ind2 = np.array(list(range(2,sep*(N),sep)))
    p2 = plt.bar(ind2, mean_pid_per_camid_v, width, color = mcolors.to_rgba("orange", 1.0), edgecolor="darkslategray")

    ind3 = np.array(list(range(3,sep*(N),sep)))
    p3 = plt.bar(ind3, max_pid_per_camid_v, width, color = mcolors.to_rgba("green", 1.0), edgecolor="darkslategray")

    plt.xticks(ind2, names, rotation=30, ha='right')
    plt.ylim(top=8100)
    plt.legend((p1[0], p2[0], p3[0]), ('min', 'avg', 'max'))
    plt.ylabel("#IDs per camera", size=12)
    plt.tight_layout()
    plt.savefig('PidXcamim_plot.png')


if __name__ == "__main__":
    img_per_pid_v_1, pid_per_camid_v_1 = unrealperson2.process_dir(unrealperson2.train_dir)
    get_store_stats(img_per_pid_v_1, pid_per_camid_v_1)
    img_per_pid_v_2, pid_per_camid_v_2  = personx2.process_dir(personx2.train_dir)
    get_store_stats(img_per_pid_v_2, pid_per_camid_v_2)
    img_per_pid_v_3, pid_per_camid_v_3  = ClonedPerson2.process_dir(ClonedPerson2.train_dir)
    get_store_stats(img_per_pid_v_3, pid_per_camid_v_3)
    img_per_pid_v_4, pid_per_camid_v_4  = syri2.process_dir(syri2.train_dir)
    get_store_stats(img_per_pid_v_4, pid_per_camid_v_4)
    img_per_pid_v_5, pid_per_camid_v_5  = randperson2.process_dir(randperson2.train_dir)
    get_store_stats(img_per_pid_v_5, pid_per_camid_v_5)
    img_per_pid_v_6, pid_per_camid_v_6  = finegpr3.process_dir(finegpr3.train_dir)
    get_store_stats(img_per_pid_v_6, pid_per_camid_v_6)
    img_per_pid_v_7, pid_per_camid_v_7  = weperson2.process_dir(weperson2.train_dir)
    get_store_stats(img_per_pid_v_7, pid_per_camid_v_7)

    plot_v2()
