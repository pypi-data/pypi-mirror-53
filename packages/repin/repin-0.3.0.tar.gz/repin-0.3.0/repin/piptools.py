pip_args = []
if namespace.index_url:
    pip_args.extend(['-i', namespace.index_url])
from piptools.repositories import PyPIRepository

repository = PyPIRepository(pip_args)
constraints = []
for src_file in src_files:
    is_setup_file = os.path.basename(src_file) == "setup.py"
    if is_setup_file or src_file == "-":
        # pip requires filenames and not files. Since we want to support
        # piping from stdin, we need to briefly save the input from stdin
        # to a temporary file and have pip read that.  also used for
        # reading requirements from install_requires in setup.py.
        tmpfile = tempfile.NamedTemporaryFile(mode="wt", delete=False)
        if is_setup_file:
            from distutils.core import run_setup

            dist = run_setup(src_file)
            tmpfile.write("\n".join(dist.install_requires))
        else:
            tmpfile.write(sys.stdin.read())
        tmpfile.flush()
        constraints.extend(
            parse_requirements(
                tmpfile.name,
                finder=repository.finder,
                session=repository.session,
                options=repository.options,
            )
        )
    else:
        constraints.extend(
            parse_requirements(
                src_file,
                finder=repository.finder,
                session=repository.session,
                options=repository.options,
            )
        )

constraints.extend(upgrade_install_reqs.values())
