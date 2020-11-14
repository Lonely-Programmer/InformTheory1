import time

def encoding(search_buffer_size,look_ahead_size,s_ori):
    cr = [];      #  存储每一条编码结果
    sbi = search_buffer_size - 1
    lai = search_buffer_size
    sLen = len(s_ori)
    s = s_ori + "$"    # '$'是空字符，只出现在末尾, 不算长度
    while lai < sLen:       #  lai是look_ahead_buffer首字符下标
        sbj = sbi
        max_match_length = 0
        max_j = lai # max_j 最长匹配串在search_buffer的开始位置
        while sbj > sbi - search_buffer_size:          # 遍历search_buffer
            if s[sbj] == s[lai]:
                j_match = sbj + 1
                laj_match = lai + 1
                sup=min(lai+look_ahead_size,sLen) #  sup是上界
                while j_match <= sbi and laj_match < sup and s[j_match] == s[laj_match]:
                    j_match += 1
                    laj_match += 1

                if j_match == sbi + 1:                 # 扫到search_buffer尾部，循环 sbj->sbi
                    j_match = sbj
                    while laj_match < sLen and s[j_match] == s[laj_match]:
                        j_match +=1
                        laj_match +=1
                        if j_match == sbi:
                            j_match = sbj

                if laj_match - lai > max_match_length:  # 保存最长的匹配点
                    max_match_length = laj_match - lai
                    max_j = sbj
            
            sbj -= 1

        cr.append((lai - max_j,max_match_length,s[lai + max_match_length]))
        sbi += max_match_length + 1
        lai = sbi + 1

    s = s[0:-1]
    return cr

def decoding(search_buffer_size,look_ahead_size,sb_init,cr):
    s = sb_init    # 最初的search_ahead_buffer的内容
    for ri in range(len(cr)):
        if cr[ri][0] == 0: # 只有一个字符，直接加过来
            s += cr[ri][2]
        else:
            sb_begin = len(s) - cr[ri][0]
            sbi = sb_begin
            decoded_substr = ""

            for i in range(cr[ri][1]):
                decoded_substr += s[sbi]
                sbi += 1
                if sbi == len(s):
                    sbi = sb_begin
            decoded_substr += cr[ri][2]
            s += decoded_substr

    if s[-1] == '$':
        s = s[0,-1]
    return s

def main():
    with open('input.txt','r',encoding='utf-8') as f:
        z = f.read()

    for obj in [128,160,192,224,255]:
        start = time.time()
        cr = encoding(obj,16,z)
        t1 = time.time() - start
        s = decoding(obj,16,z[0:obj],cr)

        t2 = time.time() - start - t1

        print('Search_buffer_size:',obj)
        print('Original length:',len(z))
        print('Correctness:',z == s)
        print('Encode time:',t1)
        print('Decode time:',t2)
        print()

main()
