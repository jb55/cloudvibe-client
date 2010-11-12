
FIND_PATH(CLAM_INCLUDE_DIR CLAMVersion.hxx 
  /usr/include/CLAM
  /usr/local/include/CLAM
  /opt/local/include/CLAM
)

FIND_LIBRARY(CLAM_LIBRARY_DIR
  NAMES 
    clam_processing clam_audioio clam_core
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

