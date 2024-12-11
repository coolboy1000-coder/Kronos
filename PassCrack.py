import hashlib
import os
import subprocess

def get_hash_type():
    print("Select the hash type to crack:")
    print("1. MD5")
    print("2. SHA1")
    print("3. SHA256")
    print("4. SHA512")
    hash_types = {1: "md5", 2: "sha1", 3: "sha256", 4: "sha512"}
    choice = int(input("Enter your choice (1-4): "))
    return hash_types.get(choice, "md5")

def get_hashes():
    print("Enter the hashes to crack (one per line, type 'done' when finished):")
    hashes = []
    while True:
        hash_input = input()
        if hash_input.lower() == "done":
            break
        hashes.append(hash_input)
    return hashes

def brute_force(hash_type, hashes):
    print(f"Starting brute force attack on {len(hashes)} {hash_type} hash(es)...")
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+~`{[]}|\;:',.<>?/\""
    max_length = int(input("Enter Maximum number: ")) # Adjust as needed
    
    def brute_force_inner(target_hash, max_length, prefix=""):
        if len(prefix) > max_length:
            return None
        hash_func = getattr(hashlib, hash_type)
        for char in chars:
            attempt = prefix + char
            hashed = hash_func(attempt.encode()).hexdigest()
            if hashed == target_hash:
                return attempt
            result = brute_force_inner(target_hash, max_length, attempt)
            if result:
                return result
        return None

    for h in hashes:
        print(f"Cracking hash: {h}")
        result = brute_force_inner(h, max_length)
        if result:
            print(f"Found! Hash: {h} -> Plaintext: {result}")
        else:
            print(f"Failed to crack hash: {h}")

def use_wordlist(hash_type, hashes):
    print("Specify the location of the wordlist:")
    wordlist = input("Path to wordlist: ").strip()
    hashcat_path = "hashcat"  # Ensure hashcat is installed and accessible
    hash_file = "hashes.txt"

    with open(hash_file, "w") as file:
        file.write("\n".join(hashes))

    command = [
        hashcat_path,
        f"-m {hashcat_mode(hash_type)}",
        hash_file,
        wordlist,
        "--force",
        "--opencl-device-types", "1,2",  # Use GPU if available
    ]

    print(f"Running hashcat with command: {' '.join(command)}")
    subprocess.run(command)
    os.remove(hash_file)

def hashcat_mode(hash_type):
    modes = {"md5": 0, "sha1": 100, "sha256": 1400, "sha512": 1700}
    return modes.get(hash_type, 0)

def main():
    hash_type = get_hash_type()
    hashes = get_hashes()
    print("Select attack type:")
    print("1. Brute force")
    print("2. Wordlist")
    choice = int(input("Enter your choice (1-2): "))
    if choice == 1:
        brute_force(hash_type, hashes)
    elif choice == 2:
        use_wordlist(hash_type, hashes)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
