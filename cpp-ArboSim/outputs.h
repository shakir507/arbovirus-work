#ifndef OUTPUTS_H_
#define OUTPUTS_H_
#include "models.h"
#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <string>
#include <tuple>

template <class T>
using timed_csv_row = std::tuple<count_type, std::vector<T>>;

template <class T>
using timed_csv_data = std::vector<timed_csv_row<T>>;

struct plot_data_struct{
  std::map<std::string, timed_csv_data<double>> nums;
  // std::map<std::string, timed_csv_data<double>> susceptible_lambdas;
  // std::map<std::string, timed_csv_data<double>> total_lambda_fractions;
  // std::map<std::string, timed_csv_data<double>> mean_lambda_fractions;
  // std::map<std::string, timed_csv_data<double>> cumulative_mean_lambda_fractions;

  // std::map<std::string, timed_csv_data<long double>> infections_by_new_infectives;
  // std::map<std::string, timed_csv_data<long double>> infected_lat_lon;//--added by shakir for recording lat and lon for nodes
  // std::map<std::string, timed_csv_data<long double>> hospitalized_lat_lon;//--added by shakir for recording lat and lon for nodes
  // std::map<std::string, timed_csv_data<long double>> dead_lat_lon;//--added by shakir for recording lat and lon for nodes
  // std::map<std::string, timed_csv_data<long double>> recovered_lat_lon;//--added by shakir for recording lat and lon for nodes
  // std::map<std::string, timed_csv_data<long double>> recovered_lat_lon1;//--added by shakir for recording lat and lon for nodes
  // std::map<std::string, timed_csv_data<long double>> recovered_lat_lon2;//--added by shakir for recording lat and lon for nodes
  // std::map<std::string, timed_csv_data<long double>> susceptible_lat_lon1;//--added by shakir for recording lat and lon for nodes
  // std::map<std::string, timed_csv_data<long double>> susceptible_lat_lon2;//--added by shakir for recording lat and lon for nodes

  // std::map<std::string, timed_csv_data<long double>> vaccinated_lat_lon;//--added by shakir for recording lat and lon for nodes

  // std::map<std::string, timed_csv_data<count_type>> quarantined_stats;
  // std::map<std::string, timed_csv_data<double>> curtailment_stats;
  // std::map<std::string, timed_csv_data<count_type>> disease_label_stats;
  // std::map<std::string, timed_csv_data<int>> ward_wise_stats; // sk
  
  // std::vector<std::string> logger1;
  // std::vector<std::string> logger2;//added by shakir for recording lat and lon for infected indiv
  // std::vector<std::string> logger3;//added by shakir for recording lat and lon for infected indiv
  // std::vector<std::string> logger4;//added by shakir for recording lat and lon for infected indiv
  // std::vector<std::string> logger5;//added by shakir for recording lat and lon for recovered1 indiv
  // std::vector<std::string> logger6;//added by shakir for recording lat and lon for infected indiv
  // std::vector<std::string> logger7;//added by shakir for recording lat and lon for recovered2 indiv
  // std::vector<std::string> logger8;//added by shakir for recording lat and lon for susceptible1 indiv
  // std::vector<std::string> logger9;//added by shakir for recording lat and lon for susceptible2 indiv

};
void output_csv_files(const std::string& output_directory, const plot_data_struct& plot_data);

void output_sensitivities_csv(std::vector<std::string>& field_row, std::string& output_file);

#endif