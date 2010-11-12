
FIND_PATH(CLAM_INCLUDE_DIR CLAMVersion.hxx 
  /usr/include/CLAM
  /usr/local/include/CLAM
  /opt/local/include/CLAM
)

LINK_DIRECTORIES(
  /opt/local/lib
)

SET(CLAM_SHARED_LIBS clam_core clam_processing clam_audioio)

SET(CLAM_STATIC_LIBS
  ${CMAKE_SOURCE_DIR}/libs/clam/scons/libs/core/libclam_core.a
  ${CMAKE_SOURCE_DIR}/libs/clam/scons/libs/processing/libclam_processing.a
  ${CMAKE_SOURCE_DIR}/libs/clam/scons/libs/audioio/libclam_audioio.a
) 

#SET(CLAM_LIBS clam_core clam_processing clam_audioio)

SET(CLAM_LIB_DEPS 
  mad
  ogg
  FLAC
  vorbis
  sndfile
  vorbisenc
  vorbisfile
  id3
  fftw3
  pthread
)

# Use static libs
SET(CLAM_LIBS ${CLAM_STATIC_LIBS} ${CLAM_LIB_DEPS})

FIND_LIBRARY(CLAM_LIBRARY_DIR
  NAMES 
    ${CLAM_LIBS}
  PATH
    /usr/local/lib
    /usr/lib
    /opt/local/lib
)

IF (CLAM_INCLUDE_DIR AND CLAM_LIBRARY_DIR)
  SET(CLAM_FOUND TRUE)
  MESSAGE("-- libCLAM found")
ELSE (CLAM_INCLUDE_DIR AND CLAM_LIBRARY_DIR)
  MESSAGE("-- could not find libCLAM!")
ENDIF (CLAM_INCLUDE_DIR AND CLAM_LIBRARY_DIR)

