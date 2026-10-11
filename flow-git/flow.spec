# Flow Control, tracking the upstream zig-0.16 branch.
#
# The v0.7.2 release tag targets Zig 0.15.2 and master now requires Zig 0.17
# (see minimum_zig_version in build.zig.zon). Fedora has Zig 0.16 but not 0.17,
# so this tracks the upstream zig-0.16 maintenance branch, which pins
# minimum_zig_version = 0.16.0.
#
# build.zig.zon pins a set of git/URL dependencies (flow-syntax plus the
# tree-sitter parsers it bundles, vaxis, zeit, ...) that Zig fetches over the
# network at build time. The COPR builder has network access, as for the
# other Zig packages in this repo.
#
# The default Linux build is a statically linked (musl) binary.

%global snap_date %(date -u +%%Y%%m%%d)

Name:           flow
Version:        0.7.2
Release:        1.%{snap_date}%{?dist}
Summary:        A programmer's text editor for the terminal

License:        MIT
URL:            https://github.com/neurocyte/flow
Source0:        https://github.com/neurocyte/flow/archive/refs/heads/zig-0.16.tar.gz

# Zig uses its bundled clang for translate-c, so no system clang BR is needed.
# 0.17 is excluded: Fedora does not package it yet.
BuildRequires:  (zig >= 0.16 with zig < 0.17)
BuildRequires:  git-core

%description
Flow Control is a fast, feature-rich text editor that runs in the terminal.
It provides tabs, multiple cursors, full mouse support, syntax highlighting
for more than 70 languages via tree-sitter, LSP integration and several
pre-configured keybinding modes (Flow Control, Emacs, Vim and Helix).

This package tracks the upstream zig-0.16 branch.

%prep
# GitHub branch archives extract into flow-zig-0.16/
%autosetup -n flow-zig-0.16

# Upstream embeds the output of `git describe` in the binary. The branch
# archive has no .git, so recreate a minimal repository with a tag and an
# upstream branch to keep `flow --version` and the home screen meaningful.
git init -q -b zig-0.16
git config user.email "packager@fedoraproject.org"
git config user.name "Fedora"
git add -A
git commit -qm "Flow Control %{version} snapshot"
git tag -a v%{version} -m "Flow Control %{version}"
git remote add origin %{url}
git update-ref refs/remotes/origin/zig-0.16 HEAD
git branch --set-upstream-to=origin/zig-0.16 zig-0.16

%build
export ZIG_GLOBAL_CACHE_DIR=%{_builddir}/zig-cache
mkdir -p "$ZIG_GLOBAL_CACHE_DIR"
# --build-id=sha1: Zig does not pick up RPM's LDFLAGS.
# -Dstrip=false: leave stripping and debuginfo to RPM.
# -Dcpu=baseline: keep the binary portable across x86_64 CPUs.
zig build \
  --build-id=sha1 \
  --prefix zig-out \
  -Doptimize=ReleaseSafe \
  -Dstrip=false \
  -Dcpu=baseline

%install
install -Dpm 0755 zig-out/bin/flow %{buildroot}%{_bindir}/flow

%files
%license LICENSE
%doc README.md help.md
%{_bindir}/flow

%changelog
%autochangelog
