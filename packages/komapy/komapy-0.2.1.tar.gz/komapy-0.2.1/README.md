# KomaPy

Python library for creating customizable BPPTKG Monitoring API chart.

## Use Cases

KomaPy is suitable for the following applications:

* Building automated static chart figure
* Embedding into a web application for generating pre-defined chart configuration
* Quick data analysis and visualization
* Data correlation and processing
* Generating high quality chart for publication
* Many more

## Requirements

KomaPy depends on Python 3.5+ and several packages. You can see them in
`requirements.txt` file.

## Installation

Install the latest version from PyPI by typing this command:

    pip install -U komapy

## Quick Start

Here it is a quick start example:

```python
from komapy import Chart
from komapy.client import set_api_key

set_api_key('YOUR_API_KEY')

chart = Chart({
    'title': 'RB2',
    'theme': 'seaborn',
    'layout': {
        'data': [
            {
                'series': [
                    {
                        'name': 'edm',
                        'query_params': {
                            'benchmark': 'BAB0',
                            'reflector': 'RB2',
                            'start_at': '2019-04-01',
                            'end_at': '2019-08-01',
                            'ci': True
                        },
                        'fields': ['timestamp', 'slope_distance'],
                        'xaxis_date': True
                    }
                ]
            }
        ]
    }
})

chart.render()
chart.save('RB2.png')
```

## Documentation

Full documentation and tutorials are available at `docs/` directory. You can
build the documentation by running these commands:

    cd /path/to/komapy/
    pip install -r requirements.txt
    sphinx-build -b html docs/ /path/to/build/ 

## Contributing

See `CONTRIBUTING.md` to learn how to contribute to this project.

## Support

This project is maintained by Indra Rudianto. If you have any question about
this project, you can contact him at <indrarudianto.official@gmail.com>.

## License

By contributing to the project, you agree that your contributions will be
licensed under its MIT license.
See [LICENSE](https://gitlab.com/bpptkg/komapy/blob/master/LICENSE) for details.
