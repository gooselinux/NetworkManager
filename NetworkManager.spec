%define udev_scriptdir /lib/udev

%define dbus_version 1.1
%define dbus_glib_version 0.86-3

%define gtk2_version	2.14.0
%define glib2_version	2.16.0
%define wireless_tools_version 1:28-0pre9
%define libnl_version 1.1
%define ppp_version 2.4.5

%define snapshot .git20100811
%define applet_snapshot .git20100811
%define realversion 0.8.1

Name: NetworkManager
Summary: Network connection manager and user applications
Epoch: 1
Version: 0.8.1
Release: 5%{?dist}
Group: System Environment/Base
License: GPLv2+
URL: http://www.gnome.org/projects/NetworkManager/

Source: %{name}-%{realversion}%{snapshot}.tar.bz2
Source1: network-manager-applet-%{realversion}%{applet_snapshot}.tar.bz2
Source2: NetworkManager.conf
Patch1: nm-applet-internal-buildfixes.patch
Patch2: explain-dns1-dns2.patch
Patch3: nm-applet-no-notifications.patch
Patch4: nm-dbus-glib-disable-legacy-property-access.patch
Patch10: nm-applet-mobile-status-in-panel-later.patch
Patch11: nm-ignore-hostname-localhost.patch
Patch12: rh589230-nm-i18n-fixes.patch
Patch13: rh589230-applet-i18n-fixes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): chkconfig
Requires(preun): chkconfig
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: glib2 >= %{glib2_version}
Requires: iproute
Requires: dhclient >= 12:4.1.0
Requires: wpa_supplicant >= 1:0.6.8-4
Requires: libnl >= %{libnl_version}
Requires: %{name}-glib = %{epoch}:%{version}-%{release}
Requires: ppp = %{ppp_version}
Requires: avahi-autoipd
Requires: dnsmasq
Requires: udev
Requires: mobile-broadband-provider-info >= 0.20090602
Requires: ModemManager >= 0.3-3.git20100317
Obsoletes: dhcdbd

Conflicts: NetworkManager-vpnc < 1:0.7.0.99-1
Conflicts: NetworkManager-openvpn < 1:0.7.0.99-1
Conflicts: NetworkManager-pptp < 1:0.7.0.99-1
Conflicts: NetworkManager-openconnect < 0:0.7.0.99-1

BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: wireless-tools-devel >= %{wireless_tools_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libglade2-devel
BuildRequires: GConf2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: wpa_supplicant
BuildRequires: libnl-devel >= %{libnl_version}
BuildRequires: libnotify-devel >= 0.4
BuildRequires: perl(XML::Parser)
BuildRequires: automake autoconf intltool libtool
BuildRequires: ppp = %{ppp_version}
BuildRequires: ppp-devel = %{ppp_version}
BuildRequires: nss-devel >= 3.11.7
BuildRequires: polkit-devel
BuildRequires: dhclient
BuildRequires: gtk-doc
BuildRequires: libudev-devel
BuildRequires: libuuid-devel
BuildRequires: libgudev1-devel >= 143
BuildRequires: desktop-file-utils
# No bluetooth on s390
%ifnarch s390 s390x
BuildRequires: gnome-bluetooth-libs-devel >= 2.27.7.1-1
%endif

%description
NetworkManager is a system network service that manages your network devices
and connections, attempting to keep active network connectivity when available.
It manages ethernet, WiFi, mobile broadband (WWAN), and PPPoE devices, and
provides VPN integration with a variety of different VPN services.


%package devel
Summary: Libraries and headers for adding NetworkManager support to applications
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: dbus-devel >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: pkgconfig

%description devel
This package contains various headers accessing some NetworkManager functionality
from applications.


%package gnome
Summary: GNOME applications for use with NetworkManager
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-glib = %{epoch}:%{version}-%{release}
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: libnotify >= 0.4.3
Requires: gnome-keyring
Requires: nss >= 3.11.7
Requires: gnome-icon-theme
Requires(post): gtk2 >= %{gtk2_version}

%description gnome
This package contains GNOME utilities and applications for use with
NetworkManager, including a panel applet for wireless networks.


%package glib
Summary: Libraries for adding NetworkManager support to applications that use glib.
Group: Development/Libraries
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}

%description glib
This package contains the libraries that make it easier to use some NetworkManager
functionality from applications that use glib.


%package glib-devel
Summary: Header files for adding NetworkManager support to applications that use glib.
Group: Development/Libraries
Requires: %{name}-devel = %{epoch}:%{version}-%{release}
Requires: %{name}-glib = %{epoch}:%{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig
Requires: dbus-glib-devel >= %{dbus_glib_version}

%description glib-devel
This package contains the header and pkg-config files for development applications using
NetworkManager functionality from applications that use glib.


%prep
%setup -q -n NetworkManager-%{realversion}

# unpack the applet and nmcli
tar -xjf %{SOURCE1}

%patch1 -p1 -b .buildfix
%patch2 -p1 -b .explain-dns1-dns2
%patch3 -p1 -b .no-notifications
%patch4 -p1 -b .dbus-glib-no-legacy-props
%patch10 -p1 -b .applet-mobile-status-later
%patch11 -p1 -b .ignore-hostname-localhost
%patch12 -p1 -b .nm-translations
%patch13 -p1 -b .applet-translations

%build

# back up pristine docs and use them instead of generated ones, which make
# multilib unhappy due to different timestamps in the generated content
%{__cp} -R docs ORIG-docs

autoreconf -i
%configure \
	--disable-static \
	--with-distro=redhat \
	--with-dhclient=yes \
	--with-dhcpcd=no \
	--with-crypto=nss \
	--enable-more-warnings=yes \
	--with-docs=yes \
	--with-system-ca-path=/etc/pki/tls/certs \
	--with-tests=yes \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version} \
	--with-dist-version=%{version}-%{release}

make %{?_smp_mflags}

# build the applet
pushd network-manager-applet-%{realversion}
	autoreconf -i
	intltoolize --force
	%configure --disable-static --enable-more-warnings=yes
	make %{?_smp_mflags}
popd

%install
%{__rm} -rf $RPM_BUILD_ROOT

# install NM
make install DESTDIR=$RPM_BUILD_ROOT

%{__cp} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/

# install the applet
pushd network-manager-applet-%{realversion}
  make install DESTDIR=$RPM_BUILD_ROOT
popd

# create a VPN directory
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/VPN

# create a keyfile plugin system settings directory
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/system-connections

%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

%{__mkdir_p} $RPM_BUILD_ROOT%{_localstatedir}/lib/NetworkManager

