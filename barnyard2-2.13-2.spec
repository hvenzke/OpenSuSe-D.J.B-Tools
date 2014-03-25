#
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


################################################################
# rpmbuild Package Options
# ========================
#       --with mysql
#               Builds a binary/package with support for MySQL.
#
#       --with postgresql
#               Builds a binary/package with support for PostgreSQL.
#
#       --with oracle
#               Builds a binary/package with support for Oracle.
#
# See pg 399 of _Red_Hat_RPM_Guide_ for rpmbuild --with and --without options.
################################################################

# Other useful bits
%define OracleHome /opt/oracle/OraHome1
%define SnortRulesDir %{_sysconfdir}/snort/rules
%define noShell /bin/false

# Default of no MySQL, but --with mysql will enable it
%define mysql 1
%{?_with_mysql:%define mysql 1}
# Default of no PostgreSQL, but --with postgresql will enable it
%define postgresql 0
%{?_with_postgresql:%define postgresql 1}

# Default of no Oracle, but --with oracle will enable it
%define oracle 0
%{?_with_oracle:%define oracle 1}

%define realname barnyard2


Summary: Snort Log Backend
Name: barnyard2
Version: 2.13
Release: 2.github_272eaf7cb9fe7dfa2faf1df22d8cb02233ad512d
License: GPL-2.0
Group: System/Monitoring
Source0: https://github.com/firnsy/barnyard2/tree/master/barnyard2-2.1.13-272eaf7cb9fe7dfa2faf1df22d8cb02233ad512d.zip
Source2: %{name}.config
Source3: %{name}-initrc
Source4: base-create_barnyard2_mysql.sql
Source5: %{name}-etc-sysconfig
Source6: %{name}-cron.hourly
Source7: %{name}-base-mysql.conf
Source8: %{name}-logrotate
Url: http://www.securixlive.com/barnyard2/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: libpcap-devel unzip libtool autoconf
Requires: snort >= 2.9.0

%description
Barnyard has 3 modes of operation:
One-shot, continual, continual w/ checkpoint.  In one-shot mode,
barnyard will process the specified file and exit.  In continual mode,
barnyard will start with the specified file and continue to process
new data (and new spool files) as it appears.  Continual mode w/
checkpointing will also use a checkpoint file (or waldo file in the
snort world) to track where it is.  In the event the barnyard process
ends while a waldo file is in use, barnyard will resume processing at
the last entry as listed in the waldo file.

%prep
%setup -q -n %{name}-master


%build
./autogen.sh
%configure --sysconfdir=%{_sysconfdir}/snort  \
   %if %{postgresql}
        --with-postgresql \
   %endif
   %if %{oracle}
        --with-oracle \
   %endif
   %if %{mysql}
        --with-mysql-libraries=/usr/%{_lib} \
   %endif
make

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/snort/
make -i install DESTDIR=$RPM_BUILD_ROOT
%{__install} -d -p $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,init.d,snort,cron.hourly,logrotate.d}
%{__install} -d -p $RPM_BUILD_ROOT%{_docdir}/%{name}/contrib
%{__install} -d -p $RPM_BUILD_ROOT%{_docdir}/%{name}/doc
%{__install} -d -p $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -d -p $RPM_BUILD_ROOT%{_sbindir}
%{__install} -d -p $RPM_BUILD_ROOT/var/log/snort
%{__install} -d -p $RPM_BUILD_ROOT/var/lib/snort
%{__install} -d -p $RPM_BUILD_ROOT/var/log/snort/archive
%{__install} -d -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
%{__install} -d -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/schemas/
%{__install} -p  schemas/create_mysql $RPM_BUILD_ROOT/%{_datadir}/%{name}/schemas/create_mysql
%{__install} -p  schemas/create_postgresql $RPM_BUILD_ROOT/%{_datadir}/%{name}/schemas/create_postgresql
%{__install} -p  schemas/create_oracle.sql $RPM_BUILD_ROOT/%{_datadir}/%{name}/schemas/create_oracle.sql
%{__install} -p  schemas/create_db2 $RPM_BUILD_ROOT/%{_datadir}/%{name}/schemas/create_db2
%{__install} -p  schemas/SCHEMA_ACCESS $RPM_BUILD_ROOT/%{_datadir}/%{name}/schemas/SCHEMA_ACCESS


