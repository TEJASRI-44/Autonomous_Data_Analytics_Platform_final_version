import os


def validate_dataset(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            "Dataset file not found"
        )

    valid_extensions = [
        ".csv",
        ".xlsx"
    ]

    is_valid = False

    for ext in valid_extensions:

        if file_path.endswith(ext):

            is_valid = True

    if not is_valid:

        raise ValueError(
            "Unsupported file format"
        )

    return True