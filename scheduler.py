import json

failedCourses = []

def parseCourseStructure(structure: str) -> tuple[list, int]:
    '''
    Function which parses number of lecture and excersies per week.
    Args:
        structure (int): structure of a course in the form of "int+int+int+int"
    Returns:
        lecturesPerWeek (list): list of lectures where the number of elements represents number of lectures
            and the value of the element the duration of the lecture
        excercisesPerWeek (int): duration of excercises per week
    '''

    lectures, seminar, excercises, laboratoryExcercises = [int(x) for x in structure.split("+")]
    lecturesPerWeek = []

    if lectures%15 == 0:

        match lectures//15:
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

def checkSlot(course: str, lecture: int, day: int, hour: int, timeSlots: [list], indexIdDictionary: dict, graphColor: list) -> bool:
    '''
    Function which checks if the selected slot is valid and able to be assigned.
    Automatically checks {lecture+1} number of slots in the day ahead.
    Args:
        course (str): unique id of the course
        lecture (int): length of the lecture
        day (int): selected day slot
        hour (int): selected hour slot
        timeSlots [list]: list of all weekly time slots
        indexIdDictionary (list): connects the unique course id with its corresponding index in the graphColor/adjacencyMatrix
        graphColor (list): list of colors assigned to each course
    Returns:
        True if slot is able to be assigned, otherwise False
    '''

    #if lecture exceedes the daily reserved time slot it cannot be assigned
    if (hour+lecture) > len(timeSlots[day]):
        return False

    #increment to fit all hours of a lecture
    for increment in range(lecture):
        #each course already assigned to this time slot
        for assignedCourse in timeSlots[day][hour+increment]:

            #should never happen but i'll leave the check here
            if assignedCourse == course:
                continue
            
            #if two courses have a different graph color they cannot overlap
            if graphColor[indexIdDictionary[course]] != graphColor[indexIdDictionary[assignedCourse]]:
                return False
    return True

def addToSchedule(course: str, courses: dict, lecture: int, timeSlots: [list], indexIdDictionary: dict, selected_day: int, graphColor: list) -> int:
    '''
    Function which adds a course to a time slot.
    Args:
        course (str): unique id of the course
        courses (dict): dictionary connecting the unique course id with data about the course
        lecture (int): length of the lecture
        timeSlots [list]: list of all weekly time slots
        indexIdDictionary (list): connects the unique course id with its corresponding index in the graphColor/adjacencyMatrix
        selected_day (list): list of all already assigned days for the current course (so that a course cannot have two different lectures on the same day)
        graphColor (list): list of colors assigned to each course
    Returns:
        day (int): selected day where the lecture has been added or None
    '''

    for hour in range(len(timeSlots[0])):
        for day in range(len(timeSlots)):
            if day in selected_day:
                continue

            if checkSlot(course, lecture, day, hour, timeSlots, indexIdDictionary, graphColor):
                for i in range(lecture):
                    timeSlots[day][hour+i].append(course)
                return day
    failedCourses.append(course)

def addByType(coursesByType: list, timeSlots: [list], indexIdDictionary: dict, courses: dict, graphColor: list) -> None:
    '''
    Function which prepares lectures for each course to be added to the schedule
    Args:
        courseByType (list): list of courses based on their types (mandatory, transversal or elective)
        timeSlots [list]: list of all weekly time slots
        indexIdDictionary (list): connects the unique course id with its corresponding index in the graphColor/adjacencyMatrix
        courses (dict): dictionary connecting the unique course id with data about the course
        graphColor (list): list of colors assigned to each course
    Returns:
        None
    '''

    for course in coursesByType:
        lectures, excercises = parseCourseStructure(courses[course]["courseStructure"])
        selected_day = []
        for lecture in lectures:
            result = addToSchedule(course, courses, lecture, timeSlots, indexIdDictionary, selected_day, graphColor)
            selected_day.append(result)



def generateSchedule(mandatoryCourses: list, electiveCourses: list,\
     transversalCourses: list, indexIdDictionary: dict, courses: dict, graphColor: list) -> [list]:
    '''
    Function which calls the helper functions to fill out the schedule
    Args:
        mandatoryCourses (list): list of all mandatory courses
        electiveCourses (list): list of all elective courses
        transversalCourses (list): list of all transversal courses
        indexIdDictionary (list): connects the unique course id with its corresponding index in the graphColor/adjacencyMatrix
        courses (dict): dictionary connecting the unique course id with data about the course
        graphColor (list): list of colors assigned to each course
    Returns:
        timeSlots [list]: generated schedule
    '''
    
    timeSlots = [[[] for _ in range(20-8)] for _ in range(5)]
    
    addByType(mandatoryCourses, timeSlots, indexIdDictionary, courses, graphColor)
    addByType(electiveCourses, timeSlots, indexIdDictionary, courses, graphColor)
    addByType(transversalCourses, timeSlots, indexIdDictionary, courses, graphColor)

    return timeSlots

