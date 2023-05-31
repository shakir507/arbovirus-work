#ifndef INITIALIZERS_H
#define INITIALIZERS_H
#include "models.h"
#include<vector>

// matrix<double> createSmallWorld(int numNodes, double prob, int k);
// matrix<double> createRandom(int numNodes, double prob);
// matrix<double> createScaleFree(int numNodes, int m0, int m);
void generateHumanNetwork(int networktype);
void generateMosquitoNetwork(int networktype);




void init_states(std::vector<double>& y0);



#endif