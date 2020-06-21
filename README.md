# Hubstaff Monitor

A small etude: Tool for reporting time tracked in Hubstaff.

## Prerequisites

Installed Docker.

## Configuring and running

1) Build the app image:

    ```
    docker build -t hubstaff-monitor .
    ```

2) Run tests:

    ```
    docker run -it --rm -v $(pwd):/app hubstaff-monitor pytest
    ```

3) Edit `config.ini`.

    Provide `Email` and `Password`.

    Optionally provide an `AuthToken`. If present, the token will take precedence over email/password authentication. This is meant to enable frequent running of the program, since Hubstaff has a rate limit of 10 authentication calls per hour.

4) Run the app:

    `cd` into the project directory.

    ```
    docker run -it --rm -v $(pwd):/app -e check_date="<YYYY-MM-DD>" hubstaff-monitor
    ```

## Implementation notes

* This project should have more tests. However, since it is intended as a demo, I only wrote a few to save time. In a production scenario, I would aim at full coverage.
* I use Docker because I believe that it is nowadays the cleanest way to package even simple projects, such as not to pollute the runtime environment with arbitrary installations. Depending on requirements, it could make sense to e.g. resign from Docker and minimize overhead.
* I use `print` statements instead of logging because of the small scope and clear context of the application. Depending on the requirements, this could be easily refactored.
* I use simple module-level functions instead of strict OOP approach whenever the problem is simple enough. However, I am also flexible and open for discussion about style.
* Hubstaff docs mention that some calls return paginated responses. I have not implemented pagination and I have not tested the program with large volumes of data. In a production setting this would definitely be a TODO.
* Currently `requirements.txt` contain both production- and testing-intended libs. In more involved scenarios this should be separated, e.g. using directives in `Dockerfile`.
