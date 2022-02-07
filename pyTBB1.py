# -*- coding: utf-8 -*-
"""
Application to construct 3D maps of the thickness of film on silicon.

Presteps before use it:
    
    1) Download also TBB1.png and icon.ico and put them in the same file as the python script. 
    These are the logo and the illustrative image of the concept.
    
    2) Redifine you file_path  in the function pushLoadImage1 and pushLoadImage2.
    So that when you load your images, the right folder place is opened.
    
    3) Ensure to have all the python libraries needed. Otherwise you need to install them.
    For example scipy is not available directly in all the versions.
    
    4) Change the molecular library with your coefficients and molecules (line 295 to 305).
    If you are not familiar with trees construction in python, you can enter new coefficients directly in the GUI.
    
    5) If you are facing problems to load images try to use the more adapted format: .png
    
If you do a wrong operation a message will pop up and guide you in the GUI. Enjoy!

@author: Benjamin Tomasetti (2020-2021)
"""


# Import stuff for computations and plotting
import numpy as np
import PIL.Image  
from PIL import ImageTk, Image                                                              # Avoid namespace issues
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.signal

# Import some tkinter things for GUI stuff
import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from tkinter import Button, Entry, Label, Checkbutton, Scale, Spinbox, LabelFrame
from tkinter import Frame, CENTER, END, LEFT, W
from tkinter import filedialog
from tkinter import messagebox


