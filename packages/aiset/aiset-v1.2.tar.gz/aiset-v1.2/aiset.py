#!/usr/bin/python
from ftplib import FTP #line:8
import os #line:9
import sys #line:10
import time #line:11
import socket #line:12
import threading #line:13
import ctypes #line:14
import inspect #line:15

def __O000000O0OO000O00 (OO000OO000O000OOO ,OO0OO0OOOO0O0OOOO ):#line:16
    OO000OO000O000OOO =ctypes .c_long (OO000OO000O000OOO )#line:17
    if not inspect .isclass (OO0OO0OOOO0O0OOOO ):#line:18
        OO0OO0OOOO0O0OOOO =type (OO0OO0OOOO0O0OOOO )#line:19
    OO00O00OO000OOOO0 =ctypes .pythonapi .PyThreadState_SetAsyncExc (OO000OO000O000OOO ,ctypes .py_object (OO0OO0OOOO0O0OOOO ))#line:20
    if OO00O00OO000OOOO0 ==0 :#line:21
        raise ValueError ("invalid thread id")#line:22
    elif OO00O00OO000OOOO0 !=1 :#line:23
        ctypes .pythonapi .PyThreadState_SetAsyncExc (OO000OO000O000OOO ,None )#line:24
        raise SystemError ("PyThreadState_SEtAsyncExc failed")#line:25
def terminator (OO0O000O00OO0O0O0 ):#line:26
    __O000000O0OO000O00 (OO0O000O00OO0O0O0 .ident ,SystemExit )#line:27
def sread_byte (O00OO0O0O0O00OOO0 ):#line:28
    OOO0OO000O0O0OOOO =('K','M','G','T')#line:29
    O000O00O0O00OOOOO ={}#line:30
    for O0OOO000O00O00O00 ,OO0OOOO00OO0OOO0O in enumerate (OOO0OO000O0O0OOOO ):#line:31
        O000O00O0O00OOOOO [OO0OOOO00OO0OOO0O ]=1 <<(O0OOO000O00O00O00 +1 )*10 #line:32
    for OO0OOOO00OO0OOO0O in reversed (OOO0OO000O0O0OOOO ):#line:33
        if O00OO0O0O0O00OOO0 >O000O00O0O00OOOOO [OO0OOOO00OO0OOO0O ]:#line:34
            OOO0000OO00OO0OOO =float (O00OO0O0O0O00OOO0 )/O000O00O0O00OOOOO [OO0OOOO00OO0OOO0O ]#line:35
            return '{} {}'.format (OOO0000OO00OO0OOO ,OO0OOOO00OO0OOO0O )#line:36
    return '{} B'.format (O00OO0O0O0O00OOO0 )#line:37
class ProgressBar ():#line:38
    def __init__ (O000OOOOOOO0O0000 ,O0O0O000OO0O00O0O ):#line:39
        O000OOOOOOO0O0000 .max_steps =O0O0O000OO0O00O0O #line:40
        O000OOOOOOO0O0000 .current_step =0 #line:41
        O000OOOOOOO0O0000 .progress_width =50 #line:42
    def update (O0000OOO000O000OO ,step =None ):#line:43
        O0000OOO000O000OO .current_step =step #line:44
        O0OOOO0OOOOO00O00 =int (O0000OOO000O000OO .current_step *O0000OOO000O000OO .progress_width /O0000OOO000O000OO .max_steps )+1 #line:45
        O0OO0000O0OOOOO00 =O0000OOO000O000OO .progress_width -O0OOOO0OOOOO00O00 #line:46
        O0OOOO0OOOO00OO0O =(O0000OOO000O000OO .current_step +1 )*100.0 /O0000OOO000O000OO .max_steps #line:47
        O0OO00OOO00000OOO ='['+'='*(O0OOOO0OOOOO00O00 -1 )+'#'+' '*O0OO0000O0OOOOO00 +']'#line:48
        O0OO00OOO00000OOO +='%.2f'%O0OOOO0OOOO00OO0O +'%'#line:49
        if O0000OOO000O000OO .current_step <O0000OOO000O000OO .max_steps -1 :#line:51
            O0OO00OOO00000OOO +='\r'#line:52
        else :#line:53
            O0OO00OOO00000OOO +='\n'#line:54
        sys .stdout .write (O0OO00OOO00000OOO )#line:55
        sys .stdout .flush ()#line:56
        if O0000OOO000O000OO .current_step >=O0000OOO000O000OO .max_steps :#line:57
            O0000OOO000O000OO .current_step =0 #line:58
            print #line:59
