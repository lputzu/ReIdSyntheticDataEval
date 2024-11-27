from __future__ import print_function, absolute_import
import os.path as osp
from glob import glob
import re
from itertools import combinations, permutations

from .bases import BaseImageDataset

class ClonedPerson(BaseImageDataset):

    dataset_dir = 'clonedperson'

    def __init__(self, root, verbose=True, **kwargs):
        super(ClonedPerson, self).__init__()

        self.dataset_dir = osp.join(root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'train')
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'bounding_box_test')

        self._check_before_run()
        train = self._process_dir(self.train_dir, relabel=True)
        query = self._process_dir(self.query_dir, relabel=False)
        gallery = self._process_dir(self.gallery_dir, relabel=False)

        if verbose:
            print("=> ClonedPerson loaded")
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
        img_paths = sorted(glob(osp.join(dir_path, '*g')))
        pattern = re.compile(r'([-\d]+)_s([-\d]+)_c([-\d]+)_f([-\d]+)')

        pid_container = set()

        data = []
        all_pids = {}
        camera_offset = [0, 0, 0, 4, 4, 8, 12, 12, 12, 12, 16, 16, 20]
        fps = 24

        #### For subset experiments ####
        process_subset = False
        list_cameras = [] # insert the considered cameras
        selected_ids = {} # insert the considered identities (pid)
        k = 1 # number of images per identity --> k
        num_img_id_cam2 = {}
        ##############################

        num_img_id_cam = {}

        count_num_imgs = 800000 * [0]
        count_camid_imgs = 24 * [0]


        for fpath in img_paths:
            # fname = osp.basename(fpath)  # filename: id6_s2_c2_f6.jpg
            pid, scene, cam, frame = map(int, pattern.search(fpath).groups())

            camid = camera_offset[scene] + cam  # make it starting from 0
            time = frame / fps
            #
            if camid in num_img_id_cam:
                num_img_id_cam[camid].extend([pid])
            else:
                num_img_id_cam[camid] = [pid]

            if process_subset and (camid in list_cameras) and (pid in selected_ids) and (num_img_id_cam[camid].count(pid) >=1) and (num_img_id_cam[camid].count(pid) < (k+1)):
                if camid in num_img_id_cam2:
                    num_img_id_cam2[camid].extend([pid])
                else:
                    num_img_id_cam2[camid] = [pid]
                if pid == -1: continue
                if pid not in all_pids:
                    all_pids[pid] = len(all_pids)
                if relabel:
                    pid = all_pids[pid]
                camid = camera_offset[scene] + cam
                count_num_imgs[pid-1] += 1
                count_camid_imgs[camid-1] += 1
                data.append((fpath, pid, camid))
            else:
                if pid == -1: continue
                if pid not in all_pids:
                    all_pids[pid] = len(all_pids)
                if relabel:
                    pid = all_pids[pid]
                camid = camera_offset[scene] + cam
                count_num_imgs[pid-1] += 1
                count_camid_imgs[camid-1] += 1
                data.append((fpath, pid, camid))


        while 0 in count_camid_imgs:
            count_camid_imgs.remove(0)
        while 0 in count_num_imgs:
            count_num_imgs.remove(0)
        print('number of images in each camera', count_camid_imgs)
        print('number of images per each identity', count_num_imgs)
        return data
