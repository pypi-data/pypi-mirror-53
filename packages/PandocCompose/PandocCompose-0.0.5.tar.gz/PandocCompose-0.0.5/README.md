# Usage

`pandoc-compose` lets you manage your documentation base by automating
conversion of mutiple markdown or other formatted text files using Pandoc.

Pandoc should be already installed on you computer.

## How does it work?

Just like `docker-compose`, when executed, `pandoc-compose` will search for a
`pandoc-compose.yml` file either in current working directory or in a sepcified
destination (see [Synopsis](https://git.feneas.org/christophehenry/pandoc-compose/blob/master/DOCUMENTATION.md#synopsis)) and extract configuration from it to
automate the conversion of you document base from any input format to any output
format supported by Pandoc.

See [the documentation](https://git.feneas.org/christophehenry/pandoc-compose/blob/master/DOCUMENTATION.md) for more informations on how to use it.

# TODO

* auto-install pandoc 
* add or remove [extensions](https://pandoc.org/MANUAL.html#extensions)
