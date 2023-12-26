from tkinter import *
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import threading as th
from PIL import ImageTk
from sys import path
import os
import multiprocessing as mp
import pandas as pd

global sys_path
sys_path = path[0]
global resource_path
resource_path = os.path.join(sys_path,"Resources")
global amu
amu = 931.5
global temp_folder
temp_folder = os.path.join(sys_path,"temp")

class Window(Tk):
    def __init__(self):
        super().__init__()

        self.KM = Kinematics()
        
        self.protocol("WM_DELETE_WINDOW",self.on_x)
        self.title("AT-TPC Sim")
        self.resizable(False, False)
        self.iconphoto(False,ImageTk.PhotoImage(file=os.path.join(resource_path,'FRIBlogo.png'),format='png'))

        self.frame = Frame(self)
        self.frame.pack()

        # Creating Reaction Input Frame
        self.reaction_frame = LabelFrame(self.frame, text = "Reaction Info")
        self.reaction_frame.grid(row=0,column=0,sticky="ew",padx=10,pady=3)

        self.mbeam_label = Label(self.reaction_frame, text = "Z and A of Beam")
        self.mbeam_label.grid(row=0,column=0)
        self.zbeam_entry = Entry(self.reaction_frame,textvariable=IntVar(value=4))
        self.zbeam_entry.grid(row=1,column=0)
        self.mbeam_entry = Entry(self.reaction_frame,textvariable=IntVar(value=10))
        self.mbeam_entry.grid(row=2,column=0)

        self.mtarget_label = Label(self.reaction_frame, text = "Z and A of Target")
        self.mtarget_label.grid(row=0,column=1)
        self.ztarget_entry = Entry(self.reaction_frame,textvariable=IntVar(value=1))
        self.ztarget_entry.grid(row=1,column=1)
        self.mtarget_entry = Entry(self.reaction_frame,textvariable=IntVar(value=1))
        self.mtarget_entry.grid(row=2,column=1)

