from Parser import Parser
import sys
import glob

if __name__ == '__main__':
    print("\nTesting good cases (should compile)")
    for file in glob.glob('test_cases/good/input*.txt'):
        print(f"Parsing {file}")
        try:
            parser = Parser(file)
            parser.analize()
            print("-> Successfully parsed")
        except Exception as e:
            print(f"-> Error: {e}")
    
    print("\nTesting bad cases (should throw error)")
    for file in glob.glob('test_cases/bad/input*.txt'):
        print(f"Parsing {file}")
        try:
            parser = Parser(file)
            parser.analize()
            print("-> This should have failed!)")
        except Exception as e:
            print(f"-> Expected Error caught: {e}")