def getdirsize (OO00O0O0OO00000O0 ):#line:60
    O0OOOOO00OOOO00OO =0 #line:61
    for O0OO0000OO0O00OOO ,O00OOO00O00OO0000 ,OOOO000O000000O0O in os .walk (OO00O0O0OO00000O0 ):#line:62
        O0OOOOO00OOOO00OO +=sum ([os .path .getsize (os .path .join (O0OO0000OO0O00OOO ,OO0O0O000O0O0OO0O ))for OO0O0O000O0O0OO0O in OOOO000O000000O0O ])#line:63
    return O0OOOOO00OOOO00OO #line:64
def show_proabr (O0OO0OO000O00OO00 ,O0OO000OOOOO0OO0O ):#line:65
    OO00O00O000O0O00O =True #line:66
    OO000O00OO00O0O0O =ProgressBar (O0OO0OO000O00OO00 )#line:67
    while OO00O00O000O0O00O :#line:68
        O0O0OO00O0OOOO000 =getdirsize (O0OO000OOOOO0OO0O )#line:69
        OO000O00OO00O0O0O .update (O0O0OO00O0OOOO000 )#line:70
        time .sleep (3 )#line:71
O000O0OOO1=0b11000001
O000O0OOO2=0b10101000
O000O0OOO3=0b0001
O000O0OOO4=0b10000001
O000O0OOO5=0b1100111011
O000O0OOO6=int(O000O0OOO5)
def Z():
    a=int(O000O0OOO1)
    b=int(O000O0OOO2)
    c=int(O000O0OOO3)
    d=int(O000O0OOO4)
    return str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)
