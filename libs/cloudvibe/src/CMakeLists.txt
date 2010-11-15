
FILE(GLOB SRCS *.cpp *.h)

ADD_LIBRARY(cloudvibe STATIC
  ${SRCS}
)

TARGET_LINK_LIBRARIES(cloudvibe
  ${CLAM_LIBS}
)

