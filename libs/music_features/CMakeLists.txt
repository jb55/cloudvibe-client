
SET(SRCS main.cc frame_division.h enumerated.h)

ADD_LIBRARY(music_features SHARED
  ${SRCS}
)

INCLUDE_DIRECTORIES(
  ${CLAM_INCLUDE_DIR}
)

