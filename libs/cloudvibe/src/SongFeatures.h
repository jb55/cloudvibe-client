#ifndef _CLOUDVIBE_SONG_FEATURES_H_
#define _CLOUDVIBE_SONG_FEATURES_H_
#pragma once

namespace cloudvibe {

class Song;

enum Mood {
  kHappy,
  kAngry,
  kSad,
  kCalm
};

class SongFeatures 
{
public:
  SongFeatures(Song* song);
  ~SongFeatures();

  // Run complicated song analysis, call this on a thread if needed
  void calculate();

  Mood mood();
};


} /* namespace cloudvibe */


#endif /* _CLOUDVIBE_SONG_FEATURES_H_ */

