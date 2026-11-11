#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT"

test -x auto/config
test -f config/package-lists/aeroos.list.chroot
test -f config/includes.chroot/etc/skel/.config/gtk-3.0/gtk.css
test -f .github/workflows/build-aeroos.yml

if command -v xmllint >/dev/null 2>&1; then
  find config/includes.chroot -type f -name '*.xml' -exec xmllint --noout {} \;
fi

grep -q -- '--distribution trixie' auto/config
grep -q 'persistence' auto/config
grep -q 'firmware-amd-graphics' config/package-lists/aeroos.list.chroot
grep -q 'firefox-esr' config/package-lists/aeroos.list.chroot

printf '%s\n' "AeroOS source configuration checks passed."
