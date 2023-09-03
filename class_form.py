import json
from datetime import datetime,date
from tkinter import *
from time import sleep

class Calender():
    def __init__(self):
        self.xroot=0 #窗口x
        self.yroot=10 #窗口y
        self.x=10 #课表左右留空
        self.y=10 #课表上下留空
        self.width=0 #窗口宽度
        self.height=0 #窗口高度
        self.classes=[] #课程
        self.labels=[] #课程label
        self.left=[] #分隔符
        self.leftlabs=[] #分隔符label
        self.selects=[] #换课选项
        self.selectlabs=None #换课label
        self.times=[] #课程时间
        self.selected=False #选中状态，False表示未选中，数字表示选中的位置
        self.window=None #窗口主体
        self.nowclass=0 #当前课程
        self.onw="" #上课提示
        self.offw="" #下课提示
        self.status=False #上/下课
        self.offtk=[] #下课窗口


    """平滑动画函数"""
    def move(self,wins,hopel,hopew,hopex,hopey,times=1.2):
        length=[]
        width=[]
        x=[]
        y=[]
        win=[]
        for b in range(len(wins)):
            length.append(wins[b].winfo_width())
            width.append(wins[b].winfo_height())
            x.append(wins[b].winfo_x())
            y.append(wins[b].winfo_y())
            a=-5
            while a<5:
                length_now=-(length[b]-hopel[b])/(1+3**(-a))+length[b]
                width_now=-(width[b]-hopew[b])/(1+3**(-a))+width[b]
                x_now=-(x[b]-hopex[b])/(1+3**(-a))+x[b]
                y_now=-(y[b]-hopey[b])/(1+3**(-a))+y[b]
                win.append(str(int(length_now))+"x"+str(int(width_now))+"+"+str(int(x_now))+"+"+str(int(y_now)))
                a+=10/int(times/0.005)
                
        b=1
        while b<int(times/0.005):        
            for a in range(len(wins)):
                wins[a].geometry(win[b+int(times/0.005)*a])
                wins[a].update()
            sleep(0.005)
            b+=1


    """读取"""
    def load_class(self,day=None):
        today=datetime.now()
        to_week=date(today.year,today.month,today.day).weekday()
        week=["一","二","三","四","五","六","日"]

        with open('config.json',encoding="utf-8") as file:
            text=json.load(file)
            if day==None:
                self.classes=["周"]+[week[to_week]]+["|"]+text["日程表"][str(to_week+1)]#读取课表
            else:
                self.classes=["周"]+[week[to_week]]+["|"]+text["日程表"][str(day+1)]#读取课表
            self.left=text["分隔符"]+["|"]
            self.selects=text["更换选项"]
            on=text["开始时间"]
            off=text["结束时间"]
            self.times=[]
            self.onw=text["开始提示"]
            self.offw=text["结束提示"]
            for x in range(len(on)):
                self.times.append(on[x])
                self.times.append(off[x])


    """显示课表"""
    def create(self):
        #初始化窗口
        self.window=Tk()
        self.window.overrideredirect(True)
        self.window.attributes('-topmost',True)
        self.window.attributes('-alpha',0.7)
        self.window.config(bg='black')
        self.window.bind('<Double-Button-1>',self.select)

        #x坐标依次显示label
        position=self.x
        for x in self.classes:
            class_lab=Label(self.window,text=x,font=('幼圆',40),fg='white',bg='black',wraplength=40)
            class_lab.place(x=position,y=self.y)
            if x in self.left:
                self.leftlabs.append(class_lab)
            else:
                class_lab.x=position #为label添加x
                class_lab.num=len(self.leftlabs+self.labels) #添加label所处classes位置
                self.labels.append(class_lab)
            position+=class_lab.winfo_reqwidth()

            #设置窗口高度，并且考虑换行情况
            height=class_lab.winfo_reqheight()+self.y*2
            if height>self.height:
                self.height=height

        self.width=position+self.x #设置窗口宽度
        self.xroot=int((self.window.winfo_screenwidth()-self.width)/2)
        self.window.geometry('1x'+str(self.height)+'+'+str(int(self.window.winfo_screenwidth()/2))+'+'+str(self.yroot))
        self.window.update()
        self.move([self.window],[self.width],[self.height],[self.xroot],[self.yroot]) #创建窗口


        """换课功能"""
    def select(self,event):
        self.window.unbind('<Double-Button-1>')
        if event.y_root-self.yroot<self.height:
            a=-1
            for l in self.labels:
                if event.x_root-self.window.winfo_x()>=l.x:
                    a+=1

            if self.selected==False:
                if a<2: #选中星期
                    self.labels[0]['bg']='grey'
                    self.labels[1]['bg']='grey'
                    self.selectlabs=Label(self.window,text='一 二 三 四 五 六 日',font=('幼圆',40),fg='white',bg='black')
                else:
                    self.labels[a]['bg']='grey'
                    self.selectlabs=Label(self.window,text=' '.join(self.selects),font=('幼圆',40),fg='white',bg='black')
                self.selectlabs.place(x=self.x,y=self.height)
                if self.width<self.selectlabs.winfo_reqwidth():
                    self.move([self.window],[self.selectlabs.winfo_reqwidth()+self.x*2],[self.height+self.selectlabs.winfo_reqheight()+self.x],[int(self.window.winfo_x()-(self.selectlabs.winfo_reqwidth()-self.width)/2)],[self.yroot],0.1)
                else:
                    self.move([self.window],[self.width],[self.height+self.selectlabs.winfo_reqheight()+self.x],[self.window.winfo_x()],[self.yroot],0.1)
                self.selected=a
            elif a==self.selected: #重复点取消换课
                if a<2:
                    self.labels[0]['bg']='black'
                    self.labels[1]['bg']='black'
                else:
                    self.labels[a]['bg']='black'
                self.move([self.window],[self.width],[self.height],[self.window.winfo_x()],[self.yroot],0.1)
                self.selectlabs.destroy()
                self.selected=False
            else:
                if self.selected<2:
                    self.labels[0]['bg']='black'
                    self.labels[1]['bg']='black'
                else:
                    self.labels[self.selected]['bg']='black'
                self.move([self.window],[self.width],[self.height],[self.window.winfo_x()],[self.yroot],0.1)
                self.selectlabs.destroy()

                if a<2: #选中星期
                    self.labels[0]['bg']='grey'
                    self.labels[1]['bg']='grey'
                    self.selectlabs=Label(self.window,text='一 二 三 四 五 六 日',font=('幼圆',40),fg='white',bg='black')
                else:
                    self.labels[a]['bg']='grey'
                    self.selectlabs=Label(self.window,text=' '.join(self.selects),font=('幼圆',40),fg='white',bg='black')
                self.selectlabs.place(x=self.x,y=self.height)
                if self.width<self.selectlabs.winfo_reqwidth():
                    self.move([self.window],[self.selectlabs.winfo_reqwidth()+self.x*2],[self.height+self.selectlabs.winfo_reqheight()+self.x],[int(self.window.winfo_x()-(self.selectlabs.winfo_reqwidth()-self.width)/2)],[self.yroot],0.1)
                else:
                    self.move([self.window],[self.width],[self.height+self.selectlabs.winfo_reqheight()+self.x],[self.window.winfo_x()],[self.yroot],0.1)
                self.selected=a

        else:
            a=int((event.x_root-self.window.winfo_x()-self.x)/80)
            if self.selected<2:
                if a>6:
                    a=6
                """重新设置课表"""
                self.load_class(a)
                for x in self.leftlabs+self.labels:
                    x.destroy()
                self.leftlabs=[]
                self.labels=[]
                #x坐标依次显示label
                self.height=0
                position=self.x
                for x in self.classes:
                    class_lab=Label(self.window,text=x,font=('幼圆',40),fg='white',bg='black',wraplength=40)
                    class_lab.place(x=position,y=self.y)
                    if x in self.left:
                        self.leftlabs.append(class_lab)
                    else:
                        class_lab.x=position #为label添加x
                        class_lab.num=len(self.leftlabs+self.labels) #添加label所处classes位置
                        self.labels.append(class_lab)
                    position+=class_lab.winfo_reqwidth()

                    #设置窗口高度，并且考虑换行情况
                    height=class_lab.winfo_reqheight()+self.y*2
                    if height>self.height:
                        self.height=height
                self.width=position+self.x #设置窗口宽度
                self.xroot=int((self.window.winfo_screenwidth()-self.width)/2)
                self.nowclass=0
            else:
                if a>len(self.selects)-1:
                    a=len(self.selects)-1
                self.labels[self.selected]['bg']='black'
                self.labels[self.selected]['text']=self.selects[a]
                self.classes[self.labels[self.selected].num]=self.selects[a]

            self.move([self.window],[self.width],[self.height],[self.window.winfo_x()],[self.yroot],0.1)
            self.selectlabs.destroy()
            self.selected=False

        self.window.bind('<Double-Button-1>',self.select)


    """上课动画"""
    def onclass(self):
        if self.times[0]==[datetime.now().hour,datetime.now().minute]:
            self.window.unbind('<Double-Button-1>')
            sleep(1)
            xe=self.labels[self.nowclass+2].x
            oncl=Label(self.window,text=self.labels[self.nowclass+2]['text'],font=('幼圆',40),fg='yellow',bg='black',wraplength=40) #先行创建上方label
            if self.offtk!=[]:
                self.move([self.window,self.offtk[0]],[self.width,1],[self.height,self.y*2+self.offtk[1].winfo_reqheight()],[self.xroot,int((self.window.winfo_screenwidth()+self.width)/2)-self.x+20],[self.yroot,self.yroot])

            #删除原有
            for l in self.labels+self.leftlabs:
                l.destroy()
            try:
                self.selectlabs.destroy()
            except AttributeError:
                pass
            if self.offtk!=[]:
                self.offtk[1].destroy()
                self.offtk[0].destroy()

            #缩至一格
            self.move([self.window],[self.x*2+oncl.winfo_reqwidth()],[self.y*2+oncl.winfo_reqheight()],[self.xroot+xe],[self.yroot])
            #居中放置
            oncl.place(y=self.y,relx=0.5,anchor='n')
            self.window.update()
            sleep(1)
            #第二动画
            onlab=Label(self.window,text=self.onw,font=('幼圆',40),fg='yellow',bg='black')
            onlab.place(relx=0.5,anchor='n',y=self.window.winfo_height())
            self.move([self.window],[self.x*2+onlab.winfo_reqwidth()],[self.y*3+oncl.winfo_reqheight()+onlab.winfo_reqheight()],[self.xroot+xe-(onlab.winfo_reqwidth()/2)],[self.yroot])
            sleep(5)
            #恢复动画
            self.move([self.window],[self.x*2+oncl.winfo_reqwidth()],[self.y*2+oncl.winfo_reqheight()],[self.xroot+xe],[self.yroot])
            oncl.destroy()
            onlab.destroy()
            self.window.update()
            self.move([self.window],[self.width],[self.height],[self.xroot],[self.yroot])

            #x坐标依次显示label
            self.leftlabs=[]
            self.labels=[]
            self.xlist=[]
            position=self.x
            for x in self.classes:
                class_lab=Label(self.window,text=x,font=('幼圆',40),fg='white',bg='black',wraplength=40)
                class_lab.place(x=position,y=self.y)
                if x in self.left:
                    self.leftlabs.append(class_lab)
                else:
                    class_lab.x=position #为label添加x
                    class_lab.num=len(self.leftlabs+self.labels) #添加label所处classes位置
                    self.labels.append(class_lab)
                position+=class_lab.winfo_reqwidth()
            self.window.bind('<Double-Button-1>',self.select)

        self.labels[self.nowclass+1]['fg']='white'
        self.labels[self.nowclass+2]['fg']='yellow'
        del(self.times[0])
        self.window.attributes('-topmost',False)
    

    """下课动画"""
    def offclass(self):
        if self.times[0]==[datetime.now().hour,datetime.now().minute]:
            self.window.unbind('<Double-Button-1>')
            sleep(0.5)
            if self.selected<2:
                self.labels[0]['bg']='black'
                self.labels[1]['bg']='black'
            else:
                self.labels[self.selected]['bg']='black'
            self.offtk=[Tk()]

            #判断放学(未完成)
            if len(self.times)==1:
                self.offtk.append(Label(self.offtk[0],text="放学了",font=('幼圆',40),fg='yellow',bg='black'))
            else:
                self.offtk.append(Label(self.offtk[0],text=self.offw,font=('幼圆',40),fg='yellow',bg='black'))
            
            self.offtk[0].overrideredirect(True)
            self.offtk[0].attributes('-topmost',True)
            self.offtk[0].attributes('-alpha',0.7)
            self.offtk[0].config(bg='black')
            self.offtk[0].geometry('1x'+str(self.y*2+self.offtk[1].winfo_reqheight())+'+'+str(int((self.window.winfo_screenwidth()+self.width)/2)-self.x+20)+'+'+str(self.yroot))
            self.offtk[1].place(x=self.x,y=self.y)
            self.offtk[0].update()
            self.move([self.window,self.offtk[0]],[self.width,self.x*2+self.offtk[1].winfo_reqwidth()],[self.height,self.y*2+self.offtk[1].winfo_reqheight()],[int((self.window.winfo_screenwidth()-self.width-self.x*2-self.offtk[1].winfo_reqwidth()-40)/2),int((self.window.winfo_screenwidth()+self.width-self.offtk[1].winfo_reqwidth())/2)+20-self.x],[self.yroot,self.yroot])
            try:
                self.selectlabs.destroy()
            except AttributeError:
                pass
            self.window.bind('<Double-Button-1>',self.select)
            
        self.window.attributes('-topmost',True)
        if len(self.times)==1:
            self.window.mainloop()
        del(self.times[0])
        self.nowclass+=1
        self.labels[self.nowclass+1]['fg']='white'
        self.labels[self.nowclass+2]['fg']='yellow'


    def find(self):
        if self.times==[]:
            self.window.mainloop()
            self.window.unbind('<Double-Button-1>')
        else:
            if self.times[0][0]<datetime.now().hour:
                if self.status:
                    self.offclass()
                    self.status=False
                else:
                    self.onclass()
                    self.status=True
            elif self.times[0][1]<=datetime.now().minute and self.times[0][0]==datetime.now().hour:
                if self.status:
                    self.offclass()
                    self.status=False
                else:
                    self.onclass()
                    self.status=True
        self.window.update()
        sleep(0.1)


cl=Calender()
cl.load_class()
cl.create()
while True:
    cl.find()