

if __name__ == '__main__':
    with open('diccionari_CB_v2.txt', 'r') as file:
        lines = file.readlines()
        dict = {}
        for line in lines:
            if len(line) not in dict:
                dict[len(line)] = [line.strip('\n')]
            else:
                dict[len(line)].append(line.strip('\n'))

        total = 0
        for key, value in dict.items():
            print(str(key-1) + ': ' + str(len(value)))
            total += len(value)
        print(total)
