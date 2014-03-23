
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

%define         name tmda
%define         version 1.1.12

Name:           %{name}
Summary:        Tagged Message Delivery Agent
Version:        %{version}
Release:        1.1_rcis
License:        GPLv2
Group:          System Environment/Daemons
URL:            http://tmda.net
Source:         %{name}-%{version}.tar.gz
Buildroot:      %{_tmppath}/%{name}-%{version}
Packager:       Horst Venzke <horst.venzke@remsnet.de>
Requires:       python-base python
Requires:       coreutils
Requires:       qmail
BuildRequires:  python >= 2.0
BuildRequires:  python-devel >= 2.0


%description
TMDA is an OSI certified software application designed to significantly
reduce the amount of SPAM/UCE (junk-mail) you receive.  TMDA combines a
"whitelist" (for known/trusted senders), a "blacklist" (for undesired
senders), and a cryptographically enhanced confirmation system (for unknown,
but legitimate senders).

%prep

%setup -q -n %{name}-%{version}


LDFLAGS="-Wl,-z,relro,-z,now,-lcrypto"
CPPFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"
export CFLAGS="%{optflags} -D_GNU_SOURCE -Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s ${OPTIMIZATION} -D_LARGEFILE64_SOURCE -DIDMAP_RID_SUPPORT_TRUSTED_DOMAINS"

%if 0%{?suse_version} && 0%{?suse_version} < 1141
%{?suse_update_config:%{suse_update_config -f}}
%endif


%build


LDFLAGS="-Wl,-z,relro,-z,now,-lcrypto"
CPPFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"
export CFLAGS="%{optflags} -D_GNU_SOURCE -Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s ${OPTIMIZATION} -D_LARGEFILE64_SOURCE -DIDMAP_RID_SUPPORT_TRUSTED_DOMAINS"

python ./compileall



%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

# python install settings
%define pyprefix %(python -c 'import sys; print sys.prefix')
%define pyver %(python -c 'import sys; print sys.version[:3]')
%define pylibdir %{pyprefix}/lib/python%{pyver}/site-packages
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}/tmda,%{pylibdir}/TMDA}

# install TMDA
install -m 755 bin/tmda-* %{buildroot}%{_bindir}
install -m 644 templates/*.txt %{buildroot}%{_datadir}/tmda
install -m 644 TMDA/*.{py,pyc} %{buildroot}%{pylibdir}/TMDA
install -m 755 contrib/{collectaddys,printcdb,printdbm} %{buildroot}%{_bindir}

# install ontrib stuff
cp -rp contrib %{buildroot}%{_datadir}/tmda/
chown root:root %{buildroot}%{_datadir}/tmda/contrib

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{version} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(755,root,root)
%{_libdir}/python2.7/site-packages/TMDA/*

%dir %{_datadir}/tmda
%{_bindir}/collectaddys
%{_bindir}/printcdb
%{_bindir}/printdbm
%{_bindir}/tmda-address
%{_bindir}/tmda-check-address
%{_bindir}/tmda-filter
%{_bindir}/tmda-inject
%{_bindir}/tmda-keygen
%{_bindir}/tmda-ofmipd
%{_bindir}/tmda-pending
%{_bindir}/tmda-rfilter
%{_bindir}/tmda-sendmail


%defattr(644,root,root)
%{_datadir}/tmda/*.txt

%package contrib
Summary: TMDA - contrib files

Group: Applications/System
Requires: %{name}
Provides: %{name}-contrib

%description contrib
TMDA - contrib files

%files contrib
%{_datadir}/tmda/contrib/*



%package doc
Summary: TMDA - Documents
Group: Applications/System
Requires: %{name}
Provides: %{name}-doc
Provides: %{name}-html
Provides: %{name}-pdf

%description doc
TMDA - Documents

%files doc
%defattr(-,root,root)
%doc ChangeLog COPYING CRYPTO INSTALL README THANKS UPGRADE contrib/
%doc doc/pdf/*.pdf
%doc doc/html/* doc/html/attachments/*

%changelog
* Sat Mar 22 2014 support@remsnet.de
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools
- added subpkg doc

* Sat May 02 2009  support@remsnet.de
- update to SLES 10 i386
* Sun Jul 04 2004 Horst Venzke <hv@remsnet.de>
- First Package
