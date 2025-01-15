from typing import TextIO
from re import sub
import json

def main() -> None:

    courseTypes = ["Obavezni", "Transverzalni", "Izborni"]
    completeStudyProgram = {}
    '''
    Study program structure
    {semesterNumber: 
                    {courseType: 
                                [courseID, ...]
                    courseType: ...
                    }
    semesterNumber: ...
    }
    '''

    def parseCourseName(line: str) -> tuple[str, str, str, str]:
        ects, structure, name = line.split(";")

        name = name.split(" ")

        courseID = sub(r'[()]', r'',name[-1])
        courseName = " ".join(name[0:-1])

        return courseID, courseName, ects, structure

    def parseCourseType(currentSemester: int, courseType: str, filePointer: TextIO) -> TextIO:

        #initialize courseType key in the currentSemester
        completeStudyProgram[currentSemester][courseType] = []

        for line in filePointer:

            line = line.rstrip()
            if line == "":
                break

            courseID, courseName, ects, structure = parseCourseName(line)
            
            completeStudyProgram[currentSemester][courseType].append(courseID)

        return filePointer
    
    def dumpCoursesByID(file: TextIO) -> None:

        courses = {}
        '''
        Courses structure
        {courseID: 
                    {courseName: name, ECTS, ects, courseStructure: structure}
        courseID: ...
        }
        '''
        courseTypeTracker = ""
        for line in file:
            
            line = line.rstrip()

            if line == "":
                continue
            
            elif line in courseTypes:
                courseType = line

            if line[0].isdigit():

                courseID, courseName, ects, structure = parseCourseName(line)

                courses[courseID] = {"courseName": courseName, "ECTS": ects, "courseType": courseType, "courseStructure": structure}

        with open("./data/ferCoursesList.json", 'w', encoding='utf-8') as output:
            json.dump(courses, output, indent=4, ensure_ascii=False)

        return

    with open("./data/ferPredmeti.txt", 'r', encoding='utf-8') as file:

        dumpCoursesByID(file)
    
        file.seek(0)

        currentSemester: int = 0

        for line in file:

            line = line.rstrip()
            if line == "":
                continue

            elif line in courseTypes:
                file: TextIO = parseCourseType(currentSemester, line, file)

            else:
                print(f'Line: {line}')
                currentSemester = line.split(" ")[1]
                completeStudyProgram[currentSemester] = {}

    with open("./data/ferCoursesBySemester.json", 'w', encoding='utf-8') as output:
        json.dump(completeStudyProgram, output, indent = 4, ensure_ascii=False)
    
    return

if __name__ == "__main__":
    main()