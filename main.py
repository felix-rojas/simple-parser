from Parser import Parser
import sys
import glob

if __name__ == '__main__':
    print("---------------------------------------")
    print("Testing good cases (should compile)")
    print("---------------------------------------")
    for file in glob.glob('test_cases/good/input*.txt'):
        print(f"Parsing {file}")
        try:
            parser = Parser(file)
            parser.analize()
            print("-> Successfully parsed\n")
        except Exception as e:
            print(f"-> Error: {e}\n")
    
    print("---------------------------------------")
    print("Testing bad cases (should throw error)")
    print("---------------------------------------")
    for file in glob.glob('test_cases/bad/input*.txt'):
        print(f"Parsing {file}")
        try:
            parser = Parser(file)
            parser.analize()
            print("-> This should have failed!\n")
        except Exception as e:
            print(f"-> Expected Error caught: {e}\n")