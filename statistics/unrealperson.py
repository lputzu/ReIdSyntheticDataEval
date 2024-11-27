from __future__ import print_function, absolute_import
import os.path as osp
import glob
import re
import urllib
import zipfile

from collections import OrderedDict

def relabel(pid_container, dataset_imgpath, dataset_pid, dataset_camid):
    dataset = []
    pid2label = {pid: label for label, pid in enumerate(pid_container)}
                # if relabel: pid = pid2label[pid]
                # dataset.append((img_path, pid, camid))
    for i in range(len(dataset_imgpath)):
        pid = dataset_pid[i]
        img_path = dataset_imgpath[i]
        # camid in realta' e'  weat
        camid = dataset_camid[i]
        # viewpoint = dataset_viewp[i]
        if relabel: pid = pid2label[pid]
        dataset.append((img_path, pid, camid)) # viewpoint
    return dataset


def process_dir(dir_path):
    img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
    pattern = re.compile(r'([-\d]+)_c([-\d]+)_([-\d]+)')

    #struttura per memorizzare i vari id
    pid_container = set()
    camid_container = set()
    frameid_container = set()

    #strutture per contare le immagini per i vari id
    img_per_pid = {}
    img_per_camid = {}
    img_per_frameid = {}


    pid_per_camid = {}
    frameid_per_camid = {}

    camid_per_pid = {}
    frameid_per_pid = {}

    img_per_camid_per_pid = {}

    for img_path in img_paths:
        pid, camid, frameid = map(int, pattern.search(img_path).groups())

        pid_container.add(pid)
        camid_container.add(camid)
        frameid_container.add(frameid)

        #contiamo le immagini per pid
        if pid in img_per_pid:
            img_per_pid[pid] += 1
        else:
            img_per_pid[pid] = 1

        if camid in img_per_camid:
            img_per_camid[camid] += 1
        else:
            img_per_camid[camid] = 1

        if frameid in img_per_frameid:
            img_per_frameid[frameid] += 1
        else:
            img_per_frameid[frameid] = 1


        #in questo if faccio un solo controllo, dato che se camid non e' presente
        #in pid_per_camid non sara' presente neanche nelle altre strutture
        if camid in pid_per_camid:
            pid_per_camid[camid].extend([pid])
            frameid_per_camid[camid].extend([frameid])
        else:
            pid_per_camid[camid] = [pid]
            frameid_per_camid[camid] = [frameid]
        #Stesso discorso anche in questo if
        if pid in camid_per_pid:
            frameid_per_pid[pid].extend([frameid])
            camid_per_pid[pid].extend([camid])
        else:
            frameid_per_pid[pid] = [frameid]
            camid_per_pid[pid] = [camid]

        #anche in questi if faccio una assunzione simile
        if pid in img_per_camid_per_pid:
            if camid in img_per_camid_per_pid[pid]:
                img_per_camid_per_pid[pid][camid] +=1
            else:
                img_per_camid_per_pid[pid].update({camid:1})
        else:
            img_per_camid_per_pid[pid] = {camid:1}

    print("# img", len(img_paths))

    print("# pid", len(pid_container))
    print("# camid", len(camid_container))
    print("# frameid", len(frameid_container))
    print("")
    img_per_pid_v = img_per_pid.values()
    print('MINIMO numero immagini per PID', min(img_per_pid_v))
    print('MEDIO numero immagini per PID', sum(img_per_pid_v)/len(img_per_pid_v))
    print('MASSIMO numero immagini per PID', max(img_per_pid_v))
    print("")
    img_per_camid_v = img_per_camid.values()
    print('Numero immagini per camera', img_per_camid_v)
    print("")
    print("")

    pid_per_camid_v = [len(set(v)) for v in pid_per_camid.values()]
    print('Numero pid per camera', pid_per_camid_v)
    print("")
    print('MINIMO numero pid per camera', min(pid_per_camid_v))
    print('MEDIO numero pid per cameraD', sum(pid_per_camid_v)/len(pid_per_camid_v))
    print('MASSIMO numero pid per camera', max(pid_per_camid_v))
    print("")

    camid_per_pid_v = [len(set(v)) for v in camid_per_pid.values()]
    print('MINIMO numero camera per pid', min(camid_per_pid_v))
    print('MASSIMO numero camera per pid', max(camid_per_pid_v))
    frameid_per_pid_v = [len(set(v)) for v in frameid_per_pid.values()]
    print('MINIMO numero frame per pid', min(frameid_per_pid_v))
    print('MASSIMO numero frame per pid', max(frameid_per_pid_v))

    img_per_camid_per_pid_v = [len(v.values()) for v in img_per_camid_per_pid.values()]
    print('MINIMO numero immagini per camera per pid', min(img_per_camid_per_pid_v))
    print('MASSIMO numero immagini per camera per pid', max(img_per_camid_per_pid_v))

    return img_per_pid_v, pid_per_camid_v

dataset_dir = '/home/rdelussu/MMT/examples/data/unrealperson/unrealperson/'
train_dir = osp.join(dataset_dir, 'bounding_box_train')

if __name__ == '__main__':
    if not osp.exists(dataset_dir):
        raise RuntimeError("'{}' is not available".format(dataset_dir))
    if not osp.exists(train_dir):
        raise RuntimeError("'{}' is not available".format(train_dir))

    img_per_pid_v, pid_per_camid_v = process_dir(train_dir)

#img_per_camid_per_pid_v = unrealperson2.process_dir(unrealperson2.train_dir)
