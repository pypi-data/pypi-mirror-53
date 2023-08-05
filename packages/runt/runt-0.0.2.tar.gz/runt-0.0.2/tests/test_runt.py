import pytest

from runt import runt


def test_dry_run(capsys):
    runt.dry_run('one', ['two', 'three'])
    assert capsys.readouterr().out == 'one two three\n'


if __name__ == "__main__":
    pytest.main()
