#ifndef _CLOUDVIBE_SONG_H_
#define _CLOUDVIBE_SONG_H_
#pragma once

namespace cloudvibe {


class Song 
{
public:
  Song();
  ~Song();

  void open(const char* filename);
};


} /* namespace cloudvibe */

#endif /* _CLOUDVIBE_SONG_H_ */
