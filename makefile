CXX = g++
INCLUDE = include
CPPFLAGS = -std=c++2a -DDUMP_INPUT -I$(INCLUDE)
CFLAGS = 
OBJ = build
SRC = src
SOURCES := $(wildcard $(SRC)/*.cpp)
OBJECTS := $(patsubst $(SRC)/%.cpp, $(OBJ)/%.o, $(SOURCES))

all: $(OBJECTS)
	$(CXX) $(CPPFLAGS) -o Run main_plotProtection.cpp $(OBJECTS) -Iinclude -I../../ 

$(OBJ)/%.o: $(SRC)/%.cpp
	$(CXX) -c $(CPPFLAGS) $< -o $@

clean: 
	rm build/* Run

# 	CXX = g++
# CPPFLAGS = -std=c++2a -DDUMP_INPUT
# CFLAGS =
# OBJECTS = covid-abm/build/*.o 

# build_abm:
# 	$(MAKE) -C covid-abm
# 	$(CXX) $(CPPFLAGS) -o Run main_read.cpp $(OBJECTS) -Icovid-abm/include -I../ 

# clean:
# 	rm Run
# 	$(MAKE) clean -C covid-abm