CXX = g++
INCLUDE = include
CPPFLAGS = -std=c++2a -DDUMP_INPUT -I$(INCLUDE)
CFLAGS = 
OBJ = build
SRC = src
SOURCES := $(wildcard $(SRC)/*.cpp)
OBJECTS := $(patsubst $(SRC)/%.cpp, $(OBJ)/%.o, $(SOURCES))
NLOHMANN = ../../json/single_include
all: $(OBJECTS)
	$(CXX) $(CPPFLAGS) -o RunBooster main_plotProtection.cpp $(OBJECTS) -Iinclude -I$(NLOHMANN)
	$(CXX) $(CPPFLAGS) -DDISABLE_BOOSTER -o RunNoBooster main_plotProtection.cpp $(OBJECTS) -Iinclude -I$(NLOHMANN)
	$(CXX) $(CPPFLAGS)  -o Run main_transmission.cpp $(OBJECTS) -Iinclude -I$(NLOHMANN)

$(OBJ)/%.o: $(SRC)/%.cpp
	$(CXX) -c $(CPPFLAGS) $< -o $@

clean: 
	rm build/* Run RunBooster RunNoBooster
