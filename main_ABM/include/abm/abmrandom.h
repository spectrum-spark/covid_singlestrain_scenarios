#ifndef WANEWORLD_ABM_ABMRANDOM_H 
#define WANEWORLD_ABM_ABMRANDOM_H
#include<random> 
/**
 * @brief Define random number generation here. This allows for an easy location to alter the seed etc.
 * 
 */
extern std::default_random_engine generator;
extern std::uniform_real_distribution<double> genunf_std;
#endif