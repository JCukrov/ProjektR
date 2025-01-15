import json

def parseCourseStructure(structure: str) -> tuple[list, int]:

    lectures, seminar, excercises, laboratoryExcercises = [int(x) for x in structure.split("+")]
    lecturesPerWeek = []

    if lectures%15 == 0:

        match lectures/15:
            case 1:
                lecturesPerWeek = [1]
            case 2:
                lecturesPerWeek = [2]
            case 3:
                lecturesPerWeek = [3]
            case 4:
                lecturesPerWeek = [2,2]
            case 5:
                lecturesPerWeek = [2,3]
            case 6:
                lecturesPerWeek = [2,2,2]

    return lecturesPerWeek, int(excercises/15)

def generateSchedule(mat: [list], mandatoryCourses: list, electiveCourses: list, transversalCourses: list, indexIdDictionary: dict, courses: dict) -> [list]:
    
    timeSlots = [[[]]*(20-8) for _ in range(5)]
    
    for course in electiveCourses:
        print(parseCourseStructure(courses[course]["courseStructure"]))

    return 

def generateAdjecancyMatrix(studentData: dict, assignedCourses: list, indexIdDictionary: dict) -> [list]:
    mat: [list] = [[0]*len(assignedCourses) for _ in range(len(assignedCourses))]
    for student in studentData:
        for firstCourse in studentData[student]["courses"]:
            for secondCourse in studentData[student]["courses"]:
                mat[indexIdDictionary[firstCourse]][indexIdDictionary[secondCourse]] += 1
    return mat

def main() -> None:

    studentData = {}
    courses = {}
    with open("./data/studentsData.json", 'r', encoding='utf-8') as file:
        studentData = json.load(file)
    with open("./data/ferCoursesList.json", 'r', encoding='utf-8') as file:
        courses = json.load(file)

    indexIdDictionary = {}
    assignedCourses = []
    mandatoryCourses = []
    electiveCourses = []
    transversalCourses = []

    for student in studentData:

        for course in studentData[student]["courses"]:

            if course not in assignedCourses:

                indexIdDictionary[course] = len(assignedCourses)
                assignedCourses.append(course)
                
                match courses[course]["courseType"]:
                    case "Obavezni":
                        mandatoryCourses.append(course)
                    case "Transverzalni":
                        transversalCourses.append(course)
                    case "Izborni":
                        electiveCourses.append(course)

    reverseIndexIdDictionary = {}
    for key, value in indexIdDictionary.items():
        reverseIndexIdDictionary[value] = key

    mat: [list] = generateAdjecancyMatrix(studentData, assignedCourses, indexIdDictionary)
    for i, line in enumerate(mat):
        courseName = courses[reverseIndexIdDictionary[i]]["courseName"]
        print(f'{courseName}: {line}')
    generateSchedule(mat, mandatoryCourses, electiveCourses, transversalCourses, indexIdDictionary, courses)
    

if __name__ == "__main__":
    main()