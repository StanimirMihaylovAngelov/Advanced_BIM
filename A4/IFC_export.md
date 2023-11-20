## From Revit to IFC
### Export IFC file from Revit:
1.  In case the model you want to edit is a Revit Autodesk format, then start by opening the model in Revit Autodesk. 
2.  Press the **File** tab, in the top left corner, on Revit’s ribbon. Then choose **Export** &rarr; **IFC**.
3.  A dialog box will appear, asking for the location where the IFC file should be saved. You can either type a directory, or find it by clicking **Browse** and choosing the the folder. 
4.  For **Current selected setup**, select the IFC setup to use to create the file and click **Modify setup**. There are 9 built-in setups. These setups correspond to the IFC version options.
    1. Under Additional Content tab:
           * Export rooms in 2D vies – exports all rooms in the model.
    3.	  Under Peoperty Set tab:
        *   Export Revit Property Set – exports Revit-specific property sets. This box should be ticked.
        *   Export IFC common property set – this box should also be ticked. The other boxes are not relevant for the project at hand, so they need not to be ticked.
    4.	Under Advanced tab:
        *	Use family and type name for reference – neccessery to identify this box should be ticked.
        *	Use 2D room bounderies 
6.	Press Export
