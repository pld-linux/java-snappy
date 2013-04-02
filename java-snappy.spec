# TODO
# - recompile org/xerial/snappy/native/*
#
# Conditional build:
%bcond_with	javadoc		# don't build javadoc

%define		srcname		snappy
%include	/usr/lib/rpm/macros.java
Summary:	Snappy compressor/decompressor for Java
Name:		java-%{srcname}
Version:	1.0.4.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
# hg clone --insecure -r snappy-java-1.0.4.1 https://code.google.com/p/snappy-java/
# cd snappy-java && hg archive -p snappy-java-1.0.4.1/ -X 'lib/*.jar' -t tgz ../snappy-java-1.0.4.1-CLEAN.tgz
Source0:	snappy-java-%{version}-CLEAN.tgz
# Source0-md5:	53d74de12e54772299b03db495c21004
URL:		http://xerial.org/snappy-java/
BuildRequires:	java-osgi-core >= 4.3
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-osgi-core >= 4.3
Requires:	jpackage-utils
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The snappy-java is a Java port of the snappy, a fast
compresser/decompresser written in C++, originally developed by
Google.

%package javadoc
Summary:	Javadocs for %{name}
Group:		Documentation

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n snappy-java-%{version}

find -name '*.class' -print -delete

%build
install -d target
topdir=${PWD:-$(pwd)}

required_jars="osgi.core"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

cd src/main/java
%javac -cp $CLASSPATH $(find -name '*.java')

# create jar
%jar cf $topdir/target/%{srcname}-%{version}.jar $(find -name '*.class') \
	org/xerial/snappy/VERSION

cd ../resources
%jar uf $topdir/target/%{srcname}-%{version}.jar \
	org/xerial/snappy/*.bytecode \
	org/xerial/snappy/native/** \

%install
rm -rf $RPM_BUILD_ROOT

# JAR
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# upstream name
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/snappy-java-%{version}.jar
ln -s snappy-java-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/snappy-java.jar

%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc LICENSE README NOTICE
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar
%{_javadir}/snappy-java-%{version}.jar
%{_javadir}/snappy-java.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