#        self.mbeamlike_label = Label(self.reaction_frame, text = "Z and A of Beamlike")
#        self.mbeamlike_label.grid(row=0,column=2)
#        self.mbeamlike_entry = Entry(self.reaction_frame,textvariable="4 10")
#        self.mbeamlike_entry.grid(row=1,column=2)

        self.mtargetlike_label = Label(self.reaction_frame, text = "Z and A of Targetlike")
        self.mtargetlike_label.grid(row=0,column=2)
        self.ztargetlike_entry = Entry(self.reaction_frame,textvariable=IntVar(value=1))
        self.ztargetlike_entry.grid(row=1,column=2)
        self.mtargetlike_entry = Entry(self.reaction_frame,textvariable=IntVar(value=1))
        self.mtargetlike_entry.grid(row=2,column=2)

        self.beamke_label = Label(self.reaction_frame,text="Beam KE (MeV/u)")
        self.beamke_label.grid(row=3,column=0)
        self.beamke_entry = Entry(self.reaction_frame,textvariable=IntVar(value=10))
        self.beamke_entry.grid(row=4,column=0)

        self.comangle_label = Label(self.reaction_frame, text = "Enter CM Angle (deg)")
        self.comangle_label.grid(row=3,column=1)
        self.comangle_entry = Entry(self.reaction_frame,textvariable=IntVar(value=45))
        self.comangle_entry.grid(row=4,column=1)

        self.nreaction_label = Label(self.reaction_frame, text = "# Reactions (thousands)")
        self.nreaction_label.grid(row=3,column=2)
        self.nreaction_entry = Entry(self.reaction_frame,textvariable=IntVar(value=10))
        self.nreaction_entry.grid(row=4,column=2)

        for widget in self.reaction_frame.winfo_children():
           widget.grid_configure(padx=5,pady=5)

        # Creating Dimension Input Frame
        self.dim_frame = LabelFrame(self.frame, text = "Dimensions of Detector")
        self.dim_frame.grid(row=1,column=0,sticky="ew",padx=10,pady=5)

        self.x_dim_label = Label(self.dim_frame, text = "Enter Length (cm)")
        self.x_dim_label.grid(row=0,column=0)
        self.x_dim_entry = Entry(self.dim_frame,textvariable=IntVar(value=100))
        self.x_dim_entry.grid(row=1,column=0)

        self.y_dim_label = Label(self.dim_frame, text = "Enter Radius (cm)")
        self.y_dim_label.grid(row=0,column=1)
        self.y_dim_entry = Entry(self.dim_frame,textvariable=IntVar(value=28))
        self.y_dim_entry.grid(row=1,column=1)

        self.deadzone_label = Label(self.dim_frame, text = "Enter Deadzone (cm)")
        self.deadzone_label.grid(row=0,column=2)
        self.deadzone_entry = Entry(self.dim_frame,textvariable=IntVar(value=3))
        self.deadzone_entry.grid(row=1,column=2)

        self.threshold_label = Label(self.dim_frame, text="Threshold to Detect (cm)")
        self.threshold_label.grid(row=0,column=3)
        self.threshold_entry = Entry(self.dim_frame,textvariable=IntVar(value=6))
        self.threshold_entry.grid(row=1,column=3)

        for widget in self.dim_frame.winfo_children():
            widget.grid_configure(padx=5,pady=5)

        # Create Run Button Frame
        self.button_frame = LabelFrame(self.frame, text = "Control Panel")
        self.button_frame.grid(row=2,column=0,sticky="ew",padx=10,pady=5)

        self.read_button = Button(self.button_frame,text="Read Inputs",command=self.read_input)
        self.read_button.grid(row=0,column=0)

        self.run_button = Button(self.button_frame,text="Run Sim",command=self.run)
        self.run_button.grid(row=0,column=1)
        self.run_button["state"] = "disabled"

        self.info_button = Button(self.button_frame,text="Info",command=self.infoWin)
        self.info_button.grid(row=0,column=2)

        for widget in self.button_frame.winfo_children():
            widget.grid_configure(padx=5,pady=5)

    def on_x(self):
        self.destroy()

    def read_input(self):
        self.KM.xdim = float(self.x_dim_entry.get())
        self.KM.ydim = float(self.y_dim_entry.get())
        self.KM.dead = float(self.deadzone_entry.get())
        self.KM.threshd = float(self.threshold_entry.get()) #  + self.dead
        self.KM.zp = int(self.zbeam_entry.get())
        self.KM.mp = int(self.mbeam_entry.get())
        self.KM.ke  = float(self.beamke_entry.get()) # kinetic energy in MeV/u
        self.KM.ep = self.KM.ke*self.KM.mp # kinetic energy in MeV
        self.KM.zt = int(self.ztarget_entry.get())
        self.KM.mt = int(self.mtarget_entry.get())
        self.KM.et = 0 # target is at rest
        self.KM.zr = int(self.ztargetlike_entry.get())
        self.KM.mr = int(self.mtargetlike_entry.get())
        self.KM.ee = 0
        self.KM.ze = self.KM.zp + self.KM.zt - self.KM.zr # Conservation of Z
        self.KM.me = self.KM.mp + self.KM.mt - self.KM.mr # Conservation of A
        self.KM.er = 0
        self.KM.cm = float(self.comangle_entry.get()) * (np.pi / 180) # in rad
        self.KM.nreactions = int(self.nreaction_entry.get()) * 1000

        if self.KM.threshd >= self.KM.ydim:
            self.errMessage("Value Error", "Detection threshold greater than radius of detector")
            self.toggleRunButton("off")
            return

        self.KM.setKinematics()
#        self.KM.setKinematics(self.mp,self.ep,self.mt,self.et,self.mr,
#                        self.er,self.me,self.ee,self.ke,self.cm,
#                        self.nreactions,self.xdim,self.ydim,
#                        self.dead,self.threshd)
        
        if self.run_button["state"] == "disabled":
            self.toggleRunButton("on")

    def run(self):
        self.toggleRunButton("off")
        t = th.Thread(self.KM.determineDetected())
        t.start()

    def errMessage(self,errtype: str,message: str):
        messagebox.showwarning(title=errtype,message=message)

    def toggleRunButton(self,state):
        """
        options for state:
        "on" or "off"
        """
        if state == "off":
            self.run_button["state"] = "disabled"
        elif state == "on":
            self.run_button["state"] = "active"
        
    def infoWin(self):
        def delete_monitor(self: GUI) -> None:
            self.infoWindow.destroy()
            self.info_button['state'] = 'active'

        self.infoWindow = Toplevel(master=self)
        self.infoWindow.protocol("WM_DELETE_WINDOW",lambda: delete_monitor(self))
        self.infoWindow.iconphoto(False,ImageTk.PhotoImage(file=os.path.join(resource_path,'FRIBlogo.png'),format='png'))
        self.infoWindow.title('What is this?')
        self.infoWindow.resizable(False, False)
        self.info_button['state'] = 'disabled'

        self.infoFrame = Frame(self.infoWindow)
        self.infoFrame.pack()

        self.infoLabelReaction = LabelFrame(self.infoFrame,text="Reaction Frame Info")
        self.infoLabelReaction.grid(row=0,column=0,sticky="ew",padx=10,pady=5)

        self.infoMessageReaction = Message(self.infoLabelReaction,text='''In the reaction frame, you can enter the Mass of the Beam (i.e. the mass of particles in beam), the Mass of the Target, the kinetic energy of the beam particles, the mass of the Beamlike product, the mass of the Targetlike product, the number of reactions to generate and the vertex of the reaction for the second plot''',aspect=700)
        self.infoMessageReaction.grid(column=0,row=0,sticky="ew")

        self.infoLabelDims = LabelFrame(self.infoFrame,text="Dimension Info")
        self.infoLabelDims.grid(row=1,column=0,sticky="ew",padx=10,pady=5)

        self.infoMessageReaction = Message(self.infoLabelDims,text='''In the Dimensions frame, you can enter the Length of the detector (X dimension), the center of mass angle (cm) of the reaction, the deadzone at the center of the detector (for more info, look at the design for the AT-TPC), and the threshold for detection (this is the distance outside of the deadzone required to classify the particle). ''',aspect=700)
        self.infoMessageReaction.grid(column=0,row=0,sticky="ew")

