import os
from tensorflow import gfile
# from pyspark import SparkFiles
import boto3
from functools import reduce

class hdfsFile(object):
    ip = ''
    client = None
    @staticmethod
    def DeleteRecursively(path):
        hdfsFile.client.delete(path)

    @staticmethod
    def Remove(path):
        hdfsFile.client.delete(path)

    @staticmethod
    def ListDirectory(dirname):
        return hdfsFile.client.listdir(dirname)

    # 上传文件
    def upload(self, fileName, tmpFile):
        fs = self.client
        fs.copy_from_local(fileName, tmpFile)

    @staticmethod
    def Copy(srcPath, dstPath):
        if not srcPath.startswith('hdfs://'):
            dstPath = dstPath.strip('/')
            _ = os.system('hadoop fs -copyFromLocal {src} {dst}'.format(src=srcPath, dst=dstPath))
            # hdfsFile.client.copy_from_local(srcPath, dstPath)
        elif not dstPath.startswith('hdfs://'):
            srcPath = srcPath.strip('/')
            _ = os.system('hadoop fs -copyToLocal {src} {dst}'.format(src=srcPath, dst=dstPath))
            # hdfsFile.client.copy_to_local(srcPath, dstPath)
        else:
            srcPath = srcPath.strip('/')
            dstPath = dstPath.strip('/')
            _ = os.system('hadoop fs -cp {src} {dst}'.format(src=srcPath, dst=dstPath))
            # tmpPath = '/tmp/dl_rank/hdfs'
            # gfile.MakeDirs(tmpPath)
            # hdfsFile.client.copy_to_local(srcPath, tmpPath)
            # hdfsFile.client.copy_from_local(tmpPath, dstPath)
            # gfile.DeleteRecursively(tmpPath)

    @staticmethod
    def MakeDirs(filePath):
        if not hdfsFile.client.exists(filePath):
            # os.system('hadoop client -mkdir '+filePath)
            hdfsFile.client.mkdirs(filePath)
            return 'mkdir'
        return 'exits'

    @staticmethod
    def Rename(srcPath, dstPath):
        if not hdfsFile.client.exists(srcPath):
            return False
        hdfsFile.client.rename(srcPath, dstPath)
        return True

    @staticmethod
    def Walk(top):
        return hdfsFile.client.walk(top)

    @staticmethod
    def Open(filename):
        return hdfsFile.client.open(filename)

    @staticmethod
    def Exists(filename):
        return hdfsFile.client.exists(filename)

    @staticmethod
    def IsDirectory(filename):
        filestatus = hdfsFile.client.get_file_status(filename)
        assert False

