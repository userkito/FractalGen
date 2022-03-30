####################################################################################
#################################···FractalGen···###################################
####################################################################################

#a simple Fractal generator

# -> recursive
# -> complex:
    # -> Mandelbrot
    # -> Julia sets
# -> IFS

#Version: 1.0
#Author: Nicolás Rodrigo Pérez
#Date: 1/12/2021

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfile
import random
import math as mt


class Recursive:

    def __init__(self):
        pass

    #koch curve
    def koch(self,x1,y1,x4,y4,n):
        if n==0:
            self.r_canvas.create_line(x1,300-y1,x4,300-y4)
        else:
            dx=(x4-x1)/3
            dy=(y4-y1)/3
            x2=x1+dx
            y2=y1+dy
            x3=x2+dx
            y3=y2+dy
            x=(dx-mt.sqrt(3)*dy)/2+(x1+dx)
            y=(mt.sqrt(3)*dx+dy)/2+(y1+dy)
            self.koch(x1,y1,x2,y2,n-1)
            self.koch(x2,y2,x,y,n-1)
            self.koch(x,y,x3,y3,n-1)
            self.koch(x3,y3,x4,y4,n-1)

    def draw_koch(self):
        #recursion Size
        if self.koch_n_box.compare("end-1c", "==", "1.0"):
            n=self.koch_n #default
        else:
            n=int(self.koch_n_box.get(0.0,END))
        #window size
        WIDTH=600
        HEIGHT=300
        #set canvas
        win=Toplevel(self.window)
        win.title("Recursive: Koch curve")
        win.resizable(False,False)
        self.r_canvas=Canvas(win,width=WIDTH,height=HEIGHT)
        self.r_canvas.pack()
        win.update()
        win.after(1,self.koch(30,80,570,80,n))
        win.mainloop()

    #sierpinsky triangle
    def sierpinsky(self,x1,y1,x2,y2,x3,y3,n):
        if n==0:
            self.r_canvas.create_line(x1,y1,x2,y2)
            self.r_canvas.create_line(x2,y2,x3,y3)
            self.r_canvas.create_line(x1,y1,x3,y3)
        else:
            ax=x1+(x2-x1)/2
            ay=y1+(y2-y1)/2
            bx=x3+(x2-x3)/2
            by=y3+(y2-y3)/2
            cx=x1+(x3-x1)/2
            cy=y1+(y3-y1)/2
            self.sierpinsky(ax,ay,x2,y2,bx,by,n-1)
            self.sierpinsky(x1,y1,ax,ay,cx,cy,n-1)
            self.sierpinsky(cx,cy,bx,by,x3,y3,n-1)

    def draw_sierpinsky(self):
        #recursion Size
        if self.sier_n_box.compare("end-1c", "==", "1.0"):
            n=self.sier_n #default
        else:
            n=int(self.sier_n_box.get(0.0,END))
        #window size
        WIDTH=822
        HEIGHT=462
        size=400
        x,y=WIDTH/2,HEIGHT-(size+30)
        #set canvas
        win=Toplevel(self.window)
        win.title("Recursive: Sierpinsky triangle")
        win.resizable(False,False)
        self.r_canvas=Canvas(win,width=WIDTH,height=HEIGHT)
        self.r_canvas.pack()
        win.update()
        win.after(1,self.sierpinsky(x,y,x+size,y+size,x-size,y+size,n))
        win.mainloop()

