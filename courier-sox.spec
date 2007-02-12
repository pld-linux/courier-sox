Summary:	Courier Socks 5 client library
Summary(pl.UTF-8):	Biblioteki klienckie Socks 5
Name:		courier-sox
Version:	0.06
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	32fde0bf5c755092722894006444dc9f
Patch0:		%{name}-build.patch
Patch1:		%{name}-init.patch
URL:		http://www.courier-mta.org
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	courier-authlib-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/courier-sox

%description
This is a generic Socks 5 client support library.

%description -l pl.UTF-8
Ogólna biblioteka kliencka Socks 5.

%package devel
Summary:	Socks 5 client header files
Summary(pl.UTF-8):	Pliki nagłówkowe klienta socks 5
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains header files for building applications that use
Socks 5 proxies.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji używających
proxy Socks 5.

%package server
Summary:	Socks 5 server
Summary(pl.UTF-8):	Serwer socks 5
Group:		Networking/Utilities
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}

%description server
This package contains the Courier Socks 5 server. Install this package
if you want to run a Socks 5 server.

%description server -l pl.UTF-8
Ten pakiet zawiera serwer couriera socks 5. Jeżeli chcesz uruchamiać
serwer socks5, zainstaluj ten pakiet.

%package static
Summary:	Socks 5 client static libraries
Summary(pl.UTF-8):	Biblioteki statyczne klienta socks 5
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libraries for building applications that
use Socks 5 proxies.

%description static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne do tworzenia aplikacji
używających proxy Socks 5.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

ln -sf ../config.sub libltdl/config.sub

%configure \
	--libexecdir=%{_libexecdir}

%{__make}
%{__make} check

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install courier-sox.sysvinit $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-sox

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post server
/sbin/chkconfig --add courier-sox
%service courier-sox restart

%preun server
if [ "$1" = "0" ]; then
	%service courier-sox stop
	/sbin/chkconfig --del courier-sox
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README *.html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/lib*.la
%{_mandir}/man1/socksify*
%{_mandir}/man3/socks*
%{_mandir}/man5/*
%{_sysconfdir}/socksrc

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files server
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/courier-sox
%{_mandir}/man1/sockd*
%attr(755,root,root) %{_sbindir}/sockd
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/sockd

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