class Kinematics:

    def __init__(self):
        pass

#    def setKinematics(self,mp,ep,mt,et,mr,er,me,ee,ke,cm,nreactions,xdim,ydim,dead,threshd) -> None:
    def setKinematics(self) -> None:
        '''
        Sets Variables for genKinematics
        '''
        # Reading mass excess table
        mexcess = pd.read_csv('Resources/mexcess.csv').to_numpy()

        # The Q value is the difference between the incoming and outgoing masses, expressed in MeV
        amu = 931.5
        mexp = mexcess[self.zp, self.mp-self.zp]
        mext = mexcess[self.zt, self.mt-self.zt]
        mexr = mexcess[self.zr, self.mr-self.zr]
        mexe = mexcess[self.ze, self.me-self.ze]
        self.mp = (self.mp*amu + mexp) / amu # convert mass to amu units
        self.mt = (self.mt*amu + mext) / amu # convert mass to amu units
        self.mr = (self.mr*amu + mexr) / amu # convert mass to amu units
        self.me = (self.me*amu + mexe) / amu # convert mass to amu units
        self.Q = (self.mp + self.mt - self.mr - self.me) * amu # in MeV
#        self.Q = (ep + et) - (er + ee)
#        print(self.Q)
#        self.mp = mp
#        print(self.mp)
#        self.ep = ep
#        print(self.ep)
#        self.mt = mt
#        print(self.mt)
#        self.et = et
#        print(self.et)
#        self.mr = mr
#        print(self.mr)
#        self.er = er
#        print(self.er)
#        self.me = me
#        print(self.me)
#        self.ee = ee
#        print(self.ee)
#        self.ke = ke
#        print(self.ke)
#        self.xdim = xdim
        #print(self.xdim)
#        self.ydim = ydim
        #print(self.ydim)
#        self.dead = dead
        #print(self.dead)
#        self.threshd = threshd
        #print(self.threshd)
#        self.cm = cm
        # print(self.cm)
#        self.nreactions = nreactions
        # print(self.nreactions)
        self.labA1 = self.labAngle()
        self.labE1 = self.labEnergy(self.mr,self.me,self.labA1)/self.mr
        self.labA2 = self.labAngle2()
        self.labE2 = self.labEnergy(self.me,self.mr,self.labA2)/self.me
        print(self.labA1*180/np.pi,self.labE1,self.labA2*180/np.pi,self.labE2)

    def determineDetected(self):
        self.detectedVert = []
        self.cmangle = self.cm*180/np.pi
        for i in range(self.nreactions):
            vz = np.random.uniform(0.01,self.xdim-0.01)
#            y1 = (self.xdim-vz)/np.tan((np.pi/2)-abs(self.labA1))
#            y2 = (self.xdim-vz)/np.tan((np.pi/2)-abs(self.labA2))
            if self.labA1 < np.pi/2:
                y1 = (self.xdim-vz)*np.tan(self.labA1)
            else:
                y1 = vz*np.tan(self.labA1)
            if self.labA2 < np.pi/2:
                y2 = (self.xdim-vz)*np.tan(self.labA2)
            else:
                y2 = vz*np.tan(self.labA2)
            # The conditions for a successful event should be:
            # target-like Y > Deadzone (which means coming out of the dead zone)
            # AND beam-like Y < Threshold (which means entering in the zero degree detector)
#            if vz < 1:
#                print(y1,y2)
            if y1 >= self.dead and y2 <= self.threshd:
                self.detectedVert.append(vz)
