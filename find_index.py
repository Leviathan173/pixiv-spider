def test():
    list = []
    for i in range(0, 7651):
        list.append(i)
    with open('./init.cfg', 'w') as f:
        for i in range(len(list)):
            f.write(str(list[i]) + '\n')
    f.close()

    read = []
    with open('./init.cfg', 'r') as f:
        while True:
            line = f.readline()
            # print(line)
            if not line:
                break
            read.append(line)
    f.close()
    for i in read:
        print(i)


def get_index():
    with open('./init.cfg', 'r') as f:
        line = f.readline()
    f.close()
    return line


def create_index(start=0):
    list_index = []
    print(type(start))
    for i in range(start, start + 10000):
        list_index.append(i)
    with open('./init.cfg', 'w') as f:
        for i in range(len(list_index)):
            f.write(str(list_index[i]) + '\n')
    f.close()


def get_allindex():
    index = []
    with open('./init.cfg', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            index.append(line)
    f.close()
    return index


def write_left(index):
    with open('./init.cfg', 'w') as f:
        for i in range(len(index)):
            f.write(str(index[i]) + '\n')
    f.close()
