def test_build_greeting_message():
    from clinicaio.hello import _build_greeting_message

    assert (
        _build_greeting_message("ClinicaIO developers")
        == "Hello ClinicaIO developers !"
    )


def test_greet(capsys):
    from clinicaio.hello import greet

    greet("John Doe")

    captured = capsys.readouterr()
    assert captured.out == "Hello John Doe !\n"
