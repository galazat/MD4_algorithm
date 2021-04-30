# -*- coding: utf-8 -*-

# Автор: Галлямов Азат, группа 06-751
# Дата: 14.03.2021


from tkinter import *
from tkinter import filedialog
import random
import matplotlib.pyplot as plt



def rotate_bytes(num,col):
    # побитовый сдвиг 4 байтового числа, col положительный -> сдвиг вправо, отрицательный <- влево
    num_bit = list(bin(num)[2:].zfill(32))
    while (len(num_bit) != 32):
        num_bit.pop(0)
    while col!=0:
        if col >= 0:
            tmp = num_bit[31]
            for i in range(31,0,-1):
                num_bit[i] = num_bit[i-1]
            num_bit[0] = tmp
            col -=1
        elif col <0:
            tmp = num_bit[0]
            for i in range(0,31,1):
                num_bit[i] = num_bit[i+1]
            num_bit[31] = tmp
            col +=1
    num_byte = [ int(''.join(num_bit[i+j] for i in range(0,8,1)),2) for j in range(0,32,8)]
    result = int.from_bytes(num_byte,'big')
    return result
def Mod512(text):
    # расширяет текст и делит на блоки по 512 бит
    tmp = text.encode('utf-8')
    if (tmp[len(tmp)-1]==10):
        text_byte = tmp[0:len(tmp)-1]
    else:
        text_byte = tmp[0:len(tmp)]
    text_bit = [bin(text_byte[i])[2:].zfill(8) for i in range(0, len(text_byte))]
    text_bit.append('10000000')
    while ((len(text_bit)*8)%512 != 448):
        text_bit.append('00000000')
    tmp = list(bin(len(text_byte*8))[2:].zfill(64))
    part1 = tmp[0:32]
    part2 = tmp[32:64]
    text_bit.append(''.join(part2[24:32]))
    text_bit.append(''.join(part2[16:24]))
    text_bit.append(''.join(part2[8:16]))
    text_bit.append(''.join(part2[0:8]))

    text_bit.append(''.join(part1[24:32]))
    text_bit.append(''.join(part1[16:24]))
    text_bit.append(''.join(part1[8:16]))
    text_bit.append(''.join(part1[0:8]))

    part512 = [''.join(text_bit[i+j] for i in range(0,64)) for j in range(0,len(text_bit),64)]
    return part512
def BlockTo16word(binpart):
    word16 = []
    for i in range(0,512,32):
        bit1 = ''.join(binpart[i:i+8])
        bit2 = ''.join(binpart[i+8:i+16])
        bit3 = ''.join(binpart[i+16:i+24])
        bit4 = ''.join(binpart[i+24:i+32])
        tmp = bit4 + bit3 + bit2 + bit1
        word16.append(int(tmp,2))
    return word16

def F(X,Y,Z):
    return ( (X&Y)|((~X)&Z) )
def FF(a,b,c,d,k,s,X):
    a = rotate_bytes((a+F(b,c,d) + X[k]), -s)
    return a
def G(X,Y,Z):
    return ( (X&Y)|(X&Z)|(Y&Z) )
def GG(a,b,c,d,k,s,X):
    a = rotate_bytes((a+G(b,c,d)+X[k]+0x5a827999),-s)
    return a
def H(X,Y,Z):
    return ( X^Y^Z )
def HH(a,b,c,d,k,s,X):
    a = rotate_bytes((a+H(b,c,d)+X[k]+0x6ed9eba1),-s )
    return a

