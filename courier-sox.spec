#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	tests		# "make check"

Summary:	Courier Socks 5 client libraries
Summary(pl.UTF-8):	Biblioteki klienckie Socks 5
Name:		courier-sox
Version:	0.15
Release:	1
License:	GPL v3 with OpenSSL exception
Group:		Networking/Utilities
Source0:	https://downloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	76576113168d9451940aa41fdd3b9141
Patch0:		%{name}-init.patch
URL:		http://www.courier-mta.org/
BuildRequires:	courier-authlib-devel >= 0.71
BuildRequires:	gdbm-devel
BuildRequires:	libltdl-devel >= 2:2.0
BuildRequires:	perl-base
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package server
Summary:	Socks 5 server
Summary(pl.UTF-8):	Serwer socks 5
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
# requires library and courierlogger
Requires:	courier-authlib >= 0.71

%description server
This package contains the Courier Socks 5 server.

%description server -l pl.UTF-8
Ten pakiet zawiera serwer Courier Socks 5.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--libexecdir=%{_libexecdir}/courier-sox \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D courier-sox.sysvinit $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-sox

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
%attr(755,root,root) %{_bindir}/mkbl4
%attr(755,root,root) %{_bindir}/socksify
%attr(755,root,root) %{_libdir}/libsocks.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsocks.so.0
%attr(755,root,root) %{_libdir}/libsockswrap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsockswrap.so.0
%{_mandir}/man1/socksify.1*
%{_mandir}/man5/socksrc.5*
%{_mandir}/man8/mkbl4.8*
%dir %{_sysconfdir}/socksrc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/socksrc/system

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsocks.so
%attr(755,root,root) %{_libdir}/libsockswrap.so
%{_libdir}/libsocks.la
%{_libdir}/libsockswrap.la
%{_includedir}/socks.h
%{_mandir}/man3/socks.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsocks.a
%{_libdir}/libsockswrap.a
%endif

%files server
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/courier-sox
%attr(755,root,root) %{_sbindir}/sockd
%dir %{_libexecdir}/courier-sox
%attr(755,root,root) %{_libexecdir}/courier-sox/sockd
%{_mandir}/man1/sockd.1*
