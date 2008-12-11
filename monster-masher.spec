%define	name	monster-masher
%define version 1.8.1
%define release %mkrel 1

Summary:	Clean caves by mashing monsters with stone
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Games/Other
URL:		http://www.cs.auc.dk/~olau/monster-masher/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		http://www.cs.auc.dk/~olau/monster-masher/source/%{name}-%{version}.tar.bz2
Patch: monster-masher-1.8-desktopentry.patch
# add handler to close the about dialog (bug #43019)
Patch1: monster-masher-1.8-about-dialog.patch
BuildRequires:	gconfmm2.6-devel >= 2.0.1
BuildRequires:	libgnomeuimm2.6-devel
BuildRequires:	imagemagick
BuildRequires:	intltool

%description
Monster Masher is an action game for the GNOME desktop environment.
The basic idea is that you, as levitation worker gnome, has to clean
the caves for monsters that want to roll over you. You do the cleaning
by mashing the monsters with stone blocks.

%prep
%setup -q
%patch -p1
%patch1 -p1

%build
%configure2_5x --bindir=%{_gamesbindir}
%make

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# menu entry

# icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -D -m 0644      monster-masher.png %{buildroot}%{_liconsdir}/monster-masher.png
convert -geometry 32x32 monster-masher.png %{buildroot}%{_iconsdir}/monster-masher.png
convert -geometry 16x16 monster-masher.png %{buildroot}%{_miconsdir}/monster-masher.png

%{find_lang} %{name}

%if %mdkversion < 200900
%post
%update_menus
%post_install_gconf_schemas monster-masher
%endif

%preun
%preun_uninstall_gconf_schemas monster-masher

%if %mdkversion < 200900
%postun
%clean_menus
%endif

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
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
