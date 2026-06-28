#!/usr/bin/env python3
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: patch_prefix.py <path_to_termux_packages_repo> [new_package_name]")
        sys.exit(1)
        
    repo_dir = os.path.abspath(sys.argv[1])
    new_package = sys.argv[2] if len(sys.argv) > 2 else "com.hostcraft.android"
    
    print(f"[*] Patching termux-packages in: {repo_dir}")
    print(f"[*] Target package name: {new_package}")
    
    # Extensions to modify
    text_extensions = {
        '.sh', '.py', '.properties', '.conf', '.txt', '.json', '.yml', 
        'Makefile', 'configure', 'status'
    }
    
    # Strictly ignore package recipe and patch directories, git metadata, and build caches
    skipped_dirs = {
        '.git', '.github', '.termux-build', 'output', 'debs',
        'packages', 'x11-packages', 'root-packages', 'disabled-packages'
    }
    
    modified_count = 0
    
    for root, dirs, files in os.walk(repo_dir):
        # Skip directories in-place
        dirs[:] = [d for d in dirs if d not in skipped_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            basename = os.path.basename(file_path)
            _, ext = os.path.splitext(basename)
            
            if ext in text_extensions or basename in text_extensions:
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    if b'com.termux' in content:
                        patched = content.replace(b'com.termux', new_package.encode('utf-8'))
                        with open(file_path, 'wb') as f:
                            f.write(patched)
                        print(f"[+] Patched: {os.path.relpath(file_path, repo_dir)}")
                        modified_count += 1
                except Exception as e:
                    print(f"[!] Error processing {file_path}: {e}")
                    
    print(f"[*] Done. Patched {modified_count} files.")

if __name__ == '__main__':
    main()
