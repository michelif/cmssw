#!/bin/sh

############
## PYTHON ##
############
export PYTHONPATH=$PYTHONPATH:${python_path}/COMP/DBS/Clients/PythonAPI
export PYTHONPATH=$PYTHONPATH:${python_path}/COMP/DLS/Client/LFCClient
export PYTHONPATH=$PYTHONPATH:${python_path}/COMP/DLS/Client/DliClient
export PATH=$PATH:${python_path}/COMP/:${python_path}/COMP/DLS/Client/LFCClient
############

#  python ${local_crab_path}/dbsreadprocdataset.py --DBSAddress=MCLocal_4/Writer --datasetPath=/TAC-TIBTOB-120-DAQ-EDM/RECO/*CMSSW_1_3_0_pre6* --logfile=${list_path}/${list}

if [ ! -e ${log_path} ]; then
  mkdir -v ${log_path}
  mkdir -v ${list_path}
fi

##############################
## Extract list of new runs ##
##############################
echo Interrogating database $1

export list_temp=list_temp.txt

if [ $1 == "Bari" ]; then
  # To access Bari reconstructed TIBTOB runs
  python ${local_crab_path}/dbsreadprocdataset.py --DBSAddress=MCGlobal/Writer --datasetPath=/TAC-*-120-DAQ-EDM/RECO/*CMSSW_1_3_0_pre6* --logfile=${list_path}/${datasets_list}
  cat ${list_path}/${datasets_list} | awk -F- '{print $2 "-" $9}' > ${list_path}/${list_temp}
fi

if [ $1 == "FNAL" ]; then
  # To access FNAL reconstructed TIBTOB runs
  python ${local_crab_path}/dbsreadprocdataset.py --DBSAddress=MCGlobal/Writer --datasetPath=/TAC-*-RecoPass0/RECO/*CMSSW_1_3_0_pre6* --logfile=${list_path}/${datasets_list}
  cat ${list_path}/${datasets_list} | awk -F- '{print $2 "-" $4}' > ${list_path}/${list_temp}
fi

if [ $1 == "RAW" ]; then
  # To access RAW TIBTOB data
  python ${local_crab_path}/dbsreadprocdataset.py --DBSAddress=MCGlobal/Writer --datasetPath=/TAC-*-120-DAQ-EDM/RAW/*CMSSW_1_2_0* --logfile=${list_path}/${datasets_list}
  cat ${list_path}/${datasets_list} | awk -F- '{print $2 "-" $8}' > ${list_path}/${list_temp}
fi

echo Selecting runs of type $2

# Clean older lists
rm -f ${list_path}/${list}
touch ${list_path}/${list}

for type_ in `echo ${Config_}`; do
  if [ ${type_} != "All" ]; then
    if [ ${type_} == "TIBTOB" ] && [ ${type_} != "TIBTOBTEC" ]; then
      echo TIBTOB type_ = ${type_}
      cat ${list_path}/${list_temp} | grep ${type_} >> ${list_path}/${list}
#      cat ${list_path}/${list}
    else
      echo type_ = ${type_}
      cat ${list_path}/${list_temp} | grep ${type_} | grep -v "TIBTOB" >> ${list_path}/${list}
#      cat ${list_path}/${list}
    fi
  else
    cp ${list_path}/${list_temp} ${list_path}/${list}
  fi
done

# Clean temporary list
rm -f ${list_path}/${list_temp}

## TEST
#######
#export LOCALHOME=/analysis/sw/CRAB
#export local_crab_path=${LOCALHOME}

#export list_path=${LOCALHOME}
#export list=test_list.txt

#python ${local_crab_path}/dbsreadprocdataset.py --DBSAddress=MCGlobal/Writer --datasetPath=/TAC-TIBTOB-RecoPass0/RECO/*CMSSW_1_3_0_pre6* --logfile=${list_path}/test_list_FNAL.txt

#python ${local_crab_path}/dbsreadprocdataset.py --DBSAddress=MCGlobal/Writer --datasetPath=/TAC-*-120-DAQ-EDM/RECO/*CMSSW_1_3_0_pre6* --logfile=${list_path}/test_list_Bari.txt

#python ${local_crab_path}/dbsreadprocdataset.py --DBSAddress=MCGlobal/Writer --datasetPath=/TAC-*-120-DAQ-EDM/RAW/*CMSSW_1_2_0* --logfile=${list_path}/test_list_RAW.txt

#######

#if [ $2 == "TIBTOB" ]; then
#  cat ${list_path}/test_list_Bari.txt | grep $2 > ${list_path}/test_list_Bari.txt
#  cat ${list_path}/test_list_Bari.txt
#else
#  cat ${list_path}/test_list_Bari.txt | grep $2 | grep -v "TIBTOB" > ${list_path}/test_list_Bari.txt
#  cat ${list_path}/test_list_Bari.txt
#fi



###############################

# Extract list of physics runs
wget -q -r "http://cmsdaq.cern.ch/cmsmon/cmsdb/servlet/RunSummaryTIF?RUN_BEGIN=$nextRun&RUN_END=1000000000&RUNMODE=PHYSIC&TEXT=1&DB=omds" -O ${list_path}/${list_phys}

# temporary patch since cmsmon is not responding
if [ "`cat ${list_path}/${list_phys}`" == "" ]; then
  echo list of physics runs is empty
  echo using list of all runs
  cp ${list_path}/${list} ${list_path}/${list_phys}
fi

