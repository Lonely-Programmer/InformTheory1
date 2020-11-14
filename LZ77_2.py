import time

def encoding(search_buffer_size, s_ori):
    code_num = 0
    sbi = 4
    lai = 5
    sLen = len(s_ori) # LZSS不可能对前5个字符编码
    max_match_num = 0;                                    # 记录所有编码中最长的一次匹配的字符个数
    s_encoded = s_ori[0:5]                    # 直接编码到字符串里
    while lai < sLen:                                       # look_ahead_buffer最左端在lai，lai=sbj+1
        sbj = sbi
        max_reduce_length = 0                  # 从search_buffer的最后一位sbj往前搜索
        sb_min = max(-1, sbi - search_buffer_size)        # 搜索的下界
        best_code = s_ori[lai]              # 记录search_buffer里最佳的一个编码
        while sbj > sb_min:                                 # 遍历search_buffer
            if s_ori[sbj] == s_ori[lai]: # search_buffer的j位置匹配到look_ahead_buffer的i位置，开始一轮匹配
                j_match = sbj + 1
                laj_match = lai + 1
                while j_match <= sbi and laj_match < sLen and s_ori[j_match] == s_ori[laj_match]:
                    j_match += 1
                    laj_match += 1

                if j_match == sbi + 1:                      # 扫到search_buffer尾部，循环 sbj->sbi
                    j_match = sbj
                    while laj_match < sLen and s_ori[j_match] == s_ori[laj_match]:
                        j_match += 1
                        laj_match += 1
                        if j_match == sbi:
                            j_match = sbj     # 仍可继续循环
                
                match_num = laj_match - lai
                ahead_num = lai - sbj
                    # 直接把数字转为string太长了

                aheads = ""
                if ahead_num < 127:
                    aheads = chr(ahead_num)# 数较小时用一个char存储再转为string
                else:
                    aheads = chr(ahead_num // 127) + chr(ahead_num % 127)

                matchc = chr(match_num)                           # 不超过126, 127用于编码左右边界字符
                matchs = matchc
                boundary = chr(127)
                #  matchs只会是一个字符，所以中间的逗号可以省掉！
                wish_code = boundary + aheads + matchs + boundary# 构造这轮search期望的编码  

                reduce_length = match_num - len(wish_code)      # 计算这个编码缩短了多少
                if reduce_length > max_reduce_length:                 # 如果缩短了更多，就记录它
                    best_code = wish_code
                    max_reduce_length = reduce_length

            sbj -= 1

        if len(best_code) > 1:
            code_num += 1                          # 记录缩短次数（编码个数）
        s_encoded += best_code
        sbi += max_reduce_length + len(best_code);              # 右移滑窗
        max_match_num = max(max_match_num, max_reduce_length + len(best_code))
        lai = sbi + 1

    if len(s_ori) == 0:
        print("null string.\n\n")
        return []

    compression_rate = (len(s_ori) - len(s_encoded)) / len(s_ori)

    return s_encoded

def decoding(s_encoded):  # 编码字符串，原始字符串
    s_decoded = ""                                 # 解码字符串
    boundary = chr(127)                             # 边界字符
    s_en_len = len(s_encoded)

    i = 0
    while i < s_en_len - 3:                               # 最后3个字符不可能编码，同时要防止下面if越界
        if s_encoded[i] != boundary:                    # 此位置未编码压缩
            s_decoded += s_encoded[i]
        else:
            lai = len(s_decoded)                # look_ahead初始位置下标
            ahead_num = 0
            match_num = 0            # 往前看字符个数
            i += 1
            if s_encoded[i + 2] == boundary:            # 现在必须先判断+2而不是+3的位置了!!! (之前必须先判断+3)
                ahead_num = ord(s_encoded[i])   # ahead_num是1位127进制数
                i += 1
            else:                                       # 否则ahead_num是2位127进制数
                ahead_num = ord(s_encoded[i]) * 127 + ord(s_encoded[i + 1])
                i += 2

            c = s_encoded[i]
            i += 1                  #此时s_encoded[i] == boundary
            match_num = ord(c)                          # 匹配的字符个数不会超过127（实际上一半都不到）

            if s_encoded[i] != boundary:              # 错误检测
                #cerr <<"Error Occurred: "<< s_encoded.substr(i - 20, 22) << endl
                break

            sb_begin = lai - ahead_num        # 从sb_begin开始获取解码后的字符
            sbi = sb_begin  
            for j in range(match_num):                         # 可兼容循环遍历search_buffer的匹配子串
                s_decoded += s_decoded[sbi]
                sbi += 1
                if sbi == lai:
                    sbi = sb_begin          # 循环
        i += 1

    s_decoded += s_encoded[max(0, s_en_len - 3):max(0, s_en_len - 3) + min(3, s_en_len)]
    return s_decoded


def main():
    with open('input.txt','r',encoding='utf-8') as f:
        z = f.read()

    for obj in [128,160,192,224,255,1024,2048,4096,6144,9192,14458]:
        start = time.time()
        cr = encoding(obj,z)
        t1 = time.time() - start
        s = decoding(cr)
        t2 = time.time() - start - t1

        print('Search_buffer_size:',obj)
        print('Original length:',len(z))
        print('Correctness:',z == s)
        print('Encode time:',t1)
        print('Decode time:',t2)
        print()

main()
