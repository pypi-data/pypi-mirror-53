%define name              ligo-scald
%define version           0.7.1
%define unmangled_version 0.7.1
%define release           1

Summary:   SCalable Analytics for Ligo/virgo/kagra Data
Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Source0:   %{name}-%{unmangled_version}.tar.gz
License:   GPLv2+
Group:     Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:    %{_prefix}
Vendor:    Patrick Godwin <patrick.godwin@ligo.org>
Url:       https://git.ligo.org/gstlal-visualisation/ligo-scald

BuildArch: noarch
BuildRequires: rpm-build
BuildRequires: epel-rpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python-setuptools

%description
ligo-scald is a gravitational-wave monitoring and dynamic data visualization
tool.

# -- python2-ligo-scald

%package -n python2-%{name}
Summary:  %{summary}
Provides: %{name}
Obsoletes: %{name}
Requires: python-dateutil
Requires: python-future
Requires: python-six
Requires: python-urllib3
Requires: python2-bottle
Requires: python2-ligo-common
Requires: python2-numpy
Requires: python2-pyyaml
Requires: h5py

%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
ligo-scald is a gravitational-wave monitoring and dynamic data visualization
tool.

# -- build steps

%prep
%setup -n %{name}-%{unmangled_version}

%build
%py2_build

%install
%py2_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python2-%{name}
%license LICENSE
%{_bindir}/scald
%{python2_sitelib}/*
