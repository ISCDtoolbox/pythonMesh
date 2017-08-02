#Make sure to have the ~/bin directory in your path!!
#add the following line to your .bashrc
#export PATH=$PATH:/path/to/dir

#Installing dependencies for medit
#sudo apt-get install libxmu-dev libxi-dev

#Installing numpy
pip install numpy

#Getting blender
#which blender
#if [ $? -ne 0 ]
#then
#    wget http://ftp.nluug.nl/pub/graphics/blender/release/Blender2.78/blender-2.78c-linux-glibc219-x86_64.tar.bz2
#    tar jxf blender-*
#    ln -s blender-2.78c-linux-glibc219-x86_64/blender /usr/local/bin/blender
#fi

#Getting mmgTools
which mmgs_O3
if [ $? -ne 0 ]
then
    git clone https://github.com/MmgTools/mmg.git
    cd mmg
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX="~"
    make -j 4
    make install
    cd ../..
fi

#Getting the commons library
if [ ! -f "$HOME/lib/libCommons.so" ]
then
    git clone https://github.com/ISCDtoolbox/Commons.git
    cd Commons
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX="~"
    make -j 4
    make install
    cd ../..
fi

#Getting the Navier Stokes library
which nstokes
if [ $? -ne 0 ]
then
    git clone https://github.com/ISCDtoolbox/NavierStokes.git
    cd NavierStokes
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX="~"
    make -j 4
    make install
    cd ../..
fi

#Getting the Elasticity library
which elastic
if [ $? -ne 0 ]
then
    git clone https://github.com/ISCDtoolbox/LinearElasticity.git
    cd LinearElasticity
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX="~"
    make -j 4
    make install
    cd ../..
fi

#Getting MshDist
#which mshdist
#if [ $? -ne 0 ]
#then
#    git clone https://github.com/ISCDtoolbox/Mshdist.git
#    cd Mshdist
#    mkdir build
#    cd build
#    cmake ..
#    make -j 4
#    sudo make install
#    cd ../..
#fi


#Getting medit
which medit
if [ $? -ne 0 ]
then
    git clone https://github.com/ISCDtoolbox/Medit.git
    cd Medit
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX="~"
    make -j 4
    make install
    cd ../..
fi

#Getting tetgen
which tetgen
if [ $? -ne 0 ]
then
    git clone https://github.com/ufz/tetgen.git
    cd tetgen
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX="~"
    make -j 4
    cp tetgen ~/bin/
    cd ../..
fi

rm -rf Commons/ Medit/ Mshdist/ NavierStokes/ tetgen/ LinearElasticity/ mmg/
