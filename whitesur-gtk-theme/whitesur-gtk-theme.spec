# WhiteSur GTK theme, tracking the upstream dated release tag 2026-09-10.
#
# The theme is generated from Sass sources by the upstream install.sh, so the
# build needs sassc plus glib-compile-resources (GNOME Shell gresource) and
# xmllint (XML processing). The output is architecture independent data, hence
# BuildArch: noarch.
#
# Variants: upstream can generate the cross product of five dimensions
#   color   Light, Dark                          (2)
#   opacity normal, solid                        (2)
#   buttons normal, alt                          (2)
#   accent  default, blue, purple, pink, red,
#           orange, yellow, green, grey         (9)
#   scheme  standard, nord                       (2)
# i.e. up to 144 distinct theme directories, each carrying its own gtk-2/3/4,
# gnome-shell and wm assets (several MB). Shipping all of them would be
# hundreds of MB and take a very long time to Sass-compile, so this package
# ships exactly what `install.sh` produces with no arguments: all colour and
# opacity variants (Light/Dark x normal/solid = 4 directories), with the
# default accent, standard scheme and normal window buttons. This matches the
# upstream default and what other distributions package. Users who want an
# accent or nord variant build it with the upstream installer into ~/.themes.
#
# Note on libadwaita: upstream's `-l` option installs gtk-4.0 CSS into
# ~/.config/gtk-4.0, which is a per-user operation and cannot be done from an
# RPM. This package ships the gtk-4.0 tree inside /usr/share/themes only;
# users of libadwaita apps need to copy it into their config (or set
# GTK_THEME for classic GTK4 apps).

%global tag 2026-09-10

Name:           whitesur-gtk-theme
Version:        2026.09.10
Release:        1%{?dist}
Summary:        A macOS Big Sur-like GTK theme

License:        MIT
URL:            https://github.com/vinceliuice/WhiteSur-gtk-theme
Source0:        %{url}/archive/refs/tags/%{tag}.tar.gz

BuildArch:      noarch

BuildRequires:  sassc
BuildRequires:  /usr/bin/glib-compile-resources
BuildRequires:  /usr/bin/xmllint

Recommends:     gtk-murrine-engine

%description
WhiteSur GTK theme is a macOS Big Sur-like theme for GTK based desktops. It
provides Light and Dark variants, in normal and solid opacity, covering
GTK 2/3/4, GNOME Shell, Cinnamon, Metacity, XFWM and Plank.

%prep
%autosetup -n WhiteSur-gtk-theme-%{tag}

# The installer also drops a per-user 'gnome-theme-switcher' helper into
# $HOME/.local/bin; that has no place in a system package build, so drop the
# call. It also tries `sudo dnf install` for missing tools when they are not
# present, which the build needs above guarantee.
sed -i 's|^  install_app$|  :|' install.sh

%build
# Nothing to compile separately: install.sh generates and installs the themes.

%install
# No flags == upstream defaults: Light/Dark x normal/solid, accent 'default',
# scheme 'standard', buttons 'normal'. Yields the WhiteSur-{Light,Dark}{,-solid}
# directories. Add e.g. `-t blue -s nord -a alt` here to ship more variants,
# at the cost of build time and package size (see the header).
./install.sh --dest %{buildroot}%{_datadir}/themes

%files
%license COPYING
%doc README.md
%{_datadir}/themes/WhiteSur*

%changelog
%autochangelog