#ifndef MyFilter_h
#define MyFilter_h

#include <Arduino.h>

struct MovingAverage {
  float total;
  int arrayLength;
  int index;
  float *win;

  //constructor
  //define the window array inside your .ino file
  MovingAverage(float w[], int len);

  //update the window with the input value and return the average
  float update( float inVal);
};

struct ZeroCrossing { 
  int zeroCrosses;
  int lastSign;
  unsigned long startTime;
  float bpm;

  ZeroCrossing();
  float update(float currentSignal);
};

#endif