# Remsnet  Spec file for package serialmail
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
%define name serialmail
%define version 0.75
%define prefix /usr
%define bindir %{prefix}/bin
%define libdir %{prefix}/lib
%define mandir %{prefix}/man
%define includedir %{prefix}/include

Name:           %{name}
Version:        %{version}
Release:        1.2_rcis
Group:          System Environment/Daemons
Source:         http://cr.yp.to/software/serialmail-0.75.tar.gz
Patch:          %{name}-0.75.errno.patch
Patch1:         %{name}-0.75.conf.home.diff
Patch2:         %{name}-auth.patch
URL:            http://cr.yp.to/serialmail.html
License:        GPL v2 - Check with DJB http://cr.yp.to/djb.html
Summary:        Qmail Mail Transfer Agent -- Serial Mail Delivery Utilities
Requires:       qmail
Requires:       coreutils
Packager:       Horst Venzke <horst.venzke@remsnet.de
Provides:       %{name}

%description
serialmail is a collection of tools for passing mail across serial
links. It works with qmail: you use qmail to deliver messages to a
maildir, and then serialmail to deliver messages out of the maildir.

serialmail is designed to handle three common types of mail delivery
between a dialup computer and an ISP:

   * Delivery to the ISP. The dialup computer sends all outgoing mail to
     the ISP.

   * AutoTURN delivery from the ISP. After the dialup computer makes an
     SMTP connection to the ISP, it automatically receives an SMTP
     connection back from the ISP if there is any new mail for it. This
     provides the same power as ETRN but does not require a special
     client.

   * User-controlled delivery from the ISP. A user with a shell account
     can switch from qmail-pop3d to serialmail without pestering the
     sysadmin. The user can also decide whether undeliverable messages
     should be left for POP retrieval or bounced back to the sender.

serialmail supports SMTP, including ESMTP PIPELINING, and QMTP.

serialmail uses ucspi-tcp/tcpclient for networking. It can also be used
with future UCSPI clients for transparent compression, IPv6, etc.


%prep
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%setup %{name}-%{version}-root

%patch -p1
%patch1 -p0
%patch2 -p1

%build

        make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_mandir}/man0
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

make install

install -m 755 maildirqmtp %{buildroot}%{_bindir}/maildirqmtp
install -m 755 auto-str %{buildroot}%{_bindir}/auto-str
install -m 755 maildirserial %{buildroot}%{_bindir}/maildirserial
install -m 755 maildirsmtp %{buildroot}%{_bindir}/maildirsmtp
install -m 755 serialqmtp %{buildroot}%{_bindir}/serialqmtp
install -m 755 serialsmtp %{buildroot}%{_bindir}/serialsmtp
install -m 755 *.0 %{buildroot}%{_mandir}/man0/
ranlib mess822.a
install -m 644 mess822.a %{buildroot}%{_libdir}/mess822.a
install -m 644 mess822.h %{buildroot}%{_includedir}/mess822.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%{_bindir}/maildirserial
%{_bindir}/auto-str
%{_bindir}/maildirqmtp
%{_bindir}/maildirsmtp
%{_bindir}/serialqmtp
%{_bindir}/serialsmtp
%{_mandir}/man0/
%{_libdir}/*.a
%{_includedir}/*.h

%doc AUTOTURN   BLURB   CHANGES  FROMISP  INSTALL  README
%doc THANKS     TODO    TOISP    VERSION
%doc *.3

%changelog
* Sat Mar 22 2014 support@remsnet.de
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools
- updated serialmail errno.patch form netqmail-1.06
- added serialmail-auth.patch

* Sat May 02 2009  support@remsnet.de
- update to SLES 10 i386
* Sun Jul 04 2004 Horst Venzke <hv@remsnet.de>
- First Package