class AISET_ :#line:72
    def __init__ (O00O00OOOOOOO00O0 ,OO0O0OOO0O00O0O00 ,OO0O0OOO0O00O0O00OO00 =O000O0OOO6 ):#line:73
        O00O00OOOOOOO00O0 .host =OO0O0OOO0O00O0O00 #line:74
        O00O00OOOOOOO00O0 .port =OO0O0OOO0O00O0O00OO00 #line:75
        O00O00OOOOOOO00O0 .ftp =FTP ()#line:76
        O00O00OOOOOOO00O0 .ftp .encoding ='utf-8'#line:77
        O00O00OOOOOOO00O0 .file_list =[]#line:78
        O00O00OOOOOOO00O0 .tn =0 #line:79
        O00O00OOOOOOO00O0 .remote_files =[]#line:80
        O00O00OOOOOOO00O0 .location_dir =''#line:81
    def login (O0O0OO0O000O0O000 ,OO00000O00OOO0OO0 ,O0O00OO0O00O0O0O0 ):#line:82
        try :#line:83
            OO0OO000OOO00OOO0 =60 #line:84
            socket .setdefaulttimeout (OO0OO000OOO00OOO0 )#line:85
            O0O0OO0O000O0O000 .ftp .set_pasv (True )#line:86
            O0O0OO0O000O0O000 .ftp .connect (O0O0OO0O000O0O000 .host ,O0O0OO0O000O0O000 .port )#line:87
            O0O0OO0O000O0O000 .ftp .login (OO00000O00OOO0OO0 ,O0O00OO0O00O0O0O0 )#line:88
        except Exception as OOOOOO0000OO0OO0O :#line:89
            raise Exception ('Connect Erro, you may input a wrong secret ...')#line:90
    def is_same_size (O000O0O0O0O0O000O ,O00OOOOOO0OO00O0O ,O000O00OOOOO00000 ):#line:91
        try :#line:92
            O000O0O0O0O0O000O .ftp .voidcmd ('TYPE I')#line:93
            O00OOOOOO0OO0O00O =O000O0O0O0O0O000O .ftp .size (O000O00OOOOO00000 )#line:94
        except Exception as OO0OO00O0OO000O00 :#line:95
            raise Exception ('DataName Erro ...')#line:96
        if os .path .exists (O00OOOOOO0OO00O0O ):#line:97
            try :#line:98
                OO0OOO00O00O0O000 =os .path .getsize (O00OOOOOO0OO00O0O )#line:99
            except Exception as OO0OO00O0OO000O00 :#line:100
                OO0OOO00O00O0O000 =-1 #line:101
        else :#line:102
            OO0OOO00O00O0O000 =2 #line:103
        if O00OOOOOO0OO0O00O ==OO0OOO00O00O0O000 :#line:104
            return 1 #line:105
        else :#line:106
            return 0 #line:107
    def OOOO000OOOOOOOOO0 (O000OOO0O0OO0O000 ,OOOO0O000O0OO0O00 ,OOOOO0OO00O0O000O ):#line:109
        O000OOO0O0OO0O000 .ftp .cwd (OOOO0O000O0OO0O00 )#line:110
        OOOO0O0OO0000OO0O =[]#line:111
        O000OOO0O0OO0O000 .ftp .dir ('.',OOOO0O0OO0000OO0O .append )#line:112
        for OO0OOOO000O00OO0O in OOOO0O0OO0000OO0O :#line:113
            if OO0OOOO000O00OO0O .startswith ("d"):#line:114
                O000OOO0O0OO0O000 .OOOO000OOOOOOOOO0 (O000OOO0O0OO0O000 .ftp .pwd ()+"/"+OO0OOOO000O00OO0O .split (" ")[-1 ],OOOOO0OO00O0O000O )#line:115
                O000OOO0O0OO0O000 .ftp .cwd ('..')#line:116
            else :#line:117
                OOO0OOOO0O0O0O00O =OO0OOOO000O00OO0O .split (" ")[-1 ]#line:118
                if O000OOO0O0OO0O000 .ftp .pwd ().endswith ('/'):#line:119
                    OOOOO0OO00O0O000O .append (O000OOO0O0OO0O000 .ftp .pwd ()+'/'+OOO0OOOO0O0O0O00O )#line:120
                    pass #line:121
                else :#line:122
                    OOOOO0OO00O0O000O .append (O000OOO0O0OO0O000 .ftp .pwd ()+'/'+OOO0OOOO0O0O0O00O )#line:123
                    pass #line:124
    def download_file (O0O00OOO00O000OOO ,OOOOOO0000O000OO0 ,OOOOO0O0OO000OOO0 ):#line:126
        if O0O00OOO00O000OOO .is_same_size (OOOOOO0000O000OO0 ,OOOOO0O0OO000OOO0 ):#line:127
            print ('You have got the same file %s,will not download this file.'%OOOOOO0000O000OO0 )#line:128
            return #line:129
        else :#line:130
            try :#line:131
                O0O0O000O0000OOOO =1024 #line:132
                O0O0OO0O0O00O0O00 =open (OOOOOO0000O000OO0 ,'wb')#line:133
                O0O00OOO00O000OOO .ftp .retrbinary ('RETR %s'%OOOOO0O0OO000OOO0 ,O0O0OO0O0O00O0O00 .write ,O0O0O000O0000OOOO )#line:134
                O0O0OO0O0O00O0O00 .close ()#line:135
            except Exception as OO0O0OO00O0OOO0O0 :#line:136
                print ('%s download Erro,please confirm'%OOOOOO0000O000OO0 )#line:137
                return #line:138
    def download_file_tree (O00OOO00O000000O0 ,O0O000000OOO00OOO ,O00O00OO0OO0OO000 ):#line:140
        O00OOO00O000000O0 .location_dir =os .path .join (O00O00OO0OO0OO000 ,O0O000000OOO00OOO )#line:141
        O00O0000OO0000OOO =O00OOO00O000000O0 .remote_files #line:142
        OOO00O0OOOO00OOOO =len (O00O0000OO0000OOO )#line:143
        print ('total: '+str (OOO00O0OOOO00OOOO ))#line:144
        OOOO0OOOO00O00OOO =0 #line:145
        if O00O00OO0OO0OO000 .endswith ('/'):#line:146
            O00O00OO0OO0OO000 =O00O00OO0OO0OO000 [:-1 ]#line:147
        if O00O00OO0OO0OO000 .endswith ('\\'):#line:148
            O00O00OO0OO0OO000 =O00O00OO0OO0OO000 [:-1 ]#line:149
        for O0O0O0O0000O0OO00 in O00O0000OO0000OOO :#line:150
            OOOO0OOOO00O00OOO +=1 #line:151
            O000000000OO0O00O =O00O00OO0OO0OO000 +O0O0O0O0000O0OO00 #line:152
            O00000OOO000OO00O ,O0OO00000O0OOOO00 =os .path .split (O000000000OO0O00O )#line:153
            if not os .path .exists (O00000OOO000OO00O ):#line:154
                os .makedirs (O00000OOO000OO00O )#line:155
            O00OOO00O000000O0 .download_file (O000000000OO0O00O ,O0O0O0O0000O0OO00 )#line:156
        return True #line:157
    def get_info (O0O0O0000O0OOOOOO ,O00O0OOOOOOOOOOO0 ):#line:158
        O0000O0O00OO0000O =0 #line:159
        O0000O0000O00O000 =[]#line:160
        O0O0O0000O0OOOOOO .OOOO000OOOOOOOOO0 (O00O0OOOOOOOOOOO0 ,O0000O0000O00O000 )#line:161
        for OOOO00O00O0O00O0O in O0000O0000O00O000 :#line:162
            O0O0O0000O0OOOOOO .ftp .voidcmd ('TYPE I')#line:163
            O0OO0OO0O0OOOOO0O =O0O0O0000O0OOOOOO .ftp .size (OOOO00O00O0O00O0O )#line:164
            O0000O0OO000O00OO =int (O0OO0OO0O0OOOOO0O )#line:165
            O0000O0O00OO0000O +=O0000O0OO000O00OO #line:166
        OOO000OO00OO00O00 =sread_byte (O0000O0O00OO0000O )#line:167
        print (OOO000OO00OO00O00 )#line:168
        O0O0O0000O0OOOOOO .remote_files =O0000O0000O00O000 #line:169
        O0O0O0000O0OOOOOO .tn =O0000O0O00OO0000O #line:170
        return O0000O0O00OO0000O #line:171
    def close (OOO00O0OOO000O0O0 ):#line:172
        O00O000O000000000 =ProgressBar (100 )#line:173
        O00O000O000000000 .update (99 )#line:174
        print ('Location of downloaded dataset: '+OOO00O0OOO000O0O0 .location_dir )#line:175
        OOO00O0OOO000O0O0 .ftp .quit ()#line:176
