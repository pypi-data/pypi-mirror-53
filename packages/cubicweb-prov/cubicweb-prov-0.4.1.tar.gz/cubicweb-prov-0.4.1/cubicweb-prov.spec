# for el5, force use of python2.6
%if 0%{?el5}
%define python python26
%define __python /usr/bin/python2.6
%else
%define python python
%define __python /usr/bin/python
%endif
%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           cubicweb-prov
Version:        0.4.0
Release:        logilab.1%{?dist}
Summary:        The PROV Ontology
Group:          Applications/Internet
License:        LGPL
Source0:        cubicweb-prov-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  %{python} %{python}-setuptools
Requires:       cubicweb >= 3.24.0

%description
The PROV Ontology

%prep
%setup -q -n cubicweb-prov-%{version}
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
