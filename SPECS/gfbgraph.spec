%global api 0.2

Name:           gfbgraph
Version:        %{api}.4
Release:        1%{?dist}
Summary:        GLib/GObject wrapper for the Facebook Graph API

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/GFBGraph
Source0:        https://download.gnome.org/sources/%{name}/%{api}/%{name}-%{version}.tar.xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1997941
Patch0:         %{name}-Fix-CVE-2021-39358-by-forcing-TLS-certificate-valida.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(goa-1.0)
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(rest-0.7)
Requires:       gobject-introspection

%description
GLib/GObject wrapper for the Facebook Graph API that integrates with GNOME
Online Accounts.

%package        devel
Summary:        Development files for %{name}
Requires:       gobject-introspection-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1


%build
gtkdocize
autoreconf --install --verbose
%configure \
  --disable-silent-rules \
  --disable-static \
  --enable-gtk-doc \
  --enable-introspection

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build


%install
%make_install

find $RPM_BUILD_ROOT -name '*.la' -delete
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%ldconfig_scriptlets


%files
%doc AUTHORS
%doc COPYING
%doc NEWS
%doc README
%{_libdir}/lib%{name}-%{api}.so.*

%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GFBGraph-%{api}.typelib

%files devel
%{_libdir}/lib%{name}-%{api}.so
%{_libdir}/pkgconfig/libgfbgraph-%{api}.pc

%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GFBGraph-%{api}.gir

%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%doc %{_datadir}/gtk-doc/html/%{name}-%{api}

%dir %{_includedir}/%{name}-%{api}
%{_includedir}/%{name}-%{api}/%{name}


%changelog
* Tue Oct 12 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.2.4-1
- Update to 0.2.4
Resolves: #1997941

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 31 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.2.3-1
- Update to 0.2.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.2-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 18 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2

* Thu Nov 28 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.2.1-2
- Use %%global instead of %%define
- Define Version in terms of %%{api}
- Drop redundant Requires: pkgconfig from devel

* Wed Nov 27 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.2.1-1
- Initial spec.
