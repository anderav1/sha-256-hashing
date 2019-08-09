import hashlib
import os
import time

# task 1: determine hashes/second for files of various lengths & compare to another hashing
# function; calculate time to find a collision for a particular value with both algorithms


# file generation function from project 2
def generate_file(file_name: str, file_size: int):
    with open(file_name + '.txt', 'wb') as file:
        file.write(os.urandom(file_size))


def sha_256_file_hash(file_name: str):
    with open(file_name + '.txt', 'rb') as file:
        file_contents = file.read()

    sha_256 = hashlib.sha256()
    sha_256.update(file_contents)
    return sha_256.digest()


def md5_file_hash(file_name: str):
    with open(file_name + '.txt', 'rb') as file:
        file_contents = file.read()

    md5 = hashlib.md5()
    md5.update(file_contents)
    return md5.digest()


def sha_256_hashes_in_1_sec(file_name: str):
    num_of_hashes = 0
    elapsed_time = 0
    start_time = time.time()
    while elapsed_time < 1.0:
        sha_256_file_hash(file_name)
        num_of_hashes += 1
        elapsed_time = time.time() - start_time
    print(file_name, "was hashed", num_of_hashes, "times by SHA-256 in 1 sec")


def md5_hashes_in_1_sec(file_name: str):
    num_of_hashes = 0
    elapsed_time = 0
    start_time = time.time()
    while elapsed_time < 1.0:
        md5_file_hash(file_name)
        num_of_hashes += 1
        elapsed_time = time.time() - start_time
    print(file_name, "was hashed", num_of_hashes, "times by MD5 in 1 sec")


def time_for_sha_256_collision(file_name: str):
    target_hash = sha_256_file_hash(file_name)

    i = 0
    elapsed_time = 0

    while True:
        sha_256 = hashlib.sha256()
        test_value = i.to_bytes(8, byteorder='big')
        i += 1

        start_time = time.time()
        new_hash = sha_256.update(test_value)
        end_time = time.time()
        elapsed_time += end_time - start_time

        if new_hash == target_hash:
            return elapsed_time


def time_for_collision(hash_name: str, file_name: str):
    if hash_name == "sha-256":
        target_hash = sha_256_file_hash(file_name)
        hash_func = hashlib.sha256
    elif hash_name == "md5":
        target_hash = md5_file_hash(file_name)
        hash_func = hashlib.md5
    else:
        return

    i = 0
    elapsed_time = 0

    while True:
        hash_function = hash_func().copy()
        test_value = i.to_bytes(8, byteorder='big')
        i += 1

        start_time = time.time()
        hash_function.update(test_value)
        new_hash = hash_function.digest()
        end_time = time.time()
        elapsed_time += end_time - start_time

        if new_hash == target_hash:
            return elapsed_time


def birthday_prefix(num_of_chars: int):
    target_prefix = "11221996"
    i = 0
    elapsed_time = 0

    while True:
        sha_256 = hashlib.sha256()
        test_value = i.to_bytes(32, byteorder="big")
        i += 1

        start_time = time.time()
        new_hash = hashlib.sha256(test_value).hexdigest()
        end_time = time.time()
        elapsed_time += end_time - start_time

        if new_hash.startswith(target_prefix[:num_of_chars]):
            print("Found first", num_of_chars, "digits in", elapsed_time, "sec")
            print(new_hash)
            return


def main():
    # configure files
    file_names = ["file0", "file1", "file2", "file3", "file4"]
    file_sizes = [16, 156, 328, 641, 1000]

    for index in range(len(file_names)):
        generate_file(file_names[index], file_sizes[index])

    # task 1
    # for file_name in file_names:
    #     sha_256_hashes_in_1_sec(file_name)
    #     md5_hashes_in_1_sec(file_name)

    # sha256_collision_time = time_for_collision("sha-256", file_names[0])
    # print("It took", sha256_collision_time, "sec to find a collision for", file_names[0],
    #       "of size", file_sizes[0], "with SHA-256")
    # md5_collision_time = time_for_collision("md5", file_names[0])
    # print("It took", md5_collision_time, "sec to find a collision for", file_names[0], "of size",
    #       file_sizes[0], "with MD5")

    # task 2
    for i in range(1, 9):
        birthday_prefix(i)


main()
