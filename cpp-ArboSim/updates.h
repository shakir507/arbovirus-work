#ifndef UPDATE_H
#define UPDATE_H
#include"models.h"
#include <cmath>
#include<iostream>
#include<fstream>
using std::vector;

void rk4(double t, vector<double>& y0, vector<double>& yf0, vector<double>& dy0, vector<double>& dyf0, double h, vector<double>& y1, vector<double>& yf1, void dif(double, vector<double>&, vector<double>&, vector<double>&, vector<double>&));
void dif(double t, vector<double>& y0,vector<double>& dy,vector<double>& yf0,vector<double>& dyf);


void gs(vector<double> &y,int id,int M,int N,vector<double> &sum);
// void degree(vector<double> &AA, const matrix<double> &adj_matirx);

struct casualty_stats{
       count_type symptomatic = 0;

};

casualty_stats get_infected_community(std::vector<double>& y, matrix<double>& community);


#endif
