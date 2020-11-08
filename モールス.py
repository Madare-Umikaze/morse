import tkinter
from tkinter import *
from tkinter import ttk
import ast
import re
import unicodedata
import win32com.client
import jaconv
from pykakasi import kakasi
from tkinter import messagebox
from tkinter import simpledialog
import os

kakasi = kakasi()
kakasi.setMode('J', 'H') 

root1 = tkinter.Tk()
root1.title('モールス変換')
root1.minsize(450,300)
now = os.getcwd() 
icon = now + str('\モールス.ico')
root1.iconbitmap(icon)

label1 = tkinter.Label(text = u'モールスを入力する際は、\n必ず5bitごとに空白を入れてください。')
label1.pack()
label1.place(x=2, y=1)

label2 = tkinter.Label(text = u'入力を')
label2.pack()
label2.place(x=2, y=85)

Button1 = tkinter.Button(text='平文化')
Button1.pack()
Button1.place(x=75,y=81)

Button2 = tkinter.Button(text='モールス化')
Button2.pack()
Button2.place(x=150,y=80)

Button3 = tkinter.Button(text='保存', width=10)
Button3.pack()
Button3.place(x=230,y=150)

Button4 = tkinter.Button(text='入力',width=8)
Button4.pack()
Button4.place(x=280,y=10)

txt = StringVar()
cb = ttk.Combobox(root1, state="readonly", textvariable=txt)
cb['values']=('入力値と結果','入力値のみ','結果のみ')
cb.set("入力値と結果")
cb.grid(row=100, column=100)
cb.grid_configure(padx=8, pady=155)
    
root2 = tkinter.Toplevel()
root2.title('入力フォーム')
root2.geometry("400x200")
root2.withdraw()

text_widget = tkinter.Text(root2, wrap = tkinter.NONE)
text_widget.grid(column=0, row=0, sticky = (tkinter.N, tkinter.S, tkinter.E, tkinter.W))
root2.columnconfigure(0, weight = 1)
root2.rowconfigure(0, weight = 1)
    
yscroll = tkinter.Scrollbar(text_widget, command=text_widget.yview)
xscroll = tkinter.Scrollbar(text_widget, command=text_widget.xview, orient=tkinter.HORIZONTAL)
yscroll.pack(side=tkinter.RIGHT, fill = "y")
xscroll.pack(side=tkinter.BOTTOM, fill = "x")
text_widget['yscrollcommand'] = yscroll.set
text_widget['xscrollcommand'] = xscroll.set

root3 = tkinter.Toplevel()
root3.title("結果")

readOnlyText = tkinter.Text(root3, wrap = tkinter.NONE)
readOnlyText.grid(column=0, row=0, sticky = (tkinter.N, tkinter.S, tkinter.E, tkinter.W))
root3.columnconfigure(0, weight = 1)
root3.rowconfigure(0, weight = 1)

yscroll = tkinter.Scrollbar(readOnlyText, command=readOnlyText.yview)
xscroll = tkinter.Scrollbar(readOnlyText, command=readOnlyText.xview, orient=tkinter.HORIZONTAL)
yscroll.pack(side=tkinter.RIGHT, fill = "y")
xscroll.pack(side=tkinter.BOTTOM, fill = "x")
readOnlyText['yscrollcommand'] = yscroll.set
readOnlyText['xscrollcommand'] = xscroll.set

root3.geometry("400x200")
root3.withdraw()


num1 = {'-----': '0', '.----': '1', '..---': '2', '...--':'3',
     '....-':'4', '.....':'5', '-....':'6', '--...':'7',
     '---..':'8', '----.':'9', '...':'a', '---':'b', '.-.':'c'}

num2 = {'0':'-----', '1':'.----', '2':'..---', '3':'...--',
       '4':'....-', '5':'.....','6':'-....', '7':'--...',
       '8':'---..', '9':'----.', 'a':'...', 'b':'---',
       'c':'.-.'}

