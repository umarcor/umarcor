# Based on https://github.com/utensils/docker-opengl

ARG LLVM_VERSION=9
ARG MESA_VERSION=20.1.10

#- BASE

FROM alpine:3.12 AS base

RUN apk -U add --no-cache \
    git

#- BUILD

FROM base AS build

ARG LLVM_VERSION
ARG MESA_VERSION

RUN apk add --no-cache \
    autoconf \
    automake \
    bison \
    build-base \
    cmake \
    curl \
    elfutils-dev \
    expat-dev \
    flex \
    gettext \
    glproto \
    libdrm-dev \
    libtool \
    libva-dev \
    libx11-dev \
    libxcb-dev \
    libxdamage-dev \
    libxext-dev \
    libxfixes-dev \
    libxrandr-dev \
    libxshmfence-dev \
    libxt-dev \
    libxvmc-dev \
    libxxf86vm-dev \
    llvm${LLVM_VERSION} \
    llvm${LLVM_VERSION}-dev \
    makedepend \
    meson \
    py-mako \
    py3-libxml2 \
    py3-mako \
    python3 \
    python3-dev \
    talloc-dev \
    wayland-dev \
    wayland-protocols \
    xorg-server-dev \
    xorgproto \
    zlib-dev \
    zstd-dev \
 && ln -sf /usr/lib/llvm${LLVM_VERSION}/bin/llvm-config /usr/bin/llvm-config

# https://bugs.freedesktop.org/show_bug.cgi?id=107865
RUN mkdir -p /var/tmp/build/mesa \
 && cd /var/tmp/build/mesa \
 && curl -fsSL https://gitlab.freedesktop.org/mesa/mesa/-/archive/mesa-${MESA_VERSION}/mesa-mesa-${MESA_VERSION}.tar.gz | tar xzf - --strip-components=1

RUN cd /var/tmp/build/mesa \
 && libtoolize \
 && meson \
    --buildtype=release \
    --prefix=/usr/local \
    --sysconfdir=/etc \
    -Db_ndebug=true \
    -Degl=true \
    -Dgallium-nine=false \
    -Dgallium-xvmc=false \
    -Dgbm=true \
    -Dgles1=false \
    -Dgles2=true \
    -Dopengl=true \
    -Ddri-drivers-path=/usr/local/lib/xorg/modules/dri \
    -Ddri-drivers= \
    -Ddri3=true  \
    -Degl=false \
    -Dgallium-drivers="swrast,swr" \
    -Dgbm=false \
    -Dglx=dri \
    -Dllvm=true \
    -Dlmsensors=false \
    -Dosmesa=gallium  \
    -Dplatforms=drm,x11,wayland \
    -Dshared-glapi=true \
    -Dshared-llvm=true \
    -Dvulkan-drivers= \
    build/ \
 && ninja -C build/ -j $(getconf _NPROCESSORS_ONLN) \
 && ninja -C build/ install \
 && ninja -C build/ xmlpool-pot xmlpool-update-po xmlpool-gmo

#- IMAGE

FROM base

ARG LLVM_VERSION
ARG MESA_VERSION

COPY --from=build /usr/local /usr/local

RUN apk --update add --no-cache \
    binutils \
    expat \
    ffmpeg \
    gource \
    llvm${LLVM_VERSION}-libs \
    setxkbmap \
    xdpyinfo \
    xrandr \
    xvfb \
    xvfb-run \
    zstd-libs \
 && ln -sf /usr/local/lib/xorg/modules/dri/* /usr/lib/xorg/modules/dri/

ENV \
  DISPLAY=":99" \
  GALLIUM_DRIVER="llvmpipe" \
  LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH" \
  LIBGL_ALWAYS_SOFTWARE="1" \
  LP_DEBUG="" \
  LP_NO_RAST="false" \
  LP_NUM_THREADS="" \
  LP_PERF="" \
  MESA_VERSION="${MESA_VERSION}" \
  XVFB_WHD="1920x1080x24"
