#!/usr/bin/env python3
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: patch_prefix.py <path_to_termux_packages_repo> [new_package_name]")
        sys.exit(1)
        
    repo_dir = os.path.abspath(sys.argv[1])
    new_package = sys.argv[2] if len(sys.argv) > 2 else "com.hostcraft.android"
    
    properties_file = os.path.join(repo_dir, "scripts", "properties.sh")
    if not os.path.exists(properties_file):
        print(f"[!] properties.sh not found at {properties_file}")
        sys.exit(1)
        
    print(f"[*] Patching properties.sh: {properties_file}")
    print(f"[*] Target package name: {new_package}")
    
    try:
        with open(properties_file, 'rb') as f:
            content = f.read()
        
        if b'com.termux' in content:
            patched = content.replace(b'com.termux', new_package.encode('utf-8'))
            with open(properties_file, 'wb') as f:
                f.write(patched)
            print("[+] Patched properties.sh successfully.")
        else:
            print("[!] com.termux not found in properties.sh.")
    except Exception as e:
        print(f"[!] Error patching properties.sh: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