%{__install} -m 644 %{S:7} $RPM_BUILD_ROOT%{_sysconfdir}/snort/barnyard2.conf
%{__install} -D -m 0644 %{S:2} %{buildroot}%{_localstatedir}/adm/fillup-templates/sysconfig.%{name}
%{__install} -m 755 %{S:3} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/barnyard2
%{__install} -m 755 %{S:4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/barnyard2
%{__install} -m 755 %{S:5} $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/barnyard2
%{__install} -m 755 %{S:8} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/barnyard2


cd %{buildroot}/usr/sbin/
%__ln_s ../../etc/init.d/%{name} rc%{name}
cd

%preun
%stop_on_removal

%postun
%restart_on_update
%insserv_cleanup

%post
%fillup_and_insserv



%clean
if [ -d $RPM_BUILD_ROOT ] && [ "$RPM_BUILD_ROOT" != "/"  ] ; then
        rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
%attr(755,root,root)  %dir /var/lib/snort
%attr(755,root,root) %dir /var/log/snort/archive
%attr(755,root,root) %dir %{_sysconfdir}/snort
%attr(755,root,root) %{_initrddir}/barnyard2
%attr(755,root,root) %{_bindir}/barnyard2
%attr(755,root,root) %{_sbindir}/rcbarnyard2
%attr(644,root,root) /var/adm/fillup-templates/sysconfig.%{name}
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/barnyard2
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/barnyard2
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/snort/barnyard2.conf


#---------------------------------------

%package doc
Summary:  Barnyard2 documentation
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php5
Requires: man
Requires: %{name}

%description doc
Barnyard2 with - Basic Analysis and Security Engine

 BASE - Basic Analysis and Security Engine

%files doc
%defattr(0644,root,root)
%doc  doc/* etc/barnyard2.conf
%attr(755,root,root) %{_bindir}/barnyard2
%_docdir/*

#---------------------------------------

%package cron
Summary:  Barnyard2 cronjob
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php5
Requires: man
Requires: %{name}

%description cron
 barnyard2 with - Basic Analysis and Security Engine
 barnyard2 cronjob

%files cron
%attr(755,root,root) %{_bindir}/barnyard2
%{_sysconfdir}/cron.hourly/barnyard2


#---------------------------------------
%package mysql
Summary: barnyard2 with MySQL support
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%if %{mysql}
Requires: mysql
BuildRequires: mysql-devel
%endif
%description mysql
barnyard2 binary compiled with mysql support.

%package postgresql
Summary: barnyard2 with PostgreSQL support
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%if %{postgresql}
Requires: postgresql
BuildRequires: postgresql-devel
%endif
%description postgresql
barnyard2 binary compiled with postgresql support.

%package oracle
Summary: barnyard2 with Oracle support
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%description oracle
barnyard2 binary compiled with Oracle support.

EXPERIMENTAL!!  I don't have a way to test this, so let me know if it works!
ORACLE_HOME=%{OracleHome}


#---------------------------------------

%package sql
Summary:  Barnyard2 with BASE- sql setup
Group: Networking/Other
BuildArch: noarch
Packager: Horst Venzke <horst.venzke@remsnet.de>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: libmysqlclient18
Requires: %{name}

%description sql
Barnyard2 with BASE- sql setup

 BASE - Basic Analysis and Security Engine

%files sql
%defattr(0644,root,root)
%dir %{_datadir}/%{name}/schemas
%{_datadir}/%{name}/schemas/*



%post sql
echo " Barnyard2 + BASE sample setup for Mysql"
echo " Base orign sql schema files with BASE installed at /usr/share/base/sql "
echo " Barnyard2 orign  sql schema files installed at /usr/share/barnyard2/schema"
echo " Barnyard2 with BASE sql schema file are /usr/share/base/sql/base-create_barnyard2_mysql.sql "
echo " BASE base_config.php at /usr/share/base/"
echo ""
echo "Important NOTE : "
echo "Snort after 2.9.3 has no more DB suport into the snort-core - "
echo "As same as bevor 1999 you must use barnyard2 to bridge data to i.e Mysql ."
echo "This HowTo descibe the usage & install : "
echo "http://gsxbinary.blogspot.de/2010/07/snort-barnyard2-mysql-base-intro.html"
echo ""
echo "Important NOTE : "
echo " to setup BASE SAM DB with barnyard2 , if not allready exist , use for mysql > v5.5.x i.e:"
echo " mysqladmin create snort"
echo " mysql -u snort -D snort -h localhost -P 3306 -p < /usr/share/base/sql/base-create_barnyard2_mysql.sql"

%post cron
rccron reload

#---------------------------------------

%changelog
* Mon Mar 24  2014 support@remsnet.de
- added sub-pack sql
- updated SAMPLE barnyard2.conf for  mysql with BASE
- only create configs if not exist
- add barnyard2-base-mysql.conf, barnyard2-etc-sysconfig samples
- added barnyard2.cron.hourly, added subpackage cron
- added barnyard2.logrotate , updated barnyard2-initrc


* Sat Mar 22 2014 support@remsnet.de
- rebuild & on Opensuse 13.1 RPI arm
- updated BUILD based on https://github.com/remsnet/DJB-Tools

* Wed Feb  8 2012 stoppe@gmx.de
- Initial release
