from algs import multiply_base, multiply_win, multiply_win_op, insert_matrix, create_random_matrix, print_answer
from in_out import input_matrix, check_input
from compare_time import run_time_analysis

def main():
    command = -1
    
    while command != 0:
        command = check_input()

        if command == 1:
            matrix1, matrix2 = input_matrix()
            print ("Matrix1:")
            print_answer(matrix1)
            print ("Matrix2:")
            print_answer(matrix2)
            print ("Result:")
            print_answer(multiply_base(matrix1, matrix2))
            
        elif command == 2:
            matrix1, matrix2 = input_matrix()
            print ("Matrix1:")
            print_answer(matrix1)
            print ("Matrix2:")
            print_answer(matrix2)
            print ("Result:")
            print_answer(multiply_win(matrix1, matrix2))
            
        elif command == 3:
            matrix1, matrix2 = input_matrix()
            print ("Matrix1:")
            print_answer(matrix1)
            print ("Matrix2:")
            print_answer(matrix2)
            print ("Result:")
            print_answer(multiply_win_op(matrix1, matrix2))

        elif command == 4:
            run_time_analysis()
            
if __name__ == "__main__": 
    main()