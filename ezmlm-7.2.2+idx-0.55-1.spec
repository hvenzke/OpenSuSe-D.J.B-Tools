# Remsnet  Spec file for package ezmlm-idx
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


%define name ezmlm
%define idxversion 0.55
%define htmlversion 0.40
%define version 7.2.2

%define qlog /var/log/qmail
%define prefix /usr
%define bin_dir /usr/bin
%define sbin_dir /usr/sbin
%define conf_dir /var/qmail/control
%define tmppath /var/tmp
%define webroot /srv/www
%define dbase mysql

Name:           %{name}
Summary:        Qmail Easy Mailing List Manager + IDX patches.
Version:        %{version}
Release:        1.rcis
Group:          Utilities/System
URL:            http://untroubled.org/ezmlm/
License:        Check with http://cr.yp.to/djb.html
Buildroot:      %{_tmppath}/%{name}-%{version}
Packager:       Horst Venzke <hv@remsnet.de>
Source0:        http://untroubled.org/ezmlm/archive/7.2.2/%{name}-idx-%{version}.tar.gz
Source2:        ezman-%{htmlversion}.html.tar.bz2
Summary:        Qmail Easy Mailing List Manager + IDX patches with %{dbase} database support.
Group:          Utilities/System
Obsoletes:      ezmlm-idx
Conflicts:      ezmlm, ezmlm-idx-std, ezmlm-idx-pgsql, ezmlm-idx-mysql , ezmlm-toaster
Provides:       ezmlm
BuildRequires:  bison >= 2.6
BuildRequires:  flex >=  2.5.34
BuildRequires:  gettext-tools >= 0.18.2
BuildRequires:  automake >= 1.13.2
BuildRequires:  autoconf >= 2.67
BuildRequires:  gcc  >= 4.7
BuildRequires:  openldap2-devel >= 2.4.31
BuildRequires:  binutils  >= 2.23.1
BuildRequires:  libtool >= 2.4.1
BuildRequires:  libmysqlclient-devel
Requires:       coreutils
Requires:       libmysqlclient18
Requires:       qmail >= 1.05
Requires:       tinycdb >= 0.78

%description
ezmlm lets users set up their own mailing lists within qmail's address
hierarchy. A user, Joe, types

   ezmlm-make ~/SOS ~/.qmail-sos joe-sos isp.net

and instantly has a functioning mailing list, joe-sos@isp.net, with all
relevant information stored in a new ~/SOS directory.

ezmlm sets up joe-sos-subscribe and joe-sos-unsubscribe for automatic
processing of subscription and unsubscription requests. Any message to
joe-sos-subscribe will work; Joe doesn't have to explain any tricky
command formats. ezmlm will send back instructions if a subscriber sends
a message to joe-sos-request or joe-sos-help.

ezmlm automatically archives new messages. Messages are labelled with
sequence numbers; a subscriber can fetch message 123 by sending mail to
joe-sos-get.123. The archive format supports fast message retrieval even
when there are thousands of messages.

ezmlm takes advantage of qmail's VERPs to reliably determine the
recipient address and message number for every incoming bounce message.
It waits ten days and then sends the subscriber a list of message
numbers that bounced. If that warning bounces, ezmlm sends a probe; if
the probe bounces, ezmlm automatically removes the subscriber from the
mailing list.

