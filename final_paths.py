import os

def gen_paths(main_path):
    final_paths = []
    for watched_path in main_path:
        watched_path = os.path.abspath(watched_path)

        if not os.path.isdir(watched_path):
            print(f"Skipping invalid path: {watched_path}")
            continue

        try:
            for name in os.listdir(watched_path):
                full_path = os.path.join(watched_path, name)

                # Only keep directories
                if os.path.isdir(full_path):
                    final_paths.append(full_path)

        except OSError as e:
            print(f"Failed to read {watched_path}: {e}")

    return final_paths
    