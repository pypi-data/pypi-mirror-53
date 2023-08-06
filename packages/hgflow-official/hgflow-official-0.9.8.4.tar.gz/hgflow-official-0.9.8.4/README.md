# README #

Hgflow is an extension of the [Mercurial distributed version control system](https://www.mercurial-scm.org/) to provide users a set of high level commands for creating, merging, and deleting branches, which includes the support for the [Driessen's branching model](http://nvie.com/posts/a-successful-git-branching-model/). We also generalized the original Driessen's model by allowing user to use any branch as the base to start a (sub-)feature branch (and more).

## Get started ##

#### Download ####

* The hgflow extension contains a single Python file: `hgflow.py`.
* The latest release is [`v0.9.8.4`](https://hg.sr.ht/~wu/hgflow/tags).

* Developers can clone the repository with `hg clone ssh://hg@hg.sr.ht/~wu/hgflow`.

#### Install and configure ####

1. Untar the downloaded tar ball, and move the hgflow.py file to the directory where you place your Mercurial plugins.
2. Edit your `$HOME/.hgrc` file to add the following lines:

```
[extensions]
flow = path/to/hgflow.py
mq =

[flow]
autoshelve = yes
```

#### Help and tutorials ####

1. Use `hg flow -h` to see a synopsis of the help message.
2. Use `hg flow help @<topic>` to see detailed help message on a particular topic, e.g., `hg flow help @help`, `hg flow help @start`.
3. Other resources:

    * [A nice introductory tutorial by Ralph Lange](http://epics-pvdata.sourceforge.net/hgflow/using_hgflow_20130828.html)

## Contributing ##

#### Coding style ####

* Please pay attention to the coding style in the hgflow.py file.
* Consistency of the coding style will be strictly and relentlessly maintained here.

#### Contributing enhancements and/or fixes ####

* To file an issue, use [this page](https://todo.sr.ht/~wu/hg-flow).
* If you have a fix, please post it [here](https://lists.sr.ht/~wu/hgflow).
* Ensure that your change does not break any tests.
* `hgflow` has entered the maintenance mode: For last several years, we only updated hgflow to catch up Mercurial's APIs changes. There is no requests for major new features for hgflow. If you have a bugfix, please put it into the latest hotfix branch.

#### Writing and running tests ####

* We use Mercurial's testing framework. For writing new tests, refer to [this document](https://www.mercurial-scm.org/wiki/WritingTests).
* All tests should be put to the tests/ directory.
* To run tests, `cd` to the root dir of the hgflow repository, and then `make <test-name>` to run the specified test.

## License ##

* [GPL v2](http://www.gnu.org/licenses/gpl-2.0.html)
