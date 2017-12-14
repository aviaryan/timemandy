# Installation instructions

First create virtualenv in conda and activate it.

```
conda create -n timemanager python=3.5
```

Check if the env was created.

```
conda info --envs
```

Then activate the virtualenv.

```sh
source activate timemanager
# source deactivate
```

PS - To delete the environment, run

```sh
conda remove --name timemanager --all
```

-------

The next step is to install requirements. After making sure that you have activated the virtualenv, run the following command.

```sh
pip install -r requirements.txt
```
