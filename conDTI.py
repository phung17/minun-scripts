#!/usr/bin/env python
import os, sys
from glob import glob
from optparse import OptionParser


class DWI2DTIMasked:
    def __init__(self, args):
        self.options = options
        self.args = args

    def startProc(self):
        print ("\nConverting DWI to DTI with Otsu Masking on: " + args[0])
        os.chdir(args[0])
        self.subjDir = os.getcwd()
        self.subjName = os.path.basename(os.getcwd())
        global keep, dire, search
        keep = self.options.keep
        print (options.keep)
        dire = str(self.options.dire)
        search = self.options.search
        if not options.dire:
            prog.searchProc()
        else:
            prog.dirProc()


    def searchProc(self):
        dirs = glob("*"+search+"*")
        if dirs == []:
            print ("\nCannot find any subject folders using *" + str(search) + "* search string. \nPlease try again.\n")
            sys.exit(2)
        else:
            print ("\nFound: " + str(dirs) + " subject folders")
            for dti in dirs:
                os.chdir(dti)
                if os.path.isdir("nifti"):
                    os.chdir("nifti")
                    print ("\n-------------------------------------------------------------------------------")
                    print ("\nProcessing: " + os.getcwd())
                    os.system("EstimateDTI-masked.sh")
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
                os.chdir("..")
            os.chdir("..")

    def dirProc(self):
        if not os.path.isdir(dire):
            print ("\nDirectory: " + str(args[0]) + str(dire) + " does not exist. Please read usage below. " + "\n")
            parser.print_help()
            print ("\n")
            sys.exit(2)
        else:
            os.chdir(dire)
            if os.path.isdir("nifti"):
                os.chdir("nifti")
                print ("\n-------------------------------------------------------------------------------")
                print ("\nProcessing: " + os.getcwd())
                os.system("EstimateDTI-masked.sh")
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
            os.chdir("..")

if __name__ == '__main__':
    parser = OptionParser(usage="%prog [options] <subject_dir>")
    parser.add_option("-s", "--search", dest="search", default='DTI', help="Subdirectory names to search for nifti under. Default: DTI")
    parser.add_option("-d", "--dti_dir", dest="dire", help="Only process this subdirectory, ignore -s option.")
    parser.add_option("-k", "--keep", action="store_true", dest="keep", help="Keep .tmp files after conversion. Default: False")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(2)
    else:
        prog = DWI2DTIMasked(args)
        prog.startProc()
