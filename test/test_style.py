import sys
import os
import shutil

sys.path.append("../src")

from style_transfer import transfer_random_style_folder

if __name__ == "__main__":
    content = "./content"
    style = "./style"
    result = "./results"

    # empty results folder
    for filename in os.listdir(result):
        file_path = os.path.join(result, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

    print("starting test")
    transfer_random_style_folder(content, style, result)
    print("end test")
    try:
        assert len(os.listdir(result)) == 2
        print("test passed")
    except Exception as e:
        print(f"test failed because of {e}")
