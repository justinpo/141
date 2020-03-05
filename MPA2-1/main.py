
class Expression:
    def __init__(self, testCase: str):
        self._string: str = testCase
        

def tokenizeFile() -> [[str]]:
    with open("mpa2.in") as file:
        inputString: str = file.read()

        return inputString

def main():
    tokens = tokenizeFile()
    print(tokens)

if __name__ == "__main__":
    main()