#            if y2 >= self.threshd:
#                self.detectedVert.append(vz)
#            elif y1 >= self.threshd:
#                self.detectedVert.append(vz)

        if len(self.detectedVert) <= 0:
            GUI.errMessage("Invalid Reaction","Something went wrong, check reaction info")
            return
        
        self.detection2 = []
        self.detection3 = []
        for i in range(self.nreactions):
            self.cm = np.random.uniform(0,np.pi)
            vz = np.random.uniform(0,self.xdim)
            A1 = self.labAngle()
            A2 = self.labAngle2()
#            y1 = (self.xdim-vz)/np.tan((np.pi/2)-abs(A1))
#            y2 = (self.xdim-vz)/np.tan((np.pi/2)-abs(A2))
            if A1 < np.pi/2:
                y1 = (self.xdim-vz)*np.tan(A1)
            else:
                y1 = vz*np.tan(A1)
            if A2 < np.pi/2:
                y2 = (self.xdim-vz)*np.tan(A2)
            else:
                y2 = vz*np.tan(A2)
            # The conditions for a successful event should be:
            # target-like Y > Deadzone (which means coming out of the dead zone)
            # AND beam-like Y < Threshold (which means entering in the zero degree detector)
            if y1 >= self.dead and y2 <= self.threshd:
                self.detection2.append(self.cm*180/np.pi)
                self.detection3.append(vz)
#            if y2 >= self.threshd:
#                self.detection2.append(cm)
#            elif y1 >= self.threshd:
#                self.detection2.append(cm)

        if len(self.detection2) <= 0:
            GUI.errMessage("Reaction Error","No particles detected")

        GUI.toggleRunButton(state="on")

        p = mp.Process(target=self.createFig)
        p.start()

    def createFig(self):
        fig,ax = plt.subplots(nrows=3,ncols=1)
        ax[0].set_xlabel("Vertex of Reaction")
        ax[0].set_ylabel("Counts")
        ax[0].set_title(f"Number of detections for cm = {self.cmangle}")
        ax[0].set_facecolor('#ADD8E6')
        ax[0].set_axisbelow(True)
        ax[0].yaxis.grid(color='white', linestyle='-')
        ax[0].hist(self.detectedVert,bins=100,range=(0,100))

        ax[1].set_xlabel("CM Angle")
        ax[1].set_ylabel("Counts")
        ax[1].set_title(f"Number of detections with random cm and vz")
        ax[1].set_facecolor('#ADD8E6')
        ax[1].set_axisbelow(True)
        ax[1].yaxis.grid(color='white', linestyle='-')
        ax[1].hist(self.detection2,bins=180, range=(0,180))

        ax[2].set_xlabel("Vertex")
        ax[2].set_ylabel("Counts")
        ax[2].set_title(f"Number of detections with random cm and vz")
        ax[2].set_facecolor('#ADD8E6')
        ax[2].set_axisbelow(True)
        ax[2].yaxis.grid(color='white', linestyle='-')
        ax[2].hist(self.detection3,bins=100, range=(0,100))

        plt.tight_layout()
        plt.savefig(os.path.join(temp_folder,'fig1.jpg'),format="jpg")
        plt.show()
        plt.cla()
        plt.clf()
        plt.close('all')

    def labAngle(self):
        gam = np.sqrt(self.mp*self.mr/self.mt/self.me*self.ep/(self.ep+self.Q*(1+self.mp/self.mt)))
        lab = np.arctan2(np.sin(self.cm),gam-np.cos(self.cm))
        return lab

    def labAngle2(self):
        gam = np.sqrt(self.mp*self.me/self.mt/self.mr*self.ep/(self.ep+self.Q*(1+self.mp/self.mt)))
        lab = np.arctan2(np.sin(self.cm),gam+np.cos(self.cm))
        return lab

    def labEnergy(self,mr,me,th):
        delta = np.sqrt(self.mp*mr*self.ep*np.cos(th)**2 + (me+mr)*(me*self.Q+(me-self.mp)*self.ep))
        if(np.isnan(delta)):
            print("NaN encountered, Invalid Reaction")
        fir = np.sqrt(self.mp*mr*self.ep)*np.cos(th)
        e1 = (fir + delta) / (me+mr)
        e2 = (fir - delta) / (me+mr)
        e1 = e1**2
        e2 = e2**2
        gam = np.sqrt(self.mp*mr/self.mt/me*self.ep/(self.ep+self.Q*(1+self.mp/self.mt)))
        arg = np.sin(self.cm)/(gam-np.cos(self.cm))
        der = 1/(1+arg**2)*(gam*np.cos(self.cm)-1)/(gam-np.cos(self.cm))**2
        if (der < 0):
            return e1
        else:
            return e2

if __name__ == '__main__':
    GUI = Window()
    GUI.mainloop()