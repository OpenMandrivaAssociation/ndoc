Summary:	Code Documentation Generator for .NET
Name:		ndoc
Version:	1.3.1
Release:	12
Url:		http://ndoc.sourceforge.net/
License:	GPLv2+
Group:		Development/Other
Source0:	http://download.sourceforge.net/sourceforge/ndoc/ndoc-devel-v%{version}.zip
Source1:	ndoc.pc
#gw Ubuntu patches:
Patch0:		fix-build-system.diff
Patch1:		01_unused_private_methods.dpatch
Patch2:		02_ds_reference.dpatch
Patch3:		03_sdkdoc_location.dpatch
Patch4:		04_default_documenter.dpatch
#gw: fix build with old keyfile syntax warning
Patch5:		ndoc-1.3.1-no-warnaserror.patch
BuildArch:	noarch
BuildRequires:	nant
BuildRequires:	unzip

%description
NDoc generates class library documentation from .NET assemblies and the XML 
documentation files generated by the C# compiler. NDoc uses pluggable 
documenters to generate documentation in several different formats, including 
the MSDN-style HTML Help format (.chm), the Visual Studio .NET Help format 
(HTML Help 2), and MSDN-online style web pages.

%package devel
Summary:	Code Documentation Generator for .NET
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for Ndoc.

%prep
%setup -q -c
%apply_patches
sed -i 's/\r//' COPYING.txt
sed -i 's/\r//' README.txt

%build
# Use the mono system key instead of generating our own here.
%if %mdvver >= 201100
cp -a /etc/pki/mono/mono.snk NDoc.snk
%endif
nant -t:mono-2.0
# This one gets far enough, before throwing an odd windows error.
nant -t:mono-2.0 sdkdoc ||:

%install
mkdir -p %{buildroot}/%{_datadir}/pkgconfig
cp -p %{SOURCE1} %{buildroot}/%{_datadir}/pkgconfig
mkdir -p %{buildroot}/%{_prefix}/lib/mono/gac/
gacutil -i bin/mono/1.0/NDoc.Core.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.Documenter.JavaDoc.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.Documenter.Latex.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.Documenter.LinearHtml.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.Documenter.Msdn2.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.Documenter.Msdn.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.Documenter.Xml.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.ExtendedUI.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.Test.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDoc.VisualStudio.dll -f -package ndoc -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/NDocConsole.exe -f -package ndoc -root %{buildroot}/%{_prefix}/lib

# Cleanup docs
sed -i 's/\r//' doc/sdk/ndoc.log
sed -i 's/\r//' doc/sdk/ndoc.js
sed -i 's/\r//' doc/sdk/ndoc.css
sed -i 's/\r//' doc/sdk/tree.css
sed -i 's/\r//' doc/sdk/MSDN.css
sed -i 's/\r//' doc/sdk/tree.js
iconv -f iso-8859-1 -t utf-8 -o doc/sdk/tree.js{.utf8,}
mv doc/sdk/tree.js{.utf8,}

# Sometimes this temp dir sticks around. We don't want it.
rm -rf doc/sdk/ndoc_msdn_temp

%files
%doc COPYING.txt README.txt
%{_prefix}/lib/mono/gac/NDoc*/
%{_prefix}/lib/mono/ndoc

%files devel
%doc doc/sdk/
%{_datadir}/pkgconfig/ndoc.pc

