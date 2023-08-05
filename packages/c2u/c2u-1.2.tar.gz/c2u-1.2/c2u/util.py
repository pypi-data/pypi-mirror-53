def c2u(input):
    '''
    先写一个check函数

    :param input:
    :return:
    '''

    if type(input)==list:
        return [c2u(i) for i in input]
    else:



        out=''
        for i in range(len(input)):
            if input[i].isupper():
                out+=('_')
                out+=input[i].lower()
            else:
                out+=input[i]


        return out

def u2c(input):
    if type(input)==list:
        return [u2c(i) for i in input]


    else:
        out=''
        for i in range(len(input)):
            if i>0 and input[i-1]=='_':
                continue
            if input[i]=='_':


                out+=input[i+1].upper()
            else:
                out+=input[i]
        return out
