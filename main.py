from utils import process_file

if __name__ == "__main__":

    test_string = input("Ingrese una cadena w: ")
    filename = 'regex.txt'
    process_file(filename, test_string)