line11 = {'1':'あ', '2':'い', '3':'う', '4':'え', '5':'お',}
line12 = {'1':'か', '2':'き', '3':'く', '4':'け', '5':'こ',}
line13 = {'1':'さ', '2':'し', '3':'す', '4':'せ', '5':'そ',}
line14 = {'1':'た', '2':'ち', '3':'つ', '4':'て', '5':'と', '6':'っ',}
line15 = {'1':'な', '2':'に', '3':'ぬ', '4':'ね', '5':'の',}
line16 = {'1':'は', '2':'ひ', '3':'ふ', '4':'へ','5':'ほ',}
line17 = {'1':'ま', '2':'み', '3':'む', '4':'め', '5':'も',}
line18 = {'1':'や', '2':'ゆ', '3':'よ', '4':'ヰ', '5':'ヱ', '6':'ゃ', '7':'ゅ', '8':'ょ', '9':'ー',}
line19 = {'1':'ら', '2':'り', '3':'る', '4':'れ', '5':'ろ',}
line10 = {'0':'\n','1':'わ', '2':'を', '3':'ん', '4':'、', '5':'。', '6':'ぁ', '7':'ぃ', '8':'ぇ', '9':'ぉ'}

line21 = {'1':'ア', '2':'イ', '3':'ウ', '4':'エ', '5':'オ',}
line22 = {'1':'カ', '2':'キ', '3':'ク', '4':'ケ', '5':'コ',}
line23 = {'1':'サ', '2':'シ', '3':'ス', '4':'セ', '5':'ソ',}
line24 = {'1':'タ', '2':'チ', '3':'ツ', '4':'テ', '5':'ト', '6':'ッ',}
line25 = {'1':'ナ', '2':'ニ', '3':'ヌ', '4':'ネ', '5':'ノ',}
line26 = {'1':'ハ', '2':'ヒ', '3':'フ', '4':'ヘ','5':'ホ',}
line27 = {'1':'マ', '2':'ミ', '3':'ム', '4':'メ', '5':'モ',}
line28 = {'1':'ヤ', '2':'ユ', '3':'ヨ', '4':'ヰ', '5':'ヱ', '6':'ャ', '7':'ュ', '8':'ョ', '9':'ー',}
line29 = {'1':'ラ', '2':'リ', '3':'ル', '4':'レ', '5':'ロ',}
line20 = {'0':'\n','1':'ワ', '2':'ヲ', '3':'ン', '4':'、', '5':'。', '6':'ァ', '7':'ィ', '8':'ェ', '9':'ォ'}

line31 = {'1':'A', '2':'B', '3':'C', '4':'D', '5':'E', '6':'F', '7':'G', '8':'H', '9':'I',}
line32 = {'1':'J', '2':'K', '3':'L', '4':'M', '5':'N', '6':'O', '7':'P', '8':'Q', '9':'R',}
line33 = {'1':'S', '2':'T', '3':'U', '4':'V', '5':'W', '6':'X', '7':'Y', '8':'Z',}
line34 = {'1':'a', '2':'b', '3':'c', '4':'d', '5':'e', '6':'f', '7':'g', '8':'h', '9':'i',}
line35 = {'1':'j', '2':'k', '3':'l', '4':'m', '5':'n', '6':'o', '7':'p', '8':'q', '9':'r',}
line36 = {'1':'s', '2':'t', '3':'u', '4':'v', '5':'w', '6':'x', '7':'y', '8':'z',}

line37 = {'1':'\'', '2':'"', '3':',', '4':'.', '5':'!', '6':'?', '7':'#', '8':'$', '9':'%',}
line38 = {'1':'(', '2':')', '3':'&', '4':';', '5':':', '6':'/', '7':'\\', '8':'_'}
line30 = {'0':'\n',}

pokhira = {'あ':'11', 'い':'12', 'う':'13', 'え':'14', 'お':'15',
           'か':'21', 'き':'22', 'く':'23', 'け':'24', 'こ':'25',
           'さ':'31', 'し':'32', 'す':'33', 'せ':'34', 'そ':'35',
           'た':'41', 'ち':'42', 'つ':'43', 'て':'44', 'と':'45', 'っ':'46',
           'な':'51', 'に':'52', 'ぬ':'53', 'ね':'54', 'の':'55',
           'は':'61', 'ひ':'62', 'ふ':'63', 'へ':'64', 'ほ':'65',
           'ま':'71', 'み':'72', 'む':'73', 'め':'74', 'も':'75',
           'や':'81', 'ゆ':'82', 'よ':'83', 'ヰ':'84', 'ヱ':'85', 'ゃ':'86', 'ゅ':'87', 'ょ':'88', 'ー':'89',
           'ら':'91', 'り':'92', 'る':'93', 'れ':'94', 'ろ':'95',
           'わ':'01', 'を':'02', 'ん':'03', '、':'04', '。':'05', 'ぁ':'06', 'ぃ':'07', 'ぇ':'08', 'ぉ':'09', '\n':''}

