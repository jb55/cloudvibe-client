
FIND_PATH(CLAM_INCLUDE_DIR CLAMVersion.hxx 
  /usr/include/CLAM
  /usr/local/include/CLAM
  /opt/local/include/CLAM
)

IF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
  SET(PlatformLinux True)
ENDIF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")

LINK_DIRECTORIES(
  /opt/local/lib
)

SET(CLAM_SHARED_LIBS clam_core clam_processing clam_audioio)

SET(CLAM_STATIC_LIBS
  ${CMAKE_SOURCE_DIR}/libs/clam/scons/libs/core/libclam_core.a
  ${CMAKE_SOURCE_DIR}/libs/clam/scons/libs/processing/libclam_processing.a
  ${CMAKE_SOURCE_DIR}/libs/clam/scons/libs/audioio/libclam_audioio.a
) 

ADD_DEFINITIONS(-DUSE_SNDFILE -DUSE_FFTW3 -DUSE_MAD -DUSE_OGGVORBIS)

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
)

IF (PlatformLinux)
  SET(CLAM_LIB_DEPS ${CLAM_LIB_DEPS}
    dl
  )

  # Used shared libs on linux for now
  SET(CLAM_LIBS ${CLAM_SHARED_LIBS} ${CLAM_LIB_DEPS})
ELSE (PlatformLinux)

  # Static libs on osx
  SET(CLAM_LIBS ${CLAM_STATIC_LIBS} ${CLAM_LIB_DEPS})
ENDIF (PlatformLinux)

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

