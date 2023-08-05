import os

import sh

SHEBANG = "#!/usr/bin/bash\n"
HOOK = """
PATH=$PATH:/usr/local/bin:/usr/local/sbin
skipswiftlint=$(git config --bool hooks.skipswiftlint)
if [ "$skipswiftlint" != "true" ]
then
    python3 -m selective_linter
    retVal=$?
    if [ $retVal != 0 ]
    then
    cat <<\EOF

You can disable this check by using:

    git config hooks.skipswiftlint true
EOF
fi
    exit $retVal
else
    exit 0
fi
"""
PRE_COMMIT = '/.git/hooks/pre-commit'
GITIGNORE = '/.gitignore'
LINT_CACHE = '.lint_cache'

class Installer:

    def __init__(self, dir):
        self.dir = dir 

    def is_repository(self):
        git_dir = self.dir + '/.git'
        if not os.path.isdir(git_dir):
            print("{} is not a valid git repository!".format(self.dir))
            return False
        return True

    def install(self): 
        pre_hook_dir = self.dir + PRE_COMMIT
        if os.path.exists(pre_hook_dir):
            with open(self.pre_hook_dir, 'r') as pre_commit_hook:
                if 'skipswiftlint' in pre_commit_hook.read():
                    return
            self._write_pre_commit_hook(append=True)
        else:
            self._write_pre_commit_hook(append=False)
        self._make_pre_commit_hook_executable()
        self._add_lint_cache_to_gitignore()

    @property
    def pre_hook_dir(self):
        return self.dir + PRE_COMMIT

    @property
    def gitignore_dir(self):
        return self.dir + GITIGNORE

    def _write_pre_commit_hook(self, append=False):
        if append:
            with open(self.pre_hook_dir, 'a') as pre_commit_hook:
                pre_commit_hook.write(HOOK)
        else: 
            with open(self.pre_hook_dir, 'w+') as pre_commit_hook:
                pre_commit_hook.write(SHEBANG)
                pre_commit_hook.write(HOOK)
        print("Wrote hook to {}".format(self.pre_hook_dir))
        self._sanitize_file(self.pre_hook_dir)
        
    def _sanitize_file(self, file):
        text = ''
        with open(file, 'r') as content:
            import pdb; pdb.set_trace()
            text = content.read()
        text.replace('\r', '')
        with open(file, 'w+') as content:
            content.write(text)

    def _make_pre_commit_hook_executable(self):
        sh.chmod('744', self.pre_hook_dir)
        print("Made hook executable")

    def _add_lint_cache_to_gitignore(self):
        should_add_to_gitignore = False
        with open(self.gitignore_dir, 'r') as gitignore:
            if LINT_CACHE not in gitignore.read():
                should_add_to_gitignore = True
        if should_add_to_gitignore:
            with open(self.gitignore_dir, 'a') as gitignore:
                gitignore.write('\n' + '# swiftlint')
                gitignore.write(LINT_CACHE + '\n')
