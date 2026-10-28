%global snap_date %(date -u +%%Y%%m%%d)

Name:           zmx
Version:        0.8.1
Release:        1.%{snap_date}%{?dist}
Summary:        Session persistence for terminal processes.

License:        MIT
URL:            https://github.com/neurosnap/zmx
Source0:        https://github.com/neurosnap/zmx/archive/refs/heads/main.tar.gz

# zmx 0.8 needs Zig >= 0.17, which needs LLVM 22.1.8. Fedora has only zig 0.16
# (LLVM 21) and rawhide is on LLVM 23, so no system zig works. Fetch the
# official prebuilt compiler at build time (the COPR builder has network
# access, same as for Zig's build.zig.zon deps).
%global zig_version 0.17.0
%ifarch aarch64
%global zig_arch aarch64
%global zig_sha256 9e8d11661d4ae3bd57702a3832781e23ad151dde5798e16a5ccd503f65234ff8
%else
%global zig_arch x86_64
%global zig_sha256 1cbe9df9f27e6b78d14ccbca43b6703a404ef79ef1c463de901d7f088d4e2026
%endif
%global zig_url https://ziglang.org/download/%{zig_version}/zig-%{zig_arch}-linux-%{zig_version}.tar.xz

BuildRequires:  curl
BuildRequires:  tar
BuildRequires:  git-core

%description
Session persistence for terminal processes.

%prep
# Download the prebuilt Zig and verify it before unpacking into %%{_builddir}.
curl -fL --retry 3 -o zig.tar.xz %{zig_url}
echo "%{zig_sha256}  zig.tar.xz" | sha256sum -c -
tar -xf zig.tar.xz
# GitHub branch archives extract into zmx-main/
%autosetup -n zmx-main

%build
export PATH=%{_builddir}/zig-%{zig_arch}-linux-%{zig_version}:$PATH
# Zig does not automatically honor RPM's LDFLAGS for build-id, so pass it explicitly.
# Build for the native target (no -Dtarget) so aarch64 and other arches work.
zig build --build-id=sha1 -Doptimize=ReleaseFast --prefix "zig-out"

%install
install -Dm755 zig-out/bin/zmx %{buildroot}%{_bindir}/zmx
# Generate and install shell completions
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
mkdir -p %{buildroot}%{_datadir}/nushell/completions

zig-out/bin/zmx completions bash > %{buildroot}%{_datadir}/bash-completion/completions/zmx
zig-out/bin/zmx completions zsh  > %{buildroot}%{_datadir}/zsh/site-functions/_zmx
zig-out/bin/zmx completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/zmx.fish
zig-out/bin/zmx completions nu   > %{buildroot}%{_datadir}/nushell/completions/zmx.nu

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/zmx
%{_datadir}/bash-completion/completions/zmx
%{_datadir}/zsh/site-functions/_zmx
%{_datadir}/fish/vendor_completions.d/zmx.fish
%{_datadir}/nushell/completions/zmx.nu

%changelog
%autochangelog

