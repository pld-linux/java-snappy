%define		srcname		snappy
%include	/usr/lib/rpm/macros.java
Summary:	Fast compressor/decompresser
Name:		java-%{srcname}
Version:	1.0.4.1
Release:	0.1
License:	ASL 2.0
Group:		Libraries/Java
# hg clone --insecure -r snappy-java-1.0.4.1 https://code.google.com/p/snappy-java/
# cd snappy-java && hg archive -p snappy-java-1.0.4.1/ -X 'lib/*.jar' -t tgz ../snappy-java-1.0.4.1-CLEAN.tgz
Source0:	snappy-java-%{version}-CLEAN.tgz
# Source0-md5:	53d74de12e54772299b03db495c21004
URL:		http://code.google.com/p/snappy-java
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	maven >= 2.0
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Java port of the snappy, a fast compresser/decompresser written in
C++.

%package javadoc
Summary:	Javadocs for %{name}
Group:		Documentation

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n snappy-java-%{version}

%build
mvn -Dmaven.test.skip=true install javadoc:aggregate

%install
rm -rf $RPM_BUILD_ROOT

# JAR
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p target/snappy-java-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# APIDOCS
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc LICENSE README NOTICE
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
