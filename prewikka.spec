# TODO:
# - do everything
Summary:	Prelude IDS web application
Summary(pl):	Aplikacja WWW dla Prelude IDS
Name:		prewikka
%define	_rc	rc7
Version:	0.9.0
Release:	0.%{_rc}.1
License:	GPL
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	85407fa9c89cd0aab2f76cdc28197d90
URL:		http://www.prelude-ids.org/
BuildRequires:	python-cheetah
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prewikka is a professional looking application providing advanced
feature like contextual filtering, aggregation, etc.

%description -l pl
Prewikka to profesjonalnie wygl±daj±ca aplikacja daj±ca zaawansowane
mo¿liwo¶ci, takie jak filtrowanie kontekstowe, agregacjê itp.

%prep
%setup -q -n %{name}-%{version}-%{_rc}

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
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*.[co]
