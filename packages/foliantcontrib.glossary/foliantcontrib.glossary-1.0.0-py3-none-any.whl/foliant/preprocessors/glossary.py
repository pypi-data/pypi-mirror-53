'''
Preprocessor for Foliant documentation authoring tool.
Replaces terms with definitions from dictionary.
'''

from pathlib import Path
import re

from foliant.preprocessors.base import BasePreprocessor
from foliant.preprocessors import includes
from foliant.utils import output


class Preprocessor(BasePreprocessor):
    defaults = {
        'term_definitions': 'term_definitions.md',
        'definition_mark': ':   ',
        'files_to_process': '',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('glossary')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._term_def_file = self.options['term_definitions']
        self._def_mark = self.options['definition_mark']
        self._files_to_process = set(map(str.strip, list(self.options['files_to_process'].split(';'))))

    def _get_term_defs(self, filename):
        glossary = {}

        if filename.startswith('http'):
            repo_url = filename.split('/blob')[0]
            revision = filename.split('/blob/')[1].split('/')[0]
            repo_path = includes.Preprocessor(
                        self.context,
                        self.logger,
                        self.quiet,
                        self.debug,
                        {}
                    )._sync_repo(repo_url, revision)
            filename = str(repo_path) + filename.split(revision)[1]

        with open(filename, encoding="utf-8") as file_to_read:
            term = ''
            definition = ''
            for string in file_to_read:
                if re.match('[A-Z,a-z,А-Я,а-я,0-9]', string):
                    if term:
                        if term not in glossary.keys():
                            glossary.update({term: definition})
                        else:
                            output('\nTerm "%s" repetition' % term)
                            self.logger.debug(f'Term "{term}" repetition')
                    term = string.strip()
                    definition = ''
                elif not re.match('#', string):
                    definition += string
            if term not in glossary.keys():
                glossary.update({term: definition})
            else:
                output('\nTerm "%s" repetition' % term)
                self.logger.debug(f'Term "{term}" repetition')

        return glossary

    def apply(self):
        self.logger.info('Applying preprocessor')

        term_defs = self._get_term_defs(self._term_def_file)

        for markdown_file_path in self.working_dir.rglob('*.md'):
            if markdown_file_path.name in self._files_to_process or self._files_to_process == {''}:
                self.logger.debug(f'Processing Markdown file: {markdown_file_path}')

                with open(markdown_file_path, encoding='utf8') as file_to_read:
                    file_data = list(file_to_read)

                new_file_data = []

                for string in file_data:
                    if string.startswith(self._def_mark):
                        term = string[len(self._def_mark):].strip()
                        if term in term_defs.keys():
                            new_file_data.append('%s\n%s' % (term, term_defs[term]))
                        else:
                            output('\nThere is no definition for term "%s"' % term)
                            self.logger.debug(f'No definition for term: {term}')
                    else:
                        new_file_data.append(string)

                with open(markdown_file_path, 'w', encoding="utf-8") as file_to_write:
                    for string in new_file_data:
                        file_to_write.write(string)

        self.logger.info('Preprocessor applied')
