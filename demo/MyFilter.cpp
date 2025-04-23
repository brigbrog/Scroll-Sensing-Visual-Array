#include "MyFilter.h"

// implementation for MovingAverage struct - takes window array and length integer params.
MovingAverage::MovingAverage(float w[], int len){
  win = w;
  arrayLength = len;
  index = 0;
  total = 0.0;
  for (int i = 0; i < arrayLength; i++) {
    win[i] = 0.0;
  }
}

// update method, calculates the average across the current window and updates the index for the circular array.
float MovingAverage::update(float inVal){

  total = total - win[index] + inVal;
  win[index] = inVal;
  index = (index + 1) % arrayLength;
  return total / arrayLength;
}

// implementation for ZeroCrossing struct - takes no params.
ZeroCrossing::ZeroCrossing() {
  zeroCrosses = 0;
  lastSign = 0;
  startTime = millis();
  bpm = 0.0;
}

// update method, finds the sign of current signal, updates zero cross count and (after 15 seconds) bpm.
float ZeroCrossing::update(float curSig) {
  int curSign = (curSig > 0) ? 1 : (curSig < 0) ? -1 : 0;
  if (curSign != 0 && curSign != lastSign) {
    zeroCrosses++;
    lastSign = curSign;
  }
  unsigned long elapsedTime = millis() - startTime;
  if (elapsedTime >= 15000) {
    bpm = (zeroCrosses / 2.0) * (60.0 / 15.0);
    zeroCrosses = 0;
    startTime = millis();
  }
  return bpm; 
}