%find_lang %{name}
%find_lang nm-applet
cat nm-applet.lang >> %{name}.lang

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/pppd/%{ppp_version}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/NetworkManager/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/gnome-bluetooth/plugins/*.la

install -m 0755 test/.libs/nm-online %{buildroot}/%{_bindir}

# install the pristine docs
%{__cp} ORIG-docs/libnm-glib/html/* $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/libnm-glib/
%{__cp} ORIG-docs/libnm-util/html/* $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/libnm-util/

# don't autostart in KDE on F13+ (#541353)
%if 0%{?fedora} > 12
echo 'NotShowIn=KDE;' >>$RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%endif

# validate the autostart .desktop file
desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nm-applet.desktop


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%post
if [ "$1" == "1" ]; then
	/sbin/chkconfig --add NetworkManager
	/sbin/chkconfig NetworkManager resetpriorities
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service NetworkManager stop >/dev/null 2>&1
    killall -TERM nm-system-settings >/dev/null 2>&1
    /sbin/chkconfig --del NetworkManager
fi

%triggerun -- NetworkManager < 1:0.7.0-0.9.2.svn3614
/sbin/service NetworkManagerDispatcher stop >/dev/null 2>&1
/sbin/chkconfig --del NetworkManagerDispatcher
exit 0

%post	glib -p /sbin/ldconfig
%postun	glib -p /sbin/ldconfig

%pre gnome
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  if [ -f "%{_sysconfdir}/gconf/schemas/nm-applet.schemas" ]; then
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/nm-applet.schemas >/dev/null
  fi
fi

%preun gnome
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  if [ -f "%{_sysconfdir}/gconf/schemas/nm-applet.schemas" ]; then
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/nm-applet.schemas >/dev/null
  fi
fi

%post gnome
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
if [ -f "%{_sysconfdir}/gconf/schemas/nm-applet.schemas" ]; then
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/nm-applet.schemas >/dev/null
fi

%postun gnome
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING NEWS AUTHORS README CONTRIBUTING TODO
%{_sysconfdir}/dbus-1/system.d/NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-dhcp-client.conf
%{_sysconfdir}/dbus-1/system.d/nm-avahi-autoipd.conf
%{_sysconfdir}/dbus-1/system.d/nm-dispatcher.conf
%{_sysconfdir}/dbus-1/system.d/nm-ifcfg-rh.conf
%config %{_sysconfdir}/rc.d/init.d/NetworkManager
%{_sbindir}/%{name}
%{_bindir}/nmcli
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/dispatcher.d
%dir %{_sysconfdir}/%{name}/VPN
%config(noreplace) %{_sysconfdir}/%{name}/NetworkManager.conf
%{_bindir}/nm-tool
%{_bindir}/nm-online
%{_libexecdir}/nm-dhcp-client.action
%{_libexecdir}/nm-avahi-autoipd.action
%{_libexecdir}/nm-dispatcher.action
%dir %{_libdir}/NetworkManager
%{_libdir}/NetworkManager/*.so*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_localstatedir}/run/NetworkManager
%dir %{_localstatedir}/lib/NetworkManager
%{_prefix}/libexec/nm-crash-logger
%dir %{_datadir}/NetworkManager
%{_datadir}/NetworkManager/gdb-cmd
%dir %{_sysconfdir}/NetworkManager/system-connections
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_libdir}/pppd/%{ppp_version}/nm-pppd-plugin.so
%{_datadir}/polkit-1/actions/*.policy
%{udev_scriptdir}/rules.d/*.rules

%files devel
%defattr(-,root,root,0755)
%doc ChangeLog docs/spec.html
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/%{name}.h
%{_includedir}/%{name}/NetworkManagerVPN.h
%{_libdir}/pkgconfig/%{name}.pc

%files gnome
%defattr(-,root,root,0755)
%{_sysconfdir}/dbus-1/system.d/nm-applet.conf
%{_bindir}/nm-applet
%{_bindir}/nm-connection-editor
%{_datadir}/applications/*.desktop
%{_datadir}/nm-applet/
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%dir %{_datadir}/gnome-vpn-properties
%{_sysconfdir}/gconf/schemas/nm-applet.schemas
%ifnarch s390 s390x
%{_libdir}/gnome-bluetooth/plugins/*
%endif

%files glib
%defattr(-,root,root,0755)
%{_libdir}/libnm-glib.so.*
%{_libdir}/libnm-glib-vpn.so.*
%{_libdir}/libnm-util.so.*

%files glib-devel
%defattr(-,root,root,0755)
%dir %{_includedir}/libnm-glib
%{_includedir}/libnm-glib/*.h
%{_includedir}/%{name}/nm-*.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-glib.so
%{_libdir}/libnm-glib-vpn.so
%{_libdir}/libnm-util.so
%dir %{_datadir}/gtk-doc/html/libnm-glib
%{_datadir}/gtk-doc/html/libnm-glib/*
%dir %{_datadir}/gtk-doc/html/libnm-util
%{_datadir}/gtk-doc/html/libnm-util/*

%changelog
* Wed Aug  11 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-5
- core: quiet annoying warnings (rh #612991)
- core: fix retrieval of various IP options in libnm-glib (rh #611141)
- core: ship NetworkManager.conf instead of deprecated nm-system-settings.conf (rh #606160)
- core: add short hostname to /etc/hosts too (rh #621910)
- core: recheck autoactivation when new system connections appear
- cli: wait a bit for NM's permissions check to complete (rh #614866)
- ifcfg-rh: ignore BRIDGE and VLAN configs and treat as unmanaged (rh #619863)
- man: add manpage for nm-online
- applet: fix crash saving ignore-missing-CA-cert preference (rh #619775)
- applet: hide PIN/PUK by default in the mobile PIN/PUK dialog (rh #615085)
- applet: ensure Enter closes the PIN/PUK dialog (rh #611831)
- applet: fix another crash in ignore-CA-certificate handling (rh #557495)
- editor: fix handling of Wired/s390 connections (rh #618620)

* Wed Jul 28 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-4
- core: enable DHCPv6-only configurations (rh #612445)
- core: don't fail connection immediately if DHCP lease expires (rh #616084) (rh #590874)
- core: read deprecated nm-system-settings.conf first (rh #606160)
- core: fix editing of PPPoE system connections
- core: work around twitchy frequency reporting of various wifi drivers
- core: don't tear down user connections on console changes (rh #614556)
- editor: fix crash when canceling editing in IP address pages (rh #610891)
- editor: fix handling of s390-specific options

* Wed Jul 14 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-3
- core: fix access to NMAccessPoint objects HwAddress property (rh #606147)
- core: more cleanly handle s390-specific options
- core: better behavior when missing firmware appears (rh #609587)
- core: map hostname to current IP address (rh #613821)
- ifcfg-rh: match initscripts behavior for persistent hostnames (rh #613841)
- editor: fix crash checking permissions during editor window close (rh #603566) (rh #614057)
- editor: fix listing of connections on ppc64 (rh #608663)
- applet: fix remembering "Don't warn me again" for missing CA certs (rh #610084)

* Mon Jun 28 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-2
- core: fix crash getting IPv6 nameservers via D-Bus
- core: fix possible crash updating VPN secrets (rh #587784)
- cli: print IPv6 settings too
- dhcp: look for interface-specific options in /etc/dhcp too (rh #607759)

* Sun Jun 27 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-1
- core: allow S390 subchannels for connection locking (rh #591533)
- core: don't request wifi scans when connection is BSSID-locked
- core: handle MAC spoofing/cloning (rh #447827)
- core: add domain part of hostname to resolv.conf search list (rh #600407)
- core: protect various network functions via PolicyKit (rh #585182)

* Fri Jun 25 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-0.4
- Update to 0.8.1 release candidate
- core: fix WWAN hardware enable state tracking (rh #591622)
- core: fix Red Hat initscript return value on double-start (rh #584321)
- core: add multicast route entry for IPv4 link-local connections
- core: fix connection sharing in cases where a dnsmasq config file exists
- core: fix handling of Ad-Hoc wifi connections to indicate correct network
- core: ensure VPN interface name is passed to dispatcher when VPN goes down
- ifcfg-rh: fix handling of ASCII WEP keys
- ifcfg-rh: fix double-quoting of some SSIDs (rh #606518)
- applet: ensure deleted connections are actually forgotten (rh #618973)
- applet: don't crash if the AP's BSSID isn't availabe (rh #603236)
- editor: don't crash on PolicyKit events after windows are closed (rh #572466)

* Wed May 26 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-0.3
- core: fix nm-online crash (rh #593677)
- core: fix failed suspend disables network (rh #589108)
- core: print out missing firmware errors (rh #594578)
- applet: fix device descriptions for some mobile broadband devices
- keyfile: bluetooth fixes
- applet: updated translations (rh #589230)

* Wed May 19 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-0.2.git20100519
- core: use GIO in local mode only (rh #588745)
- core: updated translations (rh #589230)
- core: be more lenient in IPv6 RDNSS server expiry (rh #590202)
- core: fix headers to be C++ compatible (rh #592783)
- core: rebuild to fix D-Bus property access (for dbus-glib CVE-2010-1172)
- applet: updated translations (rh #589230)
- applet: lock connections with well-known SSIDs to their specific AP

* Mon May 10 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-0.1.git20100510
- core: fix handling of IPv6 RA flags when router goes away (rh #588560)
- bluetooth: fix crash configuring DUN connections from the wizard (rh #590666)

* Sun May  9 2010 Dan Williams <dcbw@redhat.com> - 0.8-13.git20100509
- core: restore initial accept_ra value for IPv6 ignored connections (rh #588619)
- bluetooth: fix bad timeout on PAN connections (rh #586961)
- applet: updated translations

* Wed May  4 2010 Dan Williams <dcbw@redhat.com> - 0.8-12.git20100504
- core: treat missing IPv6 configuration as ignored (rh #588814)
- core: don't flush IPv6 link-local routes (rh #587836)
- cli: update output formatting

* Mon May  3 2010 Dan Williams <dcbw@redhat.com> - 0.8-11.git20100503
- core: allow IP configuration as long as one method completes (rh #567978)
- core: don't prematurely remove IPv6 RDNSS nameservers (rh #588192)
- core: ensure router advertisements are only used when needed (rh #588613)
- editor: add IPv6 gateway editing capability

* Sun May  2 2010 Dan Williams <dcbw@redhat.com> - 0.8-10.git20100502
- core: IPv6 autoconf, DHCP, link-local, and manual mode fixes
- editor: fix saving IPv6 address in user connections

* Thu Apr 29 2010 Dan Williams <dcbw@redhat.com> - 0.8-9.git20100429
- core: fix crash when IPv6 is enabled and interface is deactivated

* Mon Apr 26 2010 Dan Williams <dcbw@redhat.com> - 0.8-8.git20100426
- core: fix issues with IPv6 router advertisement mishandling (rh #530670)
- core: many fixes for IPv6 RA and DHCP handling (rh #538499)
- core: ignore WWAN ethernet devices until usable (rh #585214)
- ifcfg-rh: fix handling of WEP passphrases (rh #581718)
- applet: fix crashes (rh #582938) (rh #582428)
- applet: fix crash with multiple concurrent authorization requests (rh #585405)
- editor: allow disabling IPv4 on a per-connection basis
- editor: add support for IPv6 DHCP-only configurations

* Thu Apr 22 2010 Dan Williams <dcbw@redhat.com> - 0.8-7.git20100422
- core: fix crash during install (rh #581794)
- wifi: fix crash when supplicant segfaults after resume (rh #538717)
- ifcfg-rh: fix MTU handling for wired connections (rh #569319)
- applet: fix display of disabled mobile broadband devices

* Thu Apr  8 2010 Dan Williams <dcbw@redhat.com> - 0.8-6.git20100408
- core: fix automatic WiFi connections on resume (rh #578141)

* Thu Apr  8 2010 Dan Williams <dcbw@redhat.com> - 0.8-5.git20100408
- core: more flexible logging
- core: fix crash with OLPC mesh devices after suspend
- applet: updated translations
- applet: fix continuous password requests for 802.1x connections (rh #576925)
- applet: many updated translations

* Thu Mar 25 2010 Dan Williams <dcbw@redhat.com> - 0.8-4.git20100325
- core: fix modem enable/disable
- core: fix modem default route handling

* Tue Mar 23 2010 Dan Williams <dcbw@redhat.com> - 0.8-3.git20100323
- core: don't exit early on non-fatal state file errors
- core: fix Bluetooth connection issues (rh #572340)
- applet: fix some translations (rh #576056)
- applet: better feedback when wrong PIN/PUK is entered
- applet: many updated translations
- applet: PIN2 unlock not required for normal modem functionality
- applet: fix wireless secrets dialog display

* Wed Mar 17 2010 Dan Williams <dcbw@redhat.com> - 0.8-2.git20100317
- man: many manpage updates
- core: determine classful prefix if non is given via DHCP
- core: ensure /etc/hosts is always up-to-date and correct (rh #569914)
- core: support GSM network and roaming preferences
- applet: startup speed enhancements
- applet: better support for OTP/token-based WiFi connections (rh #526383)
- applet: show GSM and CDMA registration status and signal strength when available
- applet: fix zombie GSM and CDMA devices in the menu
- applet: remove 4-character GSM PIN/PUK code limit
- applet: fix insensitive WiFi Create... button (rh #541163)
- applet: allow unlocking of mobile devices immediately when plugged in

* Fri Feb 19 2010 Dan Williams <dcbw@redhat.com> - 0.8-1.git20100219
- core: update to final 0.8 release
- core: fix Bluetooth DUN connections when secrets are needed
- ifcfg-rh: add helper for initscripts to determine ifcfg connection UUIDs
- applet: fix Bluetooth connection secrets requests
- applet: fix rare conflict with other gnome-bluetooth plugins

* Thu Feb 11 2010 Dan Williams <dcbw@redhat.com> - 0.8-0.4.git20100211
- core: fix mobile broadband PIN handling (rh #543088) (rh #560742)
- core: better handling of /etc/hosts if hostname was already added by the user
- applet: crash less on D-Bus property errors (rh #557007)
- applet: fix crash entering wired 802.1x connection details (rh #556763)

* Tue Feb 09 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.8-0.3.git20100129
- core: validate the autostart .desktop file
- build: fix nmcli for the stricter ld (fixes FTBFS)
- build: fix nm-connection-editor for the stricter ld (fixes FTBFS)
- applet: don't autostart in KDE on F13+ (#541353)

* Fri Jan 29 2010 Dan Williams <dcbw@redhat.com> - 0.8-0.2.git20100129
- core: add Bluetooth Dial-Up Networking (DUN) support (rh #136663)
- core: start DHCPv6 on receipt of RA 'otherconf'/'managed' bits
- nmcli: allow enable/disable of WiFi and WWAN

* Fri Jan 22 2010 Dan Williams <dcbw@redhat.com> - 0.8-0.1.git20100122
- ifcfg-rh: read and write DHCPv6 enabled connections (rh #429710)
- nmcli: update

* Thu Jan 21 2010 Dan Williams <dcbw@redhat.com> - 0.7.999-2.git20100120
- core: clean NSS up later to preserve errors from crypto_init()

* Wed Jan 20 2010 Dan Williams <dcbw@redhat.com> - 0.7.999-1.git20100120
- core: support for managed-mode DHCPv6 (rh #429710)
- ifcfg-rh: gracefully handle missing PREFIX/NETMASK
- cli: initial preview of command-line client
- applet: add --help to explain what the applet is (rh #494641)

* Wed Jan  6 2010 Dan Williams <dcbw@redhat.com> - 0.7.998-1.git20100106
- build: fix for new pppd (rh #548520)
- core: add WWAN enable/disable functionality
- ifcfg-rh: IPv6 addressing and routes support (rh #523288)
- ifcfg-rh: ensure connection is updated when route/key files change
- applet: fix crash when active AP isn't found (rh #546901)
- editor: fix crash when editing connections (rh #549579)

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 0.7.997-2.git20091214
- core: fix recognition of standalone 802.1x private keys
- applet: clean notification text to ensure it passes libnotify validation

* Mon Dec  7 2009 Dan Williams <dcbw@redhat.com> - 0.7.997-1
- core: remove haldaemon from initscript dependencies (rh #542078)
- core: handle PEM certificates without an ending newline (rh #507315)
- core: fix rfkill reporting for ipw2x00 devices
- core: increase PPPoE timeout to 30 seconds
- core: fix re-activating system connections with secrets
- core: fix crash when deleting automatically created wired connections
- core: ensure that a VPN's DNS servers are used when sharing the VPN connection
- ifcfg-rh: support routes files (rh #507307)
- ifcfg-rh: warn when device will be managed due to missing HWADDR (rh #545003)
- ifcfg-rh: interpret DEFROUTE as never-default (rh #528281)
- ifcfg-rh: handle MODE=Auto correctly
- rpm: fix rpmlint errors
- applet: don't crash on various D-Bus and other errors (rh #545011) (rh #542617)
- editor: fix various PolicyKit-related crashes (rh #462944)
- applet+editor: notify user that private keys must be protected

* Fri Nov 13 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-7.git20091113
- nm: better pidfile handing (rh #517362)
- nm: save WiFi and Networking enabled/disabled states across reboot
- nm: fix crash with missing VPN secrets (rh #532084)
- applet: fix system connection usage from the "Connect to hidden..." dialog
- applet: show Bluetooth connections when no other devices are available (rh #532049)
- applet: don't die when autoconfigured connections can't be made (rh #532680)
- applet: allow system administrators to disable the "Create new wireless network..." menu item
- applet: fix missing username connecting to VPNs the second time
- applet: really fix animation stuttering
- editor: fix IP config widget tooltips
- editor: allow unlisted countries in the mobile broadband wizard (rh #530981)
- ifcfg-rh: ignore .rpmnew files (rh #509621)

* Wed Nov 04 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-6.git20091021
- nm: fix PPPoE connection authentication (rh #532862)

* Wed Oct 21 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-5.git20091021
- install: better fix for (rh #526519)
- install: don't build Bluetooth bits on s390 (rh #529854)
- nm: wired 802.1x connection activation fixes
- nm: fix crash after modifying default wired connections like "Auto eth0"
- nm: ensure VPN secrets are requested again after connection failure
- nm: reset 'accept_ra' to previous value after deactivating IPv6 connections
- nm: ensure random netlink events don't interfere with IPv6 connection activation
- ifcfg-rh: fix writing out LEAP connections
- ifcfg-rh: recognize 'static' as a valid BOOTPROTO (rh #528068)
- applet: fix "could not find required resources" error (rh #529766)

* Fri Oct  2 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-4.git20091002
- install: fix -gnome package pre script failures (rh #526519)
- nm: fix failures validating private keys when using the NSS crypto backend
- applet: fix crashes when clicking on menu but not associated (rh #526535)
- editor: fix crash editing wired 802.1x settings
- editor: fix secrets retrieval when editing connections

* Mon Sep 28 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-3.git20090928
- nm: fix connection takeover when carrier is not on
- nm: handle certificate paths (CA chain PEM files are now fully usable)
- nm: defer action for 4 seconds when wired carrier drops
- ifcfg-rh: fix writing WPA passphrases with odd characters
- editor: fix editing of IPv4 settings with new connections (rh #525819)
- editor: fix random crashes when editing due to bad widget refcounting
- applet: debut reworked menu layout (not final yet...)

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 0.7.996-3.git20090921
- Install GConf schemas

* Mon Sep 21 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-2.git20090921
- nm: allow disconnection of all device types
- nm: ensure that wired connections are torn down when their hardware goes away
- nm: fix crash when canceling a VPN's request for secrets
- editor: fix issues changing connections between system and user scopes
- editor: ensure changes are thrown away when editing is canceled
- applet: ensure connection changes are noticed by NetworkManager
- applet: fix crash when creating new connections
- applet: actually use wired 802.1x secrets after they are requested

* Wed Aug 26 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-1.git20090826
- nm: IPv6 zeroconf support and fixes
- nm: port to polkit (rh #499965)
- nm: fixes for ehea devices (rh #511304) (rh #516591)
- nm: work around PPP bug causing bogus nameservers for mobile broadband connections
- editor: fix segfault with "Unlisted" plans in the mobile broadband assistant

* Thu Aug 13 2009 Dan Williams <dcbw@redhat.com> - 0.7.995-3.git20090813
- nm: add iSCSI support
- nm: add connection assume/takeover support for ethernet (rh #517333)
- nm: IPv6 fixes
- nm: re-add OLPC XO-1 mesh device support (removed with 0.7.0)
- applet: better WiFi dialog focus handling

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 0.7.995-2.git20090804
- Add patch to fix service detection on phones

* Tue Aug  4 2009 Dan Williams <dcbw@redhat.com> - 0.7.995-1.git20090804
- nm: IPv6 support for manual & router-advertisement modes

* Sun Aug  2 2009 Matthias Clasen <mclasen@redhat.com> - 0.7.995-1.git20090728
- Move some big docs to -devel to save space

* Tue Jul 28 2009 Dan Williams <dcbw@redhat.com> - 0.7.995-0.git20090728
- Update to upstream 'master' branch
- Use modem-manager for better 3G modem support
- Integrated system settings with NetworkManager itself
- Use udev instead of HAL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.1-9.git20090708
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Dan Williams <dcbw@redhat.com> - 0.7.1-8.git20090708
- applet: fix certificate validation in hidden wifi networks dialog (rh #508207)

* Wed Jul  8 2009 Dan Williams <dcbw@redhat.com> - 0.7.1-7.git20090708
- nm: fixes for ZTE/Onda modem detection
- nm: prevent re-opening serial port when the SIM has a PIN
- applet: updated translations
- editor: show list column headers

* Thu Jun 25 2009 Dan Williams <dcbw@redhat.com> - 0.7.1-6.git20090617
- nm: fix serial port settings

* Wed Jun 17 2009 Dan Williams <dcbw@redhat.com> - 0.7.1-5.git20090617
- nm: fix AT&T Quicksilver modem connections (rh #502002)
- nm: fix support for s390 bus types (rh #496820)
- nm: fix detection of some CMOtech modems
- nm: handle unsolicited wifi scans better
- nm: resolv.conf fixes when using DHCP and overriding search domains
- nm: handle WEP and WPA passphrases (rh #441070)
- nm: fix removal of old APs when none are scanned
- nm: fix Huawei EC121 and EC168C detection and handling (rh #496426)
- applet: save WEP and WPA passphrases instead of hashed keys (rh #441070)
- applet: fix broken notification bubble actions
- applet: default to WEP encryption for Ad-Hoc network creation
- applet: fix crash when connection editor dialogs are canceled
- applet: add a mobile broadband provider wizard

* Tue May 19 2009 Karsten Hopp <karsten@redhat.com> 0.7.1-4.git20090414.1
- drop ExcludeArch s390 s390x, we need at least the header files

* Tue May 05 2009 Adam Jackson <ajax@redhat.com> 1:0.7.1-4.git20090414
- nm-save-the-leases.patch: Use per-connection lease files, and don't delete
  them on interface deactivate.

* Thu Apr 16 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.1-3.git20090414
- ifcfg-rh: fix problems noticing changes via inotify (rh #495884)

* Tue Apr 14 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.1-2.git20090414
- ifcfg-rh: enable write support for wired and wifi connections

* Sun Apr 12 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.1-1
- nm: update to 0.7.1
- nm: fix startup race with HAL causing unmanaged devices to sometimes be managed (rh #494527)

* Wed Apr  8 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.100-2.git20090408
- nm: fix recognition of Option GT Fusion and Option GT HSDPA (nozomi) devices (rh #494069)
- nm: fix handling of spaces in DHCP 'domain-search' option
- nm: fix detection of newer Option 'hso' devices
- nm: ignore low MTUs returned by broken DHCP servers

* Sun Apr  5 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.100-1
- Update to 0.7.1-rc4
- nm: use PolicyKit for system connection secrets retrieval
- nm: correctly interpret errors returned from chmod(2) when saving keyfile system connections
- editor: use PolicyKit to get system connection secrets

* Thu Mar 26 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-5
- nm: fix crashes with out-of-tree modules that provide no driver link (rh #492246)
- nm: fix USB modem probing on recent udev versions

* Tue Mar 24 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-4
- nm: fix communication with Option GT Max 3.6 mobile broadband cards
- nm: fix communication with Huawei mobile broadband cards (rh #487663)
- nm: don't look up hostname when HOSTNAME=localhost unless asked (rh #490184)
- nm: fix crash during IP4 configuration (rh #491620)
- nm: ignore ONBOOT=no for minimal ifcfg files (f9 & f10 only) (rh #489398)
- applet: updated translations

* Wed Mar 18 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-3.5
- nm: work around unhandled device removals due to missing HAL events (rh #484530)
- nm: improve handling of multiple modem ports
- nm: support for Sony Ericsson F3507g / MD300 and Dell 5530
- applet: updated translations

* Mon Mar  9 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-3
- Missing ONBOOT should actually mean ONBOOT=yes (rh #489422)

* Mon Mar  9 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-2
- Fix conflict with NetworkManager-openconnect (rh #489271)
- Fix possible crash when resynchronizing devices if HAL restarts

* Wed Mar  4 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-1
- nm: make default wired "Auto ethX" connection modifiable if an enabled system settings
    plugin supports modifying connections (rh #485555)
- nm: manpage fixes (rh #447233)
- nm: CVE-2009-0365 - GetSecrets disclosure
- applet: CVE-2009-0578 - local users can modify the connection settings
- applet: fix inability to choose WPA Ad-Hoc networks from the menu
- ifcfg-rh: add read-only support for WPA-PSK connections

* Wed Feb 25 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.98-1.git20090225
- Fix getting secrets for system connections (rh #486696)
- More compatible modem autodetection
- Better handle minimal ifcfg files

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0.97-6.git20090220
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.97-5.git20090220
- Use IFF_LOWER_UP for carrier detect instead of IFF_RUNNING
- Add small delay before probing cdc-acm driven mobile broadband devices

* Thu Feb 19 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.97-4.git20090219
- Fix PEAP version selection in the applet (rh #468844)
- Match hostname behavior to 'network' service when hostname is localhost (rh #441453)

* Thu Feb 19 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.97-2
- Fix 'noreplace' for nm-system-settings.conf

* Wed Feb 18 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.97-1
- Update to 0.7.1rc1
- nm: support for Huawei E160G mobile broadband devices (rh #466177)
- nm: fix misleading routing error message (rh #477916)
- nm: fix issues with 32-character SSIDs (rh #485312)
- nm: allow root to activate user connections
- nm: automatic modem detection with udev-extras
- nm: massive manpage rewrite
- applet: fix crash when showing the CA certificate ignore dialog a second time
- applet: clear keyring items when deleting a connection
- applet: fix max signal strength calculation in menu (rh #475123)
- applet: fix VPN export (rh #480496)

* Sat Feb  7 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0-2.git20090207
- applet: fix blank VPN connection message bubbles
- applet: better handling of VPN routing on update
- applet: silence pointless warning (rh #484136)
- applet: desensitize devices in the menu until they are ready (rh #483879)
- nm: Expose WINS servers in the IP4Config over D-Bus
- nm: Better handling of GSM Mobile Broadband modem initialization
- nm: Handle DHCP Classless Static Routes (RFC 3442)
- nm: Fix Mobile Broadband and PPPoE to always use 'noauth'
- nm: Better compatibility with older dual-SSID AP configurations (rh #445369)
- nm: Mark nm-system-settings.conf as config (rh #465633)
- nm-tool: Show VPN connection information
- ifcfg-rh: Silence message about ignoring loopback config (rh #484060)
- ifcfg-rh: Fix issue with wrong gateway for system connections (rh #476089)

* Fri Jan  2 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0-1.git20090102
- Update to 0.7.1 pre-release
- Allow connections to be ignored when determining the default route (rh #476089)
- Own /usr/share/gnome-vpn-properties (rh #477155)
- Fix log flooding due to netlink errors (rh #459205)
- Pass connection UUID to dispatcher scripts via the environment
- Fix possible crash after deactivating a VPN connection
- Fix issues with editing wired 802.1x connections
- Fix issues when using PKCS#12 certificates with 802.1x connections

* Fri Nov 21 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.12.svn4326
- API and documentation updates
- Fix PIN handling on 'hso' mobile broadband devices

* Tue Nov 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.12.svn4296
- Fix PIN/PUK issues with high-speed Option HSDPA mobile broadband cards
- Fix desensitized OK button when asking for wireless keys

* Mon Nov 17 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.12.svn4295
- Fix issues reading ifcfg files
- Previously fixed:
- Doesn't send DHCP hostname (rh #469336)
- 'Auto eth0' forgets settings (rh #468612)
- DHCP renewal sometimes breaks VPN (rh #471852)
- Connection editor menu item in the wrong place (rh #471495)
- Cannot make system-wide connections (rh #471308)

* Fri Nov 14 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.12.svn4293
- Update to NetworkManager 0.7.0 RC2
- Handle gateways on a different subnet from the interface
- Clear VPN secrets on connection failure to ensure they are requested again (rh #429287)
- Add support for PKCS#12 private keys (rh #462705)
- Fix mangling of VPN's default route on DHCP renew
- Fix type detection of qemu/kvm network devices (rh #466340)
- Clear up netmask/prefix confusion in the connection editor
- Make the secrets dialog go away when it's not needed
- Fix inability to add system connections (rh #471308)

* Mon Oct 27 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4229
- More reliable mobile broadband card initialization
- Handle mobile broadband PINs correctly when PPP passwords are also used
- Additional PolicyKit integration for editing system connections
- Close the applet menu if a keyring password is needed (rh #353451)

* Tue Oct 21 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4201
- Fix issues with hostname during anaconda installation (rh #461933)
- Fix Ad-Hoc WPA connections (rh #461197)
- Don't require gnome-panel or gnome-panel-devel (rh #427834)
- Fix determination of WPA encryption capabilities on some cards
- Fix conflicts with PPTP and vpnc plugins
- Allow .cer file extensions when choosing certificates

* Sat Oct 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4175
- Fix conflicts for older PPTP VPN plugins

* Sat Oct 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4174
- Ensure that mobile broadband cards are powered up before trying to use them
- Hostname changing support (rh #441453)
- Fix mobile broadband secret requests to happen less often
- Better handling of default devices and default routes
- Better information in tooltips and notifications
- Various UI cleanups; hide widgets that aren't used (rh #465397, rh #465395)
- Accept different separators for DNS servers and searches
- Make applet's icon accurately reflect signal strength of the current AP

* Wed Oct  1 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022.4
- Fix connection comparison that could cause changes to get overwritten (rh #464417)

* Tue Sep 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022.3
- Fix handling of VPN settings on upgrade (rh #460730, bgo #553465)

* Thu Sep 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022.2
- Fix hang when reading system connections from ifcfg files

* Thu Sep  4 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022.1
- Fix WPA Ad-Hoc connections

* Wed Aug 27 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022
- Fix parsing of DOMAIN in ifcfg files (rh #459370)
- Fix reconnection to mobile broadband networks after an auth failure
- Fix recognition of timeouts of PPP during mobile broadband connection
- More compatible connection sharing (rh #458625)
- Fix DHCP in minimal environments without glibc locale information installed
- Add support for Option mobile broadband devices (like iCON 225 and iCON 7.2)
- Add IP4 config information to dispatcher script environment
- Merge WEP ASCII and Hex key types for cleaner UI
- Pre-fill PPPoE password when authentication fails
- Fixed some changes not getting saved in the connection editor
- Accept both prefix and netmask in the conection editor's IPv4 page

* Mon Aug 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn3930
- Fix issue with mobile broadband connections that don't require authentication

* Mon Aug 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn3927
- Expose DHCP-returned options over D-Bus and to dispatcher scripts
- Add support for customized static routes
- Handle multiple concurrent 3G or PPPoE connections
- Fix GSM/CDMA username and password issues
- Better handling of unmanaged devices from ifcfg files
- Fix timeout handling of errors during 3G connections
- Fix some routing issues (rh #456685)
- Fix applet crashes after removing a device (rh #457380)

* Thu Jul 24 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn3846
- Convert stored IPv4 static IP addresses to new prefix-based scheme automatically
- Fix pppd connections to some 3G providers (rh #455348)
- Make PPPoE "Show Password" option work
- Hide IPv4 config options that don't make sense in certain configurations

* Fri Jul 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn3830
- Expose server-returned DHCP options via D-Bus
- Use avahi-autoipd rather than old built-in IPv4LL implementation
- Send hostname to DHCP server if provided (DHCP_HOSTNAME ifcfg option)
- Support sending DHCP Client Identifier to DHCP server
- Allow forcing 802.1x PEAP Label to '0'
- Make connection sharing more robust
- Show status for shared and Ad-Hoc connections if no other connection is active

* Fri Jul 11 2008 Matthias Clasen <mclasen@redhat.com> - 1:0.7.0-0.10.svn3801
- Drop explicit hal dep in -gnome

* Wed Jul 02 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.10.svn3801
- Move VPN configuration into connection editor
- Fix mobile broadband username/password issues
- Fix issues with broken rfkill setups (rh #448889)
- Honor APN setting for GSM mobile broadband configurations
- Fix adding CDMA connections in the connection editor

* Wed Jun 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.10.svn3747
- Update to latest SVN
- Enable connection sharing
- Respect VPN-provided routes

* Wed Jun  4 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.4.svn3675
- Move NM later in the shutdown process (rh #449070)
- Move libnm-util into a subpackage to allow NM to be removed more easily (rh #351101)

* Mon May 19 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3675
- Read global gateway from /etc/sysconfig/network if missing (rh #446527)
- nm-system-settings now terminates when dbus goes away (rh #444976)

* Tue May 14 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3669
- Fix initial carrier state detection on devices that are already up (rh #134886)

* Tue May 13 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3667
- Restore behavior of marking wifi devices as "down" when disabling wireless
- Fix a crash on resume when a VPN was active when going to sleep

* Tue May 13 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3665
- Fix issues with the Fedora plugin not noticing changes made by
    system-config-network (rh #444502)
- Allow autoconnection of GSM and CDMA connections
- Multiple IP address support for user connections
- Fixes for Mobile Broadband cards that return line speed on connect
- Implement PIN entry for GSM mobile broadband connections
- Fix crash when editing unencrypted WiFi connections in the connection editor

* Wed Apr 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3623
- Clean up the dispatcher now that it's service is gone (rh #444798)

* Wed Apr 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3623
- Fix asking applets for the GSM PIN/PUK

* Wed Apr 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3622
- Guess WEP key type in applet when asking for new keys
- Correct OK button sensitivity in applet when asking for new WEP keys

* Wed Apr 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3620
- Fix issues with Mobile Broadband connections caused by device init race patch

* Tue Apr 29 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3619
- Fix device initialization race that caused ethernet devices to get stuck on
    startup
- Fix PPPoE connections not showing up in the applet
- Fix disabled OK button in connection editor some wireless and IP4 settings
- Don't exit if HAL isn't up yet; wait for it
- Fix a suspend/resume crash

* Sun Apr 27 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3614
- Don't ask for wireless keys when the driver sends disconnect events during
	association; wait until the entire assocation times out
- Replace dispatcher daemon with D-Bus activated callout
- Fix parsing of DNS2 and DNS3 ifcfg file items
- Execute dispatcher scripts in alphabetical order
- Be active at runlevel 2
- Hook up MAC address widgets for wired & wireless; and BSSID widget for wireless
- Pre-populate anonymous identity and phase2 widgets correctly
- Clear out unused connection keys from GConf

* Tue Apr 22 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3590
- Don't select devices without a default gateway as the default route (rh #437338)
- Fill in broadcast address if not specified (rh #443474)
- Respect manual VPN IPv4 configuration options
- Show Connection Information for the device with the default route only

* Fri Apr 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3578
- Add dbus-glib-devel BuildRequires for NetworkManager-glib-devel (rh #442978)
- Add PPP settings page to connection editor
- Fix a few crashes with PPPoE
- Fix active connection state changes that confused clients 

* Thu Apr 17 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3571
- Fix build in pppd-plugin

* Thu Apr 17 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3570
- PPPoE authentication fixes
- More robust handing of mobile broadband device communications

* Wed Apr 16 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3566
- Honor options from /etc/sysconfig/network for blocking until network is up

* Wed Apr 16 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3566
- Turn on Add/Edit in the connection editor
- Don't flush or change IPv6 addresses or routes
- Enhance nm-online tool
- Some serial communication fixes for mobile broadband

* Wed Apr  9 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3549
- Fix issues with VPN passwords not getting found

* Tue Apr  8 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3548
- Fix builds due to glib2 breakage of GStaticMutex with gcc 4.3

* Tue Apr  8 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3547
- Fix WEP key index handling in UI
- Fix handling of NM_CONTROLLED in ifcfg files
- Show device managed state in applet menu
- Show wireless enabled state in applet menu
- Better handling of default DHCP connections for wired devices
- Fix loading of connection editor on KDE (rh #435344)

* Wed Apr  2 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3527
- Honor MAC address locking for wired & wireless devices

* Mon Mar 31 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3521
- Show VPN failures
- Support Static WEP key indexes
- Fix parsing of WEP keys from ifcfg files
- Pre-fill wireless security UI bits in connection editor and applet

* Tue Mar 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3476
- Grab system settings from /etc/sysconfig/network-scripts, not from profiles

* Tue Mar 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3473
- Fix crashes when returning VPN secrets from the applet to NM

* Tue Mar 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3472
- Fix crashes on suspend/resume and exit (rh #437426)
- Ensure there's always an option to chose the wired device
- Never set default route via an IPv4 link-local addressed device (rh #437338)

* Wed Mar 12 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3440
- Fix DHCP rebind behavior
- Preliminary PPPoE support

* Mon Mar 10 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3417
- Fix gnome-icon-theme Requires, should be on gnome subpackage

* Mon Mar 10 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3417
- Honor DHCP rebinds
- Multiple active device support
- Better error handling of mobile broadband connection failures
- Allow use of interface-specific dhclient config files
- Recognize system settings which have no TYPE item

* Sun Mar  2 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3370
- Fix crash of nm-system-settings on malformed ifcfg files (rh #434919)
- Require gnome-icon-theme to pick up lock.png (rh #435344)
- Fix applet segfault after connection removal via connection editor or GConf

* Fri Feb 29 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3369
- Don't create multiple connections for hidden access points
- Fix scanning behavior

* Thu Feb 14 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3319
- Rework connection editor connection list

* Tue Feb 12 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3312
- Better handling of changes in the profile directory by the system settings
	serivce

* Thu Feb  7 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3302
- Enable system settings service
- Allow explicit disconnection of mobile broadband devices
- Fix applet memory leaks (rh #430178)
- Applet Connection Information dialog tweaks (gnome.org #505899)
- Filter input characters to passphrase/key entry (gnome.org #332951)
- Fix applet focus stealing prevention behavior

* Mon Jan 21 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3261
- Add CDMA mobile broadband support (if supported by HAL)
- Rework applet connection and icon handling
- Enable connection editor (only for deleting connections)

* Fri Jan 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3235
- Fix crash when activating a mobile broadband connection
- Better handling of non-SSID-broadcasting APs on kernels that support it
    (gnome.org #464215) (rh #373841)
- Honor DHCP-server provided MTU if present (gnome.org #332953)
- Use previous DNS settings if the VPN concentrator doesn't provide any
    (gnome.org #346833)

* Fri Jan  4 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3204
- Fix WPA passphrase hashing on big endian (PPC, Sparc, etc) (rh #426233)

* Tue Dec 18 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3181
- Fixes to work better with new libnl (rh #401761)

* Tue Dec 18 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3180
- Fix WPA/WPA2 Enterprise Phase2 connections (rh #388471)

* Wed Dec  5 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3138
- Fix applet connection comparison which failed to send connection updated
    signals to NM in some cases
- Make VPN connection applet more robust against plugin failures

* Tue Dec  4 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3134
- 64-bit -Wall compile fixes

* Tue Dec  4 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3133
- Fix applet crash when choosing to ignore the CA certificate (rh #359001)
- Fix applet crash when editing VPN properties and VPN connection failures (rh #409351)
- Add file filter name in certificate file picker dialog (rh #410201)
- No longer start named when starting NM (rh #381571)

* Tue Nov 27 2007 Jeremy Katz <katzj@redhat.com> - 1:0.7.0-0.8.svn3109
- Fix upgrading from an earlier rawhide snap

* Mon Nov 26 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.6.svn3109
- Fix device descriptions shown in applet menu

* Mon Nov 26 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.5.svn3109
- Fix crash when deactivating VPN connections

* Mon Nov 19 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.5.svn3096
- Fix crash and potential infinite nag dialog loop when ignoring CA certificates

* Mon Nov 19 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.4.svn3096
- Fix crash when ignoring CA certificate for EAP-TLS, EAP-TTLS, and EAP-PEAP

* Mon Nov 19 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.3.svn3096
- Fix connections when picking a WPA Enterprise AP from the menu
- Fix issue where applet would provide multiple same connections to NM

* Thu Nov 15 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.3.svn3094
- Add support for EAP-PEAP (rh #362251)
- Fix EAP-TLS private key handling

* Tue Nov 13 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.2.svn3080
- Clarify naming of WPA & WPA2 Personal encryption options (rh #374861, rh #373831)
- Don't require a CA certificate for applicable EAP methods (rh #359001)
- Fix certificate and private key handling for EAP-TTLS and EAP-TLS (rh #323371)
- Fix applet crash with USB devices (rh #337191)
- Support upgrades from NM 0.6.x GConf settings

* Thu Nov  1 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.1.svn3030
- Fix applet crash with USB devices that don't advertise a product or vendor
    (rh #337191)

* Sat Oct 27 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.5.svn3030
- Fix crash when getting WPA secrets (rh #355041)

* Fri Oct 26 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.4.svn3030
- Bring up ethernet devices by default if no connections are defined (rh #339201)
- Fix crash when switching networks or bringing up secrets dialog (rh #353091)
- Fix crash when editing VPN connection properties a second time
- Fix crash when cancelling the secrets dialog if another connection was
    activated in the mean time
- Fix disembodied notification bubbles (rh #333391)

* Thu Oct 25 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.4.svn3020
- Handle PEM certificates
- Hide WPA-PSK Type combo since it's as yet unused
- Fix applet crash when AP security options changed and old secrets are still
    in the keyring
- Fix applet crash connecting to unencrypted APs via the other network dialog

* Wed Oct 24 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3020
- Fix WPA Enterprise connections that use certificates
- Better display of SSIDs in the menu

* Wed Oct 24 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3016
- Fix getting current access point
- Fix WPA Enterprise connections
- Wireless dialog now defaults to sensible choices based on the connection
- Tell nscd to restart if needed, don't silently kill it

* Tue Oct 23 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3014
- Suppress excessive GConf updates which sometimes caused secrets to be cleared
    at the wrong times, causing connections to fail
- Various EAP and LEAP related fixes

* Tue Oct 23 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3008
- Make WPA-EAP and Dynamic WEP options connect successfully
- Static IPs are now handled correctly in NM itself

* Mon Oct 22 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2995
- Add Dynamic WEP as a supported authentication/security option

* Sun Oct 21 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2994
- Re-enable "Connect to other network"
- Switch to new GUI bits for wireless security config and password entry

* Tue Oct 16 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2983
- Add rfkill functionality
- Fix applet crash when choosing wired networks from the menu

* Wed Oct 10 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2970
- Fix segfault with deferred connections
- Fix default username with vpnc VPN plugin
- Hidden SSID fixes

* Tue Oct  9 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2962
- Fix merging of non-SSID-broadcasting APs into a device's scan list
- Speed up opening of the applet menu

* Tue Oct  9 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2961
- New snapshot
	- Add timestamps to networks to connect to last used wireless network
	- Turn autoconnect on in the applet
	- Hidden SSID support
	- Invalidate failed or cancelled connections again
	- Fix issues with reactivation of the same device
	- Handle connection updates in the applet (ex. find new VPN connections)
	- Fix vertical sizing of menu items
	- Fix AP list on wireless devices other than the first device in the applet
	- Fix matching of current AP with the right menu item

* Fri Sep 28 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2914
- New snapshot
	- Add WPA passphrase support to password dialog
	- Applet now reflects actual VPN behavior of one active connection
	- Applet now notices VPN active connections on startup
	- Fix connections with some WPA and WEP keys

* Thu Sep 27 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2907
- New snapshot
	- VPN support (only vpnc plugin ported at this time)

* Tue Sep 25 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2886
- New snapshot
	- Make wired device carrier state work in the applet
	- Fix handling of errors with unencrypted APs
	- Fix "frozen" applet icon by reporting NM state better
	- Fix output of AP frequency in nm-tool

* Tue Sep 25 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2880
- New snapshot
	- Fix applet icon sizing on start (mclasen)
	- Fix nm-tool installation (mclasen)
	- Fix 'state' method call return (#303271)
	- Fix 40-bit WEP keys (again)
	- Fix loop when secrets were wrong/invalid
	- Fix applet crash when clicking Cancel in the password dialog
	- Ensure NM doesn't get stuck waiting for the supplicant to re-appear
		if it crashes or goes away
	- Make VPN properties applet work again
	- Increase timeout for network password entry

* Fri Sep 21 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2852
- New snapshot (fix unencrypted & 40 bit WEP)

* Fri Sep 21 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2849
- New snapshot

* Fri Sep 21 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2844
- New snapshot

* Thu Sep 20 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.2.svn2833
- New SVN snapshot of 0.7 that sucks less

* Thu Aug 30 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.1.svn2736
- Update to SVN snapshot of 0.7

* Mon Aug 13 2007 Christopher Aillon <caillon@redhat.com> 1:0.6.5-9
- Update the license tag

* Tue Aug  8 2007 Christopher Aillon <caillon@redhat.com> 1:0.6.5-8
- Own /etc/NetworkManager/dispatcher.d and /etc/NetworkManager/VPN (#234004)

* Wed Jun 27 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-7
- Fix Wireless Enabled checkbox when no killswitches are present

* Thu Jun 21 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-6
- Update to stable branch snapshot:
    - More fixes for ethernet link detection (gnome #354565, rh #194124)
    - Support for HAL-detected rfkill switches

* Sun Jun 10 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-5
- Fix applet crash on 64-bit platforms when choosing
    "Connect to other wireless network..." (gnome.org #435036)
- Add debug output for ethernet device link changes

* Thu Jun  7 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-4
- Fix ethernet link detection (gnome #354565, rh #194124)
- Fix perpetual credentials request with private key passwords in the applet
- Sleep a bit before activating wireless cards to work around driver bugs

* Mon Jun  4 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-3
- Don't spawn wpa_supplicant with -o

* Wed Apr 25 2007 Christopher Aillon <caillon@redhat.com> 1:0.6.5-2
- Fix requires macro (237806)

* Thu Apr 19 2007 Christopher Aillon <caillon@redhat.com> 1:0.6.5-1
- Update to 0.6.5 final
- Don't lose scanned security information

* Mon Apr  9 2007 Dan Williams <dcbw@redhat.com> - 1:0.6.5-0.7.svn2547
- Update from trunk
	* Updated translations
	* Cleaned-up VPN properties dialogs
	* Fix 64-bit kernel leakage issues in WEXT
	* Don't capture and redirect wpa_supplicant log output

* Wed Mar 28 2007 Matthew Barnes  <mbarnes@redhat.com> 1:0.6.5-0.6.svn2474
- Close private D-Bus connections. (#232691)

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> 1:0.6.5-0.5.svn2474
- Fix a directory ownership issue.  (#233763)

* Thu Mar 15 2007 Dan Williams <dcbw@redhat.com> - 1:0.6.5-0.4.svn2474
- Update to pre-0.6.5 snapshot

* Thu Feb  8 2007 Christopher Aillon <caillon@redhat.com> - 1:0.6.5-0.3.cvs20061025
- Guard against D-Bus LimitExceeded messages

* Fri Feb  2 2007 Christopher Aillon <caillon@redhat.com> - 1:0.6.5-0.2.cvs20061025
- Move .so file to -devel package

* Sat Nov 25 2006 Matthias Clasen <mclasen@redhat.com> 
- Own the /etc/NetworkManager/dispatcher.d directory
- Require pkgconfig for the -devel packages
- Fix compilation with dbus 1.0

* Wed Oct 25 2006 Dan Williams <dcbw@redhat.com> - 1:0.6.5-0.cvs20061025
- Update to a stable branch snapshot
    - Gnome applet timeout/redraw suppression when idle
    - Backport of LEAP patch from HEAD (from Thiago Bauermann)
    - Backport of asynchronous scanning patch from HEAD
    - Make renaming of VPN connections work (from Tambet Ingo)
    - Dial down wpa_supplicant debug spew
    - Cleanup of key/passphrase request scenarios (from Valentine Sinitsyn)
    - Shut down VPN connections on logout (from Robert Love)
    - Fix WPA passphrase hashing on PPC

* Thu Oct 19 2006 Christopher Aillon <caillon@redhat.com> - 1:0.6.4-6
- Own /usr/share/NetworkManager and /usr/include/NetworkManager

* Mon Sep  4 2006 Christopher Aillon <caillon@redhat.com> - 1:0.6.4-5
- Don't wake up to redraw if NM is inactive (#204850)

* Wed Aug 30 2006 Bill Nottingham <notting@redhat.com> - 1:0.6.4-4
- add epochs in requirements

* Wed Aug 30 2006 Dan Williams <dcbw@redhat.com> - 1:0.6.4-3
- Fix FC-5 buildreqs

* Wed Aug 30 2006 Dan Williams <dcbw@redhat.com> - 1:0.6.4-2
- Revert FC6 to latest stable NM
- Update to stable snapshot
- Remove bind/caching-nameserver hard requirement

* Tue Aug 29 2006 Christopher Aillon <caillon@redhat.com> - 0.7.0-0.cvs20060529.7
- BuildRequire wireless-tools-devel and perl-XML-Parser
- Update the BuildRoot tag

* Wed Aug 16 2006 Ray Strode <rstrode@redhat.com> - 0.7.0-0.cvs20060529.6
- add patch to make networkmanager less verbose (bug 202832)

* Wed Aug  9 2006 Ray Strode <rstrode@redhat.com> - 0.7.0-0.cvs20060529.5
- actually make the patch in 0.7.0-0.cvs20060529.4 apply

* Fri Aug  4 2006 Ray Strode <rstrode@redhat.com> - 0.7.0-0.cvs20060529.4
- Don't ever elect inactive wired devices (bug 194124).

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.7.0-0.cvs20060529.3
- Add patch to fix deprecated dbus functions

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.7.0-0.cvs20060529.2
- Add BR for dbus-glib-devel

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.7.0-0.cvs20060529.1.1
- rebuild

* Mon May 29 2006 Dan Williams <dcbw@redhat.com> - 0.7.0-0.cvs20060529
- Update to latest CVS
	o Gnome.org #333420: dialog do not have window icons
	o Gnome.org #336913: HIG tweaks for vpn properties pages
	o Gnome.org #336846: HIG tweaks for nm-vpn-properties
	o Gnome.org #336847: some bugs in nm-vpn-properties args parsing
	o Gnome.org #341306: nm-vpn-properties crashes on startup
	o Gnome.org #341263: Version 0.6.2-0ubuntu5 crashes on nm_device_802_11_wireless_get_type
	o Gnome.org #341297: displays repeated keyring dialogs on resume from suspend
	o Gnome.org #342400: Building libnm-util --without-gcrypt results in linker error
	o Gnome.org #342398: Eleminate Gnome dependency for NetworkManager
	o Gnome.org #336532: declaration of 'link' shadows a global declaration
- Specfile fixes (#rh187489#)

* Sun May 21 2006 Dan Williams <dcbw@redhat.com> - 0.7.0-0.cvs20060521
- Update to latest CVS
- Drop special-case-madwifi.patch, since WEXT code is in madwifi-ng trunk now

* Fri May 19 2006 Bill Nottingham <notting@redhat.com> - 0.6.2-3.fc6
- use the same 0.6.2 tarball as FC5, so we have the same VPN interface
  (did he fire ten args, or only nine?)

* Thu Apr 27 2006 Jeremy Katz <katzj@redhat.com> - 0.6.2-2.fc6
- use the hal device type instead of poking via ioctl so that wireless 
  devices are properly detected even if the kill switch has been used

* Thu Mar 30 2006 Dan Williams <dcbw@redhat.com> - 0.6.2-1
- Update to 0.6.2:
	* Fix various WPA-related bugs
	* Clean up leaks
	* Increased DHCP timeout to account for slow DHCP servers, or STP-enabled
		switches
	* Allow applet to reconnect on dbus restarts
	* Add "Dynamic WEP" support
	* Allow hiding of password/key entry text
	* More responsive connection switching

* Tue Mar 14 2006 Peter Jones <pjones@redhat.com> - 0.6.0-3
- Fix device bringup on resume

* Mon Mar  6 2006 Dan Williams <dcbw@redhat.com> 0.6.0-2
- Don't let wpa_supplicant perform scanning with non-WPA drivers

* Mon Mar  6 2006 Dan Williams <dcbw@redhat.com> 0.6.0-1
- Update to 0.6.0 release
- Move autostart file to /usr/share/gnome/autostart

* Thu Mar  2 2006 Jeremy Katz <katzj@redhat.com> - 0.5.1-18.cvs20060302
- updated cvs snapshot.  seems to make airo much less neurotic

* Thu Mar  2 2006 Christopher Aillon <caillon@redhat.com>
- Move the unversioned libnm_glib.so to the -devel package

* Wed Mar  1 2006 Dan Williams <dcbw@redhat.com> 0.5.1-18.cvs20060301
- Fix VPN-related crash
- Fix issue where NM would refuse to activate a VPN connection once it had timed out
- Log wpa_supplicant output for better debugging

* Tue Feb 28 2006 Christopher Aillon <caillon@redhat.com> 0.5.1-17.cvs20060228
- Tweak three-scan-prune.patch

* Mon Feb 27 2006 Christopher Aillon <caillon@redhat.com> 0.5.1-16.cvs20060227
- Don't prune networks until they've gone MIA for three scans, not one.

* Mon Feb 27 2006 Christopher Aillon <caillon@redhat.com> 0.5.1-15.cvs20060227
- Update snapshot, which fixes up the libnotify stuff.

* Fri Feb 24 2006 Dan Williams <dcbw@redhat.coM> 0.5.1-14.cvs20060221
- Move libnotify requires to NetworkManager-gnome, not core NM package

* Tue Feb 21 2006 Dan Williams <dcbw@redhat.com> 0.5.1-13.cvs20060221
- Add BuildRequires: libnl-devel (#rh179438#)
- Fix libnm_glib to not clobber an application's existing dbus connection
	(#rh177546#, gnome.org #326572)
- libnotify support
- AP compatibility fixes

* Mon Feb 13 2006 Dan Williams <dcbw@redhat.com> 0.5.1-12.cvs20060213
- Minor bug fixes
- Update to VPN dbus API for passing user-defined routes to vpn service

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> 0.5.1-11.cvs20060205
- Rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 0.5.1-10.cvs20060205.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Feb  5 2006 Dan Williams <dcbw@redhat.com> 0.5.1-10.cvs20060205
- Workarounds for madwifi/Atheros cards
- Do better with non-SSID-broadcasting access points
- Fix hangs when access points change settings

* Thu Feb  2 2006 Dan Williams <dcbw@redhat.com> 0.5.1-9.cvs20060202
- Own /var/run/NetworkManager, fix SELinux issues

* Tue Jan 31 2006 Dan Williams <dcbw@redhat.com> 0.5.1-8.cvs20060131
- Switch to autostarting the applet instead of having it be session-managed
- Work better with non-broadcasting access points
- Add more manufacturer default SSIDs to the blacklist

* Tue Jan 31 2006 Dan Williams <dcbw@redhat.com> 0.5.1-7.cvs20060131
- Longer association timeout
- Fix some SELinux issues
- General bug and cosmetic fixes

* Fri Jan 27 2006 Dan Williams <dcbw@redhat.com> 0.5.1-6.cvs20060127
- Snapshot from CVS
- WPA Support!  Woohoo!

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.5.1-5
- rebuild for new dbus

* Fri Nov 18 2005 Peter Jones <pjones@redhat.com> - 0.5.1-4
- Don't kill the network connection when you upgrade the package.

* Fri Oct 21 2005 Christopher Aillon <caillon@redhat.com> - 0.5.1-3
- Split out the -glib subpackage to have a -glib-devel package as well
- Add epoch to version requirements for bind and wireless-tools
- Update URL of project

* Wed Oct 19 2005 Christopher Aillon <caillon@redhat.com> - 0.5.1-2
- NetworkManager 0.5.1

* Mon Oct 17 2005 Christopher Aillon <caillon@redhat.com> - 0.5.0-2
- NetworkManager 0.5.0

* Mon Oct 10 2005 Dan Williams <dcbw@redaht.com> - 0.4.1-5.cvs20051010
- Fix automatic wireless connections
- Remove usage of NMLoadModules callout, no longer needed
- Try to fix deadlock when menu is down and keyring dialog pops up

* Sun Oct 09 2005 Dan Williams <dcbw@redhat.com> - 0.4.1-4.cvs20051009
- Update to latest CVS
	o Integrate connection progress with applet icon (Chris Aillon)
	o More information in "Connection Information" dialog (Robert Love)
	o Shorten time taken to sleep
	o Make applet icon wireless strength levels a bit more realistic
	o Talk to named using DBUS rather than spawning our own
		- You need to add "-D" to the OPTIONS line in /etc/sysconfig/named
		- You need to set named to start as a service on startup

* Thu Sep 22 2005 Dan Williams <dcbw@redhat.com> - 0.4.1-3.cvs20050922
- Update to current CVS to fix issues with routing table and /sbin/ip

* Mon Sep 12 2005 Jeremy Katz <katzj@redhat.com> - 0.4.1-2.cvs20050912
- update to current CVS and rebuild (workaround for #168120)

* Fri Aug 19 2005 Dan Williams <dcbw@redhat.com> - 0.4.1-2.cvs20050819
- Fix occasional hang in NM caused by the applet

* Wed Aug 17 2005 Dan Williams <dcbw@redhat.com> - 0.4.1
- Update to NetworkManager 0.4.1

* Tue Aug 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-36.cvs20050811
- Rebuild against new cairo/gtk

* Thu Aug 11 2005 Dan Williams <dcbw@redhat.com> - 0.4-35.cvs20050811
- Update to latest CVS
	o Use DHCP server address as gateway address if the DHCP server doesn't give
		us a gateway address #rh165698#
	o Fixes to the applet (Robert Love)
	o Better caching of information in the applet (Bill Moss)
	o Generate automatic suggested Ad-Hoc network name from machine's hostname
		(Robert Love)
	o Update all network information on successfull connect, not just 
		authentication method

* Fri Jul 29 2005 Ray Strode  <rstrode@redhat.com> - 0.4-34.cvs20050729
- Update to latest CVS to get fix for bug 165683.

* Mon Jul 11 2005 Dan Williams <dcbw@redhat.com> - 0.4-34.cvs20050629
- Move pkgconfig file to devel package (#162316, thanks to Michael Schwendt)

* Wed Jun 29 2005 David Zeuthen <davidz@redhat.com> - 0.4-33.cvs20050629
- Update to latest CVS to get latest VPN interface settings to satisfy
  BuildReq for NetworkManager-vpnc in Fedora Extras Development
- Latest CVS also contains various bug- and UI-fixes

* Fri Jun 17 2005 Dan Williams <dcbw@redhat.com> - 0.4-32.cvs20050617
- Update to latest CVS
	o VPN connection import/export capability
	o Fix up some menu item names
- Move nm-vpn-properties.glade to the gnome subpackage

* Thu Jun 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-31.cvs20050616
- Update to latest CVS
	o Clean up wording in Wireless Network Discovery menu
	o Robert Love's applet beautify patch

* Wed Jun 15 2005 Dan Williams <dcbw@redhat.com> - 0.4-30.cvs20050615
- Update to latest CVS

* Mon May 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-15.cvs30050404
- Fix dispatcher and applet CFLAGS so they gets compiled with FORTIFY_SOURCE

* Mon May 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-14.cvs30050404
- Fix segfault in NetworkManagerDispatcher, add an initscript for it

* Mon May 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-13.cvs30050404
- Fix condition that may have resulted in DHCP client returning success
	when it really timed out

* Sat May 14 2005 Dan Williams <dcbw@redhat.com> - 0.4-12.cvs20050404
- Enable OK button correctly in Passphrase and Other Networks dialogs when
	using ASCII or Hex WEP keys

* Thu May  5 2005 Dan Williams <dcbw@redhat.com> - 0.4-11.cvs20050404
- #rh154391# NetworkManager dies on startup (don't force-kill nifd)

* Wed May  4 2005 Dan Williams <dcbw@redhat.com> - 0.4-10.cvs20050404
- Fix leak of a socket in DHCP code

* Wed May  4 2005 Dan Williams <dcbw@redhat.com> - 0.4-9.cvs20050404
- Fix some memory leaks (Tom Parker)
- Join to threads rather than spinning for their completion (Tom Parker)
- Fix misuse of a g_assert() (Colin Walters)
- Fix return checking of an ioctl() (Bill Moss)
- Better detection and matching of hidden access points (Bill Moss)
- Don't use varargs, and therefore don't crash on PPC (Peter Jones)

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 0.4-8.cvs20050404
- fix build with newer dbus

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 0.4-7.cvs20050404
- silence %%post

* Mon Apr  4 2005 Dan Williams <dcbw@redhat.com> 0.4-6.cvs20050404
- #rh153234# NetworkManager quits/cores just as a connection is made

* Fri Apr  2 2005 Dan Williams <dcbw@redhat.com> 0.4-5.cvs20050402
- Update from latest CVS HEAD

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 0.4-4.cvs20050315
- Update the GTK+ theme icon cache on (un)install

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-3.cvs20050315
- Pull from latest CVS HEAD

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-2.cvs20050315
- Upload new source tarball (woops)

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-1.cvs20050315
- Pull from latest CVS HEAD (hopefully works again)

* Mon Mar  7 2005 Ray Strode <rstrode@redhat.com> 0.4-1.cvs20050307
- Pull from latest CVS HEAD
- Commit broken NetworkManager to satisfy to dbus dependency

* Fri Mar  4 2005 Dan Williams <dcbw@redhat.com> 0.3.4-1.cvs20050304
- Pull from latest CVS HEAD
- Rebuild for gcc 4.0

* Tue Feb 22 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050222
- Update from CVS

* Mon Feb 14 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050214.x.1
- Fix free of invalid pointer for multiple search domains

* Mon Feb 14 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050214
- Never automatically choose a device that doesn't support carrier detection
- Add right-click menu to applet, can now "Pause/Resume" scanning through it
- Fix DHCP Renew/Rebind timeouts
- Fix frequency cycling problem on some cards, even when scanning was off
- Play better with IPv6
- Don't send kernel version in DHCP packets, and ensure DHCP packets are at
	least 300 bytes in length to work around broken router
- New DHCP options D-BUS API by Dan Reed
- Handle multiple domain search options in DHCP responses

* Wed Feb  2 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050202
- Display wireless network name in applet tooltip
- Hopefully fix double-default-route problem
- Write out valid resolv.conf when we exit
- Make multi-domain search options work
- Rework signal strength code to be WEXT conformant, if strength is
	still wierd then its 95% surely a driver problem
- Fix annoying instances of suddenly dropping and reactivating a
	wireless device (Cisco cards were worst offenders here)
- Fix some instances of NetworkManager not remembering your WEP key
- Fix some races between NetworkManager and NetworkManagerInfo where
	NetworkManager wouldn't recognize changes in the allowed list
- Don't shove Ad-Hoc Access Point MAC addresses into GConf

* Tue Jan 25 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050125
- Play nice with dbus 0.23
- Update our list of Allowed Wireless Networks more quickly

* Mon Jan 24 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050124
- Update to latest CVS
- Make sure we start as late as possible so that we ensure dbus & HAL
	are already around
- Fix race in initial device activation

* Mon Jan 24 2005 Than Ngo <than@redhat.com> 0.3.3-1.cvs20050112.4
- rebuilt against new wireless tool

* Thu Jan 21 2005 <dcbw@redhat.com> - 0.3.3-1.cvs20050118
- Fix issue where NM wouldn't recognize that access points were
	encrypted, and then would try to connect without encryption
- Refine packaging to put client library in separate package
- Remove bind+caching-nameserver dep for FC-3, use 'nscd -i hosts'
	instead.  DNS queries may timeout now right after device
	activation due to this change.

* Wed Jan 12 2005 <dcbw@redhat.com> - 0.3.3-1.cvs20050112
- Update to latest CVS
- Fixes to DHCP code
- Link-Local (ZeroConf/Rendezvous) support
- Use bind in "caching-nameserver" mode to work around stupidity
	in glibc's resolver library not recognizing resolv.conf changes
- #rh144818# Clean up the specfile (Patch from Matthias Saou)
- Ad-Hoc mode support with Link-Local addressing only (for now)
- Fixes for device activation race conditions
- Wireless scanning in separate thread

* Wed Dec  8 2004 <dcbw@redhat.com> - 0.3.2-4.3.cvs20041208
- Update to CVS
- Updates to link detection, DHCP code
- Remove NMLaunchHelper so we start up faster and don't
	block for a connection.  This means services that depend
	on the network may fail if they start right after NM
- Make sure DHCP renew/rebinding works

* Wed Nov 17 2004 <dcbw@redhat.com> - 0.3.2-3.cvs20041117
- Update to CVS
- Fixes to link detection
- Better detection of non-ESSID-broadcasting access points
- Don't dialog-spam the user if a connection fails

* Mon Nov 11 2004 <dcbw@redhat.com> - 0.3.2-2.cvs20041115
- Update to CVS
- Much better link detection, works with Open System authentication
- Blacklist wireless cards rather than whitelisting them

* Fri Oct 29 2004 <dcbw@redhat.com> - 0.3.2-2.cvs20041029
- #rh134893# NetworkManagerInfo and the panel-icon life-cycle
- #rh134895# Status icon should hide when in Wired-only mode
- #rh134896# Icon code needs rewrite
- #rh134897# "Other Networks..." dialog needs implementing
- #rh135055# Menu highlights incorrectly in NM
- #rh135648# segfault with cipsec0
- #rh135722# NetworkManager will not allow zaurus to sync via usb0
- #rh135999# NetworkManager-0.3.1 will not connect to 128 wep
- #rh136866# applet needs tooltips
- #rh137047# lots of applets, yay!
- #rh137341# Network Manager dies after disconnecting from wired network second time
- Better checking for wireless devices
- Fix some memleaks
- Fix issues with dhclient declining an offered address
- Fix an activation thread deadlock
- More accurately detect "Other wireless networks" that are encrypted
- Don't bring devices down as much, won't hotplug-spam as much anymore
	about firmware
- Add a "network not found" dialog when the user chooses a network that could
	not be connected to

* Tue Oct 26 2004 <dcbw@redhat.com> - 0.3.1-2
- Fix escaping of ESSIDs in gconf

* Tue Oct 19 2004  <jrb@redhat.com> - 0.3.1-1
- minor point release to improve error handling and translations

* Fri Oct 15 2004 Dan Williams <dcbw@redhat.com> 0.3-1
- Update from CVS, version 0.3

* Tue Oct 12 2004 Dan Williams <dcbw@redhat.com> 0.2-4
- Update from CVS
- Improvements:
	o Better link checking on wireless cards
	o Panel applet now a Notification Area icon
	o Static IP configuration support

* Mon Sep 13 2004 Dan Williams <dcbw@redhat.com> 0.2-3
- Update from CVS

* Sat Sep 11 2004 Dan Williams <dcbw@redhat.com> 0.2-2
- Require gnome-panel, not gnome-panel-devel
- Turn off by default

* Thu Aug 26 2004 Dan Williams <dcbw@redhat.com> 0.2-1
- Update to 0.2

* Thu Aug 26 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- spec-changes to req glib2 instead of glib

* Fri Aug 20 2004 Dan Williams <dcbw@redhat.com> 0.1-3
- First public release

