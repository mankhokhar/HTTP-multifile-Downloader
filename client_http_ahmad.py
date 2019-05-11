import socket
import os,os.path

def write_file(msg,x,ftype,direct):
        os.chdir(direct)
        f = open('Socket'+str(x)+'.' +ftype, 'ab')
        f.write(msg)
        f.close()
def write_file1(msg,x,ftype,direct):
        os.chdir(direct)
        f = open('Socket'+str(x)+'.' +ftype, 'wb')
        f.write(msg)
        f.close()
        
def get_server_addess(site):
#procssing to string to sepearate server and address for http request
        if site.startswith('http://'):
                site = site[7:]
        server,address = site.split('/',1)
        address = '/' + address
        return (server,address)

def connect(server):
        #tcp connection establish
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server,80)
        cs.connect(server_address)
        return cs

def byte_range_download(s,q,contentlength,address,server,cs,type1,folder):
        if b'bytes' in s[b'Accept-Ranges']  :
                        #loop for multiple get requests
                        q=10 #Incase of multiple connection we get this variable from user
                        previousB= 0
                        nextB = contentlength//q
                        #nextB = 18000               
                        full_msg = b''
                        c=0
                        for x in range (1,11):
                                
                                bRange = "%s-%s"%(previousB,nextB)
                                request = 'GET ' + address + ' HTTP/1.1\r\nHOST: ' + server + '\r\nRange:bytes=' + bRange + '\r\n\r\n'
                                print(request)
                                request_header = bytes(request,'utf-8')  
                                cs.send(request_header)
                                previousB = nextB + 1
                                flag = nextB
                                if nextB>contentlength:
                                        flag = contentlength
                                nextB += contentlength//q
                                print(nextB)
                                new_msg= True
                                #c=True
                                
                                while c<flag:
                                    msg = cs.recv(15000)
                                    
                                    if new_msg:
                                        
                                        head = msg.split(b'\r\n\r\n')
                                        header=(len(head[0]))+4
                                        print(head[0])
                                        print(header)
                                        msg = head[1]
                                        new_msg = False        
                                    #print(len(msg))
                                    c+=len(msg)
                                    full_msg = full_msg + msg
                                    print(len(full_msg))
                                    write_file(msg,3,type1,folder)
                                    if len(full_msg)== contentlength:
                                        print(full_msg[header:])
                                        print('Done through special loop')
                                        #write_file(full_msg,3,type1)
                                        new_msg = True
                                        full_msg = b''
                                        c= False
                        cs.close()
                
def download_file(site,download_dir):

        server,address = get_server_addess(site)
        cs = connect(server)

        #generating request and sending to know length of data
        request = 'HEAD ' + address + ' HTTP/1.1\r\nHOST: ' + server +'\r\nAccept-Ranges: bytes\r\n\r\n'
        request_header = bytes(request,'utf-8') 
        cs.send(request_header)
        
        #processing header to find content length of file to be downloaded
        header = cs.recv(2096)
        header = header.split(b'\r\n')
        
        s = {}
        for i in range(1,len(header)-2):
            y = header[i].split(b':')
            s[y[0]] = y[1]
            #print(y)
        contentlength = int(s[b'Content-Length'])
        type1 = s[b'Content-Type'].split(b'/')[1]
        type1 = str(type1,'utf-8')
        if b'Accept-Ranges' in s:
                byte_range_download(s,10,contentlength,address,server,cs,type1,download_dir)
        else:
                print('Simulataneous connection not allowed using single connection')
                request = 'GET ' + address + ' HTTP/1.1\r\nHOST: ' + server + '\r\n\r\n'
                
                request_header = bytes(request,'utf-8')  
                cs.send(request_header)

                full_msg = b''
                new_msg= True
                c=True
                while c:
                    msg = cs.recv(4096)
                    if new_msg:
                        head = msg.split(b'\r\n\r\n')
                        header=(len(head[0]))+4
                        print(head[0])
                        print(header)
                        msg = head[1]
                        new_msg = False
                    #print("tis one did it" )
                    full_msg += msg
                    write_file(msg,2,type1,2,download_dir)
                    if len(full_msg)== contentlength:
                                print(full_msg[header:])
                                print('Done')
                                new_msg = True
#                                write_file(full_msg,2)
                                full_msg = ""
                                c= False
                                cs.close()         
                

                
#Main Function
site = 'http://open-up.eu/files/Berlin%20group%20photo.jpg?width=600&height=600'
#site = 'http://people.unica.it/vincenzofiorentini/files/2012/04/Halliday-Fundamentals-of-Physics-Extended-9th-HQ.pdf'
#site = 'http://africhthy.org/sites/africhthy.org/files/styles/slideshow_large/public/Lukuga.jpg?itok=M6ByJTZQ'
#site = 'http://ipaeg.org/sites/ipaeg.org/files/styles/medium/public/IMG_0499.JPG?itok=U8KP8f4j'
#site = 'http://s0.cyberciti.org/images/misc/static/2012/11/ifdata-welcome-0.png'
site = 'http://i.imgur.com/z4d4kWk.jpg'

#server,address = get_server_address(site)
ddir= "E:\Movies"
download_file(site,ddir)