
# Remsnet  Spec file for package tmda
#
# Copyright (c) 1995-2008 Remsnet Netzwerk Service OhG , D-73630 Remshalden
# Copyright (c) 2008-2014 Remsnet Consullting & Internet Services LTD , D-40476 Duesseldorf


# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments  https://github.com/remsnet/DJB-Tools/tree/master

Name: cdb
Version: 0.75
Release: 1.5_rcis
Group:   Applications/Databases
URL:     http://cr.yp.to/cdb.html
License:  Public Domain
Packager: Horst Venzke <horst.venzke@remsnet.de>
Source:  http://cr.yp.to/cdb/cdb-0.75.tar.gz
Source1:  %{name}-%{version}-12tocdbm.sh
Patch:   %{name}-%{version}-errno.diff
Patch1:   %{name}-%{version}-traversal.diff2
Summary: Constant DataBase
Buildroot: /usr/src/packages/BUILD/%{name}-%{version}
Conflicts:  tinycdb

%description
cdb is a fast, reliable, lightweight package for creating and reading constant databases.

%package devel
Summary: cdb static libraries and headers
Group: Development/Libraries

%description devel
Libraries and header files needed to develop applications using cdb databases

%prep
%setup -n %{name}-%{version}

%patch1 -p1 -F 10
%patch -p0 -F 10

%build
make

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man3
mkdir -p $RPM_BUILD_ROOT/usr/include
mkdir -p $RPM_BUILD_ROOT/usr/lib/
mkdir -p $RPM_BUILD_ROOT/usr/lib/cdb-0.75/

# install manpages
install -m 644 *.1 $RPM_BUILD_ROOT/usr/man/man1
install -m 644 *.3 $RPM_BUILD_ROOT/usr/man/man3


# install bin files
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/bin/12tocdbm
install -d %{buildroot}/usr/bin/
install -m 755 cdbdump %{buildroot}/usr/bin/
install -m 755 cdbget %{buildroot}/usr/bin/
install -m 755 cdbmake %{buildroot}/usr/bin/
install -m 755 cdbmake-12 %{buildroot}/usr/bin/
install -m 755 cdbmake-sv %{buildroot}/usr/bin/
install -m 755 cdbstats %{buildroot}/usr/bin/
install -m 755 cdbtest %{buildroot}/usr/bin/

# install devel files
install -d %{buildroot}%{_libdir}/cdb-0.75/
install -m 644 *.h %{buildroot}%{_libdir}/cdb-0.75/
install -m 644 *.a %{buildroot}%{_libdir}/cdb-0.75/

%post
%{__ln_s} -f %{_bindir}/cdbmake /usr/local/bin/cdbmake

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) /usr/bin/*
%attr(-,root,root) /usr/man/man1/*
%attr(-,root,root) %doc CHANGES FILES Makefile README SYSDEPS TARGETS TODO VERSION

%files devel
%attr(-,root,root) /usr/man/man3/*
%{_libdir}/cdb-0.75/*.h
%{_libdir}/cdb-0.75/*.a

%changelog
* Sat Mar 22 2014 support@remsnet.de
- updated to v0.75
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools
- added conflicks tinycdb, there can be only one ...

* Sat May 02 2009  support@remsnet.de
- update to SLES 10 SP1 i386
- added cdb-0.75-traversal.diff2

* Wed Apr 26 2006 Horst Venzke <hv@remsnet.de>
- Package for suse10.0 x86_ia64
- updated to errno cdb-0.75-errno.diff
- update to 0.75

* Sun Jul 04 2004 Horst Venzke <hv@remsnet.de>
- First Package, dovecot betta 0.2
- added errno cdb-0.55-errno.diff