def MD4(text):
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    word512 = Mod512(text)
    for i in range(0, len(word512)):

        X = BlockTo16word(word512[i])
        AA = A
        BB = B
        CC = C
        DD = D
        A = FF(A, B, C, D, 0, 3, X)
        D = FF(D, A, B, C, 1, 7, X)
        C = FF(C, D, A, B, 2, 11, X)
        B = FF(B, C, D, A, 3, 19, X)
        A = FF(A, B, C, D, 4, 3, X)
        D = FF(D, A, B, C, 5, 7, X)
        C = FF(C, D, A, B, 6, 11, X)
        B = FF(B, C, D, A, 7, 19, X)
        A = FF(A, B, C, D, 8, 3, X)
        D = FF(D, A, B, C, 9, 7, X)
        C = FF(C, D, A, B, 10, 11, X)
        B = FF(B, C, D, A, 11, 19, X)
        A = FF(A, B, C, D, 12, 3, X)
        D = FF(D, A, B, C, 13, 7, X)
        C = FF(C, D, A, B, 14, 11, X)
        B = FF(B, C, D, A, 15, 19, X)
        #----------------------------------------------------
        A = GG(A, B, C, D, 0, 3, X)
        D = GG(D, A, B, C, 4, 5, X)
        C = GG(C, D, A, B, 8, 9, X)
        B = GG(B, C, D, A, 12, 13, X)
        A = GG(A, B, C, D, 1, 3, X)
        D = GG(D, A, B, C, 5, 5, X)
        C = GG(C, D, A, B, 9, 9, X)
        B = GG(B, C, D, A, 13, 13, X)
        A = GG(A, B, C, D, 2, 3, X)
        D = GG(D, A, B, C, 6, 5, X)
        C = GG(C, D, A, B, 10, 9, X)
        B = GG(B, C, D, A, 14, 13, X)
        A = GG(A, B, C, D, 3, 3, X)
        D = GG(D, A, B, C, 7, 5, X)
        C = GG(C, D, A, B, 11, 9, X)
        B = GG(B, C, D, A, 15, 13, X)
        #-------------------------------------------
        A = HH(A, B, C, D, 0, 3, X)
        D = HH(D, A, B, C, 8, 9, X)
        C = HH(C, D, A, B, 4, 11, X)
        B = HH(B, C, D, A, 12, 15, X)
        A = HH(A, B, C, D, 2, 3, X)
        D = HH(D, A, B, C, 10, 9, X)
        C = HH(C, D, A, B, 6, 11, X)
        B = HH(B, C, D, A, 14, 15, X)
        A = HH(A, B, C, D, 1, 3, X)
        D = HH(D, A, B, C, 9, 9, X)
        C = HH(C, D, A, B, 5, 11, X)
        B = HH(B, C, D, A, 13, 15, X)
        A = HH(A, B, C, D, 3, 3, X)
        D = HH(D, A, B, C, 11, 9, X)
        C = HH(C, D, A, B, 7, 11, X)
        B = HH(B, C, D, A, 15, 15, X)

        A = (A + AA)%(pow(2,32))
        B = (B + BB)%(pow(2,32))
        C = (C + CC)%(pow(2,32))
        D = (D + DD)%(pow(2,32))
    # end -----------------------------------------------------


    tmp = A.to_bytes(4,'big')
    oneA = str(hex(tmp[3])[2:].zfill(2))
    twoA = str(hex(tmp[2])[2:].zfill(2))
    threeA = str(hex(tmp[1])[2:].zfill(2))
    fourA = str(hex(tmp[0])[2:].zfill(2))
    a_hex = oneA + twoA + threeA + fourA

    tmp = B.to_bytes(4, 'big')
    oneB = str(hex(tmp[3])[2:].zfill(2))
    twoB = str(hex(tmp[2])[2:].zfill(2))
    threeB = str(hex(tmp[1])[2:].zfill(2))
    fourB = str(hex(tmp[0])[2:].zfill(2))
    b_hex = oneB + twoB + threeB + fourB

    tmp = C.to_bytes(4, 'big')
    oneC = str(hex(tmp[3])[2:].zfill(2))
    twoC = str(hex(tmp[2])[2:].zfill(2))
    threeC = str(hex(tmp[1])[2:].zfill(2))
    fourC = str(hex(tmp[0])[2:].zfill(2))
    c_hex = oneC + twoC + threeC + fourC

    tmp = D.to_bytes(4, 'big')
    oneD = str(hex(tmp[3])[2:].zfill(2))
    twoD = str(hex(tmp[2])[2:].zfill(2))
    threeD = str(hex(tmp[1])[2:].zfill(2))
    fourD = str(hex(tmp[0])[2:].zfill(2))
    d_hex = oneD + twoD + threeD + fourD

    hash = a_hex + b_hex + c_hex + d_hex
    return hash, a_hex

def OpenFile():
    global const_hash
    name = filedialog.askopenfilename()
    text = open(name,'r', encoding='utf-8').read()
    message.delete('1.0',END)
    message.insert('1.0',text)
    hash , const_hash = MD4(text)
    const_hash = hash
    l3['text'] = hash
def ReadText():
    global const_hash, addEx
    text = message.get('1.0', 'end')
    hash , const_hash = MD4(text)
    const_hash = hash
    l3['text'] = hash

    hash1 = int(bin(int(hash, 16))[2:].zfill(128),2)
    hash2 = bin(int(hash, 16))[2:].zfill(128)
    print("\nИсходная сторка:\n" + hash2)
    print("Предыдущая сторка:\n" + str(bin(addEx)[2:].zfill(128)))
    dif = bin((hash1 ^ addEx)%(pow(2,128)))[2:].zfill(128)
    con = 0
    for i in range(0,len(dif)):
        if dif[i] == '1':
            con +=1
        else: continue
    print("Разница:\n" + dif + '\nКоличество изменённых бит : ' + str(con))

    addEx = hash1




def TextHashGen(l):
    global col_hash, col_text
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!{}[];/.,@#$%^&*()_+=-' \
               'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя\n\r\''
    text = []
    for i in range(0, l):
        text.append(random.choice(list(alphabet)))
    text = ''.join(text)
    hash, a_hex = MD4(text)
    col_text.append(text)
    col_hash.append(hash)

def KElement(hash,k):
    tmp = int(hash[0:8],16)
    tmp_bin = list(bin(tmp)[2:].zfill(32))
    result = int(''.join(tmp_bin[0:k]))
    return result

