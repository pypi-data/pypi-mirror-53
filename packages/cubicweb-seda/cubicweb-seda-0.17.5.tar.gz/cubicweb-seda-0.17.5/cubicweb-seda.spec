# for el5, force use of python2.6
%if 0%{?el5}
%define python python26
%define __python /usr/bin/python2.6
%else
%define python python
%define __python /usr/bin/python
%endif
%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           cubicweb-seda
Version:        0.13.0
Release:        logilab.1%{?dist}
Summary:        Data Exchange Standard for Archival
Group:          Applications/Internet
License:        LGPL
Source0:        cubicweb-seda-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  %{python} %{python}-setuptools
Requires:       cubicweb >= 3.25.3
Requires:       cubicweb-eac
Requires:       cubicweb-skos >= 1.3.0
Requires:       cubicweb-compound >= 0.7
Requires:       cubicweb-relationwidget >= 0.4l
Requires:       cubicweb-squareui
Requires:       %{python}-rdflib >= 4.1
Requires:       %{python}-pyxst >= 0.2
Requires:       %{python}-six >= 1.4.0

%description
Data Exchange Standard for Archival

%prep
%setup -q -n cubicweb-seda-%{version}
%if 0%{?el5}
# change the python version in shebangs
find . -name '*.py' -type f -print0 |  xargs -0 sed -i '1,3s;^#!.*python.*$;#! /usr/bin/python2.6;'
%endif

%install
%{__python} setup.py install --no-compile --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_python_sitelib}/*
