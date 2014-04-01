#
# Remsnet  Spec file for package tinycdb
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

Summary: A package for maintenance of constant databases
Name: tinycdb
Version: 0.78
Release: 1.5_rcis
Source: ftp://ftp.corpit.ru/pub/tinycdb/%{name}-%version.tar.gz
License: Public Domain
Packager: Horst Venzke <horst.venzke@remsnet.de>
Group: System Environment/Libraries
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root
Summary: TinyCDB - a Constant DataBase
Conflicts: cdb

%description
tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases. The database
structure is tuned for fast reading:
+ Successful lookups take normally just two disk accesses.
+ Unsuccessful lookups take only one disk access.
+ Small disk space and memory size requirements; a database
  uses 2048 bytes for the header and 24 bytes plus size of
  (key,value) per record.
+ Maximum database size is 4GB; individual record size is not
  otherwise limited.
+ Portable file format.
+ Fast creation of new databases.
+ No locking, updates are atomical.

This package contains both the utility and the development
files, together with nss_cdb module.

%package devel
Summary: Development files for the tinycdb library.
Group: System Environment/Libraries
Requires: %name = %version-%release
Summary: Development files for tinycdb
%description devel
tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases.

This package contains tinycdb development libraries and header files.

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS" \
 staticlib sharedlib cdb-shared nss \
 sysconfdir=/etc

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
%makeinstall DESTDIR=$RPM_BUILD_ROOT \
 libdir=%_libdir bindir=%_bindir mandir=%_mandir \
 syslibdir=/%_lib sysconfdir=/etc \
 includedir=%_includedir \
 install-all install-nss install-piclib install-sharedlib \
 INSTALLPROG=cdb-shared CP="cp -p"

%files
%defattr(-,root,root)
%_bindir/*
%_mandir/man1/*
%_mandir/man5/*
%_libdir/libcdb.so.*
/%_lib/libnss_cdb*
/etc/cdb-Makefile
%doc ChangeLog NEWS debian/changelog

%files devel
%defattr(-,root,root)
%_libdir/libcdb.a
%_libdir/libcdb_pic.a
%_libdir/libcdb.so
%_mandir/man3/*
%_includedir/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog

* Sat Mar 22 2014 support@remsnet.de
- updated to v0.78
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools
- added conflicks cdb, there can be only one ...

* Sat May 02 2009  support@remsnet.de
- update to SLES 10 SP1 i386
