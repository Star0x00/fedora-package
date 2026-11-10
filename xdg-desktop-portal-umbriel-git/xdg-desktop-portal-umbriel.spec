%global snap_date %(date -u +%%Y%%m%%d)

Name:           xdg-desktop-portal-umbriel
Version:        0.1.0
Release:        1.%{snap_date}%{?dist}
Summary:        xdg-desktop-portal backend for the Umbriel compositor

License:        MIT
URL:            https://github.com/noctalia-dev/xdg-desktop-portal-umbriel
Source0:        https://github.com/noctalia-dev/xdg-desktop-portal-umbriel/archive/refs/heads/main.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  systemd-rpm-macros
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.39
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(gtk4) >= 4.12
BuildRequires:  pkgconfig(libei) == 1.0

%description
An xdg-desktop-portal backend for the Umbriel compositor, implementing the
ScreenCast and Screenshot portal interfaces. Screen capture is delivered
through PipeWire, and the optional GTK4 share picker provides a thumbnail
grid for selecting screens and windows.

%prep
# GitHub branch archives extract into xdg-desktop-portal-umbriel-main/
%autosetup -n xdg-desktop-portal-umbriel-main

%build
%meson -Dpicker=enabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libexecdir}/xdg-desktop-portal-umbriel
%{_libexecdir}/umbriel-share-picker
%{_datadir}/xdg-desktop-portal/portals/umbriel.portal
%{_datadir}/xdg-desktop-portal/umbriel-portals.conf
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.umbriel.service
%{_userunitdir}/xdg-desktop-portal-umbriel.service

%changelog
%autochangelog
