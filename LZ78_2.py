import time

def encode(text):
    dic = dict()
    code = []
    for i in range(len(text)):
        if text[i] in dic.keys():
            continue
        dic[text[i]] = len(dic)
    
    end = text[-1]
    znext = ''
    i = 0
    tmp = ""
    while i < len(text):
        tmp = ""
        tmp += text[i]
        if i + 1 == len(text):
            break
        znext = text[i + 1]
        while tmp in dic.keys():
            tmp += znext
            i += 1
            if i + 1 == len(text):
                break
            znext = text[i + 1]
        
        tmp = tmp[0:-1]
        znext = text[i]
        code.append(dic[tmp])
        tmp += znext
        dic[tmp] = len(dic)

    return code

def decode(code,text):
    dic = dict()
    mp = dict()
    end = text[-1]

    for i in range(len(text)):
        if text[i] in dic.keys():
            continue
        dic[text[i]] = len(dic)
        mp[len(dic) - 1] = text[i]
    
    res = ""
    pre = ""
    output = mp[code[0]]
    res += output
    for i in range(1,len(code)):
        pre = output
        output = mp[code[i]]
        res += output
        if len(output) != 0:
            mp[len(mp)] = pre + output[0]
    
    res += end
    return res

def main():
    with open('input.txt','r',encoding='utf-8') as f:
        z = f.read()

    start = time.time()
    cr = encode(z)
    t1 = time.time() - start
    s = decode(cr,z)
    t2 = time.time() - start - t1

    print('Original length:',len(z))
    print('Correctness:',z == s)
    print('Encode time:',t1)
    print('Decode time:',t2)

main()