pokkana = {'ア':'11', 'イ':'12', 'ウ':'13', 'エ':'14', 'オ':'15',
           'カ':'21', 'キ':'22', 'ク':'23', 'ケ':'24', 'コ':'25',
           'サ':'31', 'シ':'32', 'ス':'33', 'セ':'34', 'ソ':'35',
           'タ':'41', 'チ':'42', 'ツ':'43', 'テ':'44', 'ト':'45', 'ッ':'46',
           'ナ':'51', 'ニ':'52', 'ヌ':'53', 'ネ':'54', 'ノ':'55',
           'ハ':'61', 'ヒ':'62', 'フ':'63', 'ヘ':'64', 'ホ':'65',
           'マ':'71', 'ミ':'72', 'ム':'73', 'メ':'74', 'モ':'75',
           'ヤ':'81', 'ユ':'82', 'ヨ':'83', 'ヰ':'84', 'ヱ':'85', 'ャ':'86', 'ュ':'87', 'ョ':'88', 'ー':'89',
           'ラ':'91', 'リ':'92', 'ル':'93', 'レ':'94', 'ロ':'95',
           'ワ':'01', 'ヲ':'02', 'ン':'03', '、':'04', '。':'05', 'ァ':'06', 'ィ':'07', 'ェ':'08', 'ォ':'09', '\n':''}

pokei = {'A':'11', 'B':'12', 'C':'13', 'D':'14', 'E':'15', 'F':'16', 'G':'17', 'H':'18', 'I':'19',
         'J':'21', 'K':'22', 'L':'23', 'M':'24', 'N':'25', 'O':'26', 'P':'27', 'Q':'28', 'R':'29',
         'S':'31', 'T':'32', 'U':'33', 'V':'34', 'W':'35', 'X':'36', 'Y':'37', 'Z':'38',
         'a':'41', 'b':'42', 'c':'43', 'd':'44', 'e':'45', 'f':'46', 'g':'47', 'h':'48', 'i':'49',
         'j':'51', 'k':'52', 'l':'53', 'm':'54', 'n':'55', 'o':'56', 'p':'57', 'q':'58', 'r':'59',
         's':'61', 't':'62', 'u':'63', 'v':'64', 'w':'65', 'x':'66', 'y':'67', 'z':'68',
         '\'':'71', '"':'72', ',':'73', '.':'74', '!':'75', '?':'76', '#':'77', '$':'78', '%':'79',
         '(':'81', ')':'82', '&':'83', ';':'84', ':':'85', '/':'86', '\\':'87', '_':'88', '\n':''}


def root2_open():
    root2.deiconify()


def root2_close():
    root2.withdraw()

    

def root3_open():
    root3.deiconify()


def root3_close():
    root3.withdraw()


    

