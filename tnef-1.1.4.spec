# Remsnet  Spec file for package tnef
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


%define         name tnef
%define         version 1.4.10

Name:           %{name}
Summary:        Decodes MS-TNEF attachments
Version:        %{version}
Release:        1.1_rcis
License:        GPLv2
Group:          System Environment/Daemons
URL:            http://sourceforge.net/projects/tnef
Source:         tnef-%{version}.tar.gz
Buildroot:      %{_tmppath}/%{name}-%{version}
Packager:       Horst Venzke <horst.venzke@remsnet.de>

%description
TNEF is a program for unpacking MIME attachments of type
"application/ms-tnef". This is a Microsoft only attachment.

Due to the proliferation of Microsoft Outlook and Exchange mail servers,
more and more mail is encapsulated into this format.

The TNEF program allows one to unpack the attachments which were
encapsulated into the TNEF attachment.  Thus alleviating the need to use
Microsoft Outlook to view the attachment.

%prep

%setup -q -n tnef-%{version}

LDFLAGS="-Wl,-z,relro,-z,now,-lcrypto"
CPPFLAGS="-Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s"
export CFLAGS="%{optflags} -D_GNU_SOURCE -Ofast -mfpu=vfp -march=armv6zk -mtune=arm1176jzf-s ${OPTIMIZATION} \
        -D_LARGEFILE64_SOURCE -DIDMAP_RID_SUPPORT_TRUSTED_DOMAINS"

%if 0%{?suse_version} && 0%{?suse_version} < 1141
%{?suse_update_config:%{suse_update_config -f}}
%endif



CONFIGURE_OPTIONS="\
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --sysconfdir=/var/qmail/control \
    --localstatedir=/var/run
"
./configure ${CONFIGURE_OPTIONS}

%build

        make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

        make DESTDIR=%{buildroot} install
        make DESTDIR=%{buildroot} install-man
        make DESTDIR=%{buildroot} install-html

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{version} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(755,root,root)
/usr/bin/tnef

%defattr(644,root,root)
%_mandir/man1/tnef.1.gz

%doc README ChangeLog AUTHORS NEWS TODO BUGS

%changelog
* Sat Mar 22 2014 support@remsnet.de
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools

* Mon Jul 04 2004 Horst Venzke <hv@remsnet.de>
- First Package