class Complex:
    def __init__(self):
        self.c1=0
        self.c2=0
        self.c3=0

    #Mandelbrot
    #creates a new window and displays mandelbrot on it
    def mandelbrot(self):
        WIDTH,HEIGHT=800,600
        #corners of the mandelbrot plan to display
        xa,xb=-2.5,1.5
        ya,yb=-1.5,1.5
        #choose random colors
        self.c1=random.randint(1,3)  #4
        self.c2=random.randint(1,8)  #8
        self.c3=random.randint(1,16) #16
        #prepare plane
        xm,ym=[xa+(xb-xa)*kx/WIDTH for kx in range(WIDTH)],[ya+(yb-ya)*ky/HEIGHT for ky in range(HEIGHT)]
        #set mandelbrot own canvas
        window=Toplevel(self.window)
        window.title("Mandelbrot")
        window.resizable(False,False)
        canvas=Canvas(window,width=WIDTH,height=HEIGHT)
        img=PhotoImage(width=WIDTH,height=HEIGHT)
        canvas.create_image((0,0),image=img,state="normal",anchor=NW)
        pixels=" ".join(("{"+" ".join(('#%02x%02x%02x'%self.mandel(i,j) for i in xm))+"}" for j in ym))
        img.put(pixels)
        canvas.pack()
        window.mainloop()

    #calculates the pixel color of the point of mandelbrot plane passed
    def mandel(self,kx,ky):
        it=256 #256
        c=complex(kx,ky)
        z=complex(0.0,0.0)
        for i in range(it):
            z=z**2+c
            if abs(z)>=2.0:
                #set colors
                rd=i%self.c1*64 #4
                gr=i%self.c2*32 #8
                bl=i%self.c3*16 #16
                return(rd,gr,bl)
        return(0,0,0)

    def draw_mandelbrot(self):
        self.window.update()
        self.window.after(1,self.mandelbrot())

    #Julia sets
    #good looking c's: (creal, cimag) offset
    # -> -0.7744099143974259, -0.15956771613807463 0.9 (700,600)
    # -> 0.39405000507034704, -0.25960764418431037 0.6
    # -> 0.24887188420046347, -0.5120682139536082 0.6
    # -> -0.5196585289743931, -0.5192902242592998 0.6
    # -> 0.3465914321338519, 0.10237761112340948 0.6
    # -> 0.37806017969189476, 0.46375043242878455 0.6
    # -> 0.3851229073900807, -0.34719955332298197 0.6
    # -> 0.08302194069530633, 0.6414672566009902 1.1
    # -> -1.248609296624023, 0.4147295307101846 1.9
    # -> -1.3900536284629723, 0.0048591690863761805 1.9
    # -> 0.4982198948289023, -0.06763157211840864 1.9
    # -> -0.1366322223671721, -0.6682646816024229 1.9
    # -> 0.36718490494583644, -0.5406770830732306 1.9
    # -> -0.7712143298491261, 0.442447116405682 1.9
    # -> -0.16471801071293002, -0.9555878171051856 1.7
    # -> -0.30603281597711707, 0.6076181968812051 2
    # -> -0.7509902464695427, -0.04188925416813394 1.3
    # -> -0.6685580179653953, 0.6967383930475726 1.5
    # -> -0.14727541612622042, 0.7575762005432978 1.5 (700,700)
    # -> -0.06618865128343421, 0.7124776514160351 1.5
    # -> 0.3593729037621811, 0.2690522504146169 1.5
    # -> 0.2012865629970424, 0.6465199250843936 1.5
    # -> -0.7243737882662373, -0.18353732032568804 1.5 (700,500)
    # -> -0.0458541343760932, 0.8234788297261839 1.5
    # -> -0.44272672961358905, 0.6799062707538917 1.5

    #creates a new window and displays julia_set on it
    def julia_set(self):
        #window size
        WIDTH,HEIGHT=700,500
        #bounds
        #offset=random.uniform(-0.6,0.6)
        offset=1.5
        xa,xb=-offset,offset
        ya,yb=-offset,offset
        #obtain creal and cimag else set them random
        if self.c_real_box.compare("end-1c", "==", "1.0") and self.c_imag_box.compare("end-1c", "==", "1.0"):
            #fixed random c
            cr,ci=random.uniform(xa,xb),random.uniform(ya,yb)
        elif self.c_real_box.compare("end-1c", "==", "1.0"):
            #fixed random c
            cr,ci=0,float(self.c_imag_box.get(0.0,END))
        elif self.c_imag_box.compare("end-1c", "==", "1.0"):
            #fixed random c
            cr,ci=float(self.c_real_box.get(0.0,END)),0
        else:
            #fixed selected c
            cr,ci=float(self.c_real_box.get(0.0,END)),float(self.c_imag_box.get(0.0,END))
        #choose random colors
        self.c1=random.randint(1,3)
        self.c2=random.randint(1,8)
        self.c3=random.randint(1,16)
        #prepare plane
        xm=[xa+(xb-xa)*kx/WIDTH for kx in range(WIDTH)]
        ym=[ya+(yb-ya)*ky/HEIGHT for ky in range(HEIGHT)]
        #set julia_set own canvas
        window=Toplevel(self.window)
        window.title("Julia set")
        window.resizable(False,False)
        canvas=Canvas(window,width=WIDTH,height=HEIGHT)
        img=PhotoImage(width=WIDTH,height=HEIGHT)
        canvas.create_image((0,0),image=img,state="normal",anchor=NW)
        pixels=" ".join(("{"+" ".join(('#%02x%02x%02x'%self.julia(i,j,cr,ci) for i in xm))+"}" for j in ym))
        img.put(pixels)
        canvas.pack()
        window.mainloop()

    #calculates the pixel color of the point of julia plane passed
    def julia(self,kx,ky,cr,ci):
        it=256 #256
        z=complex(kx,ky)
        c=complex(cr,ci)
        for i in range(it):
            z=z**2+c
            if abs(z)>=2.0:
                #set colors
                rd=i%self.c1*64 #4
                gr=i%self.c2*32 #8
                bl=i%self.c3*16 #16
                return(rd,gr,bl)
        return(0,0,0)

    def draw_julia(self):
        self.window.update()
        self.window.after(1,self.julia_set())

