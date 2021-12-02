# TBB1 introduction
3D mapping of the Thickness by Bi1+

In ToF-SIMS analysis, it has been shown that the substrate signal (Si+ in our case) is exponentially dependent of the material thickness over the substrate [1]. Therefore, to effectively measure the thickness of thin films or deposits, an image of the substrate signal Si+ can be obtained using Bi1 + primary ions (Fig. 1B). Using a calibration (Fig. 1A) conducted the molecule reference samples of known thickness (ellipsometry or other technique), these Si+ ion images can transformed in 3D maps of the deposited thickness. The example shown figure 1 illustrates the 3D map thickness of a lysozyme layer on silicon.

Since the construction of these 3D maps from Si+ ion counts images is not straightforward and involves several parameters and data processing, 2 platforms were developped. These platforms (TBB1, Thickness By Bi1) allow to load the analysis images, perform smoothing, calibration, normalization and manage the thickness mapping in a user friendly way. Two verions are available. One is in python (pyTBB1) and the other one in MATLAB (AppTBB1).

Accordingly, the purpose of these platforms is to build 3D thickness map of films from the underneath substrate ion image obtain by ToF-SIMS (Bi1+)

![image](https://user-images.githubusercontent.com/80101412/144455579-04532ae2-d838-4584-901c-ac50b996ffb8.png)
*Fig. 1. Method for the thickness mapping. Thickness calibration curve (lysozyme in this case) (A). Then, the 3D thickness map (c) is plotted using the platforms and Si+ ion images obtained by ToF-SIMS.*

[1] A. Delcorte et al., Surf. Sci., vol. 366, no. 1, pp. 149–165, 1996.

# Download and use the pyTBB1.

Presteps before use it:
    
1) Firslty download all the files. Indeed "TBB1.png" is an illustrative image and "icon.ico" is the icon of the platform. If these files are not in the same folder as the python and MATLAB script, you will have an error message. 
    
2) Redifine you file_path  in the function pushLoadImage1 (line 449) and pushLoadImage2 (line 504). So that when you load your images the right folder place is opened.
    
3) Ensure to have all the python libraries needed. Otherwise you need to install them. For example scipy is not always available directly in all the versions.
    
4) Update the molecular library with your coefficients and molecules (line 330 to 341). If you are not familiar with trees construction in python, you can enter new coefficients directly in the GUI.
    
5) If you are facing problems to load images try to use the more adapted format: .png

Figure 2 shows the python platform. It is constructed in three containers: 
- Loading and smoothing
- Calculator
- Plot


First you load the images (they will appear below). You load the Si+ ion image and you can also load the total intensity image. The latter will be used to normalize in order to be independant of the Bi1 current. Then you can smooth the 3D plot that and the result will be shown. 

Then you enter several analysis parameters (there is an interogation button to have explanation about these parameters). After you have to click on conversion button.
Subsequently you select a molecule in the library or you enter new coefficients of the calibration (exponetial expression, Counts = a.exp(-b.Thickness))
If you do a mistake or forget something an error message will guide you.

Finally, you can plot the final 3D map with the "plot" button. You can decide if you want to apply the calibration and the normalization (with the checkboxes). You can also choose the colormap of the final plot.

![image](https://user-images.githubusercontent.com/80101412/144440495-c021b3cc-ab5b-4755-99c9-6608d77dcf3d.png)
*Fig. 2. pyTBB1 platform.*

# Download and use the AppTBB1.

Presteps before use it:
    
1) First download all the files. "calibration library.xlsx" are my calibration datas. You may uptdate this file to use your own calibration.

2) The platform open directly. You have to change the folder path and use the path were you images are. If you want to edit the application, enter >> appdesigner in the command and open the file AppTBB1.mlapp in the application designer.

Figure 3 shows the MATLAB platform. It is constructed in three containers: 
- Loading and smoothing
- Calculator
- Plot

First you load the Si+ image. The format needs to be in Tiff and you have to write the name of the file (and the file needs to be in the folder path). Then, you can choose to load the entire image or to crop it. The image will appear in the prewiew. You can smooth the image with the slider just below the preview.

Then you enter several analysis parameters (there is an interogation button to have explanation about these parameters). If you want normalize you have to enter the name of the total intensity image and click on "load" button. Subsequently you select a molecule in the library or you enter new coefficients of the calibration (exponetial expression, Counts = a.exp(-b.Thickness)). You can update the molecular library by changing the values in the "function TreeSelectionChanged(app, event)" line 314.
There is also a button "show calibration curve" to plot the calibration of the selected molecule. You can update the related excel folder "calibration library.xlsx" and the "function ShowcalibrationcurveButtonPushed(app, event)" line 343.

Finally, you can plot a preview of the final 3D map with the "3D map preview" button. You can decide if you want to apply the calibration and the normalization (with the checkboxes). After that, you choose the color of the colormap and generate the final 3D map.


![image](https://user-images.githubusercontent.com/80101412/144444346-e9ac1bb3-9d77-4a24-9ac1-dc3fc5444c8f.png)
*Fig. 3. AppTBB1 platform.*