class s3File(object):
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    @staticmethod
    def split_s3_path(filename):
        filename = filename.strip('s3://')
        bucket, key = filename.split('/', 1)
        return bucket, key

    @staticmethod
    def _list_obj_under_path(filename):
        filename = filename.strip('/')
        bucket, keyname = s3File.split_s3_path(filename)
        bucket = s3File.s3.Bucket(bucket)
        objs = bucket.objects.filter(Prefix=keyname)
        return objs

    @staticmethod
    def Exists(filename):
        objs = list(s3File._list_obj_under_path(filename))
        if len(objs) > 0:   # and objs[0].key.strip('/') == keyname:
            return True
        else:
            return False

    @staticmethod
    def IsDirectory(filename):
        objs = list(s3File._list_obj_under_path(filename))
        if len(objs) == 0:
            return False
        elif len(objs) > 1 or objs[0].key[-1] == '/':
            return True
        else:
            return False

    @staticmethod
    def ListDirectory(dirname):
        _, dirs, files = s3File.Walk(dirname, True)
        dirs = [d.strip('/') for d in dirs]
        return dirs + files

    @staticmethod
    def Open(filename):
        bucket, keyname = s3File.split_s3_path(filename)
        obj = s3File.s3.Object(bucket, keyname)
        return s3FileObj(obj.get()['Body'])#.read().decode('utf-8')

    @staticmethod
    def MakeDirs(dirname):
        bucket, keyname = s3File.split_s3_path(dirname)
        if keyname[-1] != '/':
            keyname = keyname + '/'
            s3File.client.put_object(Bucket=bucket, Key=keyname)

    @staticmethod
    def DeleteRecursively(dirname):
        obj = s3File._list_obj_under_path(dirname)
        obj.delete()

    @staticmethod
    def Walk(dirname, one_step=False):
        bucket, keyroot = s3File.split_s3_path(dirname)
        all_obj = [obj.key for obj in list(s3File._list_obj_under_path(dirname))]

        def _walk(root):
            obj_under_dir = [obj.strip(root) for obj in filter(lambda name: name.startswith(root), all_obj)]
            pre_key_under_dir = set([obj.split('/')[0]+'/' if '/' in obj else obj for obj in obj_under_dir])
            dirs, files = reduce(lambda x, y: (x[0]+[os.path.join(root, y)], x[1]) if '/' in y else (x[0], x[1]+[os.path.join(root, y)]),
                                 pre_key_under_dir,
                                 initial=([], []))
            return root, dirs, files

        def _recursive_walk(root):
            root, dirs, files = _walk(root)
            yield 's3://'+os.path.join(bucket, root), \
                  [d.strip('/') for d in dirs], \
                  files
            for d in dirs:
                yield from _recursive_walk(os.path.join(root, d))

        if dirname[-1] != '/':
            dirname += '/'
        if one_step:
            return _walk(keyroot)
        else:
            return _recursive_walk(keyroot)

    @staticmethod
    def Rename(oldname, newname):
        s3File.Copy(oldname, newname)
        oldbucket, oldkey = s3File.split_s3_path(oldname)
        s3File.s3.Object(oldbucket, oldkey).delete()

    @staticmethod
    def Remove(filename):
        bucket, key = s3File.split_s3_path(filename)
        s3File.s3.Object(bucket, key).delete()

    @staticmethod
    def Copy(srcPath, dstPath):
        # if srcPath.startswith('s3://') and dstPath.startswith('s3://'):
        #     newbucket, newkey = s3File.split_s3_path(dstPath)
        #     # if newkey[-1] == '/':
        #     #     name = srcPath.rsplit('/', 1)[1]
        #     #     newkey += name
        #     oldname = srcPath.strip('s3://')
        #     s3File.s3.Object(newbucket, newkey).copy_from(CopySource=oldname)
        # else:
        recursive = '--recursive' if srcPath[-1] == '/' else ''
        _ = os.system('aws s3 cp {srcPath} {dstPath} {recursive}'.format(srcPath=srcPath, dstPath=dstPath, recursive=recursive))


class pathStr(os.PathLike):
    def __new__(cls, *args, **kwargs):
        instance = super(pathStr, cls).__new__(cls)
        instance.path = None
        return instance

    def __init__(self, path, prefix=None):
        if isinstance(path, pathStr):
            self.path = path.path
            self.attr = path.attr
        else:
            if prefix is not None:
                self.path = os.path.join(prefix, path)
            else:
                self.path = path
            self._setAttr()
            if self.attr == 'local' and prefix is None:
                self.path = os.path.abspath(path)

    def _setAttr(self):
        if self.path.startswith('s3://'):
            self.attr = 's3'
        elif self.path.startswith('hdfs://'):
            self.attr = 'hdfs'
            if self.path.startswith('hdfs:///'):
                self.path = 'hdfs://'+hdfsFile.ip + self.path.strip('hdfs://')
        else:
            self.attr = 'local'

    def __add__(self, other):
        # self + other
        if other[0] == '/':
            other = other[1:]
        path = os.path.join(self.path, other)
        return pathStr(path)

    def __radd__(self, other):
        # self + other
        path = os.path.join(other, self.path)
        return pathStr(path)

    def __iadd__(self, other):
        if other[0] == '/':
            other = other[1:]
        self.path = os.path.join(self.path, other)
        return self

    def __getitem__(self, item):
        return self.path[item]

    def __fspath__(self):
        return self.path

    def __str__(self):
        return self.path

    # def __repr__(self):
    #     return self.path

    def __getattr__(self, item):
        obj = getattr(self.path, item)
        if hasattr(obj, '__call__'):
            def wrapper(*args, **kwargs):
                result = obj(*args, **kwargs)
                if isinstance(result, str):
                    return pathStr(result)
                else:
                    return result
            return wrapper
        else:
            return obj

class s3FileObj(object):
    def __init__(self, fileobj):
        self.file = fileobj

    def read(self):
        return self.file.read().decode('utf-8')

    def readline(self):
        f = self.file.iter_lines()
        for line in f:
            yield line.decode('utf-8')

    def readlines(self):
        all_file = self.file.read().decode('utf-8')
        all_file_list = all_file.split('\n')
        return all_file_list

    def __enter__(self):
        pass

    def __exit__(self):
        self.file.close()

if __name__ == '__main__':
    p = pathStr('/Users/snoworday')
    os.stat(p)
    print(str(p))
    p[2]
    p.__str__()
    p.strip()
    t = p + 'd'
    b = 4




