def filter_and_copy(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.readlines()
        
        # 去除每行中的 '*' 并删除空行
        filtered_content = [line.replace('*', '').strip() for line in content if line.strip()]
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write('\n'.join(filtered_content))
        
        print(f"Filtered content has been written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "/home/sunrise/display_robot/txt/answer.txt"
    output_file = "/home/sunrise/display_robot/txt/bettertxt.txt"
    filter_and_copy(input_file, output_file)