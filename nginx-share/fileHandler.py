from os import path, remove
import shutil


class fileHandler(object):
    """add and remove files from the specified directory and create index"""
    def __init__(self, root):
        self.root = path.abspath(root)

    def add(self, src):
        apath = path.abspath(src)
        if path.exists(apath):
            if path.isfile(apath):
                shutil.copy2(apath, self.root)
            if path.isdir(apath):
                dst = self.root + '/' + path.basename(apath)
                shutil.copytree(apath, dst)
            else:
                pass
        else:
            print "file does not exist"

    def remove(self, src):
            apath = path.abspath(src)
            if path.exists(apath):
                if path.isfile(apath):
                    remove(apath)
                if path.isdir(apath):
                    shutil.rmtree(apath)
                else:
                    pass
            else:
                print "file does not exist"
