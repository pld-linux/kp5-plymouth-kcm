#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.26.0
%define		qtver		5.15.2
%define		kpname		plymouth-kcm

Summary:	KDE Config Module for Plyouth
Name:		kp5-%{kpname}
Version:	5.26.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	8ea8a25e120015d6ba8dd10df7ee7c05
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.0
BuildRequires:	Qt5Gui-devel >= 5.15.0
BuildRequires:	Qt5Network-devel >= 5.15.0
BuildRequires:	Qt5Qml-devel >= 5.15.2
BuildRequires:	Qt5Quick-devel >= 5.15.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 5.82
BuildRequires:	kf5-karchive-devel >= 5.82
BuildRequires:	kf5-kconfig-devel >= 5.82
BuildRequires:	kf5-kdeclarative-devel >= 5.82
BuildRequires:	kf5-ki18n-devel >= 5.82
BuildRequires:	kf5-kio-devel >= 5.82
BuildRequires:	kf5-knewstuff-devel >= 5.82
BuildRequires:	ninja
BuildRequires:	plymouth-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KDE Config Module for Plymouth.

%prep
%setup -q -n %{kpname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	../
%ninja_build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kplymouththemeinstaller
%attr(755,root,root) %{_prefix}/libexec/kauth/plymouthhelper
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmplymouth.service
%{_datadir}/dbus-1/system.d/org.kde.kcontrol.kcmplymouth.conf
%{_datadir}/knsrcfiles/plymouth.knsrc
%dir %{_datadir}/kpackage/kcms/kcm_plymouth
%dir %{_datadir}/kpackage/kcms/kcm_plymouth/contents
%dir %{_datadir}/kpackage/kcms/kcm_plymouth/contents/ui
%{_datadir}/kpackage/kcms/kcm_plymouth/contents/ui/main.qml
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmplymouth.policy
%{_libdir}/qt5/plugins/plasma/kcms/systemsettings/kcm_plymouth.so
%{_desktopdir}/kcm_plymouth.desktop
