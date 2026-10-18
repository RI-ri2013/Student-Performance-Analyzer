from project import add_student,view_student,view_specific_student,calculate_average,view_class_stats
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

def test_view_student(tmp_path):
    csv_file = tmp_path / "students.csv"

    csv_file.write_text(
        "student_name,first_score,second_score,third_score\n"
        "Ada,70,80,90\n"
        "John,60,75,85\n"
    )

    table = view_student(csv_file)

    assert "student_name" in table
    assert "first_score" in table
    assert "second_score" in table
    assert "third_score" in table

    # Check that both students appear
    assert "Ada" in table
    assert "John" in table

    # Check all their scores
    for score in ["70", "80", "90", "60", "75", "85"]:
        assert score in table


def test_view_specific_student(monkeypatch,capsys):
    inputs=iter(["123","Zainab-Amara Roberts"])
    monkeypatch.setattr("builtins.input",lambda _:next(inputs))
    view_specific_student()
    captured = capsys.readouterr()
    assert "Invalid input. Please enter a valid name." in captured.out

def test_view_specific_student_2(monkeypatch):
    inputs = iter(["Ada Obi"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    table=view_specific_student()
    assert "Ada Obi" in table
    assert "2" in table
    assert "49" in table
    assert "60" in table
    assert "student_name" in table

def test_calculate_average(monkeypatch,capsys):
    inputs=iter(["RI_RI","Ada Obi"])
    monkeypatch.setattr("builtins.input",lambda _:next(inputs))

    calculate_average()
    captured=capsys.readouterr()
    assert "Invalid input. Please enter a valid name" in captured.out


def test_calculate_average2(monkeypatch):
    inputs = iter(["RI_RI", "Ada Obi"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    table = calculate_average()
    assert "37.00%" in table

def test_view_class_stats(tmp_path):
    csv_file = tmp_path / "students.csv"
    csv_file.write_text(
        "student_name,first_score,second_score,third_score\n"
        "Ada,80,90,100\n"
        "John,40,50,60\n"
    )
    table = view_class_stats(csv_file)

    assert "Total Student" in table
    assert "Class Average" in table
    assert "Highest-Performing students" in table
    assert "Lowest Performing students" in table
    assert "2" in table
    assert "50%" in table
    assert "90%" in table
