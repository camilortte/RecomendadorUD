pkgver=1.2.18
mkdir -p $VIRTUAL_ENV/src && cd $VIRTUAL_ENV/src
 
curl -O http://oligarchy.co.uk/xapian/$pkgver/xapian-core-$pkgver.tar.xz && tar xf xapian-core-$pkgver.tar.xz
curl -O http://oligarchy.co.uk/xapian/$pkgver/xapian-bindings-$pkgver.tar.xz && tar xf xapian-bindings-$pkgver.tar.xz
 
cd $VENV/src/xapian-core-$pkgver
./configure --prefix=$VIRTUAL_ENV && make && make install
 
export LD_LIBRARY_PATH=$VIRTUAL_ENV/lib
 
cd $VIRTUAL_ENV/src/xapian-bindings-$pkgver
./configure --prefix=$VIRTUAL_ENV --with-python && make && make install
