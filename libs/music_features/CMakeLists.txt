
SET(SRCS main.cc frame_division.cc enumerated.h)

ADD_LIBRARY(music_features SHARED
  ${SRCS}
)

INCLUDE_DIRECTORIES(
  ${CLAM_INCLUDE_DIR}
)

