import os
#filename without number or extension
def mergeFiles(noFiles, fileName,ftype ,directory):
    oss.chdir(directory)
    data = b''
    for i in range(noFiles):
        f = open(fileName + str(i)+'.' + ftype,'rb')
        data += f.read()
        f.close()

    file = open(fileName + '.' + ftype, 'wb')
    file.write(data)
    file.close()