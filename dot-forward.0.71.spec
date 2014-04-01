  Remsnet  Spec file for package dot-forward
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

%define         name dot-forward
%define         version 0.71

Name:           %{name}
Summary:        Qmail Forwarding agent
Version:        %{version}
Release:        1.5_rcis
License:        GPLv2
Group:          System Environment/Daemons
URL:            http://cr.yp.to/dot-forward.html
Source:         %{name}-%{version}.tar.gz
Patch:          %{name}errno.h-suse9.diff
Buildroot:      %{_tmppath}/%{name}-%{version}
Packager:       Horst Venzke <hv@remsnet.de>
Requires:       python
BuildRequires:  python-devel
Requires:       coreutils
Requires:       qmail


%description
D. J. Bernstein, djb@pobox.com

fastforward handles qmail forwarding according to a cdb database. It can
create forwarding databases from a sendmail-style /etc/aliases or from
user-oriented virtual-domain tables. See BLURB for a more detailed
advertisement.


%prep

%setup -q -n %{name}-%{version}

%patch -p0

%build

make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}/usr
mkdir -p %{buildroot}/usr/bin

install -m 755 dot-forward %{buildroot}/usr/bin/dot-forward


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{version} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(755,root,root)
/usr/bin/*


%defattr(-,root,root)
%doc README INSTALL FILES BLURB THANKS TODO SYSDEPS VERSION

%changelog
* Sat Mar 22 2014 support@remsnet.de -r1.5
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools

* Mon Jul 04 2004 Horst Venzke <hv@remsnet.de>  -r1.1
- First Package on suse 9.0

* Sun Apr 18 1999 <leon@obsidian.co.za>
-- initial release
-- http://updates.atomicorp.com/channels/source/dot-forward/dot-forward.spec