ezmlm is easy for users to control. Joe can edit ~/SOS/text/* to change
any of the administrative messages sent to subscribers. He can remove
~/SOS/public and ~/SOS/archived to disable automatic subscription and
archiving. He can put his own address into ~/SOS/editor to set up a
moderated mailing list. He can edit ~/SOS/{headeradd,headerremove} to
control outgoing headers. ezmlm has several utilities to manually
inspect and manage mailing lists.

ezmlm uses Delivered-To to stop forwarding loops, Mailing-List to
protect other mailing lists against false subscription requests, and
real cryptographic cookies to protect normal users against false
subscription requests. ezmlm can also be used for a sublist,
redistributing messages from another list.

ezmlm is reliable, even in the face of system crashes. It writes each
new subscription and each new message safely to disk before it reports
success to qmail.

ezmlm doesn't mind huge mailing lists. Lists don't even have to fit into
memory. ezmlm hashes the subscription list into a set of independent
files so that it can handle subscription requests quickly. ezmlm uses
qmail for blazingly fast parallel SMTP deliveries.

The IDX patches add: Indexing, (Remote) Moderation, digest, make
patches, multi-language, MIME, global interface, %{dbase} database support.

%prep


#
U=`id -u`
if [ $U -gt 0 ]; then
        echo " Error:"
        echo " You must be root for installing or build this Package"
        exit
else
        echo "UID Check ok"
fi



%setup -T -b 0 -n ezmlm-idx-%{version}

#mv -f ezmlm-idx-%{idxversion}/* .


%build
        RC=%{_sysconfdir}/ezmlm/ezmlmrc
        sed -e 's{^#define TXT_ETC_EZMLMRC \"/etc/ezmlmrc\"{#define TXT_ETC_EZMLMRC \"$RC\"{' idx.h > idx.h.tmp
        mv idx.h.tmp idx.h
        perl -pi -e 's|`head -1 conf-sqlld`|-L/usr/lib/mysql -lmysqlclient -lnsl -lm -lz|g' Makefile


make %{dbase}
make it

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


mkdir -p %{buildroot}
install -d %{buildroot}/usr
install -d %{buildroot}/usr/bin
install -d %{buildroot}/usr/man
install -d %{buildroot}/%{_sysconfdir}
install -d %{buildroot}/%{_sysconfdir}/ezmlm

make install


sed '/cat/d' MAN > MAN.tmp
mv MAN.tmp MAN

./installer %{buildroot}/%{_prefix}/bin < BIN
./installer %{buildroot}/%{_prefix}/man < MAN

#
# ezmlm webadmin cgi
install -d %{buildroot}/srv/
install -d %{buildroot}/srv/www/
install -d %{buildroot}/srv/www/cgi-bin
install -m 755 ezmlm-cgi %{buildroot}/%{webroot}/cgi-bin/ezmlm.cgi
install -m 755 ezmlmrc %{buildroot}/%{_sysconfdir}/ezmlm/ezmlmrc
install -m 755 ezcgirc %{buildroot}/%{_sysconfdir}/ezmlm/ezcgirc
install -m 755 ezcgirc %{buildroot}/%{_sysconfdir}/ezmlm/ezcgirc.dist

tar fvxj $RPM_SOURCE_DIR/ezman-%{htmlversion}.html.tar.bz2


%files
%defattr (644,root,root)
%config(noreplace) %{_sysconfdir}/ezmlm/ezmlmrc
%config(noreplace) %{_sysconfdir}/ezmlm/ezcgirc
%config %{_sysconfdir}/ezmlm/ezcgirc.dist

%defattr (755,root,root)
%dir /%{webroot}/cgi-bin
/usr/bin/ezmlm*

%attr(6755,root,root) /%{webroot}/cgi-bin/ezmlm.cgi

%doc BLURB CHANGES* INSTAL*  README*
%doc THANKS TODO  VERSION FILES DOWNGRADE TARGETS UPGRADE SOURCES
%doc  ezmlmrc ezmlmrc.[a-zA-Z]*  ezman*
%doc qmail-*.tar.gz
%{_prefix}/man/*/*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{version} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%changelog
%changelog
* Wed May 21 2014 support@remsnet.de -r 7.22+idx0.55
- bumped to 7.22, idx 0.55
- updated URL from ezmlm.org to http://untroubled.org/ezmlm - ezmlm.org is no more the ezmlm home.
- install has ben renamed to installer
- spec rewrite due language file structure change

* Sat Mar 22 2014 support@remsnet.de
- updated to 6.0.1, idx 0.53
- massive spec rewrite due release bump

* Sat May 02 2009  support@remsnet.de
- update to SLES 10 SP1 i386

* Wed Apr 26 2006 Horst Venzke <hv@remsnet.de>
- Package for suse10.0 x86_ia64

* Mon Jul 5 2005 Horst Venzke <hv@remsnet.de>
- First packge
- added error.h patch for Suse9
- moved cgi staff to /srv/www/cgi-bin ( suse9 and up confrom )
