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
	# $(CXX) $(CPPFLAGS) -o Run_BA1s_BA45s main_BA1s_BA45s.cpp $(OBJECTS) 
	# $(CXX) $(CPPFLAGS) -o Run_BA1s_BA45s_cont_intros main_BA1s_BA45s_cont_intros.cpp $(OBJECTS) 
	$(CXX) $(CPPFLAGS) -o Run_BA1s_BA45s_cont_intros_many_boosters main_BA1s_BA45s_cont_intros_many_boosters.cpp $(OBJECTS) 


$(OBJ)/%.o: $(SRC)/%.cpp
	$(CXX) -c $(CPPFLAGS) $< -o $@

clean: 
	# rm build/* Run_BA1s_BA45s
	# rm build/* Run_BA1s_BA45s_cont_intros
	rm build/* Run_BA1s_BA45s_cont_intros_many_boosters
