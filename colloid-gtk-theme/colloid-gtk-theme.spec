# Colloid GTK theme, tracking the upstream dated release tag 2026-08-08.
#
# The theme is generated from Sass sources by the upstream install.sh, so the
# build only needs sassc; all the window/shell assets are shipped as ready-made
# SVG/PNG files in the tarball.
#
# Variants: upstream generates the cross product of five dimensions
#   color   standard, Light, Dark                 (3)
#   accent  default, purple, pink, red, orange,
#           yellow, green, teal, grey             (9)
#   size    standard, compact                     (2)
#   scheme  default, Nord, Dracula, Gruvbox,
#           Everforest, Catppuccin                (6)
#   window  mac, normal                           (2)
# plus the optional tweaks (black, rimless, float). Shipping all of them would
# be thousands of Sass compilations and hundreds of MB, so this package ships
# exactly what `install.sh` produces with no arguments: standard/Light/Dark
# colour variants, default accent, standard size, default colour scheme and the
# default (macOS-like) window buttons. This matches the upstream default and
# what other distributions package. Users who want an accent, Nord or compact
# variant build it with the upstream installer into ~/.themes.
#
# Note on libadwaita: upstream's `-l` option writes gtk-4.0 CSS into
# ~/.config/gtk-4.0, which is a per-user operation and cannot be done from an
# RPM. This package ships the gtk-4.0 tree inside /usr/share/themes only;
# users of libadwaita apps need to copy it into their config (or set
# GTK_THEME for classic GTK4 apps).

%global tag 2026-08-08

Name:           colloid-gtk-theme
Version:        2026.08.08
Release:        1%{?dist}
Summary:        A flat, material design GTK theme

License:        GPL-3.0-or-later
URL:            https://github.com/vinceliuice/Colloid-gtk-theme
Source0:        %{url}/archive/refs/tags/%{tag}.tar.gz

BuildArch:      noarch

BuildRequires:  sassc

Recommends:     gtk-murrine-engine

%description
Colloid is a flat, material design theme for GTK based desktops. It provides
standard, Light and Dark variants covering GTK 2/3/4, GNOME Shell, Cinnamon,
Metacity, XFWM, Plank and labwc.

%prep
%autosetup -n Colloid-gtk-theme-%{tag}

%build
# Nothing to compile separately: install.sh generates and installs the themes.

%install
# install.sh creates the destination directory itself, but only after probing
# for it; give rpmbuild's empty buildroot the expected subdirectory so the
# result lands in a known place.
install -d %{buildroot}%{_datadir}/themes

# No flags == upstream defaults: standard/Light/Dark, accent 'default',
# standard size, default colour scheme, mac-style window buttons. Yields the
# Colloid, Colloid-Light and Colloid-Dark directories (plus the -hdpi/-xhdpi
# xfwm4 variants). Add e.g. `-t grey -s compact --tweaks nord` here to ship
# more variants, at the cost of build time and package size (see the header).
./install.sh --dest %{buildroot}%{_datadir}/themes

%files
%license LICENSE
%doc README.md
%{_datadir}/themes/Colloid*

%changelog
%autochangelog
