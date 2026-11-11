#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
PARSER="$ROOT/config/includes.chroot/usr/local/lib/aeroos/persistence-free-space.awk"

actual="$(
  printf '%s\n' \
    'BYT;' \
    '/dev/sdb:15634268160B:scsi:512:512:msdos:USB DISK:;' \
    '1:1048576B:1572864B:524288B:primary:boot;' \
    ':1572865B:15634267647B:15632700000B:Free Space:;' \
    | awk -f "$PARSER"
)"
expected='1572865 15632694783'
if [ "$actual" != "$expected" ]; then
  printf 'Persistence parser returned: %s\nExpected: %s\n' "$actual" "$expected" >&2
  exit 1
fi

if printf '%s\n' \
  'BYT;' \
  '/dev/sdb:15634268160B:scsi:512:512:msdos:USB DISK:;' \
  '1:1048576B:1572864B:524288B:primary:boot;' \
  ':1572865B:200000000B:198427136B:Free Space:;' \
  | awk -f "$PARSER" >/dev/null 2>&1; then
  printf '%s\n' "Persistence parser incorrectly accepted less than 512 MiB." >&2
  exit 1
fi

printf '%s\n' "Persistence free-space parser tests passed."
