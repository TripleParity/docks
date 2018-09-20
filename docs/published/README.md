# Published Documentation

Documentation related to the COS 301 course. 

These documents will be compiled by Travis and published to [docs-bin](https://github.com/TripleParity/docs-bin)

## Requirements
### Ubuntu
See `.travis.yml`

### Fedora
- Docker
- `sudo dnf install texlive-todonotes texlive-newverbs`

## Building
Images need to be build from the UMLet files before generating the PDF files.

```
./scripts/build.sh $(pwd) build
```