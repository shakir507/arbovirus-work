#include "models.h"
#include <cmath>
#include <random>

sys_para GLOBAL;

double f_kernel(double dist){
  double a = GLOBAL.F_KERNEL_A;
  double b = GLOBAL.F_KERNEL_B;
  return 1.0/(1.0 + pow(dist/a,b));
}