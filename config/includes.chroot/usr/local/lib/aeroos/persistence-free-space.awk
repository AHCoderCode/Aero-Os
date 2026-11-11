# Parse the trailing unallocated region from: parted -m -s DEVICE unit B print free
BEGIN {
  FS = ":"
}

substr($1, 1, 5) == "/dev/" {
  disk_bytes = $2
  gsub(/[^0-9]/, "", disk_bytes)
}

/Free Space/ {
  free_start = $2
  free_end = $3
  gsub(/[^0-9]/, "", free_start)
  gsub(/[^0-9]/, "", free_end)

  # Force numeric conversion: the original fields are strings, and a string
  # comparison would incorrectly reject some valid start/end pairs.
  if (disk_bytes + 0 > 0 &&
      free_end + 0 >= disk_bytes + 0 - 4194304 &&
      free_end + 0 > free_start + 0) {
    result_start = free_start + 0
    result_bytes = free_end + 0 - free_start + 0 + 1
  }
}

END {
  if (result_start != "" && result_bytes >= 536870912) {
    printf "%.0f %.0f\n", result_start, result_bytes
  } else {
    exit 1
  }
}
