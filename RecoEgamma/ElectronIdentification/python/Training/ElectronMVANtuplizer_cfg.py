import FWCore.ParameterSet.Config as cms
from RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi import electronMVAVariableHelper
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
from Configuration.AlCa.GlobalTag import GlobalTag

process = cms.Process("ElectronMVANtuplizer")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# File with the ID variables to include in the Ntuplizer
mvaVariablesFile = "RecoEgamma/ElectronIdentification/data/ElectronIDVariables.txt"

outputFile = "electron_ntuple.root"

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 10000 )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#         '/store/mc/RunIIFall17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/RECOSIMstep_94X_mc2017_realistic_v10-v1/00000/0293A280-B5F3-E711-8303-3417EBE33927.root'
#hcal on
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_v11_RelVal_jetHT2018B-v1/10000/186E3EB8-1D80-E811-81CB-0CC47A4C8F0A.root'
#hcal off
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/10000/F8921004-1980-E811-9FDC-0CC47A4D76D6.root',
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/10000/F025E36F-1D80-E811-967D-0CC47A4D75EC.root',
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/10000/A61DE4BE-0B80-E811-B433-0CC47A7C3404.root',
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/10000/84880955-1680-E811-9CE8-0025905A60A8.root',
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/10000/3C8CA11A-0280-E811-810C-0025905A60F4.root',
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/10000/32AC5D94-1080-E811-A11D-0CC47A4C8F12.root',
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/10000/0453F57F-1480-E811-9B22-0CC47A4C8F12.root',
#        '/store/relval/CMSSW_10_1_7/JetHT/MINIAOD/101X_dataRun2_Prompt_HEmiss_v1_RelVal_jetHT2018B-v1/10000/00DBB9B1-1280-E811-A08D-0025905B85BC.root'
#        '/store/data/Run2018A/JetHT/MINIAOD/17Sep2018-v1/00000/00A64001-F644-8740-AC48-14CD4E623E40.root'
        '/store/data/Run2018C/JetHT/MINIAOD/17Sep2018-v1/60000/FCE96966-A7DE-2B40-8A89-79CE611ADAD3.root'
    )
)

useAOD = False

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate
if useAOD == True :
    dataFormat = DataFormat.AOD
else :
    dataFormat = DataFormat.MiniAOD

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = [
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V2_HEMSafe_cff',
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V2_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',
                 ]

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

process.ntuplizer = cms.EDAnalyzer('ElectronMVANtuplizer',
        # AOD case
        src                  = cms.InputTag('gedGsfElectrons'),
        vertices             = cms.InputTag('offlinePrimaryVertices'),
        pileup               = cms.InputTag('addPileupInfo'),
        genParticles         = cms.InputTag('genParticles'),
        # miniAOD case
        srcMiniAOD           = cms.InputTag('slimmedElectrons'),
        verticesMiniAOD      = cms.InputTag('offlineSlimmedPrimaryVertices'),
        pileupMiniAOD        = cms.InputTag('slimmedAddPileupInfo'),
        genParticlesMiniAOD  = cms.InputTag('prunedGenParticles'),
        #
        eleMVAs             = cms.untracked.vstring(
                                          "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-HEMSafe-loose",
                                          "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-HEMSafe-medium",
                                          "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-HEMSafe-tight",
                                          "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-loose",
                                          "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-medium",
                                          "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-tight",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wpHZZ",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wpLoose",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp80",
                                          "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wpLoose",
                                          ),
        eleMVALabels        = cms.untracked.vstring(
                                        "Fall17CutBasedV2_loose_HEMSafe",
                                        "Fall17CutBasedV2_medium_HEMSafe",
                                        "Fall17CutBasedV2_tight_HEMSafe",
                                        "Fall17CutBasedV2_loose",
                                        "Fall17CutBasedV2_medium",
                                        "Fall17CutBasedV2_tight",
                                        "Fall17noIsoV2wp80",
                                        "Fall17noIsoV2wpLoose",
                                        "Fall17noIsoV2wp90",
                                        "Fall17isoV2wpHZZ",
                                        "Fall17isoV2wp80",
                                        "Fall17isoV2wpLoose",
                                        "Fall17isoV2wp90",
                                        "Fall17noIsoV1wp90",
                                        "Fall17noIsoV1wp80",
                                        "Fall17noIsoV1wpLoose",
                                        "Fall17isoV1wp90",
                                        "Fall17isoV1wp80",
                                        "Fall17isoV1wpLoose",
                                        ),
        eleMVAValMaps        = cms.untracked.vstring(
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV2RawValues",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values",
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values",
                                           ),
        eleMVAValMapLabels   = cms.untracked.vstring(
                                           "Fall17NoIsoV2Vals",
                                           "Fall17NoIsoV2RawVals",
                                           "Fall17IsoV2Vals",
                                           "Fall17IsoV2RawVals",
                                           "Fall17IsoV1Vals",
                                           "Fall17NoIsoV1Vals",
                                           ),
        eleMVACats           = cms.untracked.vstring(
                                           "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Categories",
                                           ),
        eleMVACatLabels      = cms.untracked.vstring(
                                           "EleMVACats",
                                           ),
        #
        variableDefinition   = cms.string(mvaVariablesFile),
        isMC                 = cms.bool(True),
        deltaR               = cms.double(0.1),
        saveGenInfoEle          = cms.bool(False),                          
        )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string( outputFile )
                                   )

process.p = cms.Path(process.egmGsfElectronIDSequence * process.ntuplizer)
