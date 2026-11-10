%global snap_date %(date -u +%%Y%%m%%d)

Name:           mineral
Version:        0.5.5
Release:        1.%{snap_date}%{?dist}
Summary:        A multi-source TUI music player in Rust — ratatui frontend, pluggable channel backends, real streaming playback with lyrics & spectrum.

License:        MIT
URL:            https://github.com/10knamesmore/Mineral
Source0:        https://github.com/10knamesmore/Mineral/archive/refs/heads/main.tar.gz

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  pkgconfig(alsa)
BuildRequires:  git-core
BuildRequires:  pkgconfig(openssl)

%description
A multi-source TUI music player in Rust — ratatui frontend, pluggable channel backends, real streaming playback with lyrics & spectrum.

%prep
%autosetup -n Mineral-main

%build
cargo build --release

%install
install -Dm755 target/release/mineral %{buildroot}%{_bindir}/mineral

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/mineral

%changelog
%autochangelog

