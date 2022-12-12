from hstest.stage_test import StageTest
from hstest.check_result import CheckResult
from hstest import dynamic_test, TestedProgram
import os
import shutil

# dict for creating files
files = {
    'info.txt': {'path': ['root_folder'],
                 'content': 'eed110d0dbd1d89d1ffea807d1d88679'},
    'lost.json': {'path': ['root_folder'],
                  'content': '3a70ac2ebacf4174aa11dfbd1af835bd'},
    'phones.csv': {'path': ['root_folder'],
                   'content': '671ab9fbf94dc377568fb7b2928960c9'},
    'python.txt': {'path': ['root_folder'],
                   'content': 'd2c2ee4cbb368731f1a5399015160d7d'},
    'bikeshare.csv': {'path': ['root_folder', 'calc'],
                      'content': 'c03285172453d7278a85a5db4d06423c'},
    'server.php': {'path': ['root_folder', 'calc'],
                   'content': 'a5c662fe853b7ab48d68532791a86367'},
    'db_cities.js': {'path': ['root_folder', 'files'],
                     'content': 'f2e5cf58ae9b2d2fd0ae9bf8fa1774da'},
    'some_text.txt': {'path': ['root_folder', 'files'],
                      'content': 'd2c2ee4cbb368731f1a5399015160d7d'},
    'cars.json': {'path': ['root_folder', 'files', 'stage'],
                  'content': '3a70ac2ebacf4174aa11dfbd1af835bd'},
    'package-lock.json': {'path': ['root_folder', 'files', 'stage'],
                          'content': 'eebf1c62a13284ea1bcfe53820e83f11'},
    'index.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                 'content': '797ac79aa6a3c2ef733fecbaff5a655f'},
    'libs.txt': {'path': ['root_folder', 'files', 'stage', 'src'],
                 'content': '4909fd0404ac7ebe1fb0c50447975a2a'},
    'reviewslider.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                        'content': 'abc96a9b62c4701f27cf7c8dbd484fdc'},
    'spoiler.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                   'content': 'b614ccac263d3d78b60b37bf35e860f3'},
    'src.txt': {'path': ['root_folder', 'files', 'stage', 'src'],
                'content': 'eed110d0dbd1d89d1ffea807d1d88679'},
    'toggleminimenu.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                          'content': '7eceb7dd5a0daaccc32739e1dcc6c3b0'},
    'extraversion.csv': {'path': ['root_folder', 'project'],
                         'content': 'fc88cf4d79437fa06e6cfdd80bd0eed2'},
    'index.html': {'path': ['root_folder', 'project'],
                   'content': '3f0f7b61205b863d2051845037541835'},
    'python_copy.txt': {'path': ['root_folder', 'project'],
                        'content': 'd2c2ee4cbb368731f1a5399015160d7d'}
}

# arrs for checking results
root_dir = [
    'info.txt',
    'lost.json',
    'phones.csv',
    'python.txt',
    'bikeshare.csv',
    'server.php',
    'db_cities.js',
    'some_text.txt',
    'cars.json',
    'package-lock.json',
    'index.js',
    'libs.txt',
    'reviewslider.js',
    'spoiler.js',
    'src.txt',
    'toggleminimenu.js',
    'extraversion.csv',
    'index.html',
    'python_copy.txt'
]

files_dir = [
    'db_cities.js',
    'some_text.txt',
    'cars.json',
    'package-lock.json',
    'index.js',
    'libs.txt',
    'reviewslider.js',
    'spoiler.js',
    'src.txt',
    'toggleminimenu.js'
]

root_dir_path = os.path.join('module', 'root_folder')
files_dir_path = os.path.join('module', 'root_folder', 'files')


def create_files(path):
    # delete root_folder
    if os.path.isdir(path):
        shutil.rmtree(path)

    # create files
    for key, dict_val in files.items():
        path = os.path.join('module', *dict_val['path'])
        if not os.path.isdir(path):
            os.makedirs(path)
        file_path = os.path.join(path, key)
        with open(file_path, 'a+') as f:
            f.write(dict_val['content'])


class DuplicateFileHandlerCheck(StageTest):

    @dynamic_test()
    def check_empty_arg(self):
        main = TestedProgram()
        output = main.start().lower()
        if 'not' in output and 'specified' in output:
            return CheckResult.correct()
        return CheckResult.wrong("You should check command line argument")

    @dynamic_test()
    def check_root_folder(self):
        main = TestedProgram()
        output = main.start(root_dir_path).split('\n')
        output = [val for val in output if val]
        if len(output) > 19:
            print(output)
            return CheckResult.wrong(f"Output contains extra files. Number of files in your output is {len(output)}")
        if len(output) < 19:
            return CheckResult.wrong(f"Some files are missing. Number of files in your output is {len(output)}")
        for path in output:
            file = path.replace('/', '\\').split('\\')[-1]
            if file not in files:
                return CheckResult.wrong(f"Output contains wrong files: {file}")
        return CheckResult.correct()

    @dynamic_test()
    def check_root_folder(self):
        main = TestedProgram()
        output = main.start(files_dir_path).split('\n')
        output = [val for val in output if val]
        if len(output) > 10:
            print(output)
            return CheckResult.wrong(f"Output contains extra files. Number of files in your output is {len(output)}")
        if len(output) < 10:
            return CheckResult.wrong(f"Some files are missing. Number of files in your output is {len(output)}")
        for path in output:
            file = path.replace('/', '\\').split('\\')[-1]
            if file not in files_dir:
                return CheckResult.wrong(f"Output contains wrong files: {file}")
        return CheckResult.correct()

    def after_all_tests(self):
        try:
            if os.path.isdir(root_dir_path):
                shutil.rmtree(root_dir_path)
        except Exception as ignored:
            pass

    def generate(self):
        try:
            create_files(root_dir_path)
        except Exception as ignored:
            pass
        return []


if __name__ == '__main__':
    DuplicateFileHandlerCheck().run_tests()
