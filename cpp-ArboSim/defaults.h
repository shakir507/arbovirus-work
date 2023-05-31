#ifndef DEFAULTS_H_
#define DEFAULTS_H_
#include <string>

struct defaults{
  std::string NUM_DAYS = "120";
  std::string START_DAY = "0";
  std::string TimeSnapShopt1 = "396";
  std::string TimeSnapShopt2 = "1165";
  std::string INIT_FRAC_INFECTED = "0.0001";
  std::string INIT_FIXED_NUMBER_INFECTED = "100";
  std::string MEAN_INCUBATION_PERIOD = "4.50";
  std::string output_dir = "../outputs/test_output_timing/";
  std::string input_base = "../InputFiles/";
  std::string NetworkFileMosquito="NetworkFileMosquito.json";
  std::string NetworkFileHuman="NetworkFileHuman.json";
  std::string networktypeH = "4";
  std::string networktypeM = "3";
  std::string id = "11";
  std::string Nodes="11";
  std::string NetworkName="SmallWorld";
} DEFAULTS;


#endif