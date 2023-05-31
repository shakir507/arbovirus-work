#include <rapidjson/document.h>
#include <rapidjson/istreamwrapper.h>
#include <rapidjson/prettywriter.h>
#include <rapidjson/stringbuffer.h>
#include "models.h"
#include "initializers.h"
#include <iostream>
#include <cmath>
#include <fstream>
#include <vector>
#include <algorithm>
#include <random>
#include <set>
#include <string>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
#ifdef DEBUG
#include <cassert>
#endif


using std::string;
using std::vector;
using std::set;
using std::to_string;

auto readJSONFile(string filename){
  std::ifstream ifs(filename, std::ifstream::in);
  rapidjson::IStreamWrapper isw(ifs);
  rapidjson::Document d;
  d.ParseStream(isw);
  return d;
}

using namespace std;
void getAvector();
void getBvector();
void writeMatrixToCSV(matrix<double>& matrix, const std::string& filename);

matrix<double> identityMatrix(matrix<double>&adjMatrix ,int numNodes) {
     for (int i = 1; i <=numNodes; i++) {
        for (int j = 1; j <=numNodes; j++) {
                adjMatrix[i][j] = 0;

        }

    }
    return adjMatrix;
}

// Function to create a random network
matrix<double> createKedahNetwork(matrix<double>&adjMatrix, int numNodes, int H) {
    // Initialize the adjacency matrix
    // matrix<double> adjMatrix(numNodes+1, vector<double>(numNodes+1));
    // matrix<double> dist_matrix(size, vector<double>(size));
    if (H==0){
    getAvector();

    for (int i = 1; i <=numNodes; i++) {
        for (int j = i + 1; j <=numNodes; j++) {
                adjMatrix[i][j] = GLOBAL.A[(i-1)*GLOBAL.Nodes+j];
        }
    }
    }
    else{
    getBvector();

    for (int i = 1; i <=numNodes; i++) {
        for (int j = i + 1; j <=numNodes; j++) {
                adjMatrix[i][j] = GLOBAL.B[(i-1)*GLOBAL.Nodes+j];
        }
    }
    }

    return adjMatrix;
}

// Function to create a small-world network
matrix<double> createSmallWorld(matrix<double>&adjMatrix,int numNodes, double prob, int k) {
    // Initialize the adjacency matrix
    // matrix<double> adjMatrix(numNodes+1, vector<double>(numNodes+1));
// std::cout<<"I am in small world 1\t"<<std::endl;

    // Create a ring lattice
    for (int i = 1; i <= numNodes; i++) {
        for (int j = i - k; j <= i + k; j++) {
            if (j >= 1 && j <= numNodes && j != i) {
                adjMatrix[i][j] = 1;
            }
        }
    }
    // Randomly rewire the edges
    default_random_engine gen;
    uniform_real_distribution<double> dist(0, 1);
    for (int i = 1; i <=numNodes; i++) {
        for (int j = i - k; j <= i + k; j++) {
            if (j >= 1 && j <=numNodes && j != i && dist(gen) < prob) {
                // Choose a random node to rewire to

                int new_j = (rand() % numNodes)+1;
                                // std::cout<<"I am in small world 2\t"<<new_j<<"\t"<<i<<std::endl;

                // Check that the new edge does not already exist
                if (adjMatrix[i][new_j] == 0 && adjMatrix[new_j][i] == 0) {
                                                    // std::cout<<"I am in small world 3\t"<<new_j<<"\t"<<i<<std::endl;

                    // Rewire the edge
                    adjMatrix[i][j] = 0;
                    adjMatrix[j][i] = 0;
                    adjMatrix[i][new_j] = 1;
                    adjMatrix[new_j][i] = 1;
                }
            }
        }
    }

    return adjMatrix;
}

// Function to create a random network
matrix<double> createRandom(matrix<double>&adjMatrix,int numNodes, double prob) {
    // Initialize the adjacency matrix
    // matrix<double> adjMatrix(numNodes+1, vector<double>(numNodes+1));
    // matrix<double> dist_matrix(size, vector<double>(size));

    // Randomly connect nodes
    default_random_engine gen;
    uniform_real_distribution<double> dist(0, 1);
    for (int i = 1; i <=numNodes; i++) {
        for (int j = i + 1; j <=numNodes; j++) {
            if (dist(gen) < prob) {
                adjMatrix[i][j] = 1;
                adjMatrix[j][i] = 1;
            }
        }
    }

    return adjMatrix;
}

