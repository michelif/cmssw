#!/usr/bin/env python

def convert_to_str(vec_str):
    output = ""
    for entry in vec_str:
        if output != "": output+="\n  "
        output+=entry
    return output

def convertpair_to_str(vec_str):
    output = ""
    for entry in vec_str:
        if output != "": output+="\n  "
        output+=entry.first
    return output

# mvaEleID-Fall17-noIso-V2-wp80

def print_ele_user_data(ele):
    # print "ele userfloats:"
    # print "  "+convert_to_str(ele.userFloatNames())
    # print "ele userints:"
    # print "  "+convert_to_str(ele.userIntNames())
    # print "ele IDs:"
    # print "  "+convertpair_to_str(ele.electronIDs())
    print ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value')

def print_pho_user_data(pho):
    pass 
    # print "pho userfloats:"
    # print "  "+convert_to_str(pho.userFloatNames())
    # print "pho userints:"
    # print "  "+convert_to_str(pho.userIntNames())
    # print "pho IDs:"
    # print "  "+convertpair_to_str(pho.photonIDs())
    print pho.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value')


import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()
from DataFormats.FWLite import Events, Handle
from copy import deepcopy as dc
from pdb import set_trace
import numpy as np

import argparse
parser = argparse.ArgumentParser(description='prints E/gamma pat::Electrons/Photons user data')
parser.add_argument('filename',help='input filename')
args = parser.parse_args()

eles, ele_label = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
phos, pho_label = Handle("std::vector<pat::Photon>"), "slimmedPhotons"


min_pho_et = 10
min_ele_et = 10

done_ele = False
done_pho = False

# f_in_pog   = ROOT.TFile('2016LegacyReReco_ElectronMVA80noiso_Fall17V2.root')
f_in_pog   = ROOT.TFile('2018_ElectronMVA80noiso.root')
h_in_pog   = f_in_pog.Get('EGamma_SF2D')
h_ele_json = ROOT.TH1D('ele_mvaEleID-Fall17-noIso-V2-wp80_json', 'mvaEleID-Fall17-noIso-V2-wp80_value_json', 100, 0., 1.,)
h_ele_pog  = ROOT.TH1D('ele_mvaEleID-Fall17-noIso-V2-wp80_POG', 'mvaEleID-Fall17-noIso-V2-wp80_value_POG', 100, 0., 1.,)

l_pt  = [10., 20., 35.0, 50., 100., 200., 500.]
b_pt  = np.array(l_pt)
l_eta = [-2.5, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8, 1.444, 1.566, 2.0, 2.5] 
b_eta = np.array(l_eta)

h_ele_eta_pt = ROOT.TH2D('ele_sf_from_json', 'sf_from_json', len(b_eta)-1, b_eta, len(b_pt)-1, b_pt)

h_ele_pt_eta0t08  = ROOT.TH1D('ele_sf_from_json_eta0t08',  'sf_from_json_eta0t08',  len(b_pt)-1, b_pt)
h_ele_pt_eta08t14 = ROOT.TH1D('ele_sf_from_json_eta08t14', 'sf_from_json_eta08t14', len(b_pt)-1, b_pt)
h_ele_pt_eta16t20 = ROOT.TH1D('ele_sf_from_json_eta16t20', 'sf_from_json_eta16t20', len(b_pt)-1, b_pt)
h_ele_pt_eta20t25 = ROOT.TH1D('ele_sf_from_json_eta20t25', 'sf_from_json_eta20t25', len(b_pt)-1, b_pt)

events = Events(args.filename)
num = 0 
BREAK = False
for event_nr,event in enumerate(events):
    # if done_ele and done_pho: break
        if BREAK == True: break
    
    # if not done_pho:
        # event.getByLabel(pho_label,phos)
    
        # for pho_nr,pho in enumerate(phos.product()):  
            # if pho.et()<min_pho_et: continue
            # else:
                # # print_pho_user_data(pho)
                # done_pho = True
    # if not done_ele:
        event.getByLabel(ele_label,eles)
    
        for ele_nr,ele in enumerate(eles.product()):
            if ele.et()<min_ele_et: continue
            else:
                num +=1
                # print_ele_user_data(ele)
                # set_trace()
                val = h_in_pog.GetBinContent( h_in_pog.GetXaxis().FindBin( ele.eta() ) , h_in_pog.GetYaxis().FindBin( ele.pt() ) )
                if val == 0.0: continue
                if val != ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value'): set_trace()
                h_ele_pog.Fill(val)
                h_ele_json.Fill(ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value'))
                if num % 1000 == 0: print num
                # if num % 10000 == 0: BREAK = True

                pt_bin  = h_ele_pt_eta0t08.GetXaxis().FindBin( ele.pt() ) 
                eta_bin = h_ele_eta_pt.GetXaxis().FindBin( ele.eta() )
                if abs(ele.eta()) < 0.8:
                    h_ele_pt_eta0t08 .SetBinContent( pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value') )
                    h_ele_pt_eta0t08 .SetBinError( pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_error') )
                elif abs(ele.eta()) > 0.8 and abs(ele.eta()) < 1.444:
                    h_ele_pt_eta08t14.SetBinContent( pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value') ) 
                    h_ele_pt_eta08t14.SetBinError( pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_error') ) 
                elif abs(ele.eta()) > 1.566 and abs(ele.eta()) < 2.0:
                    h_ele_pt_eta16t20.SetBinContent( pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value') )
                    h_ele_pt_eta16t20.SetBinError( pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_error') )
                elif abs(ele.eta()) > 2.0 and abs(ele.eta()) < 2.5:
                    h_ele_pt_eta20t25.SetBinContent( pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value') )
                    h_ele_pt_eta20t25.SetBinError( pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_error') )

                h_ele_eta_pt.SetBinContent( eta_bin, pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_value') )
                h_ele_eta_pt.SetBinError  ( eta_bin, pt_bin, ele.userFloat('mvaEleID-Fall17-noIso-V2-wp80_error') )
                # set_trace()
                # done_ele = True

h_ele_diff = dc(h_ele_json)
h_ele_diff.Divide(h_ele_pog)

f_out = ROOT.TFile.Open('f_out.root', 'recreate')
f_out.cd()
h_ele_json.Write()
h_ele_pog.Write()
h_ele_diff.Write()
h_ele_eta_pt.Write()
h_ele_pt_eta0t08 .Write()
h_ele_pt_eta08t14.Write()
h_ele_pt_eta16t20.Write()
h_ele_pt_eta20t25.Write()
f_out.Close()

