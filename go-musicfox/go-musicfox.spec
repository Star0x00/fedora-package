# go-musicfox, tracking the upstream v5.1.0 release tag.
#
# Built with the upstream "enable_global_hotkey,purego" tags. The purego tag
# selects the CGo-free X11 global-hotkey backend, so no X11/Xtst development
# packages are required; only ALSA (oto) and libFLAC (goflac) still need CGo.
#
# Dependencies are vendored in the source tarball, so the build is offline.

%global debug_package %{nil}

Name:           go-musicfox
Version:        5.1.0
Release:        1%{?dist}
Summary:        Terminal music player for NetEase Cloud Music

License:        GPL-3.0-only
URL:            https://github.com/go-musicfox/go-musicfox
Source0:        https://github.com/go-musicfox/go-musicfox/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  golang >= 1.26
BuildRequires:  gcc
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(flac)

%description
go-musicfox is a terminal client for NetEase Cloud Music, written in Go.
It offers playlists, daily recommendations, search, lyrics, global hotkeys
and a music-player UI in the terminal.

This package tracks the upstream v5.1.0 release tag.

%prep
# GitHub tag archives extract into go-musicfox-5.1.0/
%autosetup -n go-musicfox-%{version}

%build
export CGO_ENABLED=1
go build -mod=vendor -trimpath -buildmode=pie \
  -tags 'enable_global_hotkey,purego' \
  -ldflags "-X github.com/go-musicfox/go-musicfox/internal/types.AppVersion=v%{version} \
            -X github.com/go-musicfox/go-musicfox/internal/types.BuildTags=enable_global_hotkey,purego" \
  -o bin/musicfox ./cmd

%install
install -Dpm 0755 bin/musicfox %{buildroot}%{_bindir}/musicfox
# The desktop file ships as musicfox.desktop upstream; rename it so that it
# matches the launchable ID referenced by the AppStream metadata.
install -Dpm 0644 deploy/musicfox.desktop \
  %{buildroot}%{_datadir}/applications/io.github.go_musicfox.go-musicfox.desktop
install -Dpm 0644 deploy/io.github.go_musicfox.go-musicfox.appdata.xml \
  %{buildroot}%{_metainfodir}/io.github.go_musicfox.go-musicfox.appdata.xml
install -d %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
convert -resize 256x256 previews/logo.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/musicfox.png

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/musicfox
%{_datadir}/applications/io.github.go_musicfox.go-musicfox.desktop
%{_metainfodir}/io.github.go_musicfox.go-musicfox.appdata.xml
%{_datadir}/icons/hicolor/256x256/apps/musicfox.png

%changelog
%autochangelog