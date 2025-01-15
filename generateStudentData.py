import random
import sys
from Student import *
from Course import *
import json

LOWER_BOUND: int = 100_000
UPPER_BOUND: int = 999_999
completeStudyProgram = {}


def assignCourses(semseter: int) -> list:
    '''
    Assigns courses to a student.
    Some assumptions are made: students will always be assigned mandatory courses and will be assigned 2 elective and 1 transversal if they're available
    Args:
        semester (int): numerical identifier of a semester
    Returns:
        list: list of assigned courses
    '''
    #line added because json.dumps silently converts integer keys into strings
    semseter = str(semseter)

    assignedCourses = []

    for courseType in list(completeStudyProgram[semseter].keys()):
    
        courses: list = completeStudyProgram[semseter][courseType]
    
        if courseType == "Obavezni":
            assignedCourses.extend(courses)
            continue

        if len(courses) == 0:
            continue

        numOfCourses: int = 1 if courseType == "Transverzalni"  else 2

        for i in range(numOfCourses):
            
            #do while loop to generate JMBAGs and check against the array so it is unique
            randomCourseID = courses[random.randint(0,len(courses)-1)]
            while randomCourseID in assignedCourses:
                randomCourseID = courses[random.randint(0, len(courses)-1)]

            assignedCourses.append(randomCourseID)

    return assignedCourses


def generateJMBAGs(n: int) -> list:
    '''
    Generates a list of unique JMBAGs
    Args:
        n (int): number of JMBAGs to generate
    Returns:
        list: generated JMBAGs
        -1: cannot generate desired number of JMBAGs
    '''

    if n > (UPPER_BOUND-LOWER_BOUND):
        print("Cannot generated desired number of JMBAGs because the possible unique numbers is lower than desired",file=sys.stderr)
        return -1

    JMBAGs = []
    for i in range(n):

        #do while loop to generate JMBAGs and check against the array so it is unique
        JMBAG: str = f'0036{random.randint(LOWER_BOUND, UPPER_BOUND)}'
        while(JMBAG in JMBAGs):
            JMBAG = f'0036{random.randint(LOWER_BOUND, UPPER_BOUND)}'

        JMBAGs.append(JMBAG)

    return JMBAGs

def generateStudents(n: int, semester) -> dict:
    '''
    Generates n number of students
    Args:
        n (int): number of students to generate
        semester (int): semester to assign to all the students
    Returns:
        dict: generated students
        -1: cannot generate students because of an issue in generateJMBAGs()
    '''
    if not isinstance(n, int):
        raise TypeError("No number provided")

    if not isinstance(semester, int):
        raise TypeError("Argument semester must be an integer")

    students = {}
    JMBAGs: list = generateJMBAGs(n)

    if JMBAGs == -1:
        print("Couldn't generate the students", file=sys.stderr)
        return -1

    for i in range(n):
        courses = assignCourses(semester)
        students[JMBAGs[i]] = {"semester": str(semester), "courses": courses}
    return students

def main() -> None:

    with open("./data/ferCoursesBySemester.json", 'r', encoding='utf-8') as file:
        global completeStudyProgram
        completeStudyProgram = json.load(file)

    n = int(input("Broj studenta: "))
    semester = int(input("Broj semestra: "))
    students: dict = generateStudents(n, semester)

    if students == -1:
        return -1

    with open("./data/studentsData.json", 'w', encoding='utf-8') as output:
        json.dump(students, output, ensure_ascii=False, indent=4)

    print(students)
if __name__ == "__main__":
    main()