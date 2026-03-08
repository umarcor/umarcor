# Based on https://github.com/utensils/docker-opengl

FROM alpine:3.22 AS base

RUN apk -U add --no-cache \
    binutils \
    expat \
    ffmpeg \
    git \
    gource \
    llvm20-libs \
    mesa-dri-gallium \
    setxkbmap \
    xdpyinfo \
    xrandr \
    xvfb \
    xvfb-run \
    zstd-libs

ENV \
  DISPLAY=":99" \
  GALLIUM_DRIVER="llvmpipe" \
  LIBGL_ALWAYS_SOFTWARE="1" \
  LP_DEBUG="" \
  LP_NO_RAST="false" \
  LP_NUM_THREADS="" \
  LP_PERF="" \
  XVFB_WHD="1920x1080x24"
