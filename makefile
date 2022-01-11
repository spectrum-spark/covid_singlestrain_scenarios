CXX = g++
INCLUDE = include
NLOHMANN = ../../
CPPFLAGS = -std=c++2a -DDUMP_INPUT -I$(INCLUDE) -I$(NLOHMANN)
CFLAGS = 
OBJ = build
SRC = src
SOURCES := $(wildcard $(SRC)/*.cpp)
OBJECTS := $(patsubst $(SRC)/%.cpp, $(OBJ)/%.o, $(SOURCES))


all: $(OBJECTS)
	$(CXX) $(CPPFLAGS) -o RunBooster main_plotProtection.cpp $(OBJECTS) 
	$(CXX) $(CPPFLAGS) -DDISABLE_BOOSTER -o RunNoBooster main_plotProtection.cpp $(OBJECTS)
	$(CXX) $(CPPFLAGS)  -o Run main_transmission.cpp $(OBJECTS) 
	$(CXX) $(CPPFLAGS) -o RunRestrictions main_restrictions.cpp $(OBJECTS)

$(OBJ)/%.o: $(SRC)/%.cpp
	$(CXX) -c $(CPPFLAGS) $< -o $@

clean: 
	rm build/* Run RunRestrictions RunBooster RunNoBooster 
