#include "models.h"
#include "outputs.h"
#include <fstream>
#include <iostream>
#include <string>
#include <cassert>

using std::string;
using std::vector;
using std::endl;
using std::cerr;

void check_stream(const std::ofstream& fout, const std::string& path){
  if(!fout){
	cerr << "simulator: could not open file "
		 << path << "\n"
		 << "simulator: please make sure the directory exists\n";
	exit(1);
  }
}
const std::string CSV_TERM = "\n";
const char CSV_SEP = ',';
template <class T>
void output_timed_csv(const std::vector<std::string>& field_row, const std::string& output_file, const timed_csv_data<T>& mat){
  std::ofstream fout(output_file, std::ios::out);
  check_stream(fout, output_file);

  fout << "Time" << CSV_SEP;
  auto end = field_row.end();
  auto penultimate = end - 1;
  for(auto it = field_row.begin(); it != end; ++it){
	fout << *it;
	if(it != penultimate){
	  fout<< CSV_SEP;
	}
  }
  fout << CSV_TERM;
  for(const auto& row: mat){
	auto end = std::get<1>(row).end();
	auto penultimate = end - 1;
	// fout << double(std::get<0>(row))/GLOBAL.SIM_STEPS_PER_DAY << CSV_SEP;
	fout << double(std::get<0>(row)) << CSV_SEP;
    
	for(auto it = std::get<1>(row).begin(); it < end; ++it){
	  fout << *it;
	  if(it != penultimate){
		fout<< CSV_SEP;
	  }
	}
	fout << CSV_TERM;
  }
  fout.close();
}

void output_csv_files(const std::string& output_directory,
					  // gnuplot& gnuplot,
					  const plot_data_struct& plot_data){
  for(const auto& elem: plot_data.nums){
	std::string csvfile_name = elem.first +GLOBAL.NetworkName+ ".csv";
	//std::string csvfile_path = output_directory + "/" + csvfile_name;
  std::string csvfile_path = output_directory + csvfile_name;
	if(elem.first == "csvContent"){
	  //This file contains everything!
     output_timed_csv({"Nodes",
						"Symptomatic"
		},
		csvfile_path, elem.second); 
	} else {
	  output_timed_csv({elem.first},
					   csvfile_path,
					   elem.second);
	  // gnuplot.plot_data(elem.first);
	}
  }
}
   void output_sensitivities_csv(std::vector<std::string>& field_row, std::string& output_file){
  //std::cout << "Storing file \n" ;    
  std::ofstream fout(output_file, std::ios::out);
  auto end = field_row.end();
  auto penultimate = end - 1;
  for(auto it = field_row.begin(); it != end; ++it){
	fout << *it;
	if(it != penultimate){
	  fout<< CSV_TERM;
	}
  }
  fout << CSV_TERM;
  fout.close();
  }

