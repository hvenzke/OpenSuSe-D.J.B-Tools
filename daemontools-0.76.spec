#
# Remsnet  Spec file for package daemontools (Version 0.76)
#
# Copyright (c) 1995-2008 Remsnet Netzwerk Service OhG , D73630 Remshalden
# Copyright (c) 2008 Remsnet Consullting & Internet Services LTD , D73630 Remshalden

# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
# norootforbuild

Name:           daemontools
Version:        0.76
Release:        oss13.1
License:        Public Domain
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Obsoletes:      %{name}-toaster %{name}-toaster-doc
Provides:       %{name}-toaster
Group:          System/Base
Packager:       Horst Venzke <horst.venzke@remsnet.de>
Summary:        DJB daemontools - tools for managing UNIX services
URL:            http://cr.yp.to/daemontools.html
Source:         %{name}-%{version}.tar.bz2
Source1:        %{name}-%{version}-man.tar.bz2
Source2:        %{name}.service
Source3:        %{name}.smtp
Source4:        %{name}.djb.ids
Source5:        %{name}.svscan-start
Patch:          %{name}-errno.patch
Patch1:         %{name}-no-return.patch
Patch2:         fix_includes_prototypes.patch


%description
Supervise monitors a service. It starts the service and restarts the
service if it dies.  The companion  svc program  stops,  pauses,  or
restarts the service on sysadmin request.  The svstat program prints
a one-line status report.

Multilog saves error  messages to  one or more  logs.  It optionally
timestamps each line and,  for each log,  includes or excludes lines
matching specified patterns.  It automatically rotates logs to limit
the amount of disk space used.   If the disk fills up, it pauses and
tries again, without losing any data.

Author:
--------
    D. J. Bernstein


%prep


%setup -q -a 1
%patch
%patch1
%patch2

cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} src/svscan-start

%build
cd src
echo 'cc %{optflags}' > conf-cc
echo 'cc -s %{optflags}' > conf-ld
echo %{buildroot}/%{_prefix} > home
%{__make}


%install
%{__install} -d %{buildroot}
%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -m 755 -d %{buildroot}%{_sysconfdir}/tcprules.d
%{__install} -m 755 -d %{buildroot}/command
%{__install} -m 755 -d %{buildroot}/service
%{__install} -m 1755 -d %{buildroot}/package
%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 755 -d %{buildroot}%_var/log/multilog
%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -d %{buildroot}%{_sysconfdir}/systemd
%{__install} -d %{buildroot}%{_sysconfdir}/systemd/system

pushd src
    for BFILE in envdir envuidgid fghack multilog pgrphack readproctitle setlock setuidgid softlimit supervise svc svok svscan svscanboot svstat tai64n tai64nlocal svscan-start
    do
        %{__install} -m 755 $BFILE %{buildroot}%{_bindir}
        cd %{buildroot}/command
        %__ln_s ../usr/bin/$BFILE  .
        cd  /usr/src/packages/BUILD/daemontools-0.76/src
    done
popd

%{__install} -d %{buildroot}%{_mandir}/man8
%{__install} -m 755 %{name}.service %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service
%{__install} -m 644 %{name}.smtp %{buildroot}%{_sysconfdir}/tcprules.d/smtp
%{__install} -m 644 %{name}-%{version}-man/*8 %{buildroot}%{_mandir}/man8


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(0755,root,root)
%{_bindir}/envdir
%{_bindir}/envuidgid
%{_bindir}/fghack
%{_bindir}/multilog
%{_bindir}/pgrphack
%{_bindir}/readproctitle
%{_bindir}/setlock
%{_bindir}/setuidgid
%{_bindir}/softlimit
%{_bindir}/supervise
%{_bindir}/svc
%{_bindir}/svok
%{_bindir}/svscan
%{_bindir}/svscanboot
%{_bindir}/svstat
%{_bindir}/tai64n
%{_bindir}/tai64nlocal
%{_bindir}/svscan-start

# http://thedjbway.b0llix.net/daemontools/installation.html
%defattr(1755,root,root)
%dir /package

%defattr(0755,root,root)
%dir /service
%dir /command
%dir %{_sysconfdir}/tcprules.d
%dir %_var/log/multilog

%defattr(0755,root,root)
%{_sysconfdir}/tcprules.d/smtp
/etc/systemd/system/daemontools.service
/command/envdir
/command/envuidgid
/command/fghack
/command/multilog
/command/pgrphack
/command/readproctitle
/command/setlock
/command/setuidgid
/command/softlimit
/command/supervise
/command/svc
/command/svok
/command/svscan
/command/svscanboot
/command/svstat
/command/tai64n
/command/tai64nlocal
/command/svscan-start


%defattr(0644,root,root,0755)
%doc src/CHANGES %doc package/README %doc src/TODO %doc daemontools.djb.ids
%{_mandir}/man8/envdir.8.*
%{_mandir}/man8/envuidgid.8.*
%{_mandir}/man8/fghack.8.*
%{_mandir}/man8/multilog.8.*
%{_mandir}/man8/pgrphack.8.*
%{_mandir}/man8/readproctitle.8.*
%{_mandir}/man8/setlock.8.*
%{_mandir}/man8/setuidgid.8.*
%{_mandir}/man8/softlimit.8.*
%{_mandir}/man8/supervise.8.*
%{_mandir}/man8/svc.8.*
%{_mandir}/man8/svok.8.*
%{_mandir}/man8/svscan.8.*
%{_mandir}/man8/svscanboot.8.*
%{_mandir}/man8/svstat.8.*
%{_mandir}/man8/tai64n.8.*
%{_mandir}/man8/tai64nlocal.8.*

%pre

/usr/bin/getent group 64011  >/dev/null || groupadd -g  64011 multilog
/usr/bin/getent passwd 64017  >/dev/null || useradd -g  multilog -u 64017 -d /var/log/multilog  -s /bin/true multilog

if [ -d /var/log/multilog ]; then
 chown -R 64017:64011 /var/log/multilog
fi

 systemctl daemon-reload

%post
if [ -e /etc/systemd/system/daemontools.service ]; then
echo " starting daemontools.service"
systemctl start daemontools.service
fi

%preun

if [ -e /etc/systemd/system/daemontools.service ]; then
echo " halting daemontools.service"
systemctl stop daemontools.service
fi

%postun
if [ -e /etc/systemd/system/daemontools.service ]; then
echo " remove daemontools.service"
rm /etc/systemd/system/daemontools.service
 systemctl daemon-reload

fi

#/usr/sbin/userdel multilog
#/usr/sbin/groupdel multilog



%changelog
* Sun Dec 22 2013 Horst.venzke@remsnet.de - RCIS LTD  0.76-oss.13.1 rc4
- rewitten daemontools spec for Opensuse 13.1 with systemd