def Collisia():
    global col_hash, col_text
    k = int(message2.get())
    gen_len = int(message3.get())

    col_text = []
    col_hash = []
    TextHashGen(gen_len)
    equal = False
    j = 0
    match = 0
    while equal == False:
        TextHashGen(gen_len)
        j +=1
        for i in range(0,len(col_hash)-1):
            if (KElement(col_hash[i],k) == KElement(col_hash[j],k)):
                equal = True
                match = i
            else:
                continue
        print(col_text[j], col_hash[j])
    ltext1['text'] = col_text[match]
    lhash1['text'] = col_hash[match]
    ltext2['text'] = col_text[j]
    lhash2['text'] = col_hash[j]
    kg.append(k)
    lg.append(len(col_text))
    return 0
def Graph():
    plt.grid()  # включение отображение сетки
    plt.title("Зависимость N(k) от k")
    plt.xlabel("Величина k бит")
    plt.ylabel("Величина N текстов")
    plt.plot(kg, lg)
    plt.show()
def ProObr():
    global col_hash, col_text, const_hash
    k = int(message4.get())
    gen_len = random.randint(1,50)
    col_text = []
    col_hash = []
    equal = False
    j = -1
    while equal == False:
        gen_len = random.randint(1, 100)
        TextHashGen(gen_len)
        j +=1
        if (KElement(col_hash[j], k) == KElement(const_hash, k)):
            equal = True
        print(col_text[j], col_hash[j])
    ltext3['text'] = col_text[j]
    lhash3['text'] = col_hash[j]
    kg.append(k)
    lg.append(len(col_text))




if __name__ == "__main__":

    addEx = 0

    kg = []
    lg = []

    col_text = []
    col_hash = []
    const_hash = ''

    a = 'abg'.encode('utf-8')
    print(a[0],a[1],a[2])
    print(bin(a[0]),bin(a[1]),bin(a[2]))

    root = Tk(); winsize = [630, 780]; root.title("MD4")
    root.geometry(str(winsize[0])+'x'+str(winsize[1])); root.resizable(False, False)
    can = Canvas(width=622, height=774, bg='#ddd')

    lMD4=Label(root, text="1. MD4 хэш-код сообщения", ba='#ddd', fg='#222', font=['Akrobat Bold', 12])
    lMD4.place(x=15, y=15)
    l1 = Label(root, text="Введите исходное сообщение:", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    l1.place(x=40,y=55)
    message = Text(root, height=5, width=50)
    message.place(x=40,y=80)
    l2 =Label(root, text="MD4 хэш сообшения: ", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    l2.place(x=40,y=210)
    l3 = Label(root, text="", ba='#ddd', fg='#666', font=['Courier New', 10])
    l3.place(x=40, y=240)
    bMD4_1 = Button(text="Обзор", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=OpenFile,padx=0)
    bMD4_1.place(x=370, y=190)
    bMD4 = Button(text="Генерация", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=ReadText,padx=0)
    bMD4.place(x=450, y=190)

    lCol = Label(root, text="2. Поиск коллизий алгоритма MD4", ba='#ddd', fg='#222', font=['Akrobat Bold', 12])
    lCol.place(x=15, y=300)
    l4 = Label(root, text="Количество бит коллизии : ", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    l4.place(x=40, y=340)
    message2 = Entry(root, width=3)
    message2.place(x=260, y=340)
    l5 = Label(root, text="Длина генерируемого сообщения в байтах : ", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    l5.place(x=40, y=370)
    message3 = Entry(root, width=6)
    message3.place(x=375, y=370)
    b1 = Button(text="Поиск", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=Collisia,padx=14)
    b1.place(x=60, y=405)
    b2 = Button(text="График", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=Graph,padx=14)
    b2.place(x=200, y=405)
    ltext1 = Label(root, text="text1", ba='#ddd', fg='#222', font=['Akrobat Bold', 9])
    ltext1.place(x=40, y=450)
    lhash1 = Label(root, text="hash1", ba='#ddd', fg='#222', font=['Courier New', 10])
    lhash1.place(x=40, y=475)
    ltext2 = Label(root, text="text2", ba='#ddd', fg='#222',font=['Akrobat Bold', 9])
    ltext2.place(x=40, y=500)
    lhash2 = Label(root, text="hash2", ba='#ddd', fg='#222',font=['Courier New', 10])
    lhash2.place(x=40, y=525)

    lPro = Label(root, text="3. Поиск прообраза для хэша из 1 пункта", ba='#ddd', fg='#222', font=['Akrobat Bold', 12])
    lPro.place(x=15, y=590)
    l10 = Label(root, text="Количество бит коллизии : ", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    l10.place(x=40, y=630)
    message4 = Entry(root, width=3)
    message4.place(x=260, y=630)
    b10 = Button(text="Поиск", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=ProObr,padx=14)
    b10.place(x=60, y=665)
    b20 = Button(text="График", font=('Akrobat Bold', 10), background="#aaa", foreground="#222", command=Graph, padx=14)
    b20.place(x=200, y=665)
    ltext3 = Label(root, text="text1", ba='#ddd', fg='#222', font=['Akrobat Bold', 10])
    ltext3.place(x=40, y=710)
    lhash3 = Label(root, text="hash1", ba='#ddd', fg='#222', font=['Courier New', 10])
    lhash3.place(x=40, y=735)



    can.place(x=2, y=0); root.mainloop()
