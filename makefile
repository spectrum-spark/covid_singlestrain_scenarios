CXX = g++
INCLUDE = include
NLOHMANN = ../../json/single_include
CPPFLAGS = -std=c++2a -DDUMP_INPUT -I$(INCLUDE) -I$(NLOHMANN)
CFLAGS = 
OBJ = build
SRC = src
SOURCES := $(wildcard $(SRC)/*.cpp)
OBJECTS := $(patsubst $(SRC)/%.cpp, $(OBJ)/%.o, $(SOURCES))


all: $(OBJECTS)
	$(CXX) $(CPPFLAGS) -o RunGenerateInitial main_generate_initial_conditions.cpp $(OBJECTS) 
	$(CXX) $(CPPFLAGS) -o RunWinterWave main_winterwave.cpp $(OBJECTS) 

$(OBJ)/%.o: $(SRC)/%.cpp
	$(CXX) -c $(CPPFLAGS) $< -o $@

clean: 
	rm build/* RunGenerateInitial RunWinterWave
