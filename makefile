CXX = g++
INCLUDE = include
NLOHMANN = ../../json/single_include
CPPFLAGS = -std=c++2a -DDUMP_INPUT -I$(INCLUDE) -I$(NLOHMANN)
CFLAGS = 
OBJ = build
SRC = src
SOURCES := $(wildcard $(SRC)/*.cpp)
# SOURCES := $(filter-out src/ibm_simulation_4th_doses.cpp, $(SOURCES)) 
SOURCES := $(filter-out src/ibm_simulation.cpp, $(SOURCES))

OBJECTS := $(patsubst $(SRC)/%.cpp, $(OBJ)/%.o, $(SOURCES))
# OBJECTS := $(filter-out build/ibm_simulation_4th_doses.o, $(OBJECTS))
OBJECTS := $(filter-out build/ibm_simulation.o, $(OBJECTS))

all: $(OBJECTS)
	# $(CXX) $(CPPFLAGS) -o RunWinter main_winter.cpp $(OBJECTS) 
	# $(CXX) $(CPPFLAGS) -o RunContinuous main_continuous_simulation.cpp $(OBJECTS) 
	# $(CXX) $(CPPFLAGS) -o RunContinuousDoubleExposure main_continuous_simulation_double_exposure.cpp $(OBJECTS) 
	# $(CXX) $(CPPFLAGS) -o RunContinuousFirstAndContExposure main_continuous_simulation_first_then_continuous_exposure.cpp $(OBJECTS) 
	# $(CXX) $(CPPFLAGS) -o RunContinuousContExposure main_continuous_simulation_continuous_exposure.cpp $(OBJECTS) 
	# $(CXX) $(CPPFLAGS) -o RunContinuousDoubleExposureNoTTIQ main_continuous_simulation_double_exposure_no_ttiq.cpp $(OBJECTS) 
	# $(CXX) $(CPPFLAGS) -o RunContinuousDoubleExposureNoTTIQibm4thdoses main_continuous_simulation_double_exposure_no_ttiq_ibm_4th_doses.cpp $(OBJECTS) 
	$(CXX) $(CPPFLAGS) -o RunNoTTIQibm4thdosesnewstrain main_continuous_simulation_double_exposure_no_ttiq_ibm_4th_doses_newstrain.cpp $(OBJECTS) 


$(OBJ)/%.o: $(SRC)/%.cpp
	$(CXX) -c $(CPPFLAGS) $< -o $@

clean: 
	# rm build/* RunWinter RunContinuous RunContinuousDoubleExposure RunContinuousFirstAndContExposure RunContinuousContExposure
	# rm build/* RunContinuousDoubleExposureNoTTIQ 
	# rm build/* RunContinuousDoubleExposureNoTTIQibm4thdoses
	rm build/* RunNoTTIQibm4thdosesnewstrain
