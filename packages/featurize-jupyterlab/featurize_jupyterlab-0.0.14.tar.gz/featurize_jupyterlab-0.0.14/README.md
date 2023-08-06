# featurize-jupyterlab

A JupyterLab extension.

## Prerequisites

* Python >= 3.7
* Node.js >= 8

It's recommended to use [nvm](https://github.com/nvm-sh/nvm) to manage your node and npm versions.

## Installation

```bash
jupyter labextension install featurize-jupyterlab
```

## Development

### For the first time

1. Clone this repo
```
git clone git@github.com:louis-she/featurize-jupyterlab.git
```

2. Create virtual environment
```
cd featurize-jupyterlab
python -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies
```
pip3 install -r requirements.txt
```

4. Install frontend dependencies
```
npm install
```

5. Install Typescript
```
npm install -g typescript
```

6. Add jupyter extension
```
pip3 install -e .
./.venv/bin/jupyter serverextension enable --py featurize_jupyterlab
./.venv/bin/jupyter labextension install . --no-build
```

7. Add featurize extension
```
pip3 install featurize-package
./.venv/bin/featurize_server package:add ftpkg.demo
```

8. Start development file watching
```
npm run dev
```

### For the regular time

1. source .venv/bin/activate
2. npm run dev
