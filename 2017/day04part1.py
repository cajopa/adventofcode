def is_valid(passphrase):
    words = passphrase.split(' ')
    unique_words = set(words)
    
    return len(words) == len(unique_words)

def count_valid(input_path):
    count = 0
    
    with open(input_path, 'r') as f:
        for line in (line.strip() for line in f):
            if line and is_valid(line):
                count += 1
    
    return count
