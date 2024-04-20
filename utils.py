def calculate_ascii_comb(data):
    ascii=0
    for i in range(0,len(data)-1):
        ascii+= abs(ord(data[i])-ord(data[i+1]))
    ascii+=sum(ord(c) for c in data)
    return ascii

