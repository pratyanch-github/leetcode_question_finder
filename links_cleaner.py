def read_input_file(filename):
    with open(filename, "r") as file:
        lines = [line.strip() for line in file]
    return lines

def write_output_file(filename, lines):
    with open(filename, "a") as file:
        for line in lines:
            file.write(line + '\n')

def remove_pattern(lines, pattern):
    new_lines = [line for line in lines if pattern not in line]
    return new_lines

if __name__ == "__main__":
    input_filename = "lc.txt"
    output_filename = "lc_problems.txt"
    pattern_to_remove = "/solution"

    input_lines = read_input_file(input_filename)

    # Removing duplicates
    unique_lines = list(set(input_lines))

    # Removing lines containing the pattern
    filtered_lines = remove_pattern(unique_lines, pattern_to_remove)

    # Write the filtered lines to the output file
    write_output_file(output_filename, filtered_lines)

    print("Number of lines in the output file:", len(filtered_lines))