# Define the GUI class
class GUI_PyTBB1:
    def __init__(self, parent):
        self.myParent = parent
        self.containerLoad    = LabelFrame(parent,text = "Loading and smooting", bg="white", fg="red", font='25')            # Create LOAD container
        self.containerCompute = LabelFrame(parent, text = "Calculator", bg="white", fg="red", font='25')                     # Create COMPUTE container
        self.containerPlot    = LabelFrame(parent,text = "Plot", bg="white", fg="red", font='25')                            # Create PLOT container

        # Place containers
        self.containerLoad.place(relwidth=0.42,relheight=0.85, relx=0.02, rely=0.1)                                          # Place the LOAD container
        self.containerCompute.place(relwidth=0.3,relheight=0.85, relx=0.46, rely=0.1)                                        # Place the COMPUTE container
        self.containerPlot.place(relwidth=0.2,relheight=0.85, relx=0.78, rely=0.1)                                           # Place the PLOT container
        
        # Frames in load container
        
        self.frame1 = LabelFrame(self.containerLoad,text = "", bg="white", fg="black", font='15')
        self.frame2 = LabelFrame(self.containerLoad,text = "Si image loaded", bg="white", fg="black", font='15')
        self.frame3 = LabelFrame(self.containerLoad,text = "Total image loaded", bg="white", fg="black", font='15')
        
        # Place Frames in load container
        self.frame1.place(relwidth=0.95,relheight=0.3, relx=0.02, rely=0.05)
        self.frame2.place(relwidth=0.46,relheight=0.55, relx=0.02, rely=0.4)
        self.frame3.place(relwidth=0.46,relheight=0.55, relx=0.5, rely=0.4)
        
        # Frames in plot container
        
        self.plotframe1 = LabelFrame(self.containerPlot,text = "", bg="white", fg="black", font='15')
        
        # Place Frames in plot container
        self.plotframe1.place(relwidth=0.90,relheight=0.55, relx=0.05, rely=0.3)

        # Instance variables
        self.I1                = None                                           # Image 1
        self.I1Orig            = None                                           # Original Image 1
        self.I1_ar             = None                                           # Image 1 in array format
        self.I2_ar_sm          = None                                           # Image 1 in array format and smoothed
        self.I1_ar_con         = None                                           # Image 1 in array format converted in intensity and µm
        self.I2                = None                                           # Image 2
        self.I2Orig            = None                                           # Original Image 2
        self.I2_ar             = None                                           # Image 2 in array format
        self.I2_ar_con         = None                                           # Image 2 in array format converted with factor counts/pixel
        self.chksmooth         = tk.IntVar()                                    # Checkbox for smoothing
        self.chkcalibration    = tk.IntVar()                                    # Checkbox for calibration
        self.chknormalization  = tk.IntVar()                                    # Checkbox for normalization
        self.chknewcoefficient = tk.IntVar()                                    # Checkbox if the user wants new calibration coefficients
        self.chklibrarycoefficient = tk.IntVar()                                # Checkbox if the user wants to use librery coefficients
        self.X                 = None                                           # X axis for surface plots (in pixels)
        self.Y                 = None                                           # Y axis for surface plots (in pixels)
        self.X_con             = None                                           # X axis for surface plots converted in mm
        self.Y_con             = None                                           # Y axis for surface plots converted in mm
        self.a                 = None
        self.b                 = None
        self.a_norm            = None
        self.b_norm            = None
        self.TBB1              = None
        
        
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # --------------------------- W I D G E T S ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # // == // ============= \\ == \\
        # // == // == L O A D == \\ == \\
        # // == // ============= \\ == \\
        
        # ===== Button: Load Image 1 =====
        self.buttonLoadImage1 = Button(self.frame1)
        self.buttonLoadImage1.configure(text="Load Si image",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.pushLoadImage1)
        # ===== Static Text: Image 1 Filename =====
        self.textImage1File = Entry(self.frame1)
        self.textImage1File.configure(bg = "White", fg = "Black", width = 65)
        
        # ===== Button: Load Image 2 =====
        self.buttonLoadImage2 = Button(self.frame1)
        self.buttonLoadImage2.configure(text="Load total ions image",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.pushLoadImage2)
        # ===== Static Text: Image 2 Filename =====
        self.textImage2File = Entry(self.frame1)
        self.textImage2File.configure(bg = "White", fg = "Black", width = 65)
        
        # ===== Slider: for image smoothing =====
        self.checksmooth = Checkbutton(self.frame1)
        self.checksmooth.configure(text = "Smooth image",
                                       variable = self.chksmooth)
        self.slider = Scale(self.frame1, from_=3, to=100,  length=500,tickinterval=15, orient=tk.HORIZONTAL)
        self.buttonSmoothing= Button(self.frame1)
        self.buttonSmoothing.configure(text="Smooth and plot image",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.plotsmoothed)
        
        # ====== Information button for the smoothing ===========
        self.buttonLoadQuestion= Button(self.frame1, width= 3)
        self.buttonLoadQuestion.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.LoadQuestion)
        
        
        # Show the Si image loaded in a separeted frame
        self.labelImage1= Label(self.frame2)
        # Show the total image loaded in a separeted frame
        self.labelImage2= Label(self.frame3)
        
        
        # // == // =================== \\ == \\
        # // == // == C O M P U T E == \\ == \\
        # // == // =================== \\ == \\
        
        # ===== free space =====
        self.labelSpace= Label(self.containerCompute,text="",bg = "white", fg="white")
        
        self.spinboxXsize = Spinbox(self.containerCompute)
        self.spinboxYsize = Spinbox(self.containerCompute)
        self.spinboxCountsPixelFactor1 = Spinbox(self.containerCompute)
        self.spinboxCountsPixelFactor2 = Spinbox(self.containerCompute)
        self.LabelXsize= Label(self.containerCompute)
        self.LabelXsize.configure(text="X size (mm)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.LabelYsize= Label(self.containerCompute)
        self.LabelYsize.configure(text="Y size (mm)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.LabelCountsPixelFactor1= Label(self.containerCompute)
        self.LabelCountsPixelFactor1.configure(text="Counts/pixels factor \n (Si image)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.LabelCountsPixelFactor2= Label(self.containerCompute)
        self.LabelCountsPixelFactor2.configure(text="Counts/pixels factor \n (Total image)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.EditPixelRasterFactor = Entry(self.containerCompute, width= 15)
        self.EditPixelRasterFactor.insert(END, 16834)
        self.LabelPixelRasterFactor= Label(self.containerCompute)
        self.LabelPixelRasterFactor.configure(text="Pixel/raster factor",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.buttonConversion= Button(self.containerCompute)
        self.buttonConversion.configure(text="Conversion",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.PixelToCount)
        
         # ===== Insert coefficient for a molecule not in the tree =====
        self.checknewcoefficient = Checkbutton(self.containerCompute)
        self.checknewcoefficient.configure(text = "Use new coefficients     ",
                                       variable = self.chknewcoefficient)

        self.Labela= Label(self.containerCompute)
        self.Labela.configure(text="a",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.spinboxa = Spinbox(self.containerCompute)
        self.spinboxa.insert(END, 1)
        self.Labelanorm= Label(self.containerCompute)
        self.Labelanorm.configure(text="a (norm.)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.spinboxanorm = Spinbox(self.containerCompute)
        self.spinboxanorm.insert(END, 1)
        self.Labelb= Label(self.containerCompute)
        self.Labelb.configure(text="b",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.spinboxb = Spinbox(self.containerCompute)
        self.spinboxb.insert(END, 1)
        self.Labelbnorm= Label(self.containerCompute)
        self.Labelbnorm.configure(text="b (norm.)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.spinboxbnorm = Spinbox(self.containerCompute)
        self.spinboxbnorm.insert(END, 1)
        
        self.labelSpace2= Label(self.containerCompute,text="",bg = "white", fg="white")
        self.Labellibrary= Label(self.containerCompute)
        self.Labellibrary.configure(text="Use library coefficients",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        
        
        # Button to ask information about the values to enter
        self.buttonComputeQuestion1= Button(self.containerCompute, width= 3)
        self.buttonComputeQuestion1.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.ComputeQuestion1)
        self.buttonComputeQuestion2= Button(self.containerCompute, width= 3)
        self.buttonComputeQuestion2.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.ComputeQuestion2)
        self.buttonComputeQuestion3= Button(self.containerCompute, width= 3)
        self.buttonComputeQuestion3.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.ComputeQuestion3)
        self.buttonComputeQuestion4= Button(self.containerCompute, width= 3)
        self.buttonComputeQuestion4.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.ComputeQuestion4)
        self.buttonComputeQuestion5= Button(self.containerCompute, width= 3)
        self.buttonComputeQuestion5.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.ComputeQuestion5)
        self.buttonComputeQuestion6= Button(self.containerCompute, width= 3)
        self.buttonComputeQuestion6.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.ComputeQuestion6)
        
        
        
        
        
        
         # ===== The tree for molecule library =====
        self.tree = ttk.Treeview(self.containerCompute)
        # Define columns of the tree
        self.tree['columns'] = ("a", "b","a (norm.)","b (norm.)")
        # Formate my colums
        self.tree.column("#0", width=120, minwidth=25)
        self.tree.column("a", anchor=CENTER, width=35)
        self.tree.column("b", anchor=CENTER, width=35)
        self.tree.column("a (norm.)", anchor=CENTER, width=45)
        self.tree.column("b (norm.)", anchor=CENTER, width=45)
        #create Headings
        self.tree.heading("#0", text= "Molecules library", anchor= W)
        self.tree.heading("a", text= "a", anchor= CENTER)
        self.tree.heading("b", text= "b", anchor= CENTER)
        self.tree.heading("a (norm.)", text= "a (norm.)", anchor= CENTER)
        self.tree.heading("b (norm.)", text= "b (norm.)", anchor= CENTER)
        # add data in the tree
        self.tree.insert(parent='', index='end', iid=0, text="Proteins", values=("", "","", ""))
        self.tree.insert(parent='', index='end', iid=1, text="Polymers", values=("", "","", ""))
        self.tree.insert(parent='', index='end', iid=2, text="Lipids", values=( "", "","", ""))
        #add child
        self.tree.insert(parent='', index='end', iid=3, text="Lysozyme", values=(2000000.0, -0.998, 0.1373, -0.999))
        self.tree.move('3', '0', '0')
        self.tree.insert(parent='', index='end', iid=4, text="Bradykinin", values=(1, 2, 1, 2))
        self.tree.move('4', '0', '0')
        self.tree.insert(parent='', index='end', iid=5, text="Irganox", values=(1, 2, 1, 2))
        self.tree.move('5', '1', '0')
        # handle the selection of the item in the tree
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
            
        
        
        
        
        # // == // =================== \\ == \\
        # // == // ==    P L O T    == \\ == \\
        # // == // =================== \\ == \\
        
        self.checkcalibration = Checkbutton(self.containerPlot)
        self.checkcalibration.configure(text = "Apply calibration      ",
                                       variable = self.chkcalibration)
        self.checknormalization = Checkbutton(self.containerPlot)
        self.checknormalization.configure(text = "Apply normalization",
                                       variable = self.chknormalization)
        self.buttonPlot= Button(self.containerPlot)
        self.buttonPlot.configure(text="Plot",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Plot)
        
        self.popColormap = ttk.Combobox(self.containerPlot,
                                        values = ["plasma",
                                                  "jet",
                                                  "bone",
                                                  "viridis"])
        
        # Load illustrative image
        self.labelImage3= Label(self.plotframe1)

        self.TBB1 = PIL.Image.open("TBB1.png")
        
        TBB1 = self.TBB1.resize((310, 305), Image.ANTIALIAS)
        TBB1 = ImageTk.PhotoImage(TBB1)
        self.labelImage3.configure(image=TBB1, justify = CENTER)
        self.labelImage3.image = TBB1

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # ----------------------------- L A Y O U T ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # LOAD (frame1)
        self.buttonLoadImage1.grid(column = 0, row = 2, sticky = "EW")
        self.textImage1File.grid(column = 1, row = 2)
        self.buttonLoadImage2.grid(column = 0, row = 3, sticky = "EW")
        self.textImage2File.grid(column = 1, row = 3)
        self.slider.grid(column = 1, row = 5,rowspan = 2)
        self.buttonLoadQuestion.grid(column = 3, row=5)
        self.buttonSmoothing.grid(column = 0, row = 6, sticky = "EW")
        self.checksmooth.grid(column = 0, row = 5, sticky = "EW")
        # LOAD (frame2)
        self.labelImage1.grid(column = 0, row = 0, sticky = "NESW")
        # LOAD (frame3)
        self.labelImage2.grid(column = 0, row = 0, sticky = "NESW")
        # COMPUTE
        self.spinboxXsize.grid(column = 1, row = 1)
        self.spinboxYsize.grid(column = 1, row = 2)
        self.spinboxCountsPixelFactor1.grid(column = 1, row = 3, padx = 5)
        self.spinboxCountsPixelFactor2.grid(column = 1, row = 4)
        self.LabelXsize.grid(column = 0, row = 1, sticky = "EW")
        self.LabelYsize.grid(column = 0, row = 2, sticky = "EW")
        self.LabelCountsPixelFactor1.grid(column = 0, row = 3, sticky = "EW")
        self.LabelCountsPixelFactor2.grid(column = 0, row = 4, sticky = "EW")
        self.LabelPixelRasterFactor.grid(column = 0, row = 5, sticky = "EW")
        self.EditPixelRasterFactor.grid(column = 1, row = 5)
        self.buttonComputeQuestion1.grid(column = 2, row=1)
        self.buttonComputeQuestion2.grid(column = 2, row=2)
        self.buttonComputeQuestion3.grid(column = 2, row=3)
        self.buttonComputeQuestion4.grid(column = 2, row=4)
        self.buttonComputeQuestion5.grid(column = 2, row=5)
        self.buttonComputeQuestion6.grid(column = 1, row=7,sticky="W")
        self.buttonConversion.grid(column = 3, row=1, rowspan = 5, sticky = "NESW")
        self.labelSpace.grid(column = 0, row = 6, sticky = "EW")
        self.checknewcoefficient.grid(column = 0, row = 7, sticky = "EW")
        self.Labela.grid(column = 0, row = 8, sticky = "EW")
        self.Labelanorm.grid(column = 0, row = 9, sticky = "EW")
        self.Labelb.grid(column = 0, row = 10, sticky = "EW")
        self.Labelbnorm.grid(column = 0, row = 11, sticky = "EW")
        self.Labellibrary.grid(column = 0, row = 13, sticky = "EW")
        self.spinboxa.grid(column = 1, row = 8)
        self.spinboxanorm.grid(column = 1, row = 9)
        self.spinboxb.grid(column = 1, row = 10)
        self.spinboxbnorm.grid(column = 1, row = 11)
        self.labelSpace2.grid(column = 0, row = 12, sticky = "EW")
        self.tree.grid(column = 0, row = 14, columnspan = 3, sticky = "EW")
        # PLOT
        self.checkcalibration.grid(column = 0, row = 1, sticky = "EW")
        self.checknormalization.grid(column = 0, row = 2, sticky = "EW")
        self.buttonPlot.grid(column = 1, row=1, rowspan = 2, sticky = "NESW")
        self.popColormap.grid(column = 1, row=3, sticky = "NESW")
        self.popColormap.current(0)
        self.labelImage3.grid(column = 0, row = 4,columnspan = 2, sticky = "NESW")
        
        
        
    # ===== Method: Load Image 1 =====
    # ================================

    def pushLoadImage1(self):
        
        file_path = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/Documents/measurements/SIMS/3D plot (carpet)",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.jpg;*.png;*.bmp"),
                                                    ("JPG Files", "*.jpg"),
                                                    ("PNG Files", "*.png"),
                                                    ("BMP Files", "*.bmp")))
#        file_path = filedialog.askopenfilename(initialdir = "C:/Users/Josh/Documents/YouTube_Files/DIY_BOS/",
#                                               title = "Select Image 1",
#                                               filetypes = (("All Files", "*.jpg;*.png;*.tif;*.tiff;*.bmp"),
#                                                            ("JPG Files", "*.jpg"),
#                                                            ("PNG Files", "*.png"),
#                                                            ("TIF Files", "*.tif;*.tiff"),
#                                                            ("BMP Files", "*.bmp")))
        
        
        self.I1 = PIL.Image.open(file_path)                                     # Open the image
        self.textImage1File.delete(0,END)                                       # Delete any strings in text box for file name
        self.textImage1File.insert(0,file_path)                                 # Add file name to the text box
        self.I1Orig = self.I1                                                   # Save original image for plotting
        self.I1 = self.I1.convert("L")                                          # Convert image to 8-bit black and white (L)
        self.I1_ar = np.transpose(np.array(self.I1))                            # Convert image to array
        
        
        #show the image in the frame2
        image1 = self.I1Orig.resize((250, 250), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)
        self.labelImage1.configure(image=image1, justify = CENTER)
        self.labelImage1.image = image1
        
        
        # create meshgrid for the surface plot
        self.X = np.arange(0, np.size(self.I1_ar, 1), 1)
        self.Y = np.arange(0, np.size(self.I1_ar, 0), 1)
        self.X, self.Y = np.meshgrid(self.X, self.Y)

        # Make a surface plot of the first image
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(self.X, self.Y, self.I1_ar, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)
        
        plt.title('Si image intensity')
        ax.set_xlabel('pixels')
        ax.set_ylabel('pixels')
        ax.set_zlabel('pixel intensity')

        plt.show()
        
    # ===== Method: Load Image 2 =====
    # ================================

    def pushLoadImage2(self):
        
        file_path = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/Documents/measurements/SIMS/3D plot (carpet)",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.jpg;*.png;*.bmp"),
                                                    ("JPG Files", "*.jpg"),
                                                    ("PNG Files", "*.png"),
                                                    ("BMP Files", "*.bmp")))
