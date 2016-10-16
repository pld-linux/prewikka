# TODO: apache (and other webservers?) configuration for prewikka WSGI
Summary:	Prelude IDS web application
Summary(pl.UTF-8):	Aplikacja WWW dla Prelude IDS
Name:		prewikka
Version:	3.1.0
Release:	1
License:	GPL v2+
Group:		Applications/Networking
#Source0Download: https://www.prelude-siem.org/projects/prelude/files
Source0:	https://www.prelude-siem.org/attachments/download/727/%{name}-%{version}.tar.gz
# Source0-md5:	a7c721c3322558f8e94608cc3a12abb2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-localedir.patch
Patch1:		%{name}-install.patch
URL:		https://www.prelude-siem.org/
BuildRequires:	python >= 1:2.6
BuildRequires:	python-cheetah
BuildRequires:	python-lesscpy
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%pyrequires_eq	python-modules
Requires:	python-babel
Requires:	python-cheetah
Requires:	python-libprelude >= 1.0.0
Requires:	python-libpreludedb >= 1.0.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prewikka is a professional looking application providing advanced
feature like contextual filtering, aggregation, etc.

%description -l pl.UTF-8
Prewikka to profesjonalnie wyglądająca aplikacja dająca zaawansowane
możliwości, takie jak filtrowanie kontekstowe, agregację itp.

%package httpd
Summary:	Standalone Prewikka HTTP server
Summary(pl.UTF-8):	Samodzielny serwer HTTP dla Prewikki
Group:		Daemons
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	rc-scripts
Provides:	group(http)
Provides:	user(http)
Requires:	%{name} = %{version}-%{release}

%description httpd
Standalone Prewikka HTTP server. Allows to run Prewikka on user
available port (>= 1024, 8000 by default).

%description httpd -l pl.UTF-8
Samodzielny serwer HTTP dla Prewikki. Pozwala na uruchomienie Prewikki
na porcie dostępnym dla użytkownika (>= 1024, domyślnie 8000).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT

%py_install

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install conf/prewikka.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

install -d $RPM_BUILD_ROOT%{_datadir}
%{__mv} $RPM_BUILD_ROOT%{py_sitescriptdir}/prewikka/locale $RPM_BUILD_ROOT%{_datadir}

%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre httpd
%groupadd -g 51 http
%useradd -u 51 -r -d /home/services/httpd -s /bin/false -c "HTTP User" -g http http

%post httpd
/sbin/chkconfig --add prewikka
if [ "$1" = "1" ]; then
%banner -e %{name} <<EOF

Create new database and database user for Prewikka (or update an existing
one if needed) and configure Prewikka. For reference visit:
https://www.prelude-siem.org/projects/prelude/wiki/InstallingPreludePrewikka

To connect to console point Your browser to:
http://`hostname`:8000/
REMEMBER to change password for admin (default: admin)

EOF
fi
%service prewikka restart "Prewikka"

%preun httpd
if [ "$1" = "0" ]; then
	%service prewikka stop
	/sbin/chkconfig --del prewikka
fi

%postun httpd
if [ "$1" = "0" ]; then
	%userremove http
	%groupremove http
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING.* NEWS README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/prewikka.conf
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/prewikka.wsgi
%{py_sitescriptdir}/prewikka
%{py_sitescriptdir}/prewikka-%{version}-py*.egg-info
%attr(770,root,http) %dir /var/lib/prewikka

%files httpd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/prewikka-httpd
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
