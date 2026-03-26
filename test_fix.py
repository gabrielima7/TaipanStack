from taipanstack.security.sanitizers import sanitize_filename

print("preserve_extension=True:", sanitize_filename("test.txt", preserve_extension=True))
print("preserve_extension=False:", sanitize_filename("test.txt", preserve_extension=False))
