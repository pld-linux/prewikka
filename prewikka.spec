Summary:	Prelude IDS web application
Summary(pl.UTF-8):	Aplikacja WWW dla Prelude IDS
Name:		prewikka
Version:	0.9.13
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
# Source0-md5:	4b922ce76bb3ae87922f8a2e63e0aa5d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.org/
BuildRequires:	python >= 1:2.5
BuildRequires:	python-cheetah
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%pyrequires_eq	python-modules
Requires:	python-cheetah
Requires:	python-libprelude
Requires:	python-libpreludedb
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prewikka is a professional looking application providing advanced
feature like contextual filtering, aggregation, etc.

%description -l pl.UTF-8
Prewikka to profesjonalnie wyglądająca aplikacja dająca zaawansowane
możliwości, takie jak filtrowanie kontekstowe, agregację itp.

%prep
%setup -q

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install conf/prewikka.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add prewikka
if [ "$1" = "1" ]; then
%banner -e %{name} <<EOF

Create new database and database user for prewikka
(or update an existing one if needed) using templates from
%{_datadir}/%{name}/database and configure Prewikka
for reference visit %{url}

To connect to console point Your browser to:
http://`hostname`:8000/
REMEMBER to change password for admin (default:admin)

EOF
fi
%service prewikka restart "Prewikka"

%preun
if [ "$1" = "0" ]; then
	%service prewikka stop
	/sbin/chkconfig --del prewikka
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/prewikka-httpd
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/prewikka.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/cgi-bin
%attr(755,root,root) %{_datadir}/%{name}/cgi-bin/prewikka.cgi
%{_datadir}/%{name}/database
%{_datadir}/%{name}/htdocs
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%dir %{py_sitescriptdir}/%{name}/modules
%{py_sitescriptdir}/%{name}/modules/*.py[co]
%dir %{py_sitescriptdir}/%{name}/modules/auth
%{py_sitescriptdir}/%{name}/modules/auth/*.py[co]
%dir %{py_sitescriptdir}/%{name}/modules/auth/anonymous
%{py_sitescriptdir}/%{name}/modules/auth/anonymous/*.py[co]
%dir %{py_sitescriptdir}/%{name}/modules/auth/cgi
%{py_sitescriptdir}/%{name}/modules/auth/cgi/*.py[co]
%dir %{py_sitescriptdir}/%{name}/modules/auth/loginpassword
%{py_sitescriptdir}/%{name}/modules/auth/loginpassword/*.py[co]
%dir %{py_sitescriptdir}/%{name}/views
%{py_sitescriptdir}/%{name}/views/*.py[co]
%dir %{py_sitescriptdir}/%{name}/templates
%{py_sitescriptdir}/%{name}/templates/*.py[co]
%{py_sitescriptdir}/prewikka-*.egg-info
