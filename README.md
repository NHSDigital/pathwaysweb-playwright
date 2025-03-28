# Pathways Web Test Automation

This project is forked from the Playwright blueprint, which was created to allow for development teams to start quickly developing UI tests using [Playwright Python](https://playwright.dev/python/), providing the base framework and utilities to allow for initial focus on writing tests, rather than configuration of the framework itself. Playwright is the current mainstream UI testing tool for NHS England, as outlined on the [NHS England Tech Radar](https://radar.engineering.england.nhs.uk/).

> NOTE: This project is currently under initial development so isn't finalised, but should work if you want to experiment with Playwright Python.

## Table of Contents

- [Pathways Web Test Automation](#pathways-web-test-automation)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Configuration](#configuration)
  - [Getting Started](#getting-started)
  - [Utilities](#utilities)
  - [Contributing](#contributing)
  - [Licence](#licence)

## Setup

You can clone this whole repository using the code below:

```shell
git clone https://github.com/NHSDigital/pathwaysweb-playwright.git
```

### Prerequisites

To utilise the blueprint code, you will need to have the following installed:

- [Python](https://www.python.org/downloads/) 3.12 or greater

> NOTE: There are currently known issues with Python 3.13 and Playwright, so if you encounter issues running this project whilst using Python 3.13 it is recommended to downgrade to Python 3.12 in the interim.

Whilst not required to get started, you may also want to [configure a Python virtual environment for your project](https://docs.python.org/3/library/venv.html) before proceeding with
the configuration.  If you are using an IDE such as Visual Studio Code or PyCharm, you will normally be prompted to do this automatically.

### Configuration

To get started using Playwright and with the examples provided, use the following commands:

```shell
pip install -r requirements.txt
playwright install --with-deps
```

This will install all the necessary packages for executing Playwright tests, and install Playwright ready for use by the framework.  You can test the configuration
has worked by running our example tests, which can be done using the following command (this will run all tests with tracing reports turned on, and in headed mode
so you can see the browser execution):

```shell
pytest --tracing on --headed
```

Alternatively if you are using Visual Studio Code as your IDE, we have pre-configured this project to work with the
[Testing functionality](https://code.visualstudio.com/docs/editor/testing) so the example tests should be discovered automatically.

## Getting Started

> NOTE: This section is currently under development.

## Utilities

This blueprint also provides the following utility classes, that can be used to aid in testing:

|Utility|Description|
|-------|-----------|
|[Axe](./docs/utility-guides/Axe.md)|Accessibility scanning using axe-core.|
|[Date Time Utility](./docs/utility-guides/DateTimeUtility.md)|Basic functionality for managing date/times.|
|[NHSNumberTools](./docs/utility-guides/NHSNumberTools.md)|Basic tools for working with NHS numbers.|
|[User Tools](./docs/utility-guides/UserTools.md)|Basic user management tool.|

## Contributing

Further guidance on contributing to this project can be found in our [contribution](./CONTRIBUTING.md) page.

## Licence

Unless stated otherwise, the codebase is released under the [MIT License](LICENCE.md). This covers both the codebase and any sample code in the documentation.

Any HTML or Markdown documentation is [© Crown Copyright](https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/) and available under the terms of the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
