-   [Overview](#overview)
-   [Install Anaconda](#install-anaconda)
    -   [Ubuntu/WSL](#ubuntuwsl)
    -   [macOS](#macos)
    -   [Update conda](#update-conda)
-   [Clone page-level-features repo](#clone-page-level-features-repo)
-   [Create Anaconda environment](#create-anaconda-environment)
    -   [Aside on sharing environments](#aside-on-sharing-environments)
    -   [Aside on TOCs](#aside-on-tocs)
-   [Get tokens for HathiTrust Data API](#get-tokens-for-hathitrust-data-api)
-   [Sync Jupyter Notebook kernel with environment](#sync-jupyter-notebook-kernel-with-environment)
-   [Open Notebook](#open-notebook)
-   [Recommended reading](#recommended-reading)

Overview
========

This repository contains a Jupyter Notebook and other resources for a workshop on [HathiTrust](https://www.hathitrust.org/) page-level features. The first presentation of the workshop will be at the [Yale DH Lab](dhlab.yale.edu) on March 27, 2018. To get the Notebook running, you will need to set up your environment following the steps below.

The instructions assume that you have a Unix-style terminal, possess admin privileges on your computer (i.e. can use `sudo`), and have some familiarity with `git`. They have been tested on Ubuntu Linux using the [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) and on macOS.

Install Anaconda
================

Anaconda is the best platform for doing data science in Python. As of March 2018, 5.1.0 is the most current release for 64-bit Python3. Unless explicitly indicated (as in this section), shell commands should work fine for either Ubuntu/WSL or Mac.

Ubuntu/WSL
----------

    cd /tmp
    sudo apt install wget
    wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
    bash Anaconda3-5.1.0-Linux-x86_64.sh
    rm Anaconda3-5.1.0-Linux-x86_64.sh
    conda --version
    sudo apt update
    sudo apt upgrade

Running the bash script will take some time, but it's worth it since most of the math and visualization packages we need will be downloaded in this full version of Anaconda. The script is interactive so press `ENTER` to agree and scroll down with the `j` key to reach the end of the license. Type `yes` and then press `ENTER` (or just `ENTER`) as requested for everything except installing Microsoft Visual Studio. That's not necessary so you can type `no`. Once installation has successfully completed we can delete the installer, check that `conda` exists, and update Ubuntu.

macOS
-----

1.  Go to https://www.anaconda.com/download/
2.  Click the green button for Python 3.6 64-Bit graphical installer
3.  Run the installer, agree to the license, and accept the defaults
4.  Continue past (decline) the option to install Microsoft VSCode
5.  Open up or return to the terminal and check that `conda` has installed

<!-- -->

    source ~/.bash_profile
    conda --version

If `git` doesn't work on your Mac, you may need to run

    xcode-select --install

and agree to the license terms. This fixes the "invalid active developer path" error.

Update conda
------------

This step is the same for both operating systems. Again, the command-line prompt will ask you to type `y` or `yes` and then `ENTER` to agree to any downloads.

    cd ~
    conda update conda
    conda update --all

Clone page-level-features repo
==============================

This step assumes that you will be making an `https` and not `ssh` connection to GitHub. Feel free to clone from a location of your choice. For simplicity I'm choosing the home folder, with its `~` shortcut.

    cd ~
    git clone https://github.com/StephenKrewson/page-level-features.git
    cd page-level-features

For the rest of the instructions, We will be staying put in the `page-level-features` folder. If you're on Mac and received error messages when trying to run `git clone`, check out the suggestion about (re)installing `xcode-select` above.

Create Anaconda environment
===========================

Now we can create a new environment following the recipe in `plfeats2.yaml`. In our case, the base name of the file is simply the name of the environment (though it can be named anything you want). Run these commands:

    conda env create --file plfeats2.yaml
    conda env list
    conda activate plfeats2
    python --version
    conda deactivate
    python --version
    conda activate plfeats2

Notice that the version of Python changes depending on whether the environment is activated or not. The wrapper that we are using to the HathiTrust data API uses libraries that are only compatible with Python2.7. Hence the "2" in `plfeats2`. Needing access to an older version of Python is less than ideal, but it is an object lesson in why using `conda` to manage Python development is so helpful. We don't need to worry about Python versions or third-party libraries that might become incompatible when updated. We can simply get to work exploring the data!

Remember to `conda activate` the relevant environment before opening the notebook. You'll know it's activated when your shell prompt is prepended by `(plfeats2)`.

Aside on sharing environments
-----------------------------

The command below is included for reference only, in case you ever want to share an environment with other users. Per the `conda env` [documentation](https://conda.io/docs/commands/env/conda-env-export.html), you can export an Anaconda environment with

    conda env export --no-builds --file environment.yml

The `--no_builds` flag is necessary for sharing across platfoms since the build IDs are going to be different depending on the target operating system. However, there are still cross-platform issues. Linux and macOS use different compilers, so `libgcc-ng` will not be resolved on macOS Anaconda. The solution is to delete every package except those that are outside of the standard Anaconda distribution. Since the standard distribution includes Jupyter and pandoc and virtually all the scientific packages, this simplifies things greatly.

A final headache is dealing with `pip` installs that build directly from version control repositories. The solution is to use the `-e` flag and include the full URL: `-e git+https://github.com/iainwatts/hathidata/#egg=hathidata`. See the `pip` [documentation](https://pip.readthedocs.io/en/1.1/requirements.html#requirements-file-format). After these two steps, the `plfeats.yml` build file is compatible with macOS.

Three guiding principles: whenever possible,

1.  Install with `conda` rather than `pip`
2.  Use packages included in standard Anaconda
3.  Document everything non-standard in an `environment.yml` requirements file

Aside on TOCs
-------------

Long READMEs, such as this one, and large notebooks are made more comprehensible by tables of contents. For a markdown README:

-   Make edits and updates in the `readme-no-toc.md` file; save file
-   Run `./generate-toc.sh` which generates a table of contents and saves the output as `README.md` which is the default landing page for the repo
-   Commit changes to both files and push to GitHub--the repo will now have a TOC at the top of the README

You can add a table of contents to Jupyter Notebook by setting up the extensions configurator ([documentation here](https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator)). Activate the environment first.

    # need to do this inside the environment
    conda activate plfeats2

    # get the extensions and the widget package
    conda install --channel conda-forge jupyter_contrib_nbextensions
    conda install --channel conda-forge jupyter_nbextensions_configurator

    # need to enable widgets and the config menu
    jupyter nbextensions_configurator enable --user

    # now start up Notebook!
    jupyter notebook

Once you get to the `localhost:8888/tree` page, you can click on the Nbextensions tab and enable table of contents. It's necessary to update `conda` because the extensions server is bundled with an outdated version of `conda` by the conda-forge channel.

Get tokens for HathiTrust Data API
==================================

Iain Watt's [very helpful library](https://github.com/iainwatts/hathidata) lets us access the HathiTrust data API. However, we need to first acquire authentication tokens. The notebook expects us to store these tokens within a Python file named `config.py`. This file is very simple and contains one dictionary object:

``` python
ht_keys = {
    'access_key': 'YOUR_ACCESS_KEY_STRING',
    'secret_key': 'YOUR_SECRET_KEY_STRING'
}
```

For security reasons, I can't track my `config.py` with `git`. So you will need to create the file yourself. In a plain text editor of your choice, open up a new file and save it as `config.py` within `page-level-features`. Copy-and-paste the above code snippet into the file. We will now replace the dictionary values with your actual access and secret keys.

Head over to

https://babel.hathitrust.org/cgi/kgs/request

and fill out your name, organization, and email to request access keys. You should receive an email response within a minute or so. Click the link, which will take you to a one-time page with both keys displayed. Careful! The link only works once so take a screenshot or picture or save the keys in some other way in case you have to fix a typo or use the keys at a later date. Once the keys have been pasted in the correct place in `config.py` (inside quotes to mark them as a string datatype), save and close the file.

Why go through all this trouble instead of pasting the keys directly into the notebook? Well, we need these keys to run the downloader script that can get us full-page images from HathiTrust. It's convenient to be able to import the keys from one centralized place. A line in our `.gitignore` file already ensures that `git` will not track the file.

Sync Jupyter Notebook kernel with environment
=============================================

By default, Jupyter Notebook will be running with an IPython 3 kernel. This is what allows it to execute Python code interactively. However, our `plfeats2` environment and all the packages in it are configured for Python 2.7. The [IPython documentation](http://ipython.readthedocs.io/en/stable/install/kernel_install.html#kernels-for-different-environments) details how to use the `ipykernel` tool to add a custom kernel to the notebook:

    python -m ipykernel install --user --name plfeats2 --display-name "Python (plfeats2)"

This installs a new kernel matching the specs of the environment named `plfeats2`. We give it a consistent name, `Python (plfeats2)` so that we can easily identify it in the Jupyter Notebook menu. Within Notebook, you can switch kernels by going to the `Kernel` tab, selecting `Change kernel` and choosing `Python (plfeats2)`.

Open Notebook
=============

At last! We are ready to open the notebook. Because WSL can't access the default browser in Windows, my process is slightly wonky. On macOS, just run

    jupyter notebook demo.ipynb

This should open a tab with the notebook running in the default browser.

For WSL, run `jupyter notebook` and then copy the URL as directed. You can copy by selecting with the cursor and then pressing `ENTER`. Your terminal should look like this, with the URL you want at the bottom:

![Jupyter Notebook in Bash](img/jupyter-bash.png)

Paste the URL in your browser and navigate to it. Leave the terminal running but feel free to minimize it. In the browser you should see something like this:

![Jupyter Notebook homepage](img/jupyter-home.png)

Click on `demo.ipynb` which will open in a new tab. Make sure to switch over to the correct kernel, as outlined in the previous section. That's it! From now on, any instructions will be contained in the notebook itself.

Recommended reading
===================

-   https://www.hathitrust.org/documents/hathitrust-data-api-v2\_20150526.pdf
-   https://programminghistorian.org/lessons/text-mining-with-extracted-features
-   https://www.youtube.com/watch?v=N56I0TRnRX0