// Function to create a scale-free network
matrix<double> createScaleFree(matrix<double> & adjMatrix,int numNodes, int m0, int m) {
    // Initialize the adjacency matrix
    // matrix<double> adjMatrix(numNodes+1, vector<double>(numNodes+1));
    // Create a complete graph with m0 nodes
   matrix<double> newAdjMatrix = adjMatrix;

    // Create a complete graph with m0 nodes
    for (int i = 1; i <= m0; i++) {
        for (int j = i + 1; j <= m0; j++) {
            newAdjMatrix[i][j] = 1;
            newAdjMatrix[j][i] = 1;
        }
    }

    // Add nodes with m edges, using preferential attachment
    std::vector<int> degrees(numNodes + 1, m0 - 1);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dis(0.0, 1.0);

    for (int i = m0; i <= numNodes; i++) {
        for (int j = 1; j <= m; j++) {
            // Choose a node to connect to, with probability proportional to degree
            double r = dis(gen);
            double sum = 0.0;
            int k = 1;

            while (sum <= r) {
                sum += degrees[k] / (2.0 * (m0 + i - 1));
                k++;
            }
            k--;

            // Connect the new node to the chosen node
            newAdjMatrix[i][k] = 1;
            newAdjMatrix[k][i] = 1;
            degrees[i]++;
            degrees[k]++;
        }
    }

    return newAdjMatrix;
}

matrix<double> readNetworkFileH(){

    matrix<double> return_object;
    auto file_JSON = readJSONFile(GLOBAL.input_base + GLOBAL.NetworkFileHuman);
// std::cout<<"I am done reading network 0\n"<<std::endl;

    auto size = file_JSON.GetArray().Size();
    return_object.resize(size, vector<double>(size));

    int i = 0;
    for (auto &elem: file_JSON.GetArray()){
// std::cout<<"I am in loop network \t"<<std::endl;

        for (count_type j = 0; j < size; ++j){

            GLOBAL.adjMatrixA[i+1][j+1] = elem[to_string(j).c_str()].GetDouble();

        }
     i += 1;
     }
// std::cout<<"I am done reading network\n"<<std::endl;

  return  GLOBAL.adjMatrixA;
}

matrix<double> readNetworkFileM(){
    matrix<double> return_object;

    auto file_JSON = readJSONFile(GLOBAL.input_base + GLOBAL.NetworkFileMosquito);//"individuals.json");
  auto size = file_JSON.GetArray().Size();
  int i = 0;
  for (auto &elem: file_JSON.GetArray()){
    for (count_type j = 0; j < size; ++j){
       GLOBAL.adjMatrixB[i+1][j+1] = elem[to_string(j).c_str()].GetDouble();
    }
    i += 1;
  }
return  GLOBAL.adjMatrixB;
}

void generateHumanNetwork(int networktype){
  double prob_rand=0.2,probrewire=0.1;
    int m=3,m0=3;
    int k=3;//the value of k generates a small worl network with average degree of k, starting from a regular network with degree k. The revwiring is done with prob prob_rewire
  switch(networktype){
        case 0:
		  GLOBAL.adjMatrixA=createKedahNetwork(GLOBAL.adjMatrixA,GLOBAL.Nodes,0);
		break;
	  case 1:
		  GLOBAL.adjMatrixA=createSmallWorld(GLOBAL.adjMatrixA,GLOBAL.Nodes, probrewire, k);
		break;
	  case 2:
      GLOBAL.adjMatrixA=createRandom(GLOBAL.adjMatrixA,GLOBAL.Nodes, prob_rand);
		break;
	  case 3:
      GLOBAL.adjMatrixA=createScaleFree(GLOBAL.adjMatrixA,GLOBAL.Nodes, m0, m);
		break;
      case 4:
       GLOBAL.adjMatrixA=readNetworkFileH();

      break;

	  }
    std::string filename = "matrix.csv";
    writeMatrixToCSV(GLOBAL.adjMatrixA, filename);
  return;
}

void generateMosquitoNetwork(int networktype){
      matrix<double> adj_matrix;

      switch (networktype)
      {
       case 0:
            GLOBAL.adjMatrixB=createKedahNetwork(GLOBAL.adjMatrixB,GLOBAL.Nodes,1);
        break;
        case 1:
            GLOBAL.adjMatrixB=readNetworkFileM();
        break;
        default:
            GLOBAL.adjMatrixB=identityMatrix(GLOBAL.adjMatrixB,GLOBAL.Nodes);
        break;
      }
       

      return;

}

