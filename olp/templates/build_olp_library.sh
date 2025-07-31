meson setup build -Dbuildtype=[% meson.buildtype %] --prefix $1 && cd build && meson compile -j [% n_jobs %] && meson install