def hirabunka():
    morse = text_widget.get('1.0', 'end')
    list = morse.split()
    print(list)

    list2 = []
    hira = ''

    for word in list:
        if word in num1:
            poke = num1[word]
            list2.append(poke)
            print(list2)
        else:
            print('error')
            speech = win32com.client.Dispatch("Sapi.SpVoice")
            speech.Speak('error')
            
        

    x = 0
    y = 0

    for p in list2:
        if y == 1:
            if x == 0:
                hira = 'error'
            if x == 1:
                y = 0
                print('a')
                print(line)
                if line == 1:
                    print(p)
                    a = line11[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 2:
                    print(p)
                    a = line12[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 3:
                    print(p)
                    a = line13[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 4:
                    print(p)
                    a = line14[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 5:
                    print(p)
                    a = line15[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 6:
                    print(p)
                    a = line16[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 7:
                    print(p)
                    a = line17[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 8:
                    print(p)
                    a = line18[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 9:
                    print(p)
                    a = line19[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 0:
                    print(p)
                    a = line10[p]
                    print(a)
                    hira = hira + a
                    
                else:
                    print('Not found')
            if x == 2:
                y = 0
                print('b')
                print(line)
                if line == 1:
                    print(p)
                    a = line21[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 2:
                    print(p)
                    a = line22[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 3:
                    print(p)
                    a = line23[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 4:
                    print(p)
                    a = line24[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 5:
                    print(p)
                    a = line25[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 6:
                    print(p)
                    a = line26[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 7:
                    print(p)
                    a = line27[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 8:
                    print(p)
                    a = line28[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 9:
                    print(p)
                    a = line29[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 0:
                    print(p)
                    a = line20[p]
                    print(a)
                    hira = hira + a
                    
                else:
                    print('Not found')

            if x == 3:
                y = 0
                print('c')
                print(line)
                if line == 1:
                    print(p)
                    a = line31[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 2:
                    print(p)
                    a = line32[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 3:
                    print(p)
                    a = line33[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 4:
                    print(p)
                    a = line34[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 5:
                    print(p)
                    a = line35[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 6:
                    print(p)
                    a = line36[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 7:
                    print(p)
                    a = line37[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 8:
                    print(p)
                    a = line38[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 9:
                    print(p)
                    a = line39[p]
                    print(a)
                    hira = hira + a
                    
                elif line == 0:
                    print(p)
                    a = line30[p]
                    print(a)
                    hira = hira + a
                    
                else:
                    print('Not found')
        

        else:
            if p == 'a':
                x = 1
            elif p == 'b':
                x = 2

            elif p == 'c':
                x = 3
            else:
                y = 1
                line = p
                line = int(line)
                
                

    print(hira)
    print(join_diacritic1(hira))
    hira = join_diacritic1(hira)
    change_word2 = jaconv.hira2kata(hira)
    print(hira)
    hira = str(hira)
    speech = win32com.client.Dispatch("Sapi.SpVoice")
    speech.Speak(hira)

    v = [hira[i: i+18] for i in range(0, len(hira), 18)]
    
    readOnlyText.configure(state='normal')
    readOnlyText.delete('1.0', 'end')
    readOnlyText.insert('insert', hira)
    readOnlyText.configure(state='disabled')
    root3_open()
    


def morseka():
    mor = []
    list1 = ''
    list2 = []
    ans2 = []
    ans3 = ''
    x = 0
    z = 0
    
    text = text_widget.get('1.0', 'end')
    conv = kakasi.getConverter()
    ans = conv.do(text)
    print(ans)
    ans = join_diacritic2(ans)
    print(ans)
    ans = list(ans)
    print(ans)

    
    for word in ans:
        if word in pokhira:
            a = pokhira[word]
            print(a)
            if not x == 1:
                x = 1
                mor.append('a')
            else:
                pass
            mor.append(a)
        elif word in pokkana:
            a = pokkana[word]
            print(a)
            if not x == 2:
                x = 2
                mor.append('b')
            else:
                pass
            mor.append(a)
        elif word in pokei:
            a = pokei[word]
            print(a)
            if not x == 3:
                x = 3
                mor.append('c')
            else:
                pass
            mor.append(a)
        else:
            print('error')
            
    print(mor)

    
    for n in mor:
        if print(n.isdecimal()):
            l = [int(x) for x in list(str(n))]
            print(l)
            list1 = list1 + l
        else:
            list1 = str(list1) + n

    print('------------------')
    print(list1)

    for word in list1:
        print(word)
        word = str(word)
        if word in num2:
            poke = num2[word]
            if poke == '...' or poke == '---' or poke == '.-.':
                list2.append(poke)
                list2.append('n')
            else:
                list2.append(poke)
            print(list2)
        else:
            print(word)
            print('error')
            speech = win32com.client.Dispatch("Sapi.SpVoice")
            speech.Speak('error')

    print('------------------')
    print(list2)

    for word in list2:
        if word == 'n':
            num = len(ans2)
            print(num)
            num = num - 1
            print(ans2)
            ans2.insert(num, '\n')
            ans2.append('\n')
            z = 0
        elif z == 3:
            z = 0
            word = word + ' '
            ans2.append(word)
            ans2.append('\n')
        else:
            z = z + 1
            word = word + ' '
            ans2.append(word)

    print(ans2)

   
    print()
    print(text)
    print()
    print(ans)
    print(ans2)

    for word in ans2:
        word = str(word)
        ans3 = ans3 + word
        
    print(ans3)

    speech = win32com.client.Dispatch("Sapi.SpVoice")
    speech.Speak(ans3)

    
    readOnlyText.configure(state='normal')
    readOnlyText.delete('1.0', 'end')
    readOnlyText.insert('insert', ans3)
    readOnlyText.configure(state='disabled')
    root3_open()
    
    


def join_diacritic1(text, mode="NFC"):
    
    bytes_text = text.encode()

    bytes_text = re.sub(b"\xe3\x83\xb0", b'\xe3\x82\x99', bytes_text)
    bytes_text = re.sub(b"\xe3\x83\xb1", b'\xe3\x82\x9a', bytes_text)

    text = bytes_text.decode()

    text = unicodedata.normalize(mode, text)

    return text


def join_diacritic2(text, mode="NFD"):
    
    text = unicodedata.normalize(mode, text)
    
    bytes_text = text.encode()
    
    bytes_text = re.sub(b'\xe3\x82\x99', b"\xe3\x83\xb0", bytes_text)
    bytes_text = re.sub(b'\xe3\x82\x9a', b"\xe3\x83\xb1", bytes_text)
    
    text = bytes_text.decode()

    return text




def hozon():
    sen = txt.get()
    print(sen)
    now = os.getcwd()
    print(now)
    messe = sen + 'を保存しますか？'
    msg = messagebox.askyesno('保存',messe)
    if msg == True:
        inp = simpledialog.askstring("保存-ファイル名", "ファイル名を入力してください。",)
        if inp != None:
            if inp != (''):
                print('入力された')
                inp = str(inp) + str('.txt')
                print(inp)
                inp = '保存\\' + inp
                yorn = os.path.exists(inp)
                if yorn == True:
                    print("あるよ")
                    msg = messagebox.askyesno('保存-Error', 'この名前のファイルはすでに存在します。上書きしますか?')
                    if msg == True:
                        if sen == '入力値と結果':
                            save_file = open(inp, 'w')
                            save_file.write(text_widget.get('1.0', 'end'))
                            save_file.write('\n\n')
                            save_file.write(readOnlyText.get('1.0', 'end'))  
                            save_file.close()
                            
                        elif sen == '入力値のみ':
                            save_file = open(inp, 'w')
                            save_file.write(text_widget.get('1.0', 'end'))  
                            save_file.close()
                            
                        elif sen == '結果のみ':
                            save_file = open(inp, 'w')
                            save_file.write(readOnlyText.get('1.0', 'end'))  
                            save_file.close()
                            
                        else:
                            print('error')
                    else:
                        pass
                         
                else:
                    print("ないよ")
                    if sen == '入力値と結果':
                        save_file = open(inp, 'w')
                        save_file.write(text_widget.get('1.0', 'end'))
                        save_file.write('\n\n')
                        save_file.write(readOnlyText.get('1.0', 'end'))  
                        save_file.close()
                            
                    elif sen == '入力値のみ':
                        save_file = open(inp, 'w')
                        save_file.write(text_widget.get('1.0', 'end'))  
                        save_file.close()
                            
                    elif sen == '結果のみ':
                        save_file = open(inp, 'w')
                        save_file.write(readOnlyText.get('1.0', 'end'))  
                        save_file.close()
                            
                    else:
                        print('error')
                    
            else:
                messagebox.showerror('保存-Error', 'ファイル名が入力されていません。')
        else:
            pass

    else:
        pass
   




Button1["command"] = hirabunka
Button2["command"] = morseka
Button3["command"] = hozon
Button4["command"] = root2_open
root2.protocol("WM_DELETE_WINDOW", root2_close)
root3.protocol("WM_DELETE_WINDOW", root3_close)

root1.mainloop()
