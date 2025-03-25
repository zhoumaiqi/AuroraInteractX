def split_file(input_file, output_files):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    total_chars = len(content)
    part_size = total_chars // len(output_files)
    
    for i, output_file in enumerate(output_files):
        start = i * part_size
        end = (i + 1) * part_size if i != len(output_files) - 1 else total_chars
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(content[start:end])

input_file = '/home/sunrise/display_robot/txt/bettertxt.txt'
output_files = [
    '/home/sunrise/display_robot/txt/better1.txt',
    '/home/sunrise/display_robot/txt/better2.txt',
    '/home/sunrise/display_robot/txt/better3.txt',
    '/home/sunrise/display_robot/txt/better4.txt',
    '/home/sunrise/display_robot/txt/better5.txt'
]

split_file(input_file, output_files)