import FWCore.ParameterSet.Config as cms

from FastSimulation.Tracking.PixelTracksProducer_cff import *
from FastSimulation.Tracking.PixelVerticesProducer_cff import *
from FastSimulation.Tracking.GeneralTracks_cfi import *
from TrackingTools.TrackFitters.TrackFitters_cff import *
from RecoJets.JetAssociationProducers.trackExtrapolator_cfi import *

from FastSimulation.Tracking.IterativeInitialStep_cff import *
from FastSimulation.Tracking.IterativeDetachedTripletStep_cff import *
from FastSimulation.Tracking.IterativeLowPtTripletStep_cff import *
from FastSimulation.Tracking.IterativePixelPairStep_cff import *
from FastSimulation.Tracking.IterativeMixedTripletStep_cff import *
from FastSimulation.Tracking.IterativePixelLessStep_cff import *
from FastSimulation.Tracking.IterativeTobTecStep_cff import *

#trackExtrapolator.trackSrc = cms.InputTag("generalTracksBeforeMixing")
trackExtrapolator.trackSrc = cms.InputTag("generalTracks")
lastTrackingSteps = cms.Sequence(generalTracksBeforeMixing)
        
import RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi
MeasurementTrackerEvent = RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi.MeasurementTrackerEvent.clone(
    pixelClusterProducer = '',
    stripClusterProducer = '',
    inactivePixelDetectorLabels = cms.VInputTag(),
    inactiveStripDetectorLabels = cms.VInputTag(),
    switchOffPixelsIfEmpty = False
)
iterativeTracking = cms.Sequence(
                                 MeasurementTrackerEvent 
                                 +iterativeInitialStep
                                 +iterativeDetachedTripletStep
                                 +iterativeLowPtTripletStep
                                 +iterativePixelPairStep
                                 +iterativeMixedTripletStep
                                 +iterativePixelLessStep
                                 +iterativeTobTecStep
                                 +lastTrackingSteps)