class IFS:
    def __init__(self):
        pass

    def ifs(self,mat):
        #default window size
        imgx=500
        imgy=300
        #iters
        if self.ifs_iters_box.compare("end-1c", "==", "1.0"):
            iters=self.ifs_iters #default
        else:
            iters=int(self.ifs_iters_box.get(0.0,END))
        #number of IFS transformations
        m = len(mat)
        #find box dimensions
        x = mat[0][4]
        y = mat[0][5]
        xa = x
        xb = x
        ya = y
        yb = y
        for k in range(imgx * imgy):
            p = random.random()
            psum = 0.0
            for i in range(m):
                psum += mat[i][6]
                if p <= psum:
                    break
            x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4]
            y  = x * mat[i][2] + y * mat[i][3] + mat[i][5]
            x = x0
            if x < xa:
                xa = x
            if x > xb:
                xb = x
            if y < ya:
                ya = y
            if y > yb:
                yb = y
        #auto-re-adjust the aspect ratio
        imgy = int(imgy * (yb - ya) / (xb - xa))
        #set ifs own canvas and PIL image
        window=Toplevel(self.window)
        window.title("IFS")
        window.resizable(False,False)
        canvas=Canvas(window,width=imgx,height=imgy)
        canvas.pack()
        image = Image.new("RGB", (imgx, imgy))
        colors=[]
        #choose random colors for each function
        for t in range(m):
            c1=random.randint(1,4)  #4
            c2=random.randint(1,8)  #8
            c3=random.randint(1,16) #16
            colors.append([c1,c2,c3])
        #draw ifs fractal
        x=0.0
        y=0.0
        for j in range(iters):
            for k in range(imgx * imgy):
                p=random.random()
                psum = 0.0
                for i in range(m):
                    psum += mat[i][6]
                    if p <= psum:
                        break
                x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4]
                y  = x * mat[i][2] + y * mat[i][3] + mat[i][5]
                x = x0
                jx = int((x - xa) / (xb - xa) * (imgx - 1))
                jy = (imgy - 1) - int((y - ya) / (yb - ya) * (imgy - 1))
                try:
                    image.putpixel((jx, jy), (j % colors[i][0] * 64, j % colors[i][1] * 32, j % colors[i][2] * 16))
                except IndexError:
                    #print("Skipping out of bounds dot")
                    pass
        img=ImageTk.PhotoImage(image)
        canvas_img=canvas.create_image((0,0),image=img,state="normal",anchor=NW)
        if len(self.user_mat)!=0:
            img=ImageTk.PhotoImage(image.rotate(180))
            canvas_img=canvas.create_image((0,0),image=img,state="normal",anchor=NW)
        window.mainloop()

    def select_ifs(self,e):
        #ifs code defined as:
        #(a, b, c, d, e, f, p)
        #where p is the probability of the function.
        if self.ifs_combo.get()=="Fern":
            #Fern fractal
            mat = [[0.0,0.0,0.0,0.16,0.0,0.0,0.01],
                   [0.85,0.04,-0.04,0.85,0.0,1.6,0.85],
                   [0.2,-0.26,0.23,0.22,0.0,1.6,0.07],
                   [-0.15,0.28,0.26,0.24,0.0,0.44,0.07]]
        elif self.ifs_combo.get()=="C":
            #C fractal
            mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
                   [0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5]]
        elif self.ifs_combo.get()=="Dragon curve":
            #Dragon curve fractal
            mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
                   [-0.5, -0.5, 0.5, -0.5, 1.0, 0.0, 0.5]]
        elif self.ifs_combo.get()=="Dragon":
            #Dragon fractal
            mat = [[0.824074, 0.281482, -0.212346,  0.864198, -1.882290, -0.110607, 0.787473],
                   [0.088272, 0.520988, -0.463889, -0.377778,  0.785360,  8.095795, 0.212527]]
        elif self.ifs_combo.get()=="Noisy":
            #Noisy fractal
            mat = [[0.424,-0.651,-0.485,-0.345,3.964,4.222,0.5],
                   [-0.080,-0.203,-0.743,0.205,-4.092,3.957,0.5]]
        elif self.ifs_combo.get()=="ZigZag":
            #ZigZag fractal
            mat = [[-0.63,-0.61,-0.55,0.66,3.84,1.28,0.5],
                   [-0.04,0.44,0.21,0.04,2.07,8.33,0.5]]
        elif self.ifs_combo.get()=="Spiral":
            #Spiral fractal
            mat = [[-0.312,-0.832,0.812,-0.283,3.870,7.404,0.76],
                   [0.125,0.317,-0.187,-0.130,2.043,7.917,0,12],
                   [-0.062,-0.197,0.250,0.173,-3.132,0.846,0.12]]
        self.window.update()
        self.window.after(1,self.ifs(mat))

    def add_function(self):
        func = []
        func.append(float(self.ifs_a_box.get(0.0,END)))
        self.ifs_a_box.delete(0.0,END)
        func.append(float(self.ifs_b_box.get(0.0,END)))
        self.ifs_b_box.delete(0.0,END)
        func.append(float(self.ifs_c_box.get(0.0,END)))
        self.ifs_c_box.delete(0.0,END)
        func.append(float(self.ifs_d_box.get(0.0,END)))
        self.ifs_d_box.delete(0.0,END)
        func.append(float(self.ifs_e_box.get(0.0,END)))
        self.ifs_e_box.delete(0.0,END)
        func.append(float(self.ifs_f_box.get(0.0,END)))
        self.ifs_f_box.delete(0.0,END)
        func.append(float(self.ifs_p_box.get(0.0,END)))
        self.ifs_p_box.delete(0.0,END)
        self.user_mat.append(func)

    def draw_user_ifs(self):
        self.window.update()
        self.window.after(1,self.ifs(self.user_mat))

    def save_user_ifs(self):
        files=[("Text Document","*.txt")]
        file=asksaveasfile(filetypes=files,defaultextension=files)
        file.write(str(self.user_mat))
        self.user_mat=[]

