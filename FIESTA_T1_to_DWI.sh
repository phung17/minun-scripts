for i in */
do
  echo $i
  cd $i
  mkdir nifti/ANTS-quan
  cp FIESTA/FIESTA.nii.gz nifti/ANTS-quan
  cp FSPGR/T1.nii.gz nifti/ANTS-quan
  cd nifti
  Slicer --launch DWIConvert --conversionMode "NrrdToFSL" --inputVolume "DWI_CORRECTED.nhdr" --outputVolume "DWI_CORRECTED.nii.gz" --outputBVectors "DWI_CORRECTED.bvec" --outputBValues "DWI_CORRECTED.bval" --echo
  mv DWI_CORRECTED.nii.gz ANTS-quan
  mv DWI_CORRECTED.bval ANTS-quan
  mv DWI_CORRECTED.bvec ANTS-quan
  cd ANTS-quan
  sh_to_apm.py DWI_CORRECTED.nii.gz -e DWI_CORRECTED.bvec -a DWI_CORRECTED.bval -o AP.nii.gz
  bet T1.nii.gz T1_bet.nii.gz -f 0.2
  echo "Starting antsRegistration"
  echo "-------------------------"
  time antsRegistration -d 3 -o "T1_to_AP_" -t Affine[0.1] -m MI["AP.nii.gz","T1_bet.nii.gz",1,32] --convergence [10000x10000x10000x10000x10000] --shrink-factors 5x4x3x2x1 --smoothing-sigmas 4x3x2x1x0mm -t SyN[0.15,3.0,0.0] -m CC["AP.nii.gz","T1_bet.nii.gz",1,3] --convergence [50x35x15,1e-7] --shrink-factors 3x2x1 --smoothing-sigmas 2x1x0mm  --use-histogram-matching 1
  time antsRegistration -d 3 -o "FIESTA_to_T1_" -t Rigid[0.1] -m CC["T1.nii.gz","FIESTA.nii.gz",1,3] --convergence [10] --shrink-factors 5 --smoothing-sigmas 4mm
  echo "Starting antsApplyTransforms"
  echo "-------------------------"
  antsApplyTransforms -d 3 -i T1.nii.gz -r T1.nii.gz -n BSpline -o ANTS_T1.nii.gz -t T1_to_AP_1Warp.nii.gz -t T1_to_AP_0GenericAffine.mat
  antsApplyTransforms -d 3 -i FIESTA.nii.gz -r FIESTA.nii.gz -n BSpline -o ANTS_FIESTA.nii.gz -t T1_to_AP_1Warp.nii.gz -t T1_to_AP_0GenericAffine.mat -t FIESTA_to_T1_0GenericAffine.mat
  cd ../../..
  echo "###############"
done