void init_states(vector<double>& y0){
    int Nodes=GLOBAL.Nodes,I[Nodes+1];
    if(SEED_INFECTION_FROM_FILE){
    auto initialJson = readJSONFile(GLOBAL.input_base + "NetworkSeeding.json");//"individuals.json");
  auto size = initialJson.GetArray().Size();
        count_type i = 0;
        // count_type travellers=0;//---delete shakir after verifying travellers
        for (auto &elem: initialJson.GetArray()){
            I[i+1] = elem["Infected"].GetInt();
             GLOBAL.PIH[i+1]=elem["birthrate"].GetDouble();

            GLOBAL.R0[i+1]=elem["R0"].GetDouble();;
            GLOBAL.muM[i+1]=elem["MosquitoDeathRate"].GetDouble();;//---------vector death rate

             ++i;
        }
    }
    else{
    //Infection cases reported from each of these mukims
    I[1]=15;
    I[2]=16;
    I[3]=18;
    I[4]=28;
    I[5]=10;
    I[6]=34;
    I[7]=31;
    I[8]=25;
    I[9]=30;
    I[10]=57;
    I[11]=14;

    GLOBAL.PIH[1]=0.157089967;
    GLOBAL.PIH[2]=0.118807849;
    GLOBAL.PIH[3]=0.059977786;
    GLOBAL.PIH[4]=0.774676046;
    GLOBAL.PIH[5]=0.449722325;
    GLOBAL.PIH[6]=1.532543502;
    GLOBAL.PIH[7]=0.823954091;
    GLOBAL.PIH[8]=0.109589041;
    GLOBAL.PIH[9]=0.601369863;
    GLOBAL.PIH[10]=0.987819326;
    GLOBAL.PIH[11]=0.104961126;
    }

    GLOBAL.Q1=GLOBAL.sigH+GLOBAL.muH;
    GLOBAL.Q2=GLOBAL.gam+GLOBAL.muH;
//Since the community index vulnerability index (as found by Makayla and Alan) a high incidence we 
//assign mosquito populations such that the basic reprodution number is greater than one on each hot spot. Assume a a Basic reproduction number between 4 and 5
    for(int i=1;i<=Nodes;i++)
    {
        if(!SEED_INFECTION_FROM_FILE){
        GLOBAL.R0[i]=4+drand48();
        GLOBAL.muM[i]=1/16.0;//---------vector death rate
        }
        GLOBAL.Qv[i]=GLOBAL.muM[i]+GLOBAL.sigM;
        GLOBAL.PIM[i]=GLOBAL.R0[i]*GLOBAL.R0[i]*GLOBAL.muM[i]*GLOBAL.muM[i]*GLOBAL.Qv[i]*GLOBAL.Q1*GLOBAL.Q2*GLOBAL.PIH[i]/(GLOBAL.b*GLOBAL.bet1*GLOBAL.bet2*GLOBAL.sigM*GLOBAL.sigH*GLOBAL.muH);

        y0[i]=GLOBAL.PIM[i]*0.4/GLOBAL.muM[i];//Susceptible Mosquitoes
        y0[Nodes+i]=GLOBAL.PIM[i]*0.03/GLOBAL.muM[i];//latent Mosquitoes
        y0[2*Nodes+i]=GLOBAL.PIM[i]*0.57/GLOBAL.muM[i];//Infectious Mosquitoes

        y0[3*Nodes+i]=GLOBAL.PIH[i]*.3/GLOBAL.muH-2*I[i]-1;//Susceptible Humans
        y0[4*Nodes+i]=2*I[i];//Latent humans
        y0[5*Nodes+i]=I[i];//Infectious humans
        y0[6*Nodes+i]=1;//Recovered humans

    }

}

void writeMatrixToCSV(matrix<double>& matrix, const std::string& fileName) {
std::ofstream file(GLOBAL.input_base + fileName);

       if (file.is_open()) {
        for (const auto& row : matrix) {
            for (size_t i = 1; i <row.size(); ++i) {
                file << row[i];

                // Add comma separator for all elements except the last one
                if (i < row.size() - 1) {
                    file << ",";
                }
            }

            file << "\n";
        }

        file.close();
        std::cout << "Matrix elements written to " << GLOBAL.input_base << "" << fileName << " successfully." << std::endl;
    } else {
        std::cout << "Unable to open file: " << GLOBAL.input_base << "/" << fileName << std::endl;
    }

}
// vector<network> init_network(){
// //Read adjacency matrix from a file  auto indivJSON = readJSONFile(GLOBAL.input_base + "individual_diversity_new_infections_travel_prob_revised_FPL.json");//"individuals.json");
// //  auto variantJSON = readJSONFile(GLOBAL.input_base + "cases_variant_prop.json");//reading variant proportions...Shakir Jun 14 2022.
// printf("I have read the files testing\n");
//   auto size = indivJSON.GetArray().Size();
//     std::cout<<"diversity read \t"<<size<<std::endl;

