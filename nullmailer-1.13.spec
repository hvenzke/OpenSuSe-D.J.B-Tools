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


Name: nullmailer
Summary: Simple relay-only mail transport agent
Version: 1.13
Release: oss13.1_01
License: GPL-2.0
Group: Networking/Daemons
Source: http://untroubled.org/nullmailer/archive/%{version}/nullmailer-%{version}.tar.gz
#
Source2: %{name}.run
Source3: %{name}-log.run
#
# PATCH-FIX-OPENSUSE conrad@quisquis.de
Patch1: %{name}-1.05-fhs.patch
# PATCH-FIX-OPENSUSE conrad@quisquis.de
Patch2: %{name}-1.05-mailuser.patch
# PATCH-FEATURE-UPSTREAM conrad@quisquis.de
Patch3: %{name}-1.10-ipv6.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-build
URL: http://untroubled.org/nullmailer/
Summary:  nullmailer relay-only -  Bruce Guenter <bruce@untroubled.org>
Provides: smtpdaemon smtp_daemon
Provides: /usr/sbin/sendmail /usr/lib/sendmail
Provides: mailer_daemon
Provides: nullmailer
Conflicts: sendmail
Conflicts: qmail
Conflicts: exim
Requires: daemontools
BuildRequires: libgnutls-devel

%description
Nullmailer is a mail transport agent designed to only relay all its
messages through a fixed set of "upstream" hosts.  It is also designed
to be secure.

%prep
%setup

%patch1 -p0
%patch2 -p0
%patch3 -p1

cp %{SOURCE2} scripts/
cp %{SOURCE3} scripts/

%build

CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-tls

for i in doc/nullmailer-queue.8 doc/nullmailer-send.8; do
    if [ ! -r "$i.orig" ]; then cp "$i" "$i.orig"; fi
    sed 's=/var/nullmailer/=%{_localstatedir}/spool/nullmailer/=;s=/usr/local/etc=%{_sysconfdir}=;s=/usr/local/libexec=%{_libexecdir}=' <"$i.orig" >"$i"
done

echo 'cc %{optflags}' > conf-cc
echo 'cc -s %{optflags}' > conf-ld
echo %{buildroot}/%{_prefix} > home

%{__make}

%install

%{__install} -d %{buildroot}
%{__install} -d %{buildroot}/service/
%{__install} -d %{buildroot}/service/nullmailer
%{__install} -d %{buildroot}/service/nullmailer/log
%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -d %{buildroot}%_var/log/multilog

make DESTDIR=%{buildroot} install-strip
%__ln_s ../sbin/sendmail %{buildroot}/usr/lib/sendmail
%{__install}  -m 755 scripts/nullmailer.run  %{buildroot}/service/nullmailer/run
%{__install}  -m 755 scripts/nullmailer-log.run %{buildroot}/service/nullmailer/log/run

#%__ln_s

%clean
rm -rf %{buildroot}

%pre
#
/usr/bin/getent group  64012 >/dev/null  || groupadd -g 64012 -r nullmail
/usr/bin/getent passwd 64018 >/dev/null || useradd  -u 64018 -g nullmail -d /var/lock/svc/nullmailer -M -r -s /bin/true nullmail ; usermod  --groups multilog nullmail

%post
if ! [ -L /service/nullmailer ]; then
        /command/svc -o /service/nullmailer
        /command/svc -o /service/nullmailer/log
fi
if ! [ -d /etc/nullmailer ]; then
       mkdir /etc/nullmailer
        chown nullmail:nullmail /etc/nullmailer
fi

if ! [ -s /etc/nullmailer/me ]; then
        /bin/hostname --fqdn >/etc/nullmailer/me
        chown nullmail:nullmail /etc/nullmailer/me
fi
if ! [ -s /etc/nullmailer/defaultdomain ]; then
        /bin/hostname --domain >/etc/nullmailer/defaultdomain
        chown nullmail:nullmail /etc/nullmailer/defaultdomain
fi

if ! [ -s /etc/nullmailer/remotes ]; then
        touch /etc/nullmailer/remotes
        echo mailip.vw.remsnet.de smtp >>/etc/nullmailer/remotes
        echo smtp1.vw.remsnet.de smtp >>/etc/nullmailer/remotes
        echo smtp2.vw.remsnet.de smtp >>/etc/nullmailer/remotes
        chown nullmail:nullmail /etc/nullmailer/remotes
fi

if ! [ -s /etc/nullmailer/adminaddr ]; then
        touch /etc/nullmailer/adminaddr
        chown nullmail:nullmail /etc/nullmailer/adminaddr
fi



%preun
if [ "$1" = 0 ]; then
        /command/svc -d /service/nullmailer
        cd /service/nullmailer
        rm run log/run
        svc -dx . log
fi

%postun
if [ "$1" = 0 ]; then
        # post-erase instructions
        /usr/sbin/userdel nullmail
        /usr/sbin/groupdel nullmail
fi

test -d /service/nullmailer && rm -rf /service/nullmailer


%files
%defattr(-,nullmail,nullmail)
%doc AUTHORS BUGS ChangeLog COPYING INSTALL NEWS README TODO
%dir /etc/nullmailer

%attr(04711,nullmail,nullmail) /usr/bin/mailq
/usr/bin/nullmailer-inject
/usr/bin/nullmailer-smtpd
/usr/lib/sendmail

%dir %{_libexecdir}/nullmailer
%{_libexecdir}/nullmailer/*
%{_mandir}/*/*
%attr(04711,nullmail,nullmail) /usr/sbin/nullmailer-queue
/usr/sbin/nullmailer-send
/usr/sbin/sendmail

%defattr(0755,root,root)
/service/nullmailer/log/run
/service/nullmailer/run

%changelog
* Sun Dec 22 2013 Horst.venzke@remsnet.de - RCIS LTD  0.76-oss.13.1 rc4
- rewitten nullmailer spec for Opensuse 13.1 with systemd
