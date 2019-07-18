# CADScripts
CADScripts it's a collection of Rhino commands, mostly for drawing, with no specific intent. 

## Commands

 - `Close2Curves`
 - `ConvertCircle2Point`
 - `ConvertPoint2Circle`
 - `DogBoneInCurve`
 - `OffsetAndClose`
 - `Rect2DogBone`
 - `SelArea`
 - `SelLength`
 - `SmashMultiple`
 
 ## Install

 1. [Download Windows Rhino 6 installation file from GitHub.](https://github.com/dfmdmx/Rhino_CADScripts/raw/master/CADScripts.rhi)
 2. Install the plugin and restart Rhino.
 3. Type any command from the list above in the Rhino command bar.

### Rhino 5 and MacOS

Some of the commands might not work properly, as in they have not been tested. Rhino 6 users can also follow this steps without expecting any problems. 

 1. [Download source folder zip file from GitHub.](https://github.com/dfmdmx/Rhino_CADScripts/archive/master.zip)
 2. Open the zip file and extract de `Scripts` folder somewhere safe. 
 3. In the Rhino command console type: `-_RunPythonScript ("\somewhere\safe\Scripts\OffsetAndClose.py")`
 4. Add the previous line into your Rhino command aliases under Tools-Options-Aliases menu to make it work as a normal command. 
 
 