//   GLOBAL.num_people = size;
//   vector<agent> nodes(size);
//   auto community_infection_prob = compute_prob_infection_given_community(GLOBAL.INIT_FRAC_INFECTED, GLOBAL.USE_SAME_INFECTION_PROB_FOR_ALL_WARDS);

// //-----------Reading and printing proportion of variants on the START_DAY---//Shakir -put on Jun 14 2022.
// double p0,p1,p2,p3,p4,p5,p6,vaccNum,totvacc1=0;
// int tstep,yes=0,vac1,vac2,wan,boost;
// double race_trasnpo[]={0.5,1.3,1.1,1.05,1.05,1.25,1.05};

//   count_type i = 0;
//   vector<count_type> seed_candidates;
//   seed_candidates.reserve(size);
//  // count_type travellers=0;//---delete shakir after verifying travellers
//   for (auto &elem: indivJSON.GetArray()){
//  	nodes[i].loc = location{elem["lat"].GetDouble(),
// 							elem["lon"].GetDouble()};
// 	nodes[i].id=elem["id"].GetInt();

// #ifdef DEBUG
// 	assert(elem["age"].IsInt());
// #endif
// 	int age = elem["age"].GetInt();
// 	nodes[i].age = age;
// 	nodes[i].age_group = get_age_group(age);
// 	nodes[i].age_index = get_age_index(age);
// 	nodes[i].age_trans_index=get_agetrans_index(age);
//   }
// }

