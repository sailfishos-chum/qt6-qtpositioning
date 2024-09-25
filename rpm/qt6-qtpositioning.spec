%global  qt_version 6.7.2

Summary: Qt6 - Positioning component
Name:    qt6-qtpositioning
Version: 6.7.2
Release: 0%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

# filter plugin/qml provides
%global __provides_exclude_from ^(%{_qt6_archdatadir}/qml/.*\\.so|%{_qt6_plugindir}/.*\\.so)$

BuildRequires: cmake
BuildRequires: clang
BuildRequires: ninja
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{qt_version}
# QtPositioning core-private
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel >= %{qt_version}
BuildRequires: qt6-qtserialport-devel >= %{qt_version}

BuildRequires: pkgconfig(dconf)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(xkbcommon) >= 0.5.0


%description
The Qt Positioning APIs gives developers the ability to
determine a position by using a variety of possible sources, including
satellite, or wifi, or text file, and so on.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# BuildRequires: qt6-qtpositioning-devel >= %{version}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}

%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF


%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%ldconfig_scriptlets

%files
%license LICENSES/GPL* LICENSES/LGPL*
%{_qt6_libdir}/libQt6Positioning.so.6*
%dir %{_qt6_archdatadir}/qml/QtPositioning
%{_qt6_archdatadir}/qml/QtPositioning/*
%{_qt6_plugindir}/position/
%{_qt6_libdir}/libQt6PositioningQuick.so.6*

%files devel
%{_qt6_headerdir}/QtPositioning/
%{_qt6_libdir}/libQt6Positioning.so
%{_qt6_libdir}/libQt6Positioning.prl
%{_qt6_headerdir}/QtPositioningQuick/
%{_qt6_libdir}/libQt6PositioningQuick.so
%{_qt6_libdir}/libQt6PositioningQuick.prl
%dir %{_qt6_libdir}/cmake/Qt6Positioning
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtPositioningTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Bundled_Clip2Tri/Qt6Bundled_Clip2TriDependencies.cmake
%{_qt6_libdir}/cmake/Qt6Positioning/*.cmake
%{_qt6_libdir}/cmake/Qt6PositioningQuick/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc
