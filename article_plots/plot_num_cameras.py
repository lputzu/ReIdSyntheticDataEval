import matplotlib.pyplot as plt
import numpy as np
import copy, joblib


num_cams = [4, 8, 12, 16, 20, 24, 28]
pkl_names = "exp_FineGPR/finegpr2duke_4sceneNUMcamere_k2"

def check(path):
    if os.path.isfile(path) and os.access(path, os.R_OK):
        print("file present")
        exist = True
    else:
        print("File not present")
        exist = False
    return exist


def getDat(path):
    exist = check(path)
    if exist:
        dat = joblib.load(path)
    else:
        dat = []
    return (exist, np.array(dat))


def create_plot():
    dist_intra, dista_extra = list(), list()
    for num_cam in num_cams:
        pkl_name_intra = pkl_names.replace('NUM', str(num_cam)) + '_dist_intra.pkl'
        (exist1,dist_intra) = getDat(pkl_name_intra)
        pkl_name_extra = pkl_names.replace('NUM', str(num_cam)) + '_dist_extra.pkl'
        (exist2,dist_extra) = getDat(pkl_name_extra)
        if not exist1 or not exist2 :
            raise ValueError('Distances with ', num_cam, ' cameras not present')
            dist_intra.append(dist_intra)
            dist_extra.append(dist_extra)

    # plot model performance for comparison
    plt.boxplot(dist_intra, labels=num_cams, showmeans=True)
    plt.boxplot(dist_extra, labels=num_cams, showmeans=True)
    plt.rcParams["figure.dpi"] = 300
    plt.xlabel("# Cams", size=12)
    plt.ylabel("Distance", size=12)
    plt.savefig(pkl_names + '_plot.png')

if __name__ == '__main__':
    create_plot()
