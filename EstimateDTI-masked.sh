#!/bin/bash
echo
echo "Making temporary folder for DWI Masking and DTI Estimation [Folder = DTIGen]"

mkdir DTIGen
cp DWI_CORRECTED.* DTIGen
cd DTIGen

echo
echo "Start Slicer 4.3.1 DiffusionWeightedVolumeMasking"
Slicer --launch DiffusionWeightedVolumeMasking --echo --removeislands DWI_CORRECTED.nhdr baseline.nrrd mask.nrrd
echo
echo "Start Slicer 4.3.1 DWIToDTIEstimation"
Slicer --launch DWIToDTIEstimation --echo --shiftNeg -e LS -m mask.nrrd DWI_CORRECTED.nhdr DTI.nhdr DTI-baseline.nrrd

echo
echo "Copying masked and estimated DTI.nhdr"
cp DTI.nhdr ../
cp DTI.raw.gz ../
#rm *.*
#cd ../
#rmdir DTIGen

#echo "DTIGen folder removed, processing complete."
#echo
