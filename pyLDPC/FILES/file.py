

def edit(file):
    with open(file, "r") as f:
        filedata = f.read()
        lines = filedata.split("\n") # list of lines
        for index, line in enumerate(lines):

            words = line.split() # ['keyword', '1.50', '1.63', '1.56', '1.45']
            for i, w in enumerate(words):
                try:
                    # transform number to float, multiply by 10000
                    # then transform to integer, then back to string
                    new_word = str(int(float(w)))
                    words[i] = new_word
                except:
                    pass
            lines[index] = " ".join(words)
        new_data = "\n".join(lines) # store new data to overwrite file


    with open(file, "w") as f: # open file with write permission
        f.write(new_data) # overwrite the file with our modified data



Zc_table = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,30,32,36,40,44,48,52,56,60,
64,72,80,88,96,104,112,120,128,144,160,176,192,208,224,240,256,288,320,352,384]


for BG in range(2,3):
    for Zc in [320]:
        print(Zc)
        ils = 7*(Zc%15==0) +6*(Zc%13==0) +5*(Zc%11==0) +4*(Zc%9==0) +3*(Zc%7==0) +2*(Zc%5==0 and Zc%15!=0) +(Zc%3==0 and Zc%9!=0 and Zc%15!=0)

        edit("../gen_matrices/NR_"+str(BG)+"_"+str(ils)+"_"+str(Zc)+".txt")
