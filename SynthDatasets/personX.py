from __future__ import print_function, absolute_import
import os.path as osp
import glob
import re
import urllib
import zipfile

from .bases import BaseImageDataset

class PersonX(BaseImageDataset):
    """
    PersonX
    Reference:
    Sun et al. Dissecting Person Re-identification from the Viewpoint of Viewpoint. CVPR 2019.
    Dataset statistics:
    # identities: 1266
    # images: 9840 (train) + 5136 (query) + 30816 (gallery)
    """
    dataset_dir = 'personX'

    def __init__(self, root, verbose=True, **kwargs):
        super(PersonX, self).__init__()
        self.dataset_dir = osp.join(root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'bounding_box_train')
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'bounding_box_test')

        self._check_before_run()

        train = self._process_dir(self.train_dir, relabel=True)
        query = self._process_dir(self.query_dir, relabel=False)
        gallery = self._process_dir(self.gallery_dir, relabel=False)

        if verbose:
            print("=> PersonX loaded")
            self.print_dataset_statistics(train, query, gallery)

        self.train = train
        self.query = query
        self.gallery = gallery

        self.num_train_pids, self.num_train_imgs, self.num_train_cams, self.num_train_vids = self.get_imagedata_info(
            self.train)
        self.num_query_pids, self.num_query_imgs, self.num_query_cams, self.num_query_vids = self.get_imagedata_info(
            self.query)
        self.num_gallery_pids, self.num_gallery_imgs, self.num_gallery_cams, self.num_gallery_vids = self.get_imagedata_info(
            self.gallery)


    def _check_before_run(self):
            """Check if all files are available before going deeper"""
            if not osp.exists(self.dataset_dir):
                raise RuntimeError("'{}' is not available".format(self.dataset_dir))
            if not osp.exists(self.train_dir):
                raise RuntimeError("'{}' is not available".format(self.train_dir))
            # if not osp.exists(self.query_dir):
            #     raise RuntimeError("'{}' is not available".format(self.query_dir))
            # if not osp.exists(self.gallery_dir):
            #     raise RuntimeError("'{}' is not available".format(self.gallery_dir))

    def _process_dir(self, dir_path, relabel=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))

        pattern = re.compile(r'([-\d]+)_c([-\d]+)s\d+_([-\d]+)')
        pid_container = set()

        #### Forsubset experiments ####
        process_subset = False
        list_cameras = []  # insert the considered cameras
        k = 1  # number of images per identity
        num_img_id_cam2 = {}
        ###############################

        dataset = []
        count_num_imgs = 1266*[0]
        count_camid_imgs = 6*[0]
        dataset_imgpath = []
        dataset_pid = []
        dataset_camid = []
        num_img_id_cam = {}

        for img_path in img_paths:
            pid, camid, viewpoint = map(int, pattern.search(img_path).groups())

            assert 1 <= pid <= 1266  # pid == 0 means background

            if camid in num_img_id_cam:
                num_img_id_cam[camid].extend([pid])
            else:
                num_img_id_cam[camid] = [pid]

            #
            if process_subset and (camid in list_cameras) and (num_img_id_cam[camid].count(pid) >= 1) and (num_img_id_cam[camid].count(pid) < (k +1)):
                if camid in num_img_id_cam2:
                    num_img_id_cam2[camid].extend([pid])
                else:
                    num_img_id_cam2[camid] = [pid]
                pid_container.add(pid)
                count_camid_imgs[camid-1] += 1
                count_num_imgs[pid-1] +=1
                camid -= 1  # index starts from 0
                dataset_imgpath.append(img_path)
                dataset_pid.append(pid)
                dataset_camid.append(camid)
            else:
                pid_container.add(pid)
                count_camid_imgs[camid - 1] += 1
                count_num_imgs[pid - 1] += 1
                camid -= 1  # index starts from 0
                dataset_imgpath.append(img_path)
                dataset_pid.append(pid)
                dataset_camid.append(camid)

        pid2label = {pid: label for label, pid in enumerate(pid_container)}
        for i in range(len(dataset_imgpath)):
            pid = dataset_pid[i]
            img_path = dataset_imgpath[i]
            camid = dataset_camid[i]
            if relabel: pid = pid2label[pid]
            dataset.append((img_path, pid, camid))

        while 0 in count_camid_imgs:
            count_camid_imgs.remove(0)
        while 0 in count_num_imgs:
            count_num_imgs.remove(0)
        print('number of images in each camera', count_camid_imgs)
        print('number of images per each identity', count_num_imgs)

        return dataset
