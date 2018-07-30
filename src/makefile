#!/bin/bash

CC=g++
CFLAGS= -m64 -std=c++14 -o3 -Wall -fopenmp
LDFLAGS= 
SOURCES= pgm.cpp options.cpp graph.cpp distributions.cpp utils.cpp 

LIBS = 
INCLUDES =

EXEC = pgm
OBJ = $(SOURCES:.cpp=.o)

all: $(EXEC)

pgm: $(SOURCES) 
	$(CC) $(SOURCES) $(LIBS) $(INCLUDES) $(CFLAGS)  $(LDFLAGS) -o $@

   

##########################################
# Generic rules
##########################################

%.o: %.cpp %.h
	$(CC) -o $@ -c $< $(CFLAGS) $(INCLUDES)

%.o: %.cpp
	$(CC) -o $@ -c $< $(CFLAGS) $(INCLUDES)

clean:
	rm -f *.o *~ $(EXEC)
