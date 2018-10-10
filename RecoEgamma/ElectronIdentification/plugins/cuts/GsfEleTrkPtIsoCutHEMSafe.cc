#include "PhysicsTools/SelectorUtils/interface/CutApplicatorBase.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/ConversionFwd.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

#include "RecoEgamma/ElectronIdentification/interface/EBEECutValues.h"

class GsfEleTrkPtIsoCutHEMSafe : public CutApplicatorBase {
public:
  GsfEleTrkPtIsoCutHEMSafe(const edm::ParameterSet& c);
  
  result_type operator()(const reco::GsfElectronPtr&) const final;

  double value(const reco::CandidatePtr& cand) const final;

  CandidateType candidateType() const final { 
    return ELECTRON; 
  }

private:
 
  EBEECutValues slopeTerm_;
  EBEECutValues slopeStart_;
  EBEECutValues constTerm_;
  
  
  edm::Handle<double> rhoHandle_;
  
};

DEFINE_EDM_PLUGIN(CutApplicatorFactory,
		  GsfEleTrkPtIsoCutHEMSafe,
		  "GsfEleTrkPtIsoCutHEMSafe");

GsfEleTrkPtIsoCutHEMSafe::GsfEleTrkPtIsoCutHEMSafe(const edm::ParameterSet& params) :
  CutApplicatorBase(params),
  slopeTerm_(params,"slopeTerm"),
  slopeStart_(params,"slopeStart"),
  constTerm_(params,"constTerm")
{

}


CutApplicatorBase::result_type 
GsfEleTrkPtIsoCutHEMSafe::
operator()(const reco::GsfElectronPtr& cand) const{  

  if (!cand->hcalOverEcalValid()){  
    const float isolTrkPt = cand->dr03TkSumPt();
    const float et = cand->et();
    const float cutValue = et > slopeStart_(cand)  ? slopeTerm_(cand)*(et-slopeStart_(cand)) + constTerm_(cand) : constTerm_(cand);
    return isolTrkPt < cutValue;
  }
    return true;
}

double GsfEleTrkPtIsoCutHEMSafe::
value(const reco::CandidatePtr& cand) const {
  reco::GsfElectronPtr ele(cand);  
  return ele->dr03TkSumPt();
}
