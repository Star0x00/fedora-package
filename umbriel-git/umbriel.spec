%global snap_date %(date -u +%%Y%%m%%d)

Name:           umbriel
Version:        0.1.0
Release:        1.%{snap_date}%{?dist}
Summary:        A Wayland compositor built on wlroots

License:        MIT
URL:            https://github.com/noctalia-dev/umbriel
Source0:        https://github.com/noctalia-dev/umbriel/archive/refs/heads/main.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  git-core
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(wayland-server) >= 1.24
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.1
BuildRequires:  pkgconfig(xkbcommon) >= 1.10.0
BuildRequires:  pkgconfig(libinput) >= 1.29
BuildRequires:  pkgconfig(libeis-1.0) >= 1.3
BuildRequires:  pkgconfig(libdisplay-info) >= 0.3.0
BuildRequires:  pkgconfig(libsystemd) >= 243
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(jemalloc)

Recommends:     xdg-desktop-portal-umbriel

%description
Umbriel is a Wayland compositor designed for daily use, with scrolling,
dwindle, and master layouts, per-output workspaces, window rules, blur,
shadows, and fluid animations. It is built in C++23 on wlroots.

Xwayland support comes from xwayland-satellite, and portal screen capture and
sharing is provided by xdg-desktop-portal-umbriel.

%prep
# GitHub branch archives extract into umbriel-main/
%autosetup -n umbriel-main

%build
%meson \
  -Dtests=disabled \
  -Djemalloc=enabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md CONTRIBUTING.md PACKAGING.md SCOPE.md
%{_bindir}/umbriel
%{_bindir}/start-umbriel
%{_datadir}/umbriel/config.toml
%{_datadir}/umbriel/effects/
%{_datadir}/wayland-sessions/umbriel.desktop
%{_userunitdir}/umbriel.service
%{_userunitdir}/umbriel-session.target
%{_userunitdir}/umbriel-shutdown.target

%changelog
%autochangelog