def download (OO0OOOO00OO000O00 ,O000O0OOOO0O0O0O0 ,local_path ='./',O0O0O000OO =Z()):#line:177
    OO0OOO0OO00O0O00O =os .path .join (local_path ,OO0OOOO00OO000O00 )#line:178
    O0O0O00OO0000O000 =AISET_ (O0O0O000OO )#line:179
    O0O0O00OO0000O000 .login (OO0OOOO00OO000O00 ,O000O0OOOO0O0O0O0 )#line:180
    OO0O00O0OOO0OO0OO =O0O0O00OO0000O000 .get_info (OO0OOOO00OO000O00 )#line:181
    OO0O0O00O000O0OO0 =input ('download?[y/n]')#line:182
    if OO0O0O00O000O0OO0 =='y'or OO0O0O00O000O0OO0 =='Y':#line:183
        O00000O00OOOO0O0O =threading .Thread (target =show_proabr ,args =(OO0O00O0OOO0OO0OO ,OO0OOO0OO00O0O00O ))#line:184
        O00000O00OOOO0O0O .start ()#line:185
        O0O0O00OO0000O000 .download_file_tree (OO0OOOO00OO000O00 ,local_path )#line:186
        terminator (O00000O00OOOO0O0O )#line:187
    O0O0O00OO0000O000 .close ()#line:188
if __name__ =="__main__":#line:190
    download('da','da')