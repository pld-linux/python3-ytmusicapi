# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	ytmusicapi
Summary:	Unofficial API for YouTube Music
Summary(pl.UTF-8):	Nieoficjalne API do YouTube Music
Name:		python3-%{module}
Version:	1.10.3
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/ytmusicapi/
Source0:	https://files.pythonhosted.org/packages/source/y/ytmusicapi/%{module}-%{version}.tar.gz
# Source0-md5:	76f51b1febebc308eeda699e48b30356
URL:		https://pypi.org/project/ytmusicapi/
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	python3-sphinx_autodoc_typehints >= 3.0
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
# replace with other requires if defined in setup.py
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ytmusicapi is a Python 3 library to send requests to the YouTube Music
API. It emulates YouTube Music web client requests using the user's
cookie data for authentication.

%description -l pl.UTF-8
ytmusicapi jest biblioteką Pythona3 do wysyłania zapytań do YouTube
Music API. Emuluje zapytania klienta web YouTube Music używając
ciasteczek użytkownika do uwierzytelniania.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}
cat > setup.py << EOF
#!%{_bindir}/python3

import setuptools

if __name__ == "__main__":
    setuptools.setup(version='%{version}')
EOF

%build
%py3_build

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/ytmusicapi
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py3.13.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/*
%endif
