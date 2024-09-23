f = open("project\data_files\data_20240828_140938.txt", "r")
counter = 0
for x in f:
    counter+=1
    print(x)
f.close()