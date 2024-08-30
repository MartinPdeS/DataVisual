# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/DataVisual/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                             |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| DataVisual/\_\_init\_\_.py       |        7 |        2 |        0 |        0 |     71% |     11-12 |
| DataVisual/multi\_array.py       |       97 |        6 |       30 |        8 |     89% |39, 42->41, 44, 47->46, 73->72, 86->85, 99->98, 126, 161, 285-286 |
| DataVisual/tables.py             |       13 |        1 |        4 |        0 |     94% |        55 |
| DataVisual/tools/\_\_init\_\_.py |        0 |        0 |        0 |        0 |    100% |           |
| DataVisual/units/\_\_init\_\_.py |        2 |        0 |        0 |        0 |    100% |           |
| DataVisual/units/base\_class.py  |      105 |       21 |       40 |       13 |     72% |106-108, 111-114, 145->144, 150->149, 152, 155->154, 166, 168, 170, 172, 175-182, 228->231, 241, 253 |
| DataVisual/units/components.py   |      101 |        0 |        0 |        0 |    100% |           |
|                        **TOTAL** |  **325** |   **30** |   **74** |   **21** | **86%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/MartinPdeS/DataVisual/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/DataVisual/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/MartinPdeS/DataVisual/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/DataVisual/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FMartinPdeS%2FDataVisual%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/DataVisual/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.