void getAvector(){
    //Node number and the name of it's associated cluster

//1 Ah
//2 Malau 0.118807849
//3 Limbong
//4 Kuala Kedah

//5 Padang Kerbau
//6 Sik

//7 Semeling
//8 Kota
//9 Pinang Tunggal

//10 Lunas
//11 Mahang

for(int i=1;i<=GLOBAL.Nodes;i++)
   {
   for(int j=1;j<=GLOBAL.Nodes;j++)
      {
        GLOBAL.A[(i-1)*GLOBAL.Nodes+j]=0;
      }
   }

//Making all to  all conections i.e. homogenoeus network

//Connetions for node 1 Ah

GLOBAL.A[(1-1)*GLOBAL.Nodes+2]=1;
GLOBAL.A[(2-1)*GLOBAL.Nodes+1]=1;

GLOBAL.A[(1-1)*GLOBAL.Nodes+3]=1;
GLOBAL.A[(3-1)*GLOBAL.Nodes+1]=1;

GLOBAL.A[(1-1)*GLOBAL.Nodes+4]=1;
GLOBAL.A[(4-1)*GLOBAL.Nodes+1]=1;

GLOBAL.A[(1-1)*GLOBAL.Nodes+5]=0;
GLOBAL.A[(5-1)*GLOBAL.Nodes+1]=0;

GLOBAL.A[(1-1)*GLOBAL.Nodes+6]=0;
GLOBAL.A[(6-1)*GLOBAL.Nodes+1]=0;

GLOBAL.A[(1-1)*GLOBAL.Nodes+7]=0;
GLOBAL.A[(7-1)*GLOBAL.Nodes+1]=0;

GLOBAL.A[(1-1)*GLOBAL.Nodes+8]=0;
GLOBAL.A[(8-1)*GLOBAL.Nodes+1]=0;

GLOBAL.A[(1-1)*GLOBAL.Nodes+9]=0;
GLOBAL.A[(9-1)*GLOBAL.Nodes+1]=0;

GLOBAL.A[(1-1)*GLOBAL.Nodes+10]=0;
GLOBAL.A[(10-1)*GLOBAL.Nodes+1]=0;

GLOBAL.A[(1-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+1]=0;

//Connections for node 2 Malau

GLOBAL.A[(2-1)*GLOBAL.Nodes+1]=1;
GLOBAL.A[(1-1)*GLOBAL.Nodes+2]=1;

GLOBAL.A[(2-1)*GLOBAL.Nodes+3]=1;
GLOBAL.A[(3-1)*GLOBAL.Nodes+2]=1;

GLOBAL.A[(2-1)*GLOBAL.Nodes+4]=1;
GLOBAL.A[(4-1)*GLOBAL.Nodes+2]=1;

GLOBAL.A[(2-1)*GLOBAL.Nodes+5]=1;
GLOBAL.A[(5-1)*GLOBAL.Nodes+2]=1;

GLOBAL.A[(2-1)*GLOBAL.Nodes+6]=0;
GLOBAL.A[(6-1)*GLOBAL.Nodes+2]=0;

GLOBAL.A[(2-1)*GLOBAL.Nodes+7]=0;
GLOBAL.A[(7-1)*GLOBAL.Nodes+2]=0;

GLOBAL.A[(2-1)*GLOBAL.Nodes+8]=0;
GLOBAL.A[(8-1)*GLOBAL.Nodes+2]=0;

GLOBAL.A[(2-1)*GLOBAL.Nodes+9]=0;
GLOBAL.A[(9-1)*GLOBAL.Nodes+2]=0;

GLOBAL.A[(2-1)*GLOBAL.Nodes+10]=0;
GLOBAL.A[(10-1)*GLOBAL.Nodes+2]=0;

GLOBAL.A[(2-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+2]=0;
//Connections for node 3 Limbong

GLOBAL.A[(3-1)*GLOBAL.Nodes+1]=1;
GLOBAL.A[(1-1)*GLOBAL.Nodes+3]=1;

GLOBAL.A[(3-1)*GLOBAL.Nodes+2]=1;
GLOBAL.A[(2-1)*GLOBAL.Nodes+3]=1;

GLOBAL.A[(3-1)*GLOBAL.Nodes+4]=1;
GLOBAL.A[(4-1)*GLOBAL.Nodes+3]=1;

GLOBAL.A[(3-1)*GLOBAL.Nodes+5]=1;
GLOBAL.A[(5-1)*GLOBAL.Nodes+3]=1;

GLOBAL.A[(3-1)*GLOBAL.Nodes+6]=0;
GLOBAL.A[(6-1)*GLOBAL.Nodes+3]=0;

GLOBAL.A[(3-1)*GLOBAL.Nodes+7]=0;
GLOBAL.A[(7-1)*GLOBAL.Nodes+3]=0;

GLOBAL.A[(3-1)*GLOBAL.Nodes+8]=0;
GLOBAL.A[(8-1)*GLOBAL.Nodes+3]=0;

GLOBAL.A[(3-1)*GLOBAL.Nodes+9]=0;
GLOBAL.A[(9-1)*GLOBAL.Nodes+3]=0;

GLOBAL.A[(3-1)*GLOBAL.Nodes+10]=0;
GLOBAL.A[(10-1)*GLOBAL.Nodes+3]=0;

GLOBAL.A[(3-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+3]=0;

//Connections for node 4 Kuala Kedah
GLOBAL.A[(4-1)*GLOBAL.Nodes+1]=1;
GLOBAL.A[(1-1)*GLOBAL.Nodes+4]=1;

GLOBAL.A[(4-1)*GLOBAL.Nodes+2]=1;
GLOBAL.A[(2-1)*GLOBAL.Nodes+4]=1;

GLOBAL.A[(4-1)*GLOBAL.Nodes+3]=1;
GLOBAL.A[(3-1)*GLOBAL.Nodes+4]=1;

GLOBAL.A[(4-1)*GLOBAL.Nodes+5]=0;
GLOBAL.A[(5-1)*GLOBAL.Nodes+4]=0;

GLOBAL.A[(4-1)*GLOBAL.Nodes+6]=0;
GLOBAL.A[(6-1)*GLOBAL.Nodes+4]=0;

GLOBAL.A[(4-1)*GLOBAL.Nodes+7]=0;
GLOBAL.A[(7-1)*GLOBAL.Nodes+4]=0;

GLOBAL.A[(4-1)*GLOBAL.Nodes+8]=0;
GLOBAL.A[(8-1)*GLOBAL.Nodes+4]=0;

GLOBAL.A[(4-1)*GLOBAL.Nodes+9]=0;
GLOBAL.A[(9-1)*GLOBAL.Nodes+4]=0;

GLOBAL.A[(4-1)*GLOBAL.Nodes+10]=0;
GLOBAL.A[(10-1)*GLOBAL.Nodes+4]=0;

GLOBAL.A[(4-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+4]=0;
//Connections for node 5 Pedang Karbeu
GLOBAL.A[(5-1)*GLOBAL.Nodes+1]=0;
GLOBAL.A[(1-1)*GLOBAL.Nodes+5]=0;

GLOBAL.A[(5-1)*GLOBAL.Nodes+2]=1;
GLOBAL.A[(2-1)*GLOBAL.Nodes+5]=1;

GLOBAL.A[(5-1)*GLOBAL.Nodes+3]=1;
GLOBAL.A[(3-1)*GLOBAL.Nodes+5]=1;

GLOBAL.A[(5-1)*GLOBAL.Nodes+4]=0;
GLOBAL.A[(4-1)*GLOBAL.Nodes+5]=0;

GLOBAL.A[(5-1)*GLOBAL.Nodes+6]=1;
GLOBAL.A[(6-1)*GLOBAL.Nodes+5]=1;

GLOBAL.A[(5-1)*GLOBAL.Nodes+7]=0;
GLOBAL.A[(7-1)*GLOBAL.Nodes+5]=0;

GLOBAL.A[(5-1)*GLOBAL.Nodes+8]=1;
GLOBAL.A[(8-1)*GLOBAL.Nodes+5]=1;

GLOBAL.A[(5-1)*GLOBAL.Nodes+9]=0;
GLOBAL.A[(9-1)*GLOBAL.Nodes+5]=0;

GLOBAL.A[(5-1)*GLOBAL.Nodes+10]=0;
GLOBAL.A[(10-1)*GLOBAL.Nodes+5]=0;

GLOBAL.A[(5-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+5]=0;
//Connections for node 6 Sik
GLOBAL.A[(6-1)*GLOBAL.Nodes+1]=0;
GLOBAL.A[(1-1)*GLOBAL.Nodes+6]=0;

GLOBAL.A[(6-1)*GLOBAL.Nodes+2]=0;
GLOBAL.A[(2-1)*GLOBAL.Nodes+6]=0;

GLOBAL.A[(6-1)*GLOBAL.Nodes+3]=0;
GLOBAL.A[(3-1)*GLOBAL.Nodes+6]=0;

GLOBAL.A[(6-1)*GLOBAL.Nodes+4]=0;
GLOBAL.A[(4-1)*GLOBAL.Nodes+6]=0;

GLOBAL.A[(6-1)*GLOBAL.Nodes+5]=1;
GLOBAL.A[(5-1)*GLOBAL.Nodes+6]=1;

GLOBAL.A[(6-1)*GLOBAL.Nodes+7]=1;
GLOBAL.A[(7-1)*GLOBAL.Nodes+6]=1;

GLOBAL.A[(6-1)*GLOBAL.Nodes+8]=0;
GLOBAL.A[(8-1)*GLOBAL.Nodes+6]=0;

GLOBAL.A[(6-1)*GLOBAL.Nodes+9]=0;
GLOBAL.A[(9-1)*GLOBAL.Nodes+6]=0;

GLOBAL.A[(6-1)*GLOBAL.Nodes+10]=0;
GLOBAL.A[(10-1)*GLOBAL.Nodes+6]=0;

GLOBAL.A[(6-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+6]=0;
//Connections for node 7 Semeling
GLOBAL.A[(7-1)*GLOBAL.Nodes+1]=0;
GLOBAL.A[(1-1)*GLOBAL.Nodes+7]=0;

GLOBAL.A[(7-1)*GLOBAL.Nodes+2]=0;
GLOBAL.A[(2-1)*GLOBAL.Nodes+7]=0;

GLOBAL.A[(7-1)*GLOBAL.Nodes+3]=0;
GLOBAL.A[(3-1)*GLOBAL.Nodes+7]=0;

GLOBAL.A[(7-1)*GLOBAL.Nodes+4]=0;
GLOBAL.A[(4-1)*GLOBAL.Nodes+7]=0;

GLOBAL.A[(7-1)*GLOBAL.Nodes+5]=0;
GLOBAL.A[(5-1)*GLOBAL.Nodes+7]=0;

GLOBAL.A[(7-1)*GLOBAL.Nodes+6]=1;
GLOBAL.A[(6-1)*GLOBAL.Nodes+7]=1;

GLOBAL.A[(7-1)*GLOBAL.Nodes+8]=1;
GLOBAL.A[(8-1)*GLOBAL.Nodes+7]=1;

GLOBAL.A[(7-1)*GLOBAL.Nodes+9]=1;
GLOBAL.A[(9-1)*GLOBAL.Nodes+7]=1;

GLOBAL.A[(7-1)*GLOBAL.Nodes+10]=1;
GLOBAL.A[(10-1)*GLOBAL.Nodes+7]=1;

GLOBAL.A[(7-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+7]=0;
//Connections for node 8 Kota
GLOBAL.A[(8-1)*GLOBAL.Nodes+1]=0;
GLOBAL.A[(1-1)*GLOBAL.Nodes+8]=0;

GLOBAL.A[(8-1)*GLOBAL.Nodes+2]=0;
GLOBAL.A[(2-1)*GLOBAL.Nodes+8]=0;

GLOBAL.A[(8-1)*GLOBAL.Nodes+3]=0;
GLOBAL.A[(3-1)*GLOBAL.Nodes+8]=0;

GLOBAL.A[(8-1)*GLOBAL.Nodes+4]=0;
GLOBAL.A[(4-1)*GLOBAL.Nodes+8]=0;

GLOBAL.A[(8-1)*GLOBAL.Nodes+5]=0;
GLOBAL.A[(5-1)*GLOBAL.Nodes+8]=0;

GLOBAL.A[(8-1)*GLOBAL.Nodes+6]=0;
GLOBAL.A[(6-1)*GLOBAL.Nodes+8]=0;

GLOBAL.A[(8-1)*GLOBAL.Nodes+7]=1;
GLOBAL.A[(7-1)*GLOBAL.Nodes+8]=1;

GLOBAL.A[(8-1)*GLOBAL.Nodes+9]=1;
GLOBAL.A[(9-1)*GLOBAL.Nodes+8]=1;

GLOBAL.A[(8-1)*GLOBAL.Nodes+10]=1;
GLOBAL.A[(10-1)*GLOBAL.Nodes+8]=1;

GLOBAL.A[(8-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+8]=0;
//Connections for node 9 Pinang Tunggal
GLOBAL.A[(9-1)*GLOBAL.Nodes+1]=0;
GLOBAL.A[(1-1)*GLOBAL.Nodes+9]=0;

GLOBAL.A[(9-1)*GLOBAL.Nodes+2]=0;
GLOBAL.A[(2-1)*GLOBAL.Nodes+9]=0;

GLOBAL.A[(9-1)*GLOBAL.Nodes+3]=0;
GLOBAL.A[(3-1)*GLOBAL.Nodes+9]=0;

GLOBAL.A[(9-1)*GLOBAL.Nodes+4]=0;
GLOBAL.A[(4-1)*GLOBAL.Nodes+9]=0;

GLOBAL.A[(9-1)*GLOBAL.Nodes+5]=0;
GLOBAL.A[(5-1)*GLOBAL.Nodes+9]=0;

GLOBAL.A[(9-1)*GLOBAL.Nodes+6]=0;
GLOBAL.A[(6-1)*GLOBAL.Nodes+9]=0;

GLOBAL.A[(9-1)*GLOBAL.Nodes+7]=1;
GLOBAL.A[(7-1)*GLOBAL.Nodes+9]=1;

GLOBAL.A[(9-1)*GLOBAL.Nodes+8]=1;
GLOBAL.A[(8-1)*GLOBAL.Nodes+9]=1;

GLOBAL.A[(9-1)*GLOBAL.Nodes+10]=1;
GLOBAL.A[(10-1)*GLOBAL.Nodes+9]=1;

GLOBAL.A[(9-1)*GLOBAL.Nodes+11]=0;
GLOBAL.A[(11-1)*GLOBAL.Nodes+9]=0;

//Connections for node 10 Lunas
GLOBAL.A[(10-1)*GLOBAL.Nodes+1]=0;
GLOBAL.A[(1-1)*GLOBAL.Nodes+10]=0;

GLOBAL.A[(10-1)*GLOBAL.Nodes+2]=0;
GLOBAL.A[(2-1)*GLOBAL.Nodes+10]=0;

GLOBAL.A[(10-1)*GLOBAL.Nodes+3]=0;
GLOBAL.A[(3-1)*GLOBAL.Nodes+10]=0;

GLOBAL.A[(10-1)*GLOBAL.Nodes+4]=0;
GLOBAL.A[(4-1)*GLOBAL.Nodes+10]=0;

GLOBAL.A[(10-1)*GLOBAL.Nodes+5]=0;
GLOBAL.A[(5-1)*GLOBAL.Nodes+10]=0;

GLOBAL.A[(10-1)*GLOBAL.Nodes+6]=0;
GLOBAL.A[(6-1)*GLOBAL.Nodes+10]=0;

GLOBAL.A[(10-1)*GLOBAL.Nodes+7]=1;
GLOBAL.A[(7-1)*GLOBAL.Nodes+10]=1;

GLOBAL.A[(10-1)*GLOBAL.Nodes+8]=1;
GLOBAL.A[(8-1)*GLOBAL.Nodes+10]=1;

GLOBAL.A[(10-1)*GLOBAL.Nodes+9]=1;
GLOBAL.A[(9-1)*GLOBAL.Nodes+10]=1;

GLOBAL.A[(10-1)*GLOBAL.Nodes+11]=1;
GLOBAL.A[(11-1)*GLOBAL.Nodes+10]=1;
//Connections for node 11 Mahang
GLOBAL.A[(11-1)*GLOBAL.Nodes+1]=0;
GLOBAL.A[(1-1)*GLOBAL.Nodes+11]=0;

GLOBAL.A[(11-1)*GLOBAL.Nodes+2]=0;
GLOBAL.A[(2-1)*GLOBAL.Nodes+11]=0;

GLOBAL.A[(11-1)*GLOBAL.Nodes+3]=0;
GLOBAL.A[(3-1)*GLOBAL.Nodes+11]=0;

GLOBAL.A[(11-1)*GLOBAL.Nodes+4]=0;
GLOBAL.A[(4-1)*GLOBAL.Nodes+11]=0;

GLOBAL.A[(11-1)*GLOBAL.Nodes+5]=0;
GLOBAL.A[(5-1)*GLOBAL.Nodes+11]=0;

GLOBAL.A[(11-1)*GLOBAL.Nodes+6]=0;
GLOBAL.A[(6-1)*GLOBAL.Nodes+11]=0;

GLOBAL.A[(11-1)*GLOBAL.Nodes+7]=0;
GLOBAL.A[(7-1)*GLOBAL.Nodes+11]=0;


GLOBAL.A[(11-1)*GLOBAL.Nodes+8]=0;
GLOBAL.A[(8-1)*GLOBAL.Nodes+11]=0;

GLOBAL.A[(11-1)*GLOBAL.Nodes+9]=0;
GLOBAL.A[(9-1)*GLOBAL.Nodes+11]=0;

GLOBAL.A[(11-1)*GLOBAL.Nodes+10]=1;
GLOBAL.A[(10-1)*GLOBAL.Nodes+11]=1;
//No mosquito movement hence the matrix GLOBAL.B is taken to be identity
/*
GLOBAL.B[(1-1)*GLOBAL.Nodes+2]=1;
GLOBAL.B[(2-1)*GLOBAL.Nodes+1]=1;


GLOBAL.B[(3-1)*GLOBAL.Nodes+2]=1;
GLOBAL.B[(2-1)*GLOBAL.Nodes+3]=1;

GLOBAL.B[(4-1)*GLOBAL.Nodes+5]=1;
GLOBAL.B[(5-1)*GLOBAL.Nodes+4]=1;

GLOBAL.B[(7-1)*GLOBAL.Nodes+5]=1;
GLOBAL.B[(5-1)*GLOBAL.Nodes+7]=1;

GLOBAL.B[(8-1)*GLOBAL.Nodes+9]=1;
GLOBAL.B[(9-1)*GLOBAL.Nodes+8]=1;

GLOBAL.B[(6-1)*GLOBAL.Nodes+10]=1;
GLOBAL.B[(10-1)*GLOBAL.Nodes+6]=1;
*/

GLOBAL.A[(1-1)*GLOBAL.Nodes+1]=1;
GLOBAL.A[(2-1)*GLOBAL.Nodes+2]=1;
GLOBAL.A[(3-1)*GLOBAL.Nodes+3]=1;
GLOBAL.A[(4-1)*GLOBAL.Nodes+4]=1;
GLOBAL.A[(5-1)*GLOBAL.Nodes+5]=1;
GLOBAL.A[(6-1)*GLOBAL.Nodes+6]=1;
GLOBAL.A[(7-1)*GLOBAL.Nodes+7]=1;
GLOBAL.A[(8-1)*GLOBAL.Nodes+8]=1;
GLOBAL.A[(9-1)*GLOBAL.Nodes+9]=1;
GLOBAL.A[(10-1)*GLOBAL.Nodes+10]=1;
GLOBAL.A[(11-1)*GLOBAL.Nodes+11]=1;


return ;
}

void getBvector(){

for(int i=1;i<=GLOBAL.Nodes;i++)
   {
   for(int j=1;j<=GLOBAL.Nodes;j++)
      {
        GLOBAL.B[(i-1)*GLOBAL.Nodes+j]=0;
      }
   }

GLOBAL.B[(1-1)*GLOBAL.Nodes+1]=1;
GLOBAL.B[(2-1)*GLOBAL.Nodes+2]=1;
GLOBAL.B[(3-1)*GLOBAL.Nodes+3]=1;
GLOBAL.B[(4-1)*GLOBAL.Nodes+4]=1;
GLOBAL.B[(5-1)*GLOBAL.Nodes+5]=1;
GLOBAL.B[(6-1)*GLOBAL.Nodes+6]=1;
GLOBAL.B[(7-1)*GLOBAL.Nodes+7]=1;
GLOBAL.B[(8-1)*GLOBAL.Nodes+8]=1;
GLOBAL.B[(9-1)*GLOBAL.Nodes+9]=1;
GLOBAL.B[(10-1)*GLOBAL.Nodes+10]=1;
GLOBAL.B[(11-1)*GLOBAL.Nodes+11]=1;

return ;
}