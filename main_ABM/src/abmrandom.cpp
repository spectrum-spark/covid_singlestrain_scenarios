#include "abm/abmrandom.h"
// Allows for a different random seeding method on Windows. _WIN32 should be defined even on 64 bit.
#ifdef _WIN32
    #include <chrono>
    std::default_random_engine generator(std::chrono::system_clock::now().time_since_epoch().count());
#else
    std::random_device rd;
    std::default_random_engine generator(rd());
#endif

std::uniform_real_distribution<double> genunf_std(0.0,1.0);