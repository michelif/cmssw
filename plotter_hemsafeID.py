#!/bin/python                                                                                                                                              

import sys
import re
import time
import argparse
import os
import subprocess
import array
import string
import ROOT
import math

from ROOT import std
from optparse import OptionParser

vstring = std.vector(std.string)
vfloat = std.vector(float)

#----function to book histos                                                                                                                               
def bookHistos(histos):
    for idname in "medium","loose","tight","medium_HEMSafe","loose_HEMSafe","tight_HEMSafe":
        name = "phi_"+idname
        histos[name]=ROOT.TH1F(name,name,100,-3.5,3.5)

#----main function
def main():
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
    parser = argparse.ArgumentParser (description = 'Draw plots from ROOT files')
    parser.add_argument("-l", "--label", default='test',metavar='test',type=str,
                      help="outfile label")
    parser.add_argument("-i", "--inputDir", default='/afs/cern.ch/work/m/micheli/vidhemsafe_103/CMSSW_10_3_0_pre6/src/',metavar='inputDir',type=str,
                      help="prefix")

    print "bef parsing"
    args = parser.parse_args()
    label = args.label
    inputDir = args.inputDir

    print "opening file ",inputDir+"electron_ntuple_"+label+".root"

    file=ROOT.TFile(inputDir+"electron_ntuple_"+label+".root")
    tree=file.Get("ntuplizer/tree")

    outPath="plots/"+label+"/"


    if not os.path.exists(outPath):
        os.mkdir(outPath)

    outfile=ROOT.TFile(outPath+"plots_"+label+".root","recreate")
#----histo definition----                                                                                                                                  
    histos={}
    bookHistos(histos)

#----loop over entries-----                                               

    for entry in tree:
        if entry.nEvent % 5000 ==0:
            print "Analyzing event:"
            print entry.nEvent
            
        for wp in "medium","loose","tight":
            if (getattr(entry,"Fall17CutBasedV2_"+wp)):
                histos["phi_"+wp].Fill(getattr(entry,"scl_phi"))
            if (getattr(entry,"Fall17CutBasedV2_"+wp+"_HEMSafe")):
                histos["phi_"+wp+"_HEMSafe"].Fill(getattr(entry,"scl_phi"))
    

 

    for x in histos.keys():
        if "HEM" not in x:
            print "plotting"
            hem = x+"_HEMSafe" 
            c1 = ROOT.TCanvas()
            histos[x].GetXaxis().SetTitle("#Phi")
            histos[hem].SetMarkerColor(ROOT.kRed)
            histos[hem].SetFillColor(ROOT.kRed)
            histos[hem].SetLineColor(ROOT.kRed)
            leg = ROOT.TLegend(0.67,0.75,0.80,0.88,"","NBNDC")
            leg.SetTextSize(0.025)
            leg.AddEntry(histos[x],"STD ID","f")
            leg.AddEntry(histos[hem],"HEM-SAFE ID","f")
            
            histos[x].Draw()
            histos[hem].Draw("sameep")
            leg.Draw("same")
            for format in ".png",".pdf",".C":
                c1.SaveAs(outPath+str(x)+format)
            c1.Delete()
            c1 = ROOT.TCanvas()
            dummy = histos[x].Clone()
            histos[x].Add(histos[hem],-1)
            histos[x].Divide(dummy)
            histos[x].Draw("hist")
            for format in ".png",".pdf",".C":
                c1.SaveAs(outPath+"ratio_"+str(x)+format)
        
    outfile.Write()
    outfile.Close()

### MAIN ###                                             
if __name__ == "__main__":
    main()

