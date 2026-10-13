from project import add_student,view_student,view_specific_student
import pytest

def test_add_student(monkeypatch,capsys):
    inputs=iter(["123","ada","70","80",90])
    monkeypatch.setattr("builtins.input",lambda _:next(inputs))
    add_student()
    captured = capsys.readouterr()
    assert "Invalid input. Please enter a valid name." in captured.out
def test_add_student2(monkeypatch,capsys):
    inputs=iter(["123","ada+","jire*jire*","David-Collins","e","70","80","90"])
    monkeypatch.setattr("builtins.input",lambda _:next(inputs))
    add_student()
    captured = capsys.readouterr()
    assert "Invalid input. Please enter a number." in captured.out
    assert "Invalid input. Please enter a valid name." in captured.out
    #assert "Enter student's score: " in captured.out

def test_view_student():
    table=view_student()
    assert "Ada Moyo" in table
    assert "100" in table
    assert "64" in table
    assert "70" in table
    assert "student_name" in table


def test_view_specific_student(monkeypatch,capsys):
    inputs=iter(["123","Zainab-Amara Roberts"])
    monkeypatch.setattr("builtins.input",lambda _:next(inputs))
    view_specific_student()
    captured = capsys.readouterr()
    assert "Invalid input. Please enter a valid name." in captured.out

def test_view_specific_student_2(monkeypatch):
    inputs = iter(["Ada Obi", "100", "64", "70"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    table=view_specific_student()
    assert "Ada Obi" in table
    assert "2" in table
    assert "49" in table
    assert "60" in table
    assert "student_name" in table
