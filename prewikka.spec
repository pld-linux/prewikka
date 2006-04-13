#
# TODO:		- do we need both pyc and pyo files?
#		- don't we need py files ?
#		- startup/init files (assume standalone http server
#		  not the apache/thttpd integration)
#		- better files section 
# 
Summary:	Prelude IDS web application
Summary(pl):	Aplikacja WWW dla Prelude IDS
Name:		prewikka
Version:	0.9.3
Release:	0.2
License:	GPL
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
# Source0-md5:	4af486dcd2317022fdf5bb5ce8c1b199
URL:		http://www.prelude-ids.org/
BuildRequires:	python-cheetah
Requires:	python-libprelude
Requires:	python-libpreludedb
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prewikka is a professional looking application providing advanced
feature like contextual filtering, aggregation, etc.

%description -l pl
Prewikka to profesjonalnie wygl±daj±ca aplikacja daj±ca zaawansowane
mo¿liwo¶ci, takie jak filtrowanie kontekstowe, agregacjê itp.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --optimize=2 \
	--root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_usr}/share/%{name}
%dir %{_usr}/share/%{name}/cgi-bin
%dir %{_usr}/share/%{name}/database
%dir %{_usr}/share/%{name}/htdocs
%dir %{_usr}/share/%{name}/htdocs/css
%dir %{_usr}/share/%{name}/htdocs/images
%dir %{_usr}/share/%{name}/htdocs/js
%dir %{py_sitescriptdir}/%{name}
%dir %{py_sitescriptdir}/%{name}/modules
%dir %{py_sitescriptdir}/%{name}/modules/auth
%dir %{py_sitescriptdir}/%{name}/modules/auth/loginpassword
%dir %{py_sitescriptdir}/%{name}/modules/log
%dir %{py_sitescriptdir}/%{name}/modules/log/stderr
%dir %{py_sitescriptdir}/%{name}/views
%dir %{py_sitescriptdir}/%{name}/templates
%attr(755,root,root) %{_bindir}/prewikka-httpd
%attr(755,root,root) %{py_sitescriptdir}/%{name}/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/%{name}/modules/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/%{name}/modules/auth/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/%{name}/modules/auth/loginpassword/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/%{name}/modules/log/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/%{name}/modules/log/stderr/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/%{name}/views/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/%{name}/templates/*.py[co]
%attr(755,root,root) %{_usr}/share/%{name}/cgi-bin/*
%{_usr}/share/%{name}/database/*
%{_usr}/share/%{name}/htdocs/css/*
%{_usr}/share/%{name}/htdocs/images/*
%{_usr}/share/%{name}/htdocs/js/*
