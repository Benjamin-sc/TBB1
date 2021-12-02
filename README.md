# TBB1
3D mapping of the Thickness by Bi1+

In ToF-SIMS analysis, it has been shown that the substrate signal (Si+ in our case) is exponentially dependent of the material thickness over the substrate [1]. Therefore, to effectively measure the thickness on of thin films, an image of the substrate signal Si+ can be obtained using Bi1 + primary ions (Fig. 1A). Using a calibration (Fig. 1B) conducted the molecule reference samples of known thickness (ellipsometry or other technique), these Si+ ion images can transformed in 3D maps of the deposited thickness. The example shown figure 1 illustrates the 3D map thickness of a lysozyme layer on silicon.

Since the construction of these 3D maps from Si+ ion images is not straightforward and involves several parameters and data processing, 2 platforms were developped. These platforms that were developed (Thickness By Bi1) allow to load the analysis images, perform smoothing, calibration, normalization and manage the thickness mapping in a user friendly way. Two verion are available. One is in python (pyTBB1) and the other one in MATLAB (AppTBB1).

![image](https://user-images.githubusercontent.com/80101412/144432057-2af652da-ca4e-40cb-b0a9-ac99995c13d0.png)

[1] A. Delcorte et al., Surf. Sci., vol. 366, no. 1, pp. 149–165, 1996.

Download and use the pyTBB1.

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

*Loading and smoothing*
First you load the images (they will appear below). You load the Si+ ion image and you can also load the total intensity image. The latter will be used to normalize in order to be independant of the Bi1 current. Then you can smooth the 3D plot that and the result will be shown. 
*Calculator*
Then you enter several analysis parameters (there is an interogation button to have explanation about these parameters). After you have to click on conversion button.
Subsequently you select a molecule in the library or you enter new coefficients of the calibration (exponetial expression, Counts = a.exp(-b.Thickness))
If you do a mistake or forget something an error message will guide you.
*Plot*
You can plot the final 3D map here. You can decide if you want to apply the calibration and the normalization (with the checkboxes). You can also choose the colormap of the final plot.

![image](https://user-images.githubusercontent.com/80101412/144440495-c021b3cc-ab5b-4755-99c9-6608d77dcf3d.png)


Download and use the AppTBB1.

Presteps before use it:
    
1) First download all the files. "calibration library.xlsx" are my calibration datas. You may uptdate this file to use your own calibration.

2) The platform open directly. You have to change the folder path and use the path were you images are. If you want to edit the application. Enter >> appdesigner in the command and open the file AppTBB1.mlapp in the application designer.



![image](https://user-images.githubusercontent.com/80101412/144444346-e9ac1bb3-9d77-4a24-9ac1-dc3fc5444c8f.png)

