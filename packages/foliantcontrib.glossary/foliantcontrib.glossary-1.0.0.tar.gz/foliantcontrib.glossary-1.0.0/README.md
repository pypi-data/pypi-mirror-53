# Glossary collector for Foliant

Glossary preprocessor collects terms and definitions from the files stated and inserts them to specified places of the document.


## Installation

```shell
$ pip install foliantcontrib.glossary
```


## Config

To enable the preprocessor, add `glossary` to `preprocessors` section in the project config.

```yaml
preprocessors:
  - glossary
```

The preprocessor has a number of options (default values stated below):

```yaml
preprocessors:
  - glossary:
        term_definitions: 'term_definitions.md'
        definition_mark: ':   '
        files_to_process: ''
```

`term_definitions`
:   Local or remote file with terms and definitions in Pandoc [definition_lists](https://pandoc.org/MANUAL.html#definition-lists) notation (by default this file stored in foliant project folder, but you can place it other folder). Also you can use [includes](https://foliant-docs.github.io/docs/preprocessors/includes/) in this file to join several glossary files. In this case `includes` preprocessor should be stated before `glossary` in `foliant.yml` preprocessors section. Note that if several definitions of one term are found, only first will be used.

`definition_mark`
:   Preprocessor uses this string to determine, if the definition should be inserted here. `":   "` for Pandoc [definition_lists](https://pandoc.org/MANUAL.html#definition-lists) notation.

`files_to_process`
:   You can set certain files to process by preprocessor.


## Usage

Just add the preprocessor to the project config, set it up and enjoy the automatically collected glossary in your document.


## Example

**foliant.yml**

```yaml
...
chapters:
    - text.md

preprocessors:
...
    - includes
    - glossary
...
```

**term_definitions.md**

```
# Glossary

<include nohead="true">
    $https://git.repo/repo_name_1$src/glossary_1.md
</include>

<include nohead="true">
    $https://git.repo/repo_name_2$src/glossary_2.md
</include>
```

**glossary_1.md** from **repo_1**

```
# Glossary

Term 1

:   Definition 1

Term 2

:   Definition 2

Term 3

:   Definition 3

```

**glossary_2.md** from **repo_2**

```
# Glossary

Term 4

:   Definition 4

        { some code, part of Definition 4 }

    Third paragraph of definition 4.

Term 5

:   Definition 5

```

**text.md**

```
# Main chapter

Some text.

# Glossary

:   Term 1

:   Term 4

:   Term 2

```

**\_\_all\_\_.md**

```
# Main chapter

Some text.

# Glossary

Term 1

:   Definition 1


Term 4

:   Definition 4

        { some code, part of Definition 4 }

    Third paragraph of definition 4.


Term 2

:   Definition 2

```
