import os
import shutil

for root, _, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            filepath = os.path.join(root, file)
            parts = file[:-3].split('_')

            if len(parts) < 4:
                module = parts[1] if len(parts) >= 2 else "unknown"
                behavior = "_".join(parts[2:]) if len(parts) > 2 else "behavior"
                expected = "expected"

                new_file = f"test_{module}_{behavior}_{expected}.py"
                new_filepath = os.path.join(root, new_file)

                os.rename(filepath, new_filepath)
                print(f"Renamed {filepath} to {new_filepath}")
