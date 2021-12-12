CXX = g++
INCLUDE = include
CPPFLAGS = -std=c++2a -DDUMP_INPUT -I$(INCLUDE)
CFLAGS = 
OBJ = build
SRC = src
SOURCES := $(wildcard $(SRC)/*.cpp)
OBJECTS := $(patsubst $(SRC)/%.cpp, $(OBJ)/%.o, $(SOURCES))

all: $(OBJECTS)
	$(CXX) $(CPPFLAGS) -o RunBooster main_plotProtection.cpp $(OBJECTS) -Iinclude -I../json/single_include
	$(CXX) $(CPPFLAGS) -DDISABLE_BOOSTER -o RunNoBooster main_plotProtection.cpp $(OBJECTS) -Iinclude -I../json/single_include

$(OBJ)/%.o: $(SRC)/%.cpp
	$(CXX) -c $(CPPFLAGS) $< -o $@

clean: 
	rm build/* Run RunBooster RunNoBooster