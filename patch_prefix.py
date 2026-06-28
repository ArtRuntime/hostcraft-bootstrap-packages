#!/usr/bin/env python3
"""
Post-process a Termux bootstrap ZIP archive to replace the default
package namespace (com.termux) with a custom one (com.hostcraft.android).

This script operates on the EXTRACTED bootstrap directory, replacing
com.termux only in text/config files. Binary ELF files are left untouched.
"""
import os
import sys
import struct

def is_elf(filepath):
    """Check if a file is an ELF binary by reading the magic bytes."""
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(4)
            return magic == b'\x7fELF'
    except (IOError, OSError):
        return False

def is_text_file(filepath):
    """Heuristic: read a chunk and check if it looks like text."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(8192)
        if not chunk:
            return True  # empty files are fine
        # If there are null bytes, it's likely binary
        if b'\x00' in chunk:
            return False
        return True
    except (IOError, OSError):
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: patch_prefix.py <extracted_bootstrap_dir> [new_package_name]")
        sys.exit(1)

    bootstrap_dir = os.path.abspath(sys.argv[1])
    new_package = sys.argv[2] if len(sys.argv) > 2 else "com.hostcraft.android"
    old_package = "com.termux"

    print(f"[*] Post-processing bootstrap in: {bootstrap_dir}")
    print(f"[*] Replacing '{old_package}' -> '{new_package}'")

    patched_count = 0
    skipped_elf = 0
    skipped_binary = 0

    for root, dirs, files in os.walk(bootstrap_dir):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Skip symlinks
            if os.path.islink(filepath):
                continue

            # Skip ELF binaries
            if is_elf(filepath):
                skipped_elf += 1
                continue

            # Skip other binary files
            if not is_text_file(filepath):
                skipped_binary += 1
                continue

            try:
                with open(filepath, 'rb') as f:
                    content = f.read()

                if old_package.encode() in content:
                    patched = content.replace(
                        old_package.encode(),
                        new_package.encode()
                    )
                    with open(filepath, 'wb') as f:
                        f.write(patched)
                    rel = os.path.relpath(filepath, bootstrap_dir)
                    print(f"  [+] Patched: {rel}")
                    patched_count += 1
            except Exception as e:
                print(f"  [!] Error: {filepath}: {e}")

    print(f"\n[*] Done. Patched {patched_count} text files.")
    print(f"[*] Skipped {skipped_elf} ELF binaries, {skipped_binary} other binary files.")

if __name__ == '__main__':
    main()