#        file_path = filedialog.askopenfilename(initialdir = "C:/Users/Josh/Documents/YouTube_Files/DIY_BOS/",
#                                               title = "Select Image 1",
#                                               filetypes = (("All Files", "*.jpg;*.png;*.tif;*.tiff;*.bmp"),
#                                                            ("JPG Files", "*.jpg"),
#                                                            ("PNG Files", "*.png"),
#                                                            ("TIF Files", "*.tif;*.tiff"),
#                                                            ("BMP Files", "*.bmp")))
        
        
        self.I2 = PIL.Image.open(file_path)                                     # Open the image
        self.textImage2File.delete(0,END)                                       # Delete any strings in text box for file name
        self.textImage2File.insert(0,file_path)                                 # Add file name to the text box
        self.I2Orig = self.I2                                                   # Save original image for plotting
        self.I2 = self.I2.convert("L")                                          # Convert image to 8-bit black and white (L)
        self.I2_ar = np.transpose(np.array(self.I2))                            # Convert image into array
        
        #show the image in the frame3
        image2 = self.I2Orig.resize((250, 250), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image2)
        self.labelImage2.configure(image=image2, justify = CENTER)
        self.labelImage2.image = image2
        
    # ===== Method: smoothing =====
    # ================================
            
    def plotsmoothed(self):
        
        if (self.chksmooth.get()):
            
            Kernel_size = self.slider.get()                                                  # accessing the slider value
            kernel = np.ones((Kernel_size,Kernel_size),np.float32)/(Kernel_size**2)
            # convolve 2d the kernel with each channel
            self.I1_ar_sm = scipy.signal.convolve2d(self.I1_ar/255, kernel, mode='same')
            self.I1_ar_sm = self.I1_ar_sm*255
            # Make a surface plot of the smooted datas
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            surf = ax.plot_surface(self.X, self.Y, self.I1_ar_sm, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

            # Add a color bar which maps values to colors.
            fig.colorbar(surf, shrink=0.5, aspect=5)
        
            plt.title('Si image smoothed intensity')
            ax.set_xlabel('pixels')
            ax.set_ylabel('pixels')
            ax.set_zlabel('pixel intensity')

            plt.show()
            
        elif self.chksmooth.get()==0:
            
           messagebox.showinfo ("warning","Allow the checkbox for smoothing before")
                
                

    # ===== Method: convert image =====
    # ================================
        
    def PixelToCount(self):
        
        if self.I1_ar is None:
            messagebox.showinfo ("warning","Before, you need to load the Si image")
        elif self.I2_ar is None:
            messagebox.showinfo ("warning","Before, you need to load the total image")
        else:
            if (self.chksmooth.get()):
                Data = self.I1_ar_sm
            elif self.chksmooth.get()==0:
                Data = self.I1_ar
        
            try:
                Xsize = float(self.spinboxXsize.get())
                Ysize = float(self.spinboxYsize.get())
                CountsPixelFactor1 = float(self.spinboxCountsPixelFactor1.get())
                CountsPixelFactor2 = float(self.spinboxCountsPixelFactor2.get())
                PixelsRasterFactor = float(self.EditPixelRasterFactor.get())
            except:
                messagebox.showinfo ("warning","Please check if your factors are numbers")
                
            self.X_con = np.linspace(0,Xsize,num=np.size(self.I1_ar, 1))            # create x axis in mm (conversion from pixel)
            self.Y_con = np.linspace(0,Ysize,num=np.size(self.I1_ar, 0))            # create y axis in mm (conversion from pixel)
            self.X_con, self.Y_con = np.meshgrid(self.X_con, self.Y_con)            # create a grid for the surface plot
            self.I1_ar_con = Data*CountsPixelFactor1*PixelsRasterFactor             # Apply the conversion factors to first image
            self.I2_ar_con = self.I2_ar*CountsPixelFactor2*PixelsRasterFactor       # Apply the conversion factors to second image
            self.I2_ar_con=np.where(self.I2_ar_con==0, 1000, self.I2_ar_con)        # Suppress 0 values that causes problem for the normalization
            self.I1_ar_con=np.where(self.I1_ar_con==0, 1, self.I1_ar_con)           # Suppress 0 values that causes problems for log
        
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            surf = ax.plot_surface(self.X_con, self.Y_con, self.I1_ar_con/PixelsRasterFactor, cmap=cm.coolwarm,
                                   linewidth=0, antialiased=False)
        
            plt.title('Si intensity')
            ax.set_xlabel('mm')
            ax.set_ylabel('mm')
            ax.set_zlabel('Counts')

            # Add a color bar which maps values to colors.
            fig.colorbar(surf, shrink=0.5, aspect=5)

            plt.show()

        # ===== Method: molecule selection in the tree =====
        # ==================================================
        
    def item_selected(self,event):

        item = self.tree.selection()[0]
        self.a = float(self.tree.item(item)['values'][0])
        self.b = float(self.tree.item(item)['values'][1])
        self.a_norm = float(self.tree.item(item)['values'][2])
        self.b_norm = float(self.tree.item(item)['values'][3])

        # ==== Method: Plot graph =====
        # =============================
        
    def Plot(self):
        
        
        # If the user want to enter the coefficients, the latter are redefined
        if self.chknewcoefficient.get()==1:
            try:
                self.a = float(self.spinboxa.get())
                self.b = float(self.spinboxb.get())
                self.a_norm = float(self.spinboxanorm.get())
                self.b_norm = float(self.spinboxbnorm.get())
            except: 
                messagebox.showinfo ("warning","Please check if your coefficients are numbers")

    
        # check if the datas were correctly selected
        if self.I1_ar is None:
            messagebox.showinfo ("warning","Before, you need to load the Si image")
        elif self.I1_ar_con is None:
            messagebox.showinfo ("warning","Before, you need to convert pixels in mm and counts")
        elif (self.a is None and self.b is None and self.a_norm is None and self.b_norm is None):
            messagebox.showinfo ("warning","Before, select a molecule in the library or enter new coefficients")
            
        else:
            if (self.chkcalibration.get()):                                         # If the user wants to apply calibration
                if (self.chknormalization.get()):                                   # Calibration and normalization
                
                    #self.I2_ar_con[self.I2_ar_con <= 0] = 0.0000001
                    I1_ar_con_norm = self.I1_ar_con/self.I2_ar_con
                    I1_ar_con_norm_cal = np.log(I1_ar_con_norm/self.a_norm)/self.b_norm
                
                    # Make a surface plot
                    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
                    surf1 = ax.plot_surface(self.X_con, self.Y_con, I1_ar_con_norm_cal, cmap = self.popColormap.get()
                                        , linewidth=0, antialiased=False)

                    # Add a color bar which maps values to colors.
                
                    fig.colorbar(surf1, shrink=0.5, aspect=5)
        
                    plt.title('Thickness (normalized)')
                    ax.set_xlabel('mm')
                    ax.set_ylabel('mm')
                    ax.set_zlabel('nm')
                    plt.show()
                
                else:
                    I1_ar_con_cal = np.log(self.I1_ar_con/self.a)/self.b
                
                    # Make a surface plot
                    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
                    surf = ax.plot_surface(self.X_con, self.Y_con, I1_ar_con_cal, cmap=self.popColormap.get(),
                                           linewidth=0, antialiased=False)

                    # Add a color bar which maps values to colors.
                    fig.colorbar(surf, shrink=0.5, aspect=5)
        
                    plt.title('Thickness')
                    ax.set_xlabel('mm')
                    ax.set_ylabel('mm')
                    ax.set_zlabel('nm')
                    plt.show()
                    
            elif self.chkcalibration.get()==0:
                if (self.chknormalization.get()):
                
                    I1_ar_con_norm = self.I1_ar_con/self.I2_ar_con
                
                    # Make a surface plot
                    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
                    surf = ax.plot_surface(self.X_con, self.Y_con, I1_ar_con_norm, cmap=self.popColormap.get(),
                                           linewidth=0, antialiased=False)

                    # Add a color bar which maps values to colors.
                    fig.colorbar(surf, shrink=0.5, aspect=5)
        
                    plt.title('Si intensity (normalyzed)')
                    ax.set_xlabel('mm')
                    ax.set_ylabel('mm')
                    ax.set_zlabel('counts')
                    plt.show()
                
                else:
                
                    # Make a surface plot
                    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
                    surf = ax.plot_surface(self.X_con, self.Y_con, self.I1_ar, cmap=self.popColormap.get(),
                                           linewidth=0, antialiased=False)

                    # Add a color bar which maps values to colors.
                    fig.colorbar(surf, shrink=0.5, aspect=5)
        
                    plt.title('Si intensity')
                    ax.set_xlabel('mm')
                    ax.set_ylabel('mm')
                    ax.set_zlabel('counts')
                    plt.show()
              
 

    # ===== Method: Questions =====
    # ================================
    def LoadQuestion(self):
        messagebox.showinfo ("information :","A 2D convolution is used to smooth the image. For that a Kernel filter is used. A kernel filter is a normalized matrix for which the size is determined by the slider (from 3 to 100). \n"
                             "The operation works like this: the kernel matrix goes above a pixel, all the pixels below this kernel ar added (sum of 9 pixels for a matrix 3x3). \n"
                             "Then, the average is computed, and the central pixel is replaced with the new average value. Finally, the kernel matrix moves and this operation is continued for all the pixels in the image. \n")
    def ComputeQuestion1(self):
        messagebox.showinfo ("information :","X size is the length of the image in mm. \n It's used to convert the initial length of the image (in pixel) to mm.")
    def ComputeQuestion2(self):
        messagebox.showinfo ("information :","Y size is the length of the image in mm. \n It's used to convert the initial length of the image (in pixel) to mm.")
    def ComputeQuestion3(self):
        messagebox.showinfo ("information :","This factor is used to convert the pixel intensity of the Si image in counts. \n"
                             "For that, you need to divide the maximun intensity in counts (e.g. Max = 33 counts) by the intensity max of the 8-bit image (e.i. 255).")
    def ComputeQuestion4(self):
        messagebox.showinfo ("information :","This factor is used to convert the pixel intensity of the total image in counts. \n"
                             "For that, you need to divide the maximun intensity in counts (e.g. Max = 8000 counts) by the intensity max of the 8-bit image (e.i. 255).")
    def ComputeQuestion5(self):
        messagebox.showinfo ("information :","This factor is the pixel size of the raster used for the calibration (128x128=16384). \n"
                             "This factor is applied because the calibration was done with raster (therefore with an intensity 16384 times higher. If the calibration is done with pixels intensities this factor should be equal to one.")
    def ComputeQuestion6(self):
        messagebox.showinfo ("information :","a and b are the coefficents of the calibration (Silicon signal in function of the thickness). \n"
                             "Counts = a*exp(-b.Thickness) \n"
                             "If you check the box it means that you use new coefficients and not the ones in the library below.")



root = Tk()
root.wm_title("3D mapping of the sample thickness from ToF-SIMS images (pyTBB1)")                                        # Set window title
root.iconbitmap("icon.ico")                                                     # Set icon bitmap
root.geometry("1800x700")
#root.configure(bg="#263D42")
gui_pyTBB1 = GUI_PyTBB1(root)                                                   # Instantiate the class GUI_BOS
root.mainloop()