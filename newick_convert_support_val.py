import sys
tbe_alrt_tree=sys.argv[1]
output='converted_'+tbe_alrt_tree
with open (output,'w') as f:
    with open (tbe_alrt_tree,'r') as f2:
        ifprint=1
        put_support=0
        support=''
        char_array=[]
        for line in f2:
            for c in line:
                char_array.append(c)
            total_char=len(char_array)
            i=0
            while(i<total_char):
                ch=char_array[i]
                if(ch==')'):
                    f.write(ch)
                    i=i+1
                    if(char_array[i]==';'):
                        f.write(char_array[i])
                        break
                    support=''
                    while(char_array[i]!=':'):
                        support=support+char_array[i]
                        i=i+1
                    f.write(char_array[i])
                    i=i+1
                    while(char_array[i]!=',' and char_array[i]!=')'):
                        f.write(char_array[i])
                        i=i+1
                    f.write('[')
                    value_support=float(support)
                    round_support=int(value_support*100)    
                    f.write(str(round_support))
                    f.write(']')
                    support=''
                else:
                    f.write(ch)
                    i=i+1
            break                



                
