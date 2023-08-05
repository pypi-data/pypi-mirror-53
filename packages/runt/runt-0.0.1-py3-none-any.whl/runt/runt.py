"""A task runner."""
import shlex


def dry_run(executable: str, args: [str] = None):
    """Print command to be run to stdout.

    >>> dry_run('cmd.exe', ['/C', 'echo Hello, world!'])
    cmd.exe /C 'echo Hello, world!'
    """
    print(shlex.join([executable, *args]))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
