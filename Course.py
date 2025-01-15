class Course:

    def __init__(self, id: int, name: str, ects: int, lectures: list) -> None:
        self.id = id
        self.name = name
        self.ects = ects
        self.lectures = lectures

    def __str__(self) -> str:
        return f'Lectures: {self.lectures}'


def main():
    arh = Course(0,0,0,[2,2])
    print(arh)

if __name__ == "__main__":
    main()