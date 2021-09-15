#!/bin/sh

homeDIR="$( pwd )"


echo -n "Install SModelS (y/n)?"
read answer
if echo "$answer" | grep -iq "^y" ;then
	echo "[installer] cloning SModelS 2.1.0"; git subtree add --prefix=smodels --squash git@github.com:SModelS/smodels.git develop;
	cd smodels;
	make;
	cd $homeDIR;
fi


echo -n "Install SoftSUSY (y/n)?"
read answer
softsusy="softsusy-4.1.11.tar.gz"
if echo "$answer" | grep -iq "^y" ;then
	URL=http://www.hepforge.org/archive/softsusy/$softsusy
	mkdir softsusy;
	echo "[installer] fetching" $softsusy; wget $URL 2>/dev/null || curl -O $URL; tar -zxf $softsusy -C softsusy --strip-components 1;
	cd softsusy;
	./configure;
	make;
	cd $homeDIR;
fi

echo -n "Install Prospino (y/n)?"
read answer
prospino="on_the_web_10_17_14.tar.gz"
if echo "$answer" | grep -iq "^y" ;then
	URL=https://www.thphys.uni-heidelberg.de/~plehn/includes/prospino/$prospino
	mkdir Prospino2;
	echo "[installer] fetching Prospino"; wget $URL 2>/dev/null || curl -O $URL; tar -zxf $prospino -C Prospino2 --strip-components 1;
	cp prospinoModFiles/* Prospino2/;
	cd Prospino2;
	make;
	make prospino_ewino;
	cd $homeDIR;
    rm $prospino;
fi

echo -n "Install MicroMegas (y/n)?"
read answer
micro="micromegas_5.2.7.a.tgz"
if echo "$answer" | grep -iq "^y" ;then
	URL=https://lapth.cnrs.fr/micromegas/downloadarea/code/$micro
	mkdir micromegas;
	echo "[installer] fetching" $micro; wget $URL 2>/dev/null || curl -O $URL; tar -zxf $micro -C micromegas --strip-components 1;
    echo "[installer] copying micromegaFiles"; cp -r micromegasFiles/* micromegas/;
	cd micromegas;
	make;
	cd MSSM;
    echo "[installer] compiling main_ewino.c";
	make main=main_ewino.c;
	cd $homeDIR
    rm $micromegas
fi

