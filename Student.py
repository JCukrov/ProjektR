import json

class Student:

    def __init__(self, JMBAG: str, courses: dict, semester: int) -> None:
        self.JMBAG = JMBAG
        self.courses = courses
        self.semester = semester

    def __str__(self):

        allAvailableCourses = {}
        with open("./data/ferCoursesList.json", 'r', encoding='utf-8') as file:
            allAvailableCourses = json.load(file)

        coursePrintList = []

        for course in self.courses:

            coursePrintList.append(allAvailableCourses[course]["courseName"])

        return f'JMBAG: {self.JMBAG}\nSemestar: {self.semester}\n{"\n".join(coursePrintList)}'

def main():

    student = Student("0036540245", ["183352", "183352"], 2)
    student2 = Student("0036540245", [], 2)
    lista = [student, student2]
    print(student)

if __name__ == "__main__":
    main()