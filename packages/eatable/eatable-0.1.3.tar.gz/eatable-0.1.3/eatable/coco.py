import os.path as osp

import cv2
import pycocotools.coco as coco



class COCO(object):

    def __init__(self, images_directory, annotation_file):
        """initialize datasets

        Args:
            images_directory: string, usually as 'COCO/images/'
            annotations_file: string, usually a json file
        """
        self.coco = coco.COCO(annotation_file)
        self.root = osp.dirname(images_directory.rstrip(osp.sep))
        self.im_dir = images_directory
        self.im_ids = sorted(self.coco.imgs.keys())
        self.size = len(self.im_ids)
    
    def __len__(self):
        return self.size

    def get_im_path(self, index=None, im_id=None):
        if index is None and im_id is None:
            raise Exception("Either index or im_id should be provided")
        if index is not None:
            im_id = self.im_ids[index]
        im_meta = self.coco.loadImgs([im_id])[0]
        return osp.join(self.im_dir, im_meta['file_name'])

    def get_im_with_anns(self, index=None, im_id=None):
        """
        Args:
            index: index of image ids list 
            im_id: image id in COCO dataset
        Returns:
            a triple of (im_id, ann_metas, im) where im is image 
            object return by cv2.imread
        """
        if index is None and im_id is None:
            raise Exception("Either index or im_id should be provided")
        if index is not None:
            im_id = self.im_ids[index]
        ann_ids = self.coco.getAnnIds(im_id)
        ann_metas = self.coco.loadAnns(ann_ids)
        
        im_path = self.get_im_path(im_id=im_id)
        im = cv2.imread(im_path)
        return im_id, ann_metas, im