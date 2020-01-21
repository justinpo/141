
def tokenizeTestCase(testCase):
    if "{" in testCase:
        return [testCase]
    elif "(" in testCase:
        return [testCase]
    
    tokenized = testCase.split(" ", 1)
    variables = tokenized[1]
    tokenized.pop()

    temp = variables.split(",")

    for x in temp:
        tokenized.append(x.replace(" ", ""))

    print(tokenized)
    
    return tokenized

def tokenizeFile() -> [[str]]:
    with open("mpa1.in") as file:
        inputString: str = file.read()
        inputString = inputString.split("\n", 1)[1]
        inputString = inputString.replace("\r", " ")
        inputString = inputString.replace("\n", " ")
        inputString = inputString.replace("\t", " ")
        testCases: [str] = inputString.split('#')
        testCases = [
            testCase for testCase in testCases if (testCase != "" and testCase != " ")
        ]
        parsed: [] = []
        for testCase in testCases:
            testCase = testCase.strip()
            testCase = testCase.strip(';')
            parsed.append(tokenizeTestCase(testCase))

        return parsed

def main():
    parsed = tokenizeFile()

if __name__ == "__main__":
    main()