from project import add_student,view_student,view_specific_student,calculate_average,view_class_stats


def test_add_student(monkeypatch,capsys):
    # iter is to prepare inputs for test in the same order that the function requests it
    inputs=iter(["6","3","3","bubu","20","20","70","40","40","40","40","40","40","40","40","40","40","40","40","40","40"])
    # Temporarily replace input() to supply test inputs automatically
    monkeypatch.setattr("builtins.input",lambda _:next(inputs))
    #call function we are testing
    add_student()
    # Capture all printed output since the test started.
    captured = capsys.readouterr()
    # Access the captured printed output to check for the warning message and assert it too.
    assert "Invalid input. Please enter a valid student name." in captured.out
    assert "Invalid score. Please enter a valid score between 0 and 40"in captured.out


def test_add_student2(monkeypatch,capsys):
    inputs=iter(["123","2","jire*jire*","David-Collins",
                 "e","70","33","90","55","33","55","33",
                 "55","33","44","y","55","33","33","33","47",
                 "20","55","40","44","30","56","25","67","55","30","55"])
    monkeypatch.setattr("builtins.input",lambda _:next(inputs))
    add_student()
    captured = capsys.readouterr()
    assert "Invalid input. Please enter a valid student name." in captured.out
    assert "Invalid score. Please enter a valid score between 0 and 40" in captured.out
    assert "Invalid score. Please enter a valid score between 0 and 60" in captured.out


def test_view_student(tmp_path):
    csv_file = tmp_path / "students.csv"
    # tmp_path is the temporary directory pytest provides.
    # "/" joins that directory with the filename "students.csv".
    # csv_file stores the resulting path.
    # temporary_directory/students.csv  is what is stored in csv_file
    # the whole point of this is to ensure the tst file does not only work with
    # current student csv as it can change overtime

    #write test points inside tempoary file
    csv_file.write_text(
        "student_id,student_name,department\n"
        "SCI001,Ada,Science\n"
        "SCI002,Tunde,Science\n"
    )

    # Pass the CSV file path to the function as a keyword argument.
    result = view_student(filename=str(csv_file))
    #assert data that will and will not be in the output(or table)
    assert "Ada" in result
    assert "Tunde" in result
    assert "SCI001" in result
    assert "SCI002" in result



def test_view_specific_student1(monkeypatch,capsys):
    inputs=iter(["123","3","Zainab-Amara Roberts"])
    monkeypatch.setattr("builtins.input",lambda _:next(inputs))
    view_specific_student()
    captured = capsys.readouterr()
    assert "Invalid department option." in captured.out
    # assert "Invalid input. Please enter a valid name in captured.out"

def test_view_specific_student_2(monkeypatch,tmp_path,capsys):
    csv_file = tmp_path / "art_student.csv"
    csv_file.write_text(
        "student_id,student_name,department,English_Language_CA,English_Language_Exam\n"
        "ART001,Flora,Art,35,52\n"
        "ART002,Tunde,Art,28,41\n"
    )
    inputs = iter(["1", "Flora"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = view_specific_student(filename=str(csv_file))
    assert "Flora" in result
    assert "ART001" in result
    assert "Tunde" not in result

def test_view_specific_student3(monkeypatch, tmp_path, capsys):
    # 1. Create a temporary CSV file
    csv_file = tmp_path / "science_student.csv"

    # 2. Add sample student records
    csv_file.write_text(
        "student_id,student_name,department\n"
        "SCI001,Ada,Science\n"
        "SCI002,Tunde,Science\n"
    )

    # 3. Simulate an invalid name followed by a valid name
    inputs = iter(["Ada123", "Ada"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # 4. Call the function with the temporary CSV
    result = view_specific_student(filename=str(csv_file))

    # 5. Capture the printed warning
    captured = capsys.readouterr()

    # 6. Check the warning and returned table
    assert "Invalid input. Please enter a valid name." in captured.out
    assert "Ada" in result
    assert "SCI001" in result
    assert "Tunde" not in result


def test_view_specific_student4(monkeypatch, tmp_path, capsys):
    # 1. Create a temporary CSV file
    csv_file = tmp_path / "art_student.csv"

    # 2. Add sample student records
    csv_file.write_text(
        "student_id,student_name,department\n"
        "SCI001,Ada,Science\n"
        "SCI002,Tunde,Science\n"
    )

    # 3. Simulate an invalid name followed by a valid name
    inputs = iter(["Ada123", "Jide"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # 4. Call the function with the temporary CSV
    result = view_specific_student(filename=str(csv_file))

    # 5. Capture the printed warning
    captured = capsys.readouterr()

    # 6. Check the warning and returned table
    assert "Invalid input. Please enter a valid name." in captured.out
    assert "Student not found" in result

def test_calculate_average(monkeypatch, tmp_path):
    csv_file = tmp_path / "science_student.csv"

    csv_file.write_text(
        "student_id,student_name,Mathematics_CA,Mathematics_Exam,"
        "English_CA,English_Exam\n"
        "SCI001,Ada,30,50,35,45\n"
        "SCI002,Tunde,20,30,25,35\n"
    )

    inputs = iter(["Ada"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = calculate_average(
        filename=str(csv_file),
        columns=["Mathematics_CA", "Mathematics_Exam",
                 "English_CA", "English_Exam"]
    )

    assert "Ada" in result
    assert "80.00%" in result


def test_calculate_average_student_not_found(monkeypatch, tmp_path):
    csv_file = tmp_path / "science_student.csv"

    csv_file.write_text(
        "student_id,student_name,Mathematics_CA,Mathematics_Exam,"
        "English_CA,English_Exam\n"
        "SCI001,Ada,30,50,35,45\n"
    )

    inputs = iter(["Ngozi"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = calculate_average(
        filename=str(csv_file),
        columns=["Mathematics_CA", "Mathematics_Exam",
                 "English_CA", "English_Exam"]
    )

    assert result == "Student not found"

def test_view_class_stats(tmp_path, monkeypatch):
    csv_file = tmp_path / "science_student.csv"

    csv_file.write_text(
        "student_id,student_name,Mathematics_CA,Mathematics_Exam\n"
        "SCI001,Ada,30,50\n"
        "SCI002,Tunde,20,40\n"
        "SCI003,Ngozi,35,55\n"
    )

    result = view_class_stats(
        filename=str(csv_file),
        columns=["Mathematics_CA", "Mathematics_Exam"]
    )

    assert "3" in result
    assert "76.67%" in result
    assert "Ngozi" in result
    assert "Tunde" in result


def test_view_class_stats_empty_csv(tmp_path):
    csv_file = tmp_path / "science_student.csv"

    csv_file.write_text(
        "student_id,student_name,Mathematics_CA,Mathematics_Exam\n"
    )

    result = view_class_stats(
        filename=str(csv_file),
        columns=["Mathematics_CA", "Mathematics_Exam"]
    )

    assert result == "No student records found."