class FractalGen(Recursive,Complex,IFS):

    def __init__(self):
        self.WIDTH=240
        self.HEIGHT=450
        self.WINDOW_SIZE = str(self.WIDTH)+"x"+str(self.HEIGHT)
        #main application window
        self.window=Tk()
        self.window.title("FractalGen")
        self.window.resizable(False,False)
        self.window.geometry(self.WINDOW_SIZE)
        self.window.configure(bg='grey')
        #recursive defaults
        self.koch_n=4 #default
        self.sier_n=4 #default
        self.r_canvas=None
        #ifs options
        self.ifs_fractals=["Fern","C","Dragon curve","Dragon","Noisy","ZigZag","Spiral"]
        self.ifs_iters=6 #default
        self.ifs_combo=None
        self.user_mat=[]

    #set a button on the main window
    def button(self,name,command,x,y,h,w):
        button=Button(self.window,text=str(name),command=command,height=h,width=w)
        button.place(x=x,y=y)
        return button

    #set a label on the main window
    def label(self,content,x,y,size):
        label=Label(self.window,text=str(content),font=(None, size),bg='grey')
        label.place(x=x,y=y)
        return label

    #set text box on the main window
    def textBox(self,text,x,y,h,w):
        t=Text(self.window,height=h,width=w)
        t.place(x=x,y=y)
        t.insert(1.0,text)
        t.bind("<Tab>",self.move_cursor_right)
        return t

    #set combobox on the main window
    def combobox(self,value,bind_function,x,y,h,w):
        c=ttk.Combobox(self.window,value=value,height=h,width=w,state="readonly")
        c.current(0)
        c.bind("<<ComboboxSelected>>",bind_function)
        c.place(x=x,y=y)
        return c

    def move_cursor_right(self,event):
        event.widget.tk_focusNext().focus()
        return("break")

    #exit application
    def close(self):
        self.window.destroy()

    #run application
    def run(self):
        #240x450
        #recursive
        self.label("----------- Recursive -----------",3,6,14)
        self.label("Koch n:",15,40,10)
        self.koch_n_box=self.textBox(str(self.sier_n),68,40,1,2)
        self.button("Koch",self.draw_koch,120,36,1,10)
        self.label("Sierp. n:",15,76,10)
        self.sier_n_box=self.textBox(str(self.koch_n),68,76,1,2)
        self.button("Sierpinsky",self.draw_sierpinsky,120,72,1,10)

        #Complex
        self.label("------------ Complex ------------",2,110,14)
        self.label("c real:",15,146,10)
        self.c_real_box=self.textBox("",55,146,1,6)
        self.label("c imag.:",115,146,10)
        self.c_imag_box=self.textBox("",166,146,1,6)
        self.button("Mandelbrot",self.draw_mandelbrot,30,180,1,10)
        self.button("Julia Set",self.draw_julia,130,180,1,10)

        #IFS
        self.label("---------------- IFS ---------------",2,218,14)
        self.label("iters:",30,254,10)
        self.ifs_iters_box=self.textBox(str(self.ifs_iters),67,254,1,2)
        self.ifs_combo=self.combobox(self.ifs_fractals,self.select_ifs,116,254,1,10)
        self.label("a:",13,290,10)
        self.ifs_a_box=self.textBox("",28,290,1,3)
        self.label("b:",58,290,10)
        self.ifs_b_box=self.textBox("",73,290,1,3)
        self.label("c:",103,290,10)
        self.ifs_c_box=self.textBox("",118,290,1,3)
        self.label("d:",13,325,10)
        self.ifs_d_box=self.textBox("",28,325,1,3)
        self.label("e:",58,325,10)
        self.ifs_e_box=self.textBox("",73,325,1,3)
        self.label("f:",106,325,10)
        self.ifs_f_box=self.textBox("",118,325,1,3)
        self.label("p:",164,290,10)
        self.ifs_p_box=self.textBox("",179,290,1,3)
        self.button("Add",self.add_function,160,322,1,7)
        self.button("Draw",self.draw_user_ifs,30,360,1,10)
        self.button("Save",self.save_user_ifs,130,360,1,10)

        #other
        self.button("Exit",self.close,80,410,1,10)
        self.window.mainloop()


fg=FractalGen()
fg.run()
