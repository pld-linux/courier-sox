#
# TODO:
#	- pl
#	- fix build (undefined @LIBNAME@)
#
Summary:	Courier Socks 5 client library
Summary(pl):	Biblioteki klienckie Socks 5
Name:		courier-sox
Version:	0.03
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	864511941045f8d4b2517de9e9c660f1
URL:		http://www.courier-mta.org
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a generic Socks 5 client support library. It does not include
a Socks 5 server (yet). This is just a client-side library.

%description -l pl

%package devel
Summary:	Socks 5 client header files
Summary(pl):	Pliki nag³ówkowe klienta socks 5
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains header files for building applications that
use Socks 5 proxies.

%description devel -l pl

%package static
Summary:	Socks 5 client static libraries
Summary(pl):	Biblioteki statyczne klienta socks 5
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libraries for building applications that
use Socks 5 proxies.

%description static -l pl

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}
%{__make} check

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README *.html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/*/*
%{_sysconfdir}/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
