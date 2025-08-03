#!/usr/bin/env python3
"""
Complete CAI MCP Bug Fix Script

This script fixes a bug in CAI where the code tries to call .get() method on 
StdioServerParameters objects (which don't have this method), causing the 
"/mcp add" command to fail with an AttributeError.

The fix replaces all server.params.get() calls with getattr(server.params, ...) 
which works correctly with StdioServerParameters objects.
"""

import os
import sys
import site

def find_cai_mcp_file():
    """
    Find the CAI MCP command file in the current Python environment
    """
    # Common paths to check
    search_paths = []
    
    # Add site-packages paths
    search_paths.extend(site.getsitepackages())
    
    # Add user site-packages
    search_paths.append(site.getusersitepackages())
    
    # Add current virtual environment if active
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        venv_site_packages = os.path.join(sys.prefix, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')
        search_paths.append(venv_site_packages)
    
    # Look for the MCP file
    for path in search_paths:
        potential_file = os.path.join(path, 'cai', 'repl', 'commands', 'mcp.py')
        if os.path.exists(potential_file):
            return potential_file
    
    return None

def fix_cai_mcp_bug():
    """
    Fix the CAI MCP bug by replacing server.params.get() calls with getattr()
    """
    file_path = find_cai_mcp_file()
    
    print("🛡️  CAI MCP BUG FIX SCRIPT")
    print("=" * 40)
    
    if not file_path:
        print("❌ CAI installation not found!")
        print("   Please ensure CAI is installed in your current Python environment:")
        print("   pip install cai-framework")
        return False
        
    print(f"✅ Found CAI installation: {os.path.dirname(file_path)}")
    print(f"Target file: {os.path.basename(file_path)}")
    
    # Create backup
    backup_path = file_path + ".backup"
    if not os.path.exists(backup_path):
        print("💾 Creating backup...")
        with open(file_path, 'r') as original:
            with open(backup_path, 'w') as backup:
                backup.write(original.read())
        print(f"✅ Backup created: {backup_path}")
    
    # Read the file
    print("🔍 Reading and analyzing file...")
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Count problematic calls before fix
    before_count = content.count('server.params.get(')
    print(f"Found {before_count} server.params.get() calls to fix")
    
    if before_count == 0:
        print("✅ No fixes needed - file appears to already be fixed")
        return True
    
    # Apply the comprehensive fix
    print("🔧 Applying fixes...")
    
    # Replace all server.params.get( with getattr(server.params, 
    content = content.replace('server.params.get(', 'getattr(server.params, ')
    
    # Write the fixed content
    with open(file_path, 'w') as f:
        f.write(content)
    
    # Verify the fix
    with open(file_path, 'r') as f:
        fixed_content = f.read()
    
    after_count = fixed_content.count('server.params.get(')
    getattr_count = fixed_content.count('getattr(server.params,')
    
    print(f"✅ Fix applied successfully!")
    print(f"   • Before: {before_count} server.params.get() calls")
    print(f"   • After: {after_count} server.params.get() calls") 
    print(f"   • Added: {getattr_count} getattr(server.params, ...) calls")
    
    if after_count == 0:
        print("🎉 All server.params.get() calls have been fixed!")
        print("\n📋 Next steps:")
        print("   1. Start CAI: cai")
        print("   2. Test the fix: /mcp add pentest-tools redteam_agent")
        print("   3. Switch to agent: /agent redteam_agent")
        print("   4. Start pentesting!")
        return True
    else:
        print(f"⚠️  Warning: {after_count} server.params.get() calls still remain")
        return False

def main():
    """Main function"""
    success = fix_cai_mcp_bug()
    
    if success:
        print("\n" + "="*50)
        print("🎯 SUMMARY")
        print("="*50)
        print("The script fixed a CAI bug where server.params.get() method calls")
        print("were failing because StdioServerParameters objects don't have a") 
        print("get() method. All calls were replaced with getattr() which works correctly.")
        print("\nBug Details:")
        print("- Error: 'StdioServerParameters' object has no attribute 'get'") 
        print("- Affects: /mcp add command when adding MCP tools to agents")
        print("- Fix: Replace server.params.get() with getattr(server.params, ...)")
        print("="*50)
    else:
        print("\n❌ Fix failed - please check the error messages above")

if __name__ == "__main__":
    main()
