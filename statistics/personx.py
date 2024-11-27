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
        camid = dataset_camid[i]
        # viewpoint = dataset_viewp[i]
        if relabel: pid = pid2label[pid]
        dataset.append((img_path, pid, camid)) # viewpoint
    return dataset


def process_dir(dir_path):
    img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
    pattern = re.compile(r'([-\d]+)_c([-\d]+)s\d+_([-\d]+)')

    #struttura per memorizzare i vari id
    pid_container = set()
    viewid_container = set()
    camid_container = set()

    #strutture per contare le immagini per i vari id
    img_per_pid = {}
    img_per_viewid = {}
    img_per_camid = {}

    pid_per_camid = {}
    viewid_per_camid = {}


    viewid_per_pid = {}
    camid_per_pid = {}

    img_per_camid_per_viewid_per_pid = {}

    for img_path in img_paths:
        pid, camid, viewid = map(int, pattern.search(img_path).groups())

        pid_container.add(pid)
        viewid_container.add(viewid)
        camid_container.add(camid)

        #contiamo le immagini per pid
        if pid in img_per_pid:
            img_per_pid[pid] += 1
        else:
            img_per_pid[pid] = 1

        if viewid in img_per_viewid:
            img_per_viewid[viewid] += 1
        else:
            img_per_viewid[viewid] = 1

        if camid in img_per_camid:
            img_per_camid[camid] += 1
        else:
            img_per_camid[camid] = 1

        #in questo if faccio un solo controllo, dato che se camid non e' presente
        #in pid_per_camid non sara' presente neanche nelle altre strutture
        if camid in pid_per_camid:
            pid_per_camid[camid].extend([pid])
            viewid_per_camid[camid].extend([viewid])
        else:
            pid_per_camid[camid] = [pid]
            viewid_per_camid[camid] = [viewid]

        #Stesso discorso anche in questo if
        if pid in viewid_per_pid:
            viewid_per_pid[pid].extend([viewid])
        else:
            viewid_per_pid[pid] = [viewid]

        #Stesso discorso anche in questo if
        if pid in img_per_camid_per_viewid_per_pid:
            if viewid in img_per_camid_per_viewid_per_pid[pid]:
                if camid in img_per_camid_per_viewid_per_pid[pid][viewid]:
                    img_per_camid_per_viewid_per_pid[pid][viewid][camid] +=1
                else:
                    img_per_camid_per_viewid_per_pid[pid][viewid].update({camid:1})
            else:
                img_per_camid_per_viewid_per_pid[pid].update({viewid:{camid:1}})
        else:
            img_per_camid_per_viewid_per_pid[pid] = {viewid:{camid:1}}


    print("# img", len(img_paths))

    print("# pid", len(pid_container))
    print("# viewid", len(viewid_container))
    print("# camid", len(camid_container))

    img_per_pid_v = img_per_pid.values()
    print('MINIMO numero immagini per PID', min(img_per_pid_v))
    print('MEDIO numero immagini per PID', sum(img_per_pid_v)/len(img_per_pid_v))
    print('MASSIMO numero immagini per PID', max(img_per_pid_v))

    img_per_viewid_v = img_per_viewid.values()
    print('MINIMO numero immagini per view', min(img_per_viewid_v))
    print('MASSIMO numero immagini per view', max(img_per_viewid_v))

    img_per_camid_v = img_per_camid.values()
    print('MINIMO numero immagini per camera', min(img_per_camid_v))
    print('MASSIMO numero immagini per camera', max(img_per_camid_v))

    pid_per_camid_v = [len(set(v)) for v in pid_per_camid.values()]
    print('Numero pid per camera', pid_per_camid_v)
    print("")
    print('MINIMO numero pid per camera', min(pid_per_camid_v))
    print('MEDIO numero pid per cameraD', sum(pid_per_camid_v)/len(pid_per_camid_v))
    print('MASSIMO numero pid per camera', max(pid_per_camid_v))
    print("")

    # viewid_per_camid_v = [len(set(v)) for v in viewid_per_camid.values()]
    # print('MINIMO numero views per camera', min(viewid_per_camid_v))
    # print('MASSIMO numero views per camera', max(viewid_per_camid_v))
    #
    # viewid_per_pid_v = [len(set(v)) for v in viewid_per_pid.values()]
    # print('MINIMO numero views per pid', min(viewid_per_pid_v))
    # print('MASSIMO numero views per pid', max(viewid_per_pid_v))
    # camid_per_pid_v = [len(set(v)) for v in camid_per_pid.values()]
    # print('MINIMO numero camera per pid', min(camid_per_pid_v))
    # print('MASSIMO numero camera per pid', max(camid_per_pid_v))
    #
    # img_per_camid_per_viewid_per_pid_v = [v2.values() for v in img_per_camid_per_viewid_per_pid.values() for v2 in v.values()]
    # print('MINIMO numero immagini per camera per view per pid', min(img_per_camid_per_viewid_per_pid_v))
    # print('MASSIMO numero immagini per camera per view per pid', max(img_per_camid_per_viewid_per_pid_v))

    return img_per_pid_v, pid_per_camid_v

dataset_dir = '/home/rdelussu/MMT/examples/data/personX/PersonX/'
train_dir = osp.join(dataset_dir, 'bounding_box_train')

if __name__ == '__main__':
    if not osp.exists(dataset_dir):
        raise RuntimeError("'{}' is not available".format(dataset_dir))
    if not osp.exists(train_dir):
        raise RuntimeError("'{}' is not available".format(train_dir))

    img_per_pid_v, pid_per_camid_v  = process_dir(train_dir)

#img_per_camid_per_viewid_per_pid_v = personx2.process_dir(personx2.train_dir)
