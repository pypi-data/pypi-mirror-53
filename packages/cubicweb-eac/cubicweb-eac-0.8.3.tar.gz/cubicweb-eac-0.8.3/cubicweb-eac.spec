# for el5, force use of python2.6
%if 0%{?el5}
%define python python26
%define __python /usr/bin/python2.6
%else
%define python python
%define __python /usr/bin/python
%endif
%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           cubicweb-eac
Version:        0.6.0
Release:        logilab.2%{?dist}
Summary:        Implementation of Encoded Archival Context for CubicWeb
Group:          Applications/Internet
License:        LGPL
Source0:        cubicweb-eac-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  %{python} %{python}-setuptools
Requires:       cubicweb >= 3.24.0
Requires:       cubicweb-prov >= 0.4.0
Requires:       cubicweb-skos
Requires:       cubicweb-addressbook
Requires:       cubicweb-compound >= 0.6.0
Requires:       %{python}-six >= 1.4.0

%description
Implementation of Encoded Archival Context for CubicWeb

%prep
%setup -q -n cubicweb-eac-%{version}
%if 0%{?el5}
# change the python version in shebangs
find . -name '*.py' -type f -print0 |  xargs -0 sed -i '1,3s;^#!.*python.*$;#! /usr/bin/python2.6;'
%endif

%build
%{__python} setup.py build

%install
%{__python} setup.py install --no-compile --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_python_sitelib}/*

