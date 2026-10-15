# Satty, tracking the upstream release tag v0.22.0.
#
# Rust dependencies are vendored at build time with `cargo vendor`. The COPR
# project runs with network access enabled, so the crates are fetched during
# %prep and the compile itself then stays offline against the vendor directory.

%bcond check 0

Name:           satty
Version:        0.22.0
Release:        1%{?dist}
Summary:        Modern screenshot annotation tool

License:        MPL-2.0
URL:            https://github.com/Satty-org/Satty
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(cairo-gobject)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(pangocairo)

%global _description %{expand:
Satty is a modern screenshot annotation tool for Linux, designed for
wlroots-based compositors. It provides smooth hardware-accelerated rendering
and an uncomplicated interface for marking up and annotating screenshots,
inspired by Swappy and Flameshot.}

%description %{_description}

%prep
# GitHub tag archives extract into Satty-%{version}/
%autosetup -n Satty-%{version}
cargo vendor
%cargo_prep -v vendor

%build
# The ci-release feature makes build.rs write completions/ and man/ into the
# source tree instead of OUT_DIR, so they can be packaged.
%cargo_build -f ci-release
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
install -Dpm 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

# Install the desktop file under the AppStream component ID so that the
# launchable ID referenced by the metainfo resolves.
sed -e 's/^Icon=satty$/Icon=org.satty.Satty/' \
    %{name}.desktop > org.satty.Satty.desktop
install -Dpm 0644 org.satty.Satty.desktop \
  %{buildroot}%{_datadir}/applications/org.satty.Satty.desktop
install -Dpm 0644 assets/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/org.satty.Satty.svg
install -Dpm 0644 org.satty.Satty.metainfo.xml \
  %{buildroot}%{_metainfodir}/org.satty.Satty.metainfo.xml

install -Dpm 0644 completions/%{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
install -Dpm 0644 completions/%{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish
install -Dpm 0644 completions/_%{name} %{buildroot}%{zsh_completions_dir}/_%{name}
install -Dpm 0644 completions/%{name}.elv %{buildroot}%{_datadir}/elvish/lib/%{name}.elv
install -Dpm 0644 completions/%{name}.nu %{buildroot}%{_datadir}/nushell/completions/%{name}.nu
install -Dpm 0644 completions/%{name}.ts %{buildroot}%{_datadir}/fig/autocomplete/%{name}.ts

install -Dpm 0644 man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.satty.Satty.desktop
%if %{with check}
%cargo_test -f ci-release
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/org.satty.Satty.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.satty.Satty.svg
%{_metainfodir}/org.satty.Satty.metainfo.xml
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}
%{_datadir}/elvish/lib/%{name}.elv
%{_datadir}/nushell/completions/%{name}.nu
%{_datadir}/fig/autocomplete/%{name}.ts
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog