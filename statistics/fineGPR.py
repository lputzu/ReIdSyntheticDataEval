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
    pattern = re.compile(r'([-\d]+)_c([-\d]+)_w([-\d]+)_l([-\d]+)_p([-\d]+)')

    trainset_imgpath = []
    trainset_pid = []
    trainset_camid = []

    testset_imgpath = []
    testset_pid = []
    testset_camid = []

    #struttura per memorizzare i vari id
    pid_container = set()
    train_pid_container = set()
    test_pid_container = set()

    viewid_container = set()
    weatid_container = set()
    illid_container = set()
    camid_container = set()

    #strutture per contare le immagini per i vari id
    img_per_pid = {}
    img_per_viewid = {}
    img_per_weatid = {}
    img_per_illid = {}
    img_per_camid = {}

    pid_per_camid = {}
    viewid_per_camid = {}
    weatid_per_camid = {}
    illid_per_camid = {}

    viewid_per_pid = {}
    weatid_per_pid = {}
    illid_per_pid = {}
    camid_per_pid = {}

    img_per_pid_per_camid = {}
    img_per_weatid_per_illid = {}
    img_per_weatid_per_pid = {}
    img_per_illid_per_pid = {}
    img_per_camid_per_viewid_per_pid = {}
    img_per_weatid_per_illid_per_pid = {}

    ill_condition = 6
    weat_conditions = [5, 6, 7]

    for img_path in img_paths:
        pid, viewid, weatid, illid, camid = map(int, pattern.search(img_path).groups())

        pid_container.add(pid)
        viewid_container.add(viewid)
        weatid_container.add(weatid)
        illid_container.add(illid)
        camid_container.add(camid)

        if (weatid in weat_conditions) and (illid == ill_condition) :
            if len(train_pid_container) >= 575 and (pid not in train_pid_container):
                test_pid_container.add(pid)
                testset_imgpath.append(img_path)
                testset_pid.append(pid)
                testset_camid.append(weatid)
            else:
                train_pid_container.add(pid)
                trainset_imgpath.append(img_path)
                trainset_pid.append(pid)
                trainset_camid.append(weatid)

        #contiamo le immagini per pid
        if pid in img_per_pid:
            img_per_pid[pid] += 1
        else:
            img_per_pid[pid] = 1

        if viewid in img_per_viewid:
            img_per_viewid[viewid] += 1
        else:
            img_per_viewid[viewid] = 1

        if weatid in img_per_weatid:
            img_per_weatid[weatid] += 1
        else:
            img_per_weatid[weatid] = 1

        if illid in img_per_illid:
            img_per_illid[illid] += 1
        else:
            img_per_illid[illid] = 1

        if camid in img_per_camid:
            img_per_camid[camid] += 1
        else:
            img_per_camid[camid] = 1


        #in questo if faccio un solo controllo, dato che se camid non e' presente
        #in pid_per_camid non sara' presente neanche nelle altre strutture
        if camid in pid_per_camid:
            pid_per_camid[camid].extend([pid])
            viewid_per_camid[camid].extend([viewid])
            weatid_per_camid[camid].extend([weatid])
            illid_per_camid[camid].extend([illid])
        else:
            pid_per_camid[camid] = [pid]
            viewid_per_camid[camid] = [viewid]
            weatid_per_camid[camid] = [weatid]
            illid_per_camid[camid] = [illid]
        #Stesso discorso anche in questo if
        if pid in viewid_per_pid:
            viewid_per_pid[pid].extend([viewid])
            weatid_per_pid[pid].extend([weatid])
            illid_per_pid[pid].extend([illid])
            camid_per_pid[pid].extend([camid])
        else:
            viewid_per_pid[pid] = [viewid]
            weatid_per_pid[pid] = [weatid]
            illid_per_pid[pid] = [illid]
            camid_per_pid[pid] = [camid]


        #anche in questi if faccio una assunzione simile
        if pid in img_per_weatid_per_pid:
            if weatid in img_per_weatid_per_pid[pid]:
                img_per_weatid_per_pid[pid][weatid] +=1
            else:
                img_per_weatid_per_pid[pid].update({weatid:1})
            if illid in img_per_illid_per_pid[pid]:
                img_per_illid_per_pid[pid][illid] +=1
            else:
                img_per_illid_per_pid[pid].update({illid:1})
        else:
            img_per_weatid_per_pid[pid] = {weatid:1}
            img_per_illid_per_pid[pid] = {illid:1}


        if illid in img_per_weatid_per_illid:
            if weatid in img_per_weatid_per_illid[illid]:
                img_per_weatid_per_illid[illid][weatid] +=1
            else:
                img_per_weatid_per_illid[illid].update({weatid:1})
        else:
            img_per_weatid_per_illid[illid] = {weatid:1}

        if camid in img_per_pid_per_camid:
            if pid in img_per_pid_per_camid[camid]:
                img_per_pid_per_camid[camid][pid] +=1
            else:
                img_per_pid_per_camid[camid].update({pid:1})
        else:
            img_per_pid_per_camid[camid] = {pid:1}

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

        if pid in img_per_weatid_per_illid_per_pid:
            if weatid in img_per_weatid_per_illid_per_pid[pid]:
                if illid in img_per_weatid_per_illid_per_pid[pid][weatid]:
                    img_per_weatid_per_illid_per_pid[pid][weatid][illid] +=1
                else:
                    img_per_weatid_per_illid_per_pid[pid][weatid].update({illid:1})
            else:
                img_per_weatid_per_illid_per_pid[pid].update({weatid:{illid:1}})
        else:
            img_per_weatid_per_illid_per_pid[pid] = {weatid:{illid:1}}

    trainset = relabel(train_pid_container, trainset_imgpath, trainset_pid, trainset_camid)
    testset = relabel(test_pid_container, testset_imgpath, testset_pid, testset_camid)


    print("# img", len(img_paths))

    print("# pid", len(pid_container))
    print("# train pid", len(train_pid_container))
    print("# test pid", len(test_pid_container))
    print("# viewid", len(viewid_container))
    print("# weatid", len(weatid_container))
    print("# illid", len(illid_container))
    print("# camid", len(camid_container))

    img_per_pid_v = img_per_pid.values()
    print('MINIMO numero immagini per PID', min(img_per_pid_v))
    print('MEDIO numero immagini per PID', sum(img_per_pid_v)/len(img_per_pid_v))
    print('MASSIMO numero immagini per PID', max(img_per_pid_v))

    img_per_viewid_v = img_per_viewid.values()
    print('MINIMO numero immagini per view', min(img_per_viewid_v))
    print('MASSIMO numero immagini per view', max(img_per_viewid_v))

    img_per_weatid_v = img_per_weatid.values()
    print('MINIMO numero immagini per weat', min(img_per_weatid_v))
    print('MASSIMO numero immagini per weat', max(img_per_weatid_v))

    img_per_illid_v = img_per_illid.values()
    print('MINIMO numero immagini per illum', min(img_per_illid_v))
    print('MASSIMO numero immagini per illum', max(img_per_illid_v))

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


    viewid_per_camid_v = [len(set(v)) for v in viewid_per_camid.values()]
    print('MINIMO numero views per camera', min(viewid_per_camid_v))
    print('MASSIMO numero views per camera', max(viewid_per_camid_v))
    weatid_per_camid_v = [len(set(v)) for v in weatid_per_camid.values()]
    print('MINIMO numero weather per camera', min(weatid_per_camid_v))
    print('MASSIMO numero weather per camera', max(weatid_per_camid_v))
    illid_per_camid_v = [len(set(v)) for v in illid_per_camid.values()]
    print('MINIMO numero illuminazioni per camera', min(illid_per_camid_v))
    print('MASSIMO numero illuminazioni per camera', max(illid_per_camid_v))

    viewid_per_pid_v = [len(set(v)) for v in viewid_per_pid.values()]
    print('MINIMO numero views per pid', min(viewid_per_pid_v))
    print('MASSIMO numero views per pid', max(viewid_per_pid_v))
    weatid_per_pid_v = [len(set(v)) for v in weatid_per_pid.values()]
    print('MINIMO numero weather per pid', min(weatid_per_pid_v))
    print('MASSIMO numero weather per pid', max(weatid_per_pid_v))
    illid_per_pid_v = [len(set(v)) for v in illid_per_pid.values()]
    print('MINIMO numero illuminazioni per pid', min(illid_per_pid_v))
    print('MASSIMO numero illuminazioni per pid', max(illid_per_pid_v))
    camid_per_pid_v = [len(set(v)) for v in camid_per_pid.values()]
    print('MINIMO numero camera per pid', min(camid_per_pid_v))
    print('MASSIMO numero camera per pid', max(camid_per_pid_v))


    img_per_pid_per_camid_v = [len(set(v)) for v in img_per_pid_per_camid.values()]
    print('Numero pid per camera', img_per_pid_per_camid.values())
    print("")
    print('MINIMO numero pid per camera', min(img_per_pid_per_camid_v))
    print('MEDIO numero pid per cameraD', sum(img_per_pid_per_camid_v)/len(img_per_pid_per_camid_v))
    print('MASSIMO numero pid per camera', max(img_per_pid_per_camid_v))
    print("")

    #
    #
    # img_per_weatid_per_pid_v = [v.values() for v in img_per_weatid_per_pid.values()]
    # print('MINIMO numero immagini per weather per pid', min(img_per_weatid_per_pid_v))
    # print('MASSIMO numero immagini per weather per pid', max(img_per_weatid_per_pid_v))
    # img_per_illid_per_pid_v = [v.values() for v in img_per_illid_per_pid.values()]
    # print('MINIMO numero immagini per illuminazione per pid', min(img_per_illid_per_pid_v))
    # print('MASSIMO numero immagini per illuminazione per pid', max(img_per_illid_per_pid_v))
    #
    # img_per_weatid_per_illid_v = [v.values() for v in img_per_weatid_per_illid.values()]
    # print('MINIMO numero immagini per illuminazione per weatid', min(img_per_weatid_per_illid_v))
    # print('MASSIMO numero immagini per illuminazione per weatid', max(img_per_weatid_per_illid_v))
    #
    # img_per_camid_per_viewid_per_pid_v = [v2.values() for v in img_per_camid_per_viewid_per_pid.values() for v2 in v.values()]
    # print('MINIMO numero immagini per camera per view per pid', min(img_per_camid_per_viewid_per_pid_v))
    # print('MASSIMO numero immagini per camera per view per pid', max(img_per_camid_per_viewid_per_pid_v))

    return img_per_pid_v, pid_per_camid_v

dataset_dir = '/home/rdelussu/MMT/examples/data/finegpr/FineGPR'
train_dir = osp.join(dataset_dir, 'bounding_box_train')

if __name__ == '__main__':
    if not osp.exists(dataset_dir):
        raise RuntimeError("'{}' is not available".format(dataset_dir))
    if not osp.exists(train_dir):
        raise RuntimeError("'{}' is not available".format(train_dir))

    img_per_pid_v, pid_per_camid_v  = process_dir(train_dir)

#trainset, testset = finegpr3.process_dir(finegpr3.train_dir)
