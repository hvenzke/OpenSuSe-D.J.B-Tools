%define         name mess822
%define         version 0.58
%define         prefix /usr
%define         bindir %{prefix}/bin
%define         libdir %{prefix}/lib
%define         mandir %{prefix}/man
%define         includedir %{prefix}/include



Name:           %{name}
Summary:        mess822 is a library for parsing Internet mail messages.
Version:        %{version}
Release:        1.3_rcis
Group:          Utilities/System
Source0:        http://cr.yp.to/software/mess822-0.58.tar.gz
Patch:          %{name}-0.58.errno.patch
Patch1:         %{name}-smtp-auth-patch.txt
Patch2:         %{name}-0.58-nonroot-20140323.patch
URL:            http://pobox.com/~djb/mess822.html
License:        GPLv2 -  Check with djb@koobera.math.uic.edu
Buildroot:      %{_tmppath}/%{name}-%{version}
Packager:       Horst Venzke <hv@remsnet.de>
Requires:       qmail
Requires:       coreutils
Provides:       mess822

%description
mess822 is a library for parsing Internet mail messages. The mess822
package contains several applications that work with qmail:

   * ofmipd rewrites messages from dumb clients. It supports a database
     of recognized senders and From lines, using cdb for fast lookups.

   * new-inject is an experimental new version of qmail-inject. It
     includes a flexible user-controlled hostname rewriting mechanism.

   * iftocc can be used in .qmail files. It checks whether a known
     address is listed in To or Cc.

   * 822header, 822field, 822date, and 822received extract various
     pieces of information from a mail message.

   * 822print converts a message into an easier-to-read format.

mess822 supports the full complexity of RFC 822 address lists, including
address groups, source routes, spaces around dots, etc. It also supports
common RFC 822 extensions: backslashes in atoms, dots in phrases,
addresses without host names, etc. It extracts each address as an
easy-to-use string, with a separate string for the accompanying comment.

mess822 converts RFC 822 dates into libtai's struct caltime format. It
supports numeric time zones, the standard old-fashioned time zones, and
many nonstandard time zones.

mess822 is fast. For example, extracting 10000 addresses from a 160KB To
field takes less than a second on a Pentium-100.

%prep
%setup

%patch -p1
%patch1 -p1
%patch2 -p0

%build
make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man0
mkdir -p %{buildroot}%{_libdir}/mess822
mkdir -p %{buildroot}%{_includedir}/mess822/

sed "s}/usr/local}$INST_ROOT/usr}" conf-home > conf-home.tmp
mv conf-home.tmp conf-home


install -m 755 822header %{buildroot}%{_bindir}/822header
install -m 755 822print %{buildroot}%{_bindir}/822print
install -m 755 822received %{buildroot}%{_bindir}/822received
install -m 755 822date %{buildroot}%{_bindir}/822date
install -m 755 ofmipd %{buildroot}%{_bindir}/ofmipd
install -m 755 parsedate %{buildroot}%{_bindir}/parsedate
install -m 755 iftocc %{buildroot}%{_bindir}/iftocc
install -m 755 new-inject %{buildroot}%{_bindir}/new-inject
install -m 755 rts %{buildroot}%{_bindir}/rts
install -m 755 tokenize %{buildroot}%{_bindir}/tokenize
install -m 755 addrlist %{buildroot}%{_bindir}/addrlist
install -m 755 *.0 %{buildroot}%{_mandir}/man0/
install -m 755 *.h %{buildroot}%{_includedir}/mess822/
install -m 755 *.a %{buildroot}%{_libdir}/mess822/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}



%files
%doc BLURB CHANGES INSTALL README
%doc THANKS TODO VERSION
%{_bindir}/822header
%{_bindir}/822print
%{_bindir}/822received
%{_bindir}/822date
%{_bindir}/ofmipd
%{_bindir}/parsedate
%{_bindir}/iftocc
%{_bindir}/new-inject
%{_bindir}/rts
%{_bindir}/tokenize
%{_bindir}/addrlist


%{_mandir}/man0/*
%{_includedir}/mess822/*
%{_libdir}/mess822/*

%changelog
* Sat Mar 22 2014 support@remsnet.de
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools
- added subpkg doc
- updated errno.patch form netqmail-1.06
- added mess822-0.58-nonroot-2003.03.05.patch
- added mess822-smtp-auth-patch.txt

* Sat May 02 2009  support@remsnet.de
- update to SLES 10 i386
* Sun Jul 04 2004 Horst Venzke <hv@remsnet.de>
- First Package
