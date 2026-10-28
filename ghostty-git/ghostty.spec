# Ghostty nightly build tracking the upstream main branch.
#
# The COPR builder has network access, so we let Zig fetch all of Ghostty's
# dependencies (build.zig.zon) at build time rather than vendoring them.

%global snap_date %(date -u +%%Y%%m%%d)

Name:           ghostty
Version:        1.4.0
Release:        1.%{snap_date}%{?dist}
Summary:        A fast, feature-rich terminal emulator written in Zig (main branch)

License:        MIT AND MPL-2.0 AND OFL-1.1 AND CC0-1.0 AND Apache-2.0
URL:            https://ghostty.org/
Source0:        https://github.com/ghostty-org/ghostty/archive/refs/heads/main.tar.gz

# Ghostty 1.4 needs Zig >= 0.17, which needs LLVM 22.1.8. Fedora has only
# zig 0.16 (LLVM 21) and rawhide is on LLVM 23, so no system zig works.
# Fetch the official prebuilt compiler and use it for the build instead.
# sha256 (x86_64):  1cbe9df9f27e6b78d14ccbca43b6703a404ef79ef1c463de901d7f088d4e2026
# sha256 (aarch64): 9e8d11661d4ae3bd57702a3832781e23ad151dde5798e16a5ccd503f65234ff8
%global zig_version 0.17.0
%ifarch aarch64
%global zig_arch aarch64
%else
%global zig_arch x86_64
%endif
Source1:        https://ziglang.org/download/%{zig_version}/zig-%{zig_arch}-linux-%{zig_version}.tar.xz

BuildRequires:  git-core
BuildRequires:  gcc
BuildRequires:  pandoc-cli
BuildRequires:  blueprint-compiler
BuildRequires:  ncurses
BuildRequires:  ncurses-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libX11-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(zlib)

# Suppress -fno-semantic-interposition warning noise from rpmbuild
%global _disable_debuginfo_attributes 1

Conflicts:       ghostty
Requires:        ncurses-term

%description
Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses
platform-native UI and GPU acceleration. This is a nightly build tracking the
upstream main branch.

%prep
# Unpack the prebuilt Zig into %%{_builddir} before entering the source tree.
tar -xf %{SOURCE1}
%autosetup -n ghostty-main

%build
export PATH=%{_builddir}/zig-%{zig_arch}-linux-%{zig_version}:$PATH
# Build and install in one step: DESTDIR redirects the install into the
# buildroot, --prefix controls the layout. This avoids the stray zig temp
# dirs that `zig build install` can copy into the buildroot.
export ZIG_GLOBAL_CACHE_DIR=%{_builddir}/zig-cache
mkdir -p "$ZIG_GLOBAL_CACHE_DIR"
DESTDIR=%{buildroot} \
zig build \
  --build-id=sha1 \
  --prefix %{_prefix} \
  -Doptimize=ReleaseFast \
  -Dcpu=baseline \
  -Dpie=true \
  -Dstrip=false \
  -Demit-docs \
  -Demit-themes=true \
  -Demit-terminfo \
  -Demit-termcap

# Ghostty puts its systemd user unit under share/ when built outside
# "system package mode"; systemd only searches lib/, so move it.
# Note: Ghostty installs non-arch-independent files under $(prefix)/lib,
# not %%{_libdir} (which is lib64 on x86_64), so use %%{_prefix}/lib here.
install -d %{buildroot}%{_prefix}/lib/systemd/user
mv %{buildroot}%{_datadir}/systemd/user/app-com.mitchellh.ghostty.service \
   %{buildroot}%{_prefix}/lib/systemd/user/
rmdir %{buildroot}%{_datadir}/systemd/user 2>/dev/null || true

# The compiled 'ghostty' terminfo entry clashes with ncurses-term; drop it.
rm -rf %{buildroot}%{_datadir}/terminfo/g/ghostty

# libghostty-vt is a library for embedding Ghostty's VT engine in other
# apps. The ghostty terminal itself is statically linked and doesn't need
# it, so drop the shared/static libs, headers, and pkg-config files.
rm -rf %{buildroot}%{_prefix}/lib/libghostty-vt.*
rm -rf %{buildroot}%{_includedir}/ghostty
rm -rf %{buildroot}%{_datadir}/pkgconfig/libghostty-vt*.pc

%files
%license LICENSE
%doc README.md
%{_bindir}/ghostty
%{_prefix}/lib/systemd/user/app-com.mitchellh.ghostty.service
%{_datadir}/ghostty/
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/dbus-1/services/com.mitchellh.ghostty.service
%{_datadir}/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_datadir}/bat/
%{_datadir}/kio/
%{_datadir}/nautilus-python/
%{_datadir}/nvim/
%{_datadir}/vim/
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_datadir}/locale/
%{_mandir}/man1/ghostty.1
%{_mandir}/man5/ghostty.5
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/zsh/site-functions/_ghostty
%{bash_completions_dir}/ghostty.bash
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/terminfo/ghostty.terminfo
%{_datadir}/terminfo/ghostty.termcap

%changelog
%autochangelog
