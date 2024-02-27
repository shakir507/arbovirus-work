#include "simulator.h"
#include "outputs.h"
#include "defaults.h"
#include "initializers.h"
#include <cassert>
#include <iostream>
#include <fstream>
#include <string>
#include <cxxopts.hpp>

int main(int argc, char **argv)
{

    cxxopts::Options options(argv[0],
			   "Simulate arbovirus model on a network");

    options.add_options("Basic")
    ("h,help", "display description of pNUM_DAYSrogram options")
    ("NUM_DAYS", "number of days in the simulation",
     cxxopts::value<count_type>()->default_value(DEFAULTS.NUM_DAYS))
    ("START_DAY", "day at the start of simulation",
     cxxopts::value<count_type>()->default_value(DEFAULTS.START_DAY))
    ("output_directory", "output directory",
     cxxopts::value<std::string>()->default_value(DEFAULTS.output_dir))
    ("input_directory", "input directory",
     cxxopts::value<std::string>()->default_value(DEFAULTS.input_base))
    ("NetworkFileMosquito", "Network file name mosquitoes",
     cxxopts::value<std::string>()->default_value(DEFAULTS.NetworkFileMosquito))
    ("NetworkFileHuman", "Network File name for humans",
     cxxopts::value<std::string>()->default_value(DEFAULTS.NetworkFileHuman))
    ("NetworkName", "Network Name: scale free, small world etc",
     cxxopts::value<std::string>()->default_value(DEFAULTS.NetworkName))
      ("networktypeH", "networktype human",
     cxxopts::value<int>()->default_value(DEFAULTS.networktypeH))
      ("networktypeM", "networktype mosquito",
     cxxopts::value<int>()->default_value(DEFAULTS.networktypeM))
     ("bet1", "Transmission rate from humans to mosquitoes",
     cxxopts::value<double>()->default_value(DEFAULTS.bet1))
     ("bet2", "Transmission rate from mosquitoes to humans",
     cxxopts::value<double>()->default_value(DEFAULTS.bet2))
      ("muV", "Mosquito death rate",
     cxxopts::value<double>()->default_value(DEFAULTS.muV))
      ("Exposed", "Initial number of infected humans",
     cxxopts::value<double>()->default_value(DEFAULTS.Exposed))
      ("InitialInfections", "Initial number of infected humans",
     cxxopts::value<double>()->default_value(DEFAULTS.InitialInfections))
      ("Recovered", "Initial number of infected humans",
     cxxopts::value<double>()->default_value(DEFAULTS.Recovered))
      ("Nodes", "Nodes",
     cxxopts::value<int>()->default_value(DEFAULTS.Nodes))
      ("id", "id",
     cxxopts::value<int>()->default_value(DEFAULTS.id))     
    ;

  auto optvals = options.parse(argc, argv);
  if(optvals.count("help")){
    std::cout << options.help({"Basic",
			       "Infection seeding",
			       "Disease progression",
			       "City",
			       "Intervention - basic",
			       "Intervention - cyclic strategy",
			       "Intervention - soft containment zones",
			       "Intervention - neighbourhood containment",
			       "Age-dependent mixing",
			       "Other",
             "Testing and contact tracing",
             "New_strain_vaccination_reinfection"
      }) << std::endl;
    return 0;
  }


  GLOBAL.NUM_DAYS = optvals["NUM_DAYS"].as<count_type>();
  GLOBAL.START_DAY = optvals["START_DAY"].as<count_type>();

  std::string output_dir(optvals["output_directory"].as<std::string>());

  GLOBAL.output_path = output_dir; //sk
  GLOBAL.input_base = optvals["input_directory"].as<std::string>();
    GLOBAL.NetworkFileHuman = optvals["NetworkFileHuman"].as<std::string>();
  GLOBAL.NetworkFileMosquito = optvals["NetworkFileMosquito"].as<std::string>();

  GLOBAL.NetworkName = optvals["NetworkName"].as<std::string>();

  GLOBAL.networktypeM=optvals["networktypeM"].as<int>();
  GLOBAL.networktypeH=optvals["networktypeH"].as<int>();

  GLOBAL.Nodes=optvals["Nodes"].as<int>();
  GLOBAL.id=optvals["id"].as<int>();
  GLOBAL.Exposed=optvals["Exposed"].as<double>();
  GLOBAL.InitialInfections=optvals["InitialInfections"].as<double>();
  GLOBAL.Recovered=optvals["Recovered"].as<double>();

  GLOBAL.bet1=optvals["bet1"].as<double>();
  GLOBAL.bet2=optvals["bet2"].as<double>();
  GLOBAL.muV=optvals["muV"].as<double>();

  auto plot_data = run_simulation();
    // std::string csv_file_name = "new_infections" + std::to_string(GLOBAL.START_DAY) + "_" + std::to_string(GLOBAL.NUM_DAYS) + ".csv";
    std::string csv_file_name = "new_infections.csv";
 
    // std::string csv_file_path = output_dir + "/" + csv_file_name;
    std::string csv_file_path = output_dir + csv_file_name; // make sure --output_directory ends with /
    // // std::cerr << "drive_simulation: Writing to " << csv_file_path << "\n";
    output_sensitivities_csv(plot_data.logger1, csv_file_path);
    output_csv_files(output_dir, 
  // gnuplot, 
  plot_data);
    return 0;
}
