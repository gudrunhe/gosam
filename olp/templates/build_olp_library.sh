[% @if extension meson %]
[% @if extension linker %]FC_LD=[% ld %] [% @end @if %]meson setup build -Dbuildtype=[% meson.buildtype %] --prefix $1 && cd build && meson install
[% @elif extension autotools %]
./autogen.sh --prefix=$1 && make install
[% @else %]
make install
[% @end @if %]