def printSchedule(schedule: [list], courses: dict) -> None:
    '''
    Helper function which prints the schedule
    Args:
        schedule[list]: list of all weekly time slots
        courses (dict): dictionary connecting the unique course id with data about the course
    Returns:
        None
    '''
    for dayIndex,day in enumerate(schedule):
        print(f'\nDay {dayIndex+1}: ')
        for hourIndex, hour in enumerate(day):
            print(f'{hourIndex+8:0>2}:00 - {hourIndex+9:0>2}:00\t {[courses[course]["courseName"] for course in hour]}')

def generateJSON(schedule: [list], courses: dict) -> dict:
    '''
    Helper function which generates a dictionary from the schedule
    Args:
        schedule[list]: list of all weekly time slots
        courses (dict): dictionary connecting the unique course id with data about the course
    Returns:
        result (dict): schedule as a dictionary
    '''
    result = {}

    for dayIndex, day in enumerate(schedule):

        for hourIndex, hour in enumerate(day):

            for course in hour:

                courseName = courses[course]["courseName"]
                lecture = {"day": dayIndex,"start": None, "end": None}
                lecture["start"] = hourIndex
                increment = 0
                while course in day[hourIndex+increment]:
                    schedule[dayIndex][hourIndex+increment].remove(course)
                    increment+=1
                    if hourIndex+increment >= len(day):
                        break
                lecture["end"] = hourIndex+increment
                if course not in result:
                    result[course] = [lecture]
                else:
                    result[course].append(lecture)
    return result


def generateAdjecancyMatrix(studentData: dict, assignedCourses: list, indexIdDictionary: dict) -> [list]:
    '''
    Generates the adjacency matrix for the courses.
    Args:
        studentData (dict): contains all data about a student (semestar and enrolled courses)
        assignedCourses (list): list of all courses assigned to at least one student
        indexIdDictionary (list): connects the unique course id with its corresponding index in the graphColor/adjacencyMatrix
    Returns:
        adjacencyMatrix [list]: Values are: 0 if no students share the courses i and j, or n if n users share those courses
    '''
    adjacencyMatrix: [list] = [[0]*len(assignedCourses) for _ in range(len(assignedCourses))]

    for student in studentData:

        for firstCourse in studentData[student]["courses"]:

            for secondCourse in studentData[student]["courses"]:

                adjacencyMatrix[indexIdDictionary[firstCourse]][indexIdDictionary[secondCourse]] += 1

    return adjacencyMatrix

def colorGraph(adjacencyMatrix: dict) -> list:
    '''
    Function which implements the coloring of graphs from the adjacency matrix using a greedy algorithm.
    Args:
        adjacencyMatrix [list]: Values are: 0 if no students share the courses i and j, or n if n users share those courses
    Returns:
        solution (list): color indexes for each course in the adjacency matrix
    '''
    solution: list = [-1] * len(adjacencyMatrix)

    solution[0] = 0

    for node in range(1, len(adjacencyMatrix)):

        forbidden_colors = set()
        for neighbour in range(len(adjacencyMatrix)):

            if adjacencyMatrix[node][neighbour]>0 and solution[neighbour] != -1:
                forbidden_colors.add(solution[neighbour])

        for color in range(len(adjacencyMatrix)):
            if solution[node] == -1 and color not in forbidden_colors:
                solution[node] = color

    return solution

def sortSubjects(studentData: dict, assignedCourses: list, mandatoryCourses: list,\
     electiveCourses: list, transversalCourses: list, indexIdDictionary: dict, courses: dict) -> None:
    '''
    Function sorts subjects(courses) based on their courseType. Also fills up the assigned courses.
    Args:
        studentData (dict): contains all data about a student (semestar and enrolled courses)
        assignedCourses (list): list of all courses assigned to at least one student
        mandatoryCourses (list): empty, to be filled in this function
        electiveCourses (list): empty, to be filled in this function
        transversalCourses (list): empty, to be filled in this function
        indexIdDictionary (list): connects the unique course id with its corresponding index in the graphColor/adjacencyMatrix
        courses (dict): dictionary connecting the unique course id with data about the course
    Returns:
        None
    '''
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

def scheduler() -> None:
    '''
    Entry point for the script
    '''
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

    sortSubjects(studentData, assignedCourses, mandatoryCourses, electiveCourses, transversalCourses, indexIdDictionary, courses)

    reverseIndexIdDictionary = {}
    for key, value in indexIdDictionary.items():
        reverseIndexIdDictionary[value] = key

    adjacencyMatrix: [list] = generateAdjecancyMatrix(studentData, assignedCourses, indexIdDictionary)
    # for i, line in enumerate(adjacencyMatrix):
    #     courseName = courses[reverseIndexIdDictionary[i]]["courseName"]
    #     print(f'{courseName}: {line}')

    graphColor = colorGraph(adjacencyMatrix)
    #print(f'Bojanje grafa: {graphColor}')

    schedule = generateSchedule(mandatoryCourses, electiveCourses,\
         transversalCourses, indexIdDictionary, courses, graphColor)

    printSchedule(schedule, courses)

    if failedCourses:
        print(f'Nije uspjelo dodavanje: {[courses[course]["courseName"] for course in failedCourses]}')

    json_result = generateJSON(schedule, courses)
    with open("./data/finalSchedule.json", 'w', encoding='utf-8') as output:
        json.dump(json_result, output, ensure_ascii=False, indent=4)


scheduler()