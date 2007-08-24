%define	name	monster-masher
%define version 1.8
%define release %mkrel 3

Summary:	Clean caves by mashing monsters with stone
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
URL:		http://www.cs.auc.dk/~olau/monster-masher/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		http://www.cs.auc.dk/~olau/monster-masher/source/%{name}-%{version}.tar.bz2
Patch: monster-masher-1.8-desktopentry.patch

BuildRequires:	gconfmm2.6-devel >= 2.0.1
BuildRequires:	libgnomeuimm2.6-devel
BuildRequires:	ImageMagick

%description
Monster Masher is an action game for the GNOME desktop environment.
The basic idea is that you, as levitation worker gnome, has to clean
the caves for monsters that want to roll over you. You do the cleaning
by mashing the monsters with stone blocks.

%prep
%setup -q
%patch -p1

%build
%configure2_5x --bindir=%{_gamesbindir}
%make

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# menu entry
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << _EOF_
?package(%{name}): \
 command="%{_gamesbindir}/monster-masher" \
 icon="monster-masher.png" \
 longtitle="Mash monsters and save the gnomes" \
 needs="x11" \
 section="More Applications/Games/Other" \
 title="Monster Masher" \
 startup_notify="true" xdg="true"
_EOF_

# icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -D -m 0644      monster-masher.png %{buildroot}%{_liconsdir}/monster-masher.png
convert -geometry 32x32 monster-masher.png %{buildroot}%{_iconsdir}/monster-masher.png
convert -geometry 16x16 monster-masher.png %{buildroot}%{_miconsdir}/monster-masher.png

%{find_lang} %{name}

%post
%update_menus
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
for SCHEMA in monster-masher; do
    gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$SCHEMA.schemas > /dev/null
done

%preun
if [ "$1" = "0" ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    for SCHEMA in monster-masher; do
        gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/$SCHEMA.schemas > /dev/null
    done
fi

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_gamesbindir}/*
%{_datadir}/applications/monster-masher.desktop
%{_datadir}/pixmaps/*
%{_datadir}/%{name}
%{_sysconfdir}/gconf/schemas/*.schemas
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
