Py3DFreeHandUS
=======

**A Python library for 3D free-hand ultra-sound measurements**.

Folder *Py3DFreeHandUS* contains source code and doc.

HTML doc is in *doc/index.html* or *sphinx/_build/html/index.html*

After installing Anaconda/Miniconda (64-bit), do the following to create a
Conda sandboxed environment and install Py3DFreeHandUS:

*Windows*:

- open a Windows console and type the following:

```
conda create -n 3dfus python=2.7 libpython msvc_runtime mingw spyder=3.1.4 pyqt vtk=6.3.0 --yes
activate 3dfus
pip install Py3DFreeHandUS --no-cache-dir
```

If the first command complains about the conda channels (conda version >= 4.6), replace it with:

```
conda create -n 3dfus python=2.7 libpython msvc_runtime mingw spyder=3.1.4 pyqt vtk=6.3.0 --yes --channel anaconda
```

To run Spyder for the sandboxed environment, open a window console and type
the following content:

```
activate 3dfus
spyder
```

and double-click on it.

To configure Spyder, in *Windows*:

- go to *Run*, in *Console*, select *Execute in current console*.
- go to *Tools, Preferences, IPython console, Graphics* and uncheck *Activate support*.
- go to Python installation folder, navigate to */envs/3dfus/Lib/site-packages/matplotlib/mpl-data/* and then open the file *matplotlibrc* with any text editor.
- around line 41, replace **backend      : TkAgg** with **backend      : Qt4Agg**. This should make IPython behave like the old classical Python console, in terms of charts.

**NOTE**: for the good behaviour of matplotlib charts, it is advised to close the IPython console after the script has terminated. A new fresh one will be automatically created.

Data files and example scripts are tracked via [Git LFS](https://docs.gitlab.com/ee/workflow/lfs/manage_large_binaries_with_git_lfs.html). To get the example data:

*Windows*:

- download and install [git](https://git-scm.com/). During installation, you can leave the default checkboxes as they are. Make sure that Git LFS is in the list of components to install.
- create a profile on [GitLab](https://gitlab.com/), if you don't have it already.
- create an empty folder where you want data to be and inside right-click on **Git Bash here**. To download the sample data for the first time, type:

  ```
  git init
  git remote add origin https://gitlab.com/u0078867/py3dfreehandus.git
  git pull origin master
  pause
  ```

  When pulling, you may be requested username and password of your GitHub account. This operation will download both raw library code and samples data; the sample data is under to folder *samples*.

-  Every time you are notified for sample data updates, double-click on *download_sample_data.bat* (created when pulling) to update your local copy.



**IMPORTANT NOTE**: this library is under active development.
We do our best to try to maintain compatibility with previous versions.
