#ifndef MODELS_H_
#define MODELS_H_
#include <vector>
#include <random>
#include <tuple>
#include <cmath>
#include <string>
#include <algorithm>
#include <unordered_map>
#include<iostream>
#include<fstream>

template<typename T>
using matrix = std::vector< std::vector<T> >;

struct network{

};

using count_type = unsigned long;
inline count_type stoct(const std::string& str){
  return std::stoul(str);
}

double f_kernel(double dist);


struct community {
    double phi;
    double bet2;
    double bet1;
    double sig;
    double th;
    double gam;
    double lamM10;
    double lamM1;
    double gamH;
    double gamM;
    double m;
    double sigH;
    double sigM;
    double cc;
    double muV;
    double pp1;
    double pp2;

};

struct dengue{
    double phi;
    double bet2;
    double bet1;
    double sig;
    double th;
    double gam;
    double lamM10;
    double lamM1;
    double gamH;
    double gamM;
    double m;
    double sigH;
    double sigM;
    double cc;
    double muV;
    double pp1;
    double pp2;

};

struct zika{
    double phi;
    double bet2;
    double bet1;
    double sig;
    double th;
    double gam;
    double lamM10;
    double lamM1;
    double gamH;
    double gamM;
    double m;
    double sigH;
    double sigM;
    double cc;
    double muV;
    double pp1;
    double pp2;

};

struct chikungunya{
    double phi;
    double bet2;
    double bet1;
    double sig;
    double th;
    double gam;
    double lamM10;
    double lamM1;
    double gamH;
    double gamM;
    double m;
    double sigH;
    double sigM;
    double cc;
    double muV;
    double pp1;
    double pp2;

};

struct sys_para{
    std::vector<double> PIH;
    std::vector<double> PIM;
    std::vector<double> Qv;
    std::vector<double> muM;
    std::vector<double> A;
    std::vector<double> B;
    std::vector<double> R0;
    std::vector<double> I;
    std::vector<double> degA;
    std::vector<double> degB;
    matrix<double> adjMatrixA;
    matrix<double> adjMatrixB;

    int Nodes=11;
    int ntrans;
    count_type NUM_DAYS;
    count_type START_DAY;
    
    double F_KERNEL_A;
    double F_KERNEL_B;
    double ep=0;
    double a;
    double a0;
    double b=0.315;
    double c;
    double d;
    double tpi;
    double w;
    double NN = 1;
    double NM;
    double NH;
    double nu;
    double gam1;
    double gam2;
    double muH=1.0 / (74.0 * 365.0); //--------host death rate;
    double rho;
    double del1;
    double del2;
    double gam3;
    double al1;
    double al2;
    double Q1;
    double Q2;
    double lamH1;
    double lamH10;
    double lamH2;
    double lamH3;
    double lamH30;
    double lamH40;
    double lamH4;
    double lamH5;
    double phi;
    double bet2= 0.9;                 //------transmission rate from vector to hosts;
    double bet1= 0.8;                 //------transmission rate from hosts to vectors;
    double sig;
    double th;
    double gam= 0.11;
    double lamM10;
    double lamM1;
    double gamH;
    double gamM;
    double m;
    double sigH= 0.16;
    double sigM= 0.0904;
    double cc= 0.25;
    double muV= 1 / 16.0;
    double pp1;
    double pp2;
    int id;
    int sid;
    int M;
    int sM;
    int N; 
    int sN; 
    int networktypeH=0;
    int networktypeM=0;
    
    double h;
   
   std::string input_base;

   std::string output_path;

   std::string NetworkName="SmallWorld";
   std::string NetworkFileMosquito="NetworkFileMosquito.json";
   std::string NetworkFileHuman="NetworkFileHuman.json";

};
extern sys_para GLOBAL;

const bool SEED_INFECTION_FROM_FILE = true;


#endif
