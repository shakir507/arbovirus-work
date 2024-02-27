#ifndef DEFAULTS_H_
#define DEFAULTS_H_
#include <string>

struct defaults{
  std::string NUM_DAYS = "120";
  std::string START_DAY = "0";
  std::string TimeSnapShopt1 = "396";
  std::string TimeSnapShopt2 = "1165";
  std::string Exposed = "10";
  std::string InitialInfections = "10";
  std::string Recovered = "10";

  std::string output_dir = "../outputs/test_output_timing/";
  std::string input_base = "../InputFiles/";
  std::string NetworkFileMosquito="NetworkFileMosquito.json";
  std::string NetworkFileHuman="NetworkFileHuman.json";
  std::string networktypeH = "4";
  std::string networktypeM = "3";
  std::string id = "11";
  std::string Nodes="11";
  std::string NetworkName="SmallWorld";
  std::string bet1="0.8";
  std::string bet2="0.9";
  std::string muV="0.0625";//"1/16.0";
} DEFAULTS;


#endif