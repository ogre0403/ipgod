
import os



def count_file(root):
    for dirname in os.listdir(root):
        dirpath = os.path.join(root,dirname)

        filecount = 0
        for _ in os.listdir(dirpath):
            filecount += 1
        dict[dirpath] = filecount
        if filecount in icount:
            icount[filecount] += 1
        else :
            icount[filecount] = 1

#    print(dict)
    print(icount)



if __name__ == "__main__" :
    icount = {}
    dict = {}
    root = "./data/"
    count_file(root)




#if __name__ == "__main__":
#	for root, dirs, files in os.walk("./data_download/"):
#		for name in dirs :
#			dirname = os.path.join(root,name)
#			file_count = 0
#			for sroot,sdir,sfiles in os.walk(dirname):
#				file_count = len(sfiles)
#			print("{} = {}".format(dirname, file_count))	
