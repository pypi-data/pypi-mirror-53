import unittest
from charset_normalizer.normalizer import CharsetNormalizerMatches as CnM

from encodings.aliases import aliases
from glob import glob

from loguru import logger
from os.path import basename
from prettytable import PrettyTable


class TestChardetFile(unittest.TestCase):

    def test_on_chardet(self):

        self.assertTrue(True)

        stats = dict()

        for path_name in glob('../data/chardet/**/*'):
            folder_name = path_name.split('/')[-2].lower().replace('-', '_')

            if folder_name.startswith('windows_'):
                folder_name = '_'.join(folder_name.split('_')[:2])

            if folder_name.startswith('iso_'):
                folder_name = '_'.join(folder_name.split('_')[:3])

            target_encoding = None

            for a, b in aliases.items():
                if a == folder_name:
                    target_encoding = b
                    break
                elif b == folder_name:
                    target_encoding = folder_name
                    break

            if target_encoding is None:
                logger.critical('We do not know {folder_name} ??! What the encoding !', folder_name=folder_name)
                continue

            if target_encoding not in stats.keys():
                stats[target_encoding] = {
                    'n_tested': 0,
                    'n_failure': 0,
                    'failed_files': list()
                }

            stats[target_encoding]['n_tested'] += 1

            r_ = CnM.from_path(path_name).best().first()

            if r_ is None:
                stats[target_encoding]['n_failure'] += 1
                stats[target_encoding]['failed_files'].append(path_name)
                logger.error('Unable to detect AT ALL "{base_file}" encoding. Expect it should be {target_encoding}.', base_file=basename(path_name), target_encoding=target_encoding)
                continue

            if target_encoding not in ' '.join(r_.could_be_from_charset):
                stats[target_encoding]['n_failure'] += 1
                stats[target_encoding]['failed_files'].append(path_name)
                logger.warning('Unable to get right "{base_file}". Marked as {target_encoding}, but got this instead {detected_encoding}.', base_file=basename(path_name), target_encoding=target_encoding, detected_encoding=r_.could_be_from_charset)
                continue

            logger.info('"{base_file}" detected correctly as {target_encoding}.', base_file=basename(path_name), target_encoding=target_encoding)

        x = PrettyTable(['Encoding', 'Tested', 'Failure', 'Success Rate'])

        for a, b in stats.items():
            x.add_row(
                [
                    a,
                    b['n_tested'],
                    b['n_failure'],
                    str(round(((b['n_tested'] - b['n_failure']) / b['n_tested']) * 100, ndigits=3))+' %'
                ]
            )

        print(x)


if __name__ == '__main__':
    unittest.main()
