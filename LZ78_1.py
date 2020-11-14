import time

def encode(text):
    mp = dict()
    dic = []
    tmp = ""
    for i in range(len(text)):
        tmp += text[i]
        if tmp not in mp.keys():
            mp[tmp] = len(mp) + 1
            if len(tmp) == 1:
                dic.append((0, text[i]))
            else:
                tmp = tmp[0:-1]
                dic.append((mp.get(tmp), text[i]))
            
            tmp = ""

    
    if tmp != "":
        dic.append((mp[tmp], '#'))

    return dic

def decode(dic):
    mp = dict()
    res = ""
    tmp = ""
    for i in range(len(dic)):
        tmp += dic[i][1]
        if dic[i][0] == 0:
            res += tmp
            mp[len(mp)+1] = tmp
            tmp = ""
        else:
            output = ""
            if dic[i][1] != '#':
                output = mp[dic[i][0]];
            res += (output + tmp)
            mp[len(mp)+1] = output + tmp
            tmp = ""

    return res

def main():
    with open('input.txt','r',encoding='utf-8') as f:
        z = f.read()

    start = time.time()
    cr = encode(z)
    t1 = time.time() - start
    s = decode(cr)
    t2 = time.time() - start - t1

    print('Original length:',len(z))
    print('Correctness:',z == s)
    print('Encode time:',t1)
    print('Decode time:',t2)

main()


