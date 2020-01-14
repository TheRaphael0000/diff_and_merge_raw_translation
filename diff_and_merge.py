from PIL import Image
import imagehash
import os
from difflib import SequenceMatcher
from shutil import copyfile


class Img:
    threshold = None

    def __init__(self, path):
        self.path = path
        self.img = Image.open(self.path)
        self.hash = imagehash.average_hash(self.img)

    def __eq__(self, other):
        return abs(self.hash - other.hash) < Img.threshold

    def __str__(self):
        return self.path

    def __hash__(self):
        return 0


class DiffMerge:

    def __init__(self, translation_folder, raw_folder, merge_folder, threshold):
        self.translation_folder = translation_folder
        self.raw_folder = raw_folder
        self.merge_folder = merge_folder
        self.threshold = threshold

        self.a = None
        self.b = None
        self.c = None

        self.merge_paths = None

    def load_path(folder):
        paths = []
        for root, dirs, files in os.walk(folder):
            for f in files:
                paths.append(os.path.join(root, f))
        return paths

    def load_img(paths):
        imgs = []
        for p in paths:
            img = Img(p)
            imgs.append(img)
        return imgs

    def load(self):
        Img.threshold = self.threshold
        a_p = DiffMerge.load_path(self.translation_folder)
        b_p = DiffMerge.load_path(self.raw_folder)

        self.a = DiffMerge.load_img(a_p)
        self.b = DiffMerge.load_img(b_p)

    def diff_and_merge(self):
        cruncher = SequenceMatcher(None, self.a, self.b, False)
        self.c = []

        for tag, alo, ahi, blo, bhi in cruncher.get_opcodes():
            if tag == 'replace':
                # replace strange things
                for i in range(blo, bhi):
                    self.c.append(self.b[i])
            elif tag == 'delete':
                # dont delete anything (maybe to be change, i dont really know)
                pass
            elif tag == 'insert':
                # insert file removed from b
                for i in range(blo, bhi):
                    self.c.append(self.b[i])
            elif tag == 'equal':
                # keep things from a
                for i in range(alo, ahi):
                    self.c.append(self.a[i])

    def create_merge(self):
        len_c = len(self.c)
        padding = len(str(len_c))
        self.merge_paths = []
        for index, ci in enumerate(self.c):
            src = ci.path
            ext = os.path.splitext(src)[1]
            file_format = "{:0>" + str(padding) + "}{}"
            filename = file_format.format(index, ext)
            dst = os.path.join(self.merge_folder, filename)
            self.merge_paths.append((src, dst))

    def merge(self,):
        if not os.path.exists(self.merge_folder):
            os.mkdir(self.merge_folder)
        for src, dst in self.merge_paths:
            copyfile(src, dst)
