# ncapi-client-python

This repository contains a python client for the NCAPI, and a
command-line utility `ncs` that allows using this client.

All the methods for non-interactive tasks (e.g. dataset management,
training, batch prediciton) are contained in the `ncapi_client.Client`
class, and all the methods for the interactive ones are contained in
the `ncapi_client.SessionClient`.

## Installation

You can install the client by running:

```bash
pip install .
```

For development purposes, you probably want to install a "editable" version,
which creates symlinks instead of actually copying stuff in the directories:
```bash
pip install -e .
```

## General description

There are several sets of commands and utils for managing your data
and models, which are exposed in all of the clients. Those are
described in more detail below.  For cli interface, `ncs`, you can see
the overall list of in the help doc:

```bash
Commands:
  auth      Authenticate with your username and password.
  dataset   Dataset management.
  evaluate  Batch evaluation.
  model     Model management.
  predict   Batch prediction.
  session   Interactive sessions management.
  train     Training jobs management.
```


## Authentication
In order to connect to the API you should first authenticate with your
username and password, which will save your settings in `~/.config/ncs`.
The easiest way to do this is to run `ncs auth`:

```bash
ncs auth
Please enter your username: ncadmin
Please enter your password:
Please enter API url [http://0.0.0.0:5000]:
```

You can then use the python client and ncs, which will load and update
your settings when necessary.

For python, you can also create an instance of `ncapi_client.Client` and pass
it credentials and API url (optional if you have custom installation):
```python
NCAPI_URL = 'https://cloud.neuralconcept.com:5000'
NCAPI_USERNAME = 'ncuser'
NCAPI_PASSWORD = 'ncpassword'
c = Client(NCAPI_URL, NCAPI_USERNAME, NCAPI_PASSWORD)
```

## Managing datasets

You can add (upload) datasets in one of the supported formats (formats
are described in the corresponding docs), and then use your datasets for training and testing

```python
# adding a dataset
d = c.dataset_add(name="name-of-the-dataset", path="/path/to/the/data")

# getting a dataset
d = c.dataset_get("name-of-some-dataset")

# deleting the dataset
c.dataset_delete(d.uuid)

# listing the datasets
for d in c.datasets:
  print(d.name, d.uuid, d.status)

# listing the files in the dataset
f = d.dataset_files_list()

# getting a sample from the dataset
s = d.dataset_samples_get(d.uuid, "<sample-id>")
```

For CLI `ncs dataset COMMAND`
```bash
  add     Add a new NAME dataset located at local PATH.
  delete  Deletes the dataset.
  sam
  files   Dataset file management.
  get     Get verbose info about the dataset.
  list    List all the datasets
```

## Managing models

For models, you can choose from a rich set of pre-defined model
templates, which you can easily customise by simply editing a
yaml-based config file. A typical config would look as follows:

```yaml
# training parameters
train:
  batch_size: 1
  tag: alpha
  num_steps: 1500000
  optimizer:
    init_lr: 1.0e-4
    min_lr: 1.0e-6
    decay_rate: 0.7
    decay_every: 30000
  loss:
    loss_fn_name: null

# model-specific parameters
model:
  name: name-of-your-model
  # this is one of the standard model types
  class_name: ncs.models.NormalizedRegressor
  characteristic_len: 0.4
  num_blocks: 8
  block_width: 64
```

There are two main blocks: `train` - which contains customizable
training parameters such as the step size schedule, `model` - which
contains the definition of the model, i.e. it's name, the class name
(type of the model), and model-specific settings, such as number of
blocks or number of parameters per block (those will really depend on
a particular model type).

For python:
```python
# listing available models
for m in c.models:
  print(m.uuid, m.name)

# adding a model
m = c.model_add('/path-to-your-model-config.yml'')

# deleting a model
c.model_delete(m.uuid)

# getting verbose info about the model
print(c.model_get(m.uuid))
```

For CLI `ncs model COMMAND`:
```bash
Commands:
  add     Add a model with yaml config at PATH.
  delete  Delete a model by UUID.
  get     Get verbose info about the model.
  list    List available models.
```


## Managing training jobs

With NCAPI you can run large-scale training jobs on a cluster (cloud
based or custom), without a need to worry about managing computational
resources: our backend does it automatically.

For python:
```python
# list the trainings
for t in sorted(c.trainings, key=lambda v: v.uuid):
    print(t.uuid, t.status)

# stop one of the trainings
c.training_stop(c.trainings[0].uuid)

# restart one of the previously stopped trainings
c.training_restart(c.trainings[0].uuid)

# submit a new training
job = c.training_submit(c.models[0].uuid, c.datasets[0].uuid)

# you can also provide additional user config for the training
# which overrides the model config, e.g. if you want to train
# with different training step size schedule or try different loss
# function
job = c.training_submit(model, dataset, "/path-to-custom-config"")

```

For CLI:
```bash
Commands:
  delete   Delete a training.
  get      Get verbose information about a training.
  list     List available trainings.
  restart  Restart a training.
  stop     Stop a training.
  submit   Submit a training to the queue.
```

## Managing prediction jobs

TODO: finish the python docs

For CLI, run `ncs predict COMMAND`:
```bash
Commands:
  delete  Delete a prediction.
  get     Get results of the prediction with UUID and save them in DST.
  stop    Stop a prediction job.
  submit  Submit a prediction job for a given MODEL and DATASET.
```

## Managing evaluation jobs

TODO: finish the python docs

For CLI, run `ncs evaluate COMMAND`:
```bash
Commands:
  delete   Delete an evaluation job.
  get      Get summary metrics of the evaluation.
  restart  Restart an evaluation job.
  stop     Stop an evaluation job.
  submit   Submit an evaluation job for a given MODEL and DATASET.
```


## Managing interactive sessions

In python:
``` python
# list running sessions
for s in c.sessions:
  print(s)

session = c.session_start(model.id, dataset.id, sample.id)
session = c.session_get(session.id)
print("waiting while the session starts...")
while session.status != "RUNNING":
    session = c.session_get(session.id)
    time.sleep(1.0)
print("it has started!")

# start a session client and interactively play with your model
sc = SessionClient(session, client=c)

# get the current mesh (if supported by the model)
verts, faces = sc.mesh

# get the predictions (if supported by the model)
preds = kc.predict(input_scalars=dict(angle=0.8, speed=0.5))

# do some post-processing on field values
fields = np.clip(preds['fields'], 0, 10)

# choosing some random control points and applying a random deformation
control_points = verts[np.random.choice(verts.shape[0], size=2)]
cp_deformations = np.random.normal(scale=0.1, size=control_points.shape)

sc.apply_deformation(
     control_points=control_points,
     cp_deformations=cp_deformations,
)

# get updated mesh and predictions
verts, faces = sc.mesh
preds = sc.predict(input_scalars=dict(angle=0.8, speed=0.5))
```

In CLI, you can run some of the high-level commands via `ncs session COMMAND`:
```bash
Commands:
  delete  Delete an existing session.
  list    List of interactive sessions.
  start   Start an interactive session with a given model and dataset
```

# Documentation
To update the html docs, you will need sphinx >= 2.0. You can then go in ncapi-python-client root directory and run
```
sphinx-build -b html docs/ docs/_build/html/
```
Corresponding docs will be created in the docs/_build/html folder.
If you added new modules, you might want to create new *.rst files in the docs/ folder for these modules.
