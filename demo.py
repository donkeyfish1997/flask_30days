import os

basepath = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
print(basepath)
dirs = os.listdir(os.path.join(basepath, 'abc'))
print(type(dirs))
dirs.insert(0, 'New Folder')
dirs.insert(0, 'Not Choose')
print(dirs)