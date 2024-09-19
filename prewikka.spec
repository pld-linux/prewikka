# TODO: apache (and other webservers?) configuration for prewikka WSGI
Summary:	Prelude IDS web application
Summary(pl.UTF-8):	Aplikacja WWW dla Prelude IDS
Name:		prewikka
Version:	5.2.0
Release:	1
License:	GPL v2+
Group:		Applications/Networking
#Source0Download: https://www.prelude-siem.org/projects/prelude/files
Source0:	https://www.prelude-siem.org/attachments/download/1400/%{name}-%{version}.tar.gz
# Source0-md5:	e1102494dfa50c9df91d5db08ffe51af
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-localedir.patch
Patch1:		%{name}-install.patch
Patch2:		locale.patch
URL:		https://www.prelude-siem.org/
# lesscpy script is used to build
BuildRequires:	python-lesscpy
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-Mako
Requires:	python3-PyYAML
Requires:	python3-babel
Requires:	python3-libprelude >= 5.2.0
Requires:	python3-libpreludedb >= 5.2.0
Requires:	python3-modules >= 1:3.2
Requires:	python3-pytz
Requires:	python3-werkzeug
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
%patch2 -p1

%build
%py3_build

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT%{_datadir}
%{__mv} $RPM_BUILD_ROOT%{py3_sitescriptdir}/prewikka/locale $RPM_BUILD_ROOT%{_datadir}

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
%attr(755,root,root) %{_bindir}/prewikka-cli
%attr(755,root,root) %{_bindir}/prewikka-crontab
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/prewikka.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/menu.yml
%dir %{_sysconfdir}/%{name}/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/auth.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/external_app.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/logs.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/riskoverview.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/prewikka.wsgi
%{py3_sitescriptdir}/prewikka
%{py3_sitescriptdir}/prewikka-%{version}-py*.egg-info
%attr(770,root,http) %dir /var/lib/prewikka

%files httpd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/prewikka-httpd
%attr(754,root,root) /etc/rc.d/init.d/prewikka
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/prewikka
