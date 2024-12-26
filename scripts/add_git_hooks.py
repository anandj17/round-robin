import os
import stat

def create_pre_commit_hook():
    hooks_dir = '.git/hooks'
    if not os.path.exists(hooks_dir):
        os.makedirs(hooks_dir)

    hook_path = os.path.join(hooks_dir, 'pre-commit')
    with open(hook_path, 'w') as f:
        f.write('''#!/bin/sh
echo "Running tests before commit..."
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
'''
        )
    
    # Make the hook executable
    st = os.stat(hook_path)
    os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
    print("Pre-commit hook installed successfully!")

if __name__ == '__main__':
    create_pre_commit_hook()