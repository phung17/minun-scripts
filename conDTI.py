#!/usr/bin/env python
import os, sys
import shutil
from glob import glob
from optparse import OptionParser


class DWI2DTIMasked:
    def __init__(self, args):
        self.options = options
        self.args = args
        self.force = False
        self.nomask = False

    def startProc(self):

        os.chdir(args[0])
        global keep, dire, search, force, nomask, otsu
        force = self.options.force
        keep = self.options.keep
        nomask = self.options.nomask
        otsu = self.options.otsu
        if not nomask:
            print ("\nConverting DWI to DTI with Otsu threshold at " + otsu + " on: " + args[0])
        else:
            print ("\nConverting DWI to DTI on: " + args[0])
        #print (options.keep)
        dire = str(self.options.dire)
        search = self.options.search
        if not options.dire:
            prog.searchProc()
        else:
            prog.dirProc()


    def searchProc(self):
        dirs = glob(search)
        if dirs == []:
            print ("\nCannot find any subject folders using *" + str(search) + "* search string. \nPlease try again.\n")
            sys.exit(2)
        else:
            print ("\nFound: " + str(dirs) + " subject folders")
            for dti in dirs:
                os.chdir(dti)
                if os.path.isdir("nifti") and not os.path.isfile("doneDTI_Calc.tmp") or os.path.isdir("nifti") and force:
                    os.chdir("nifti")
                    print ("\n-------------------------------------------------------------------------------")
                    print ("\nProcessing: " + os.getcwd())
                    #os.system("EstimateDTI-masked.sh")
                    prog.EstimateDTImasked()
                    if keep == True:

                        print ("\nProcessing complete for: " + str(dti))
                        print ("\n[" + str(os.getcwd()) +"/DTIGen] contains .tmp files.")
                    else:
                        os.chdir("DTIGen")
                        tmpfiles = glob("*.*")
                        for tmp in tmpfiles:
                            os.remove(tmp)
                        os.chdir("..")
                        os.rmdir("DTIGen")
                        print ("\nDTIGen temporary folder removed, processing complete for: " + str(dti))


                    os.chdir("..")
                    os.system("> doneDTI_Calc.tmp")
                else:
                    print ("\n-------------------------------------------------------------------------------")
                    if os.path.isfile("doneDTI_Calc.tmp"):
                        print ("\nDWI to DTI conversion is already completed for " + str(dti) + ", moving on")
                    elif not os.path.isdir("nifti"):
                        print ("\nnifti folder for " + str(dti) + " does not exist")

                os.chdir("..")
            print("\n")

            os.chdir("..")

    def dirProc(self):
        if not os.path.isdir(dire):
            print ("\nDirectory: " + str(args[0]) + str(dire) + " does not exist. Please read usage below. " + "\n")
            parser.print_help()
            print ("\n")
            sys.exit(2)
        else:
            os.chdir(dire)
            if os.path.isdir("nifti") and not os.path.isfile("doneDTI_Calc.tmp") or os.path.isdir("nifti") and force:
                os.chdir("nifti")
                print ("\n-------------------------------------------------------------------------------")
                print ("\nProcessing: " + os.getcwd())
                #os.system("EstimateDTI-masked.sh")
                prog.EstimateDTImasked()
                if keep == True:
                    print ("\nProcessing complete for: " + str(dire))
                    print ("\n[" + str(os.getcwd()) +"/DTIGen] contains .tmp files.\n")
                else:
                    os.chdir("DTIGen")
                    tmpfiles = glob("*.*")
                    for tmp in tmpfiles:
                        os.remove(tmp)
                    os.chdir("..")
                    os.rmdir("DTIGen")
                    print ("\nDTIGen temporary folder removed, processing complete for: " + str(dire) + "\n")

                os.chdir("..")
                os.system("> doneDTI_Calc.tmp")
            else:
                print ("\n-------------------------------------------------------------------------------")
                if os.path.isfile("doneDTI_Calc.tmp"):
                    print ("\nDWI to DTI conversion is already completed. Program will now exit.\n")
                elif not os.path.isdir("nifti"):
                    print ("\nnifti folder does not exist\n")
                sys.exit(2)
            os.chdir("..")

    def EstimateDTImasked(self):
        if not nomask:
            print ("\nMaking temporary folder for DWI Masking and DTI Estimation [Folder = DTIGen]")
        else:
            print ("\nMaking temporary folder for DTI Estimation [Folder = DTIGen]")
        if not os.path.isdir("DTIGen"):
            os.mkdir("DTIGen")
        os.system("cp DWI_CORRECTED.* DTIGen")
        os.chdir("DTIGen")
        if not nomask:
            print ("\nStart Slicer 4.3.1 DiffusionWeightedVolumeMasking")
            os.system("Slicer --launch DiffusionWeightedVolumeMasking --echo --removeislands -o " + otsu + " DWI_CORRECTED.nhdr baseline.nrrd mask.nrrd")
            print ("\nStart Slicer 4.3.1 DWIToDTIEstimation")
            os.system("Slicer --launch DWIToDTIEstimation --echo --shiftNeg -e LS -m mask.nrrd DWI_CORRECTED.nhdr DTI.nhdr DTI-baseline.nrrd")
            print ("\nCopying masked and estimated DTI.nhdr")
        else:
            print ("\nStart Slicer 4.3.1 DWIToDTIEstimation")
            os.system("Slicer --launch DWIToDTIEstimation --echo --shiftNeg -e LS DWI_CORRECTED.nhdr DTI.nhdr DTI-baseline.nrrd")
            print ("\nCopying estimated DTI.nhdr")
        os.system("cp DTI.nhdr ../")
        os.system("cp DTI.raw.gz ../")
        os.chdir("..")

if __name__ == '__main__':
    parser = OptionParser(usage="%prog [options] <project directory>")
    parser.add_option("-s", "--search", dest="search", default='*DTI*', help="Subdirectory names to search for nifti under. Remember to include wildcard characters!\nDefault: *DTI*")
    parser.add_option("-d", "--dti_dir", dest="dire", help="Only process this subdirectory, ignore -s option")
    parser.add_option("-f", "--force", action="store_true", dest="force", help="Force run even if already done running on this subject")
    parser.add_option("-k", "--keep", action="store_true", dest="keep", help="Keep .tmp files after conversion. Default: False")
    parser.add_option("-n", "--nomask", action="store_true", dest="nomask", help="Do not perform Otsu threshold masking. Default: False")
    parser.add_option("-o", "--otsu_thres", dest="otsu", default="0.5", help="Set the Otsu threshold, Default: 0.5")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print ("\nThis script is dependent on Slicer root folder being set in $PATH")
        parser.print_help()
        sys.exit(2)
    else:
        prog = DWI2DTIMasked(args)
        prog.startProc()
