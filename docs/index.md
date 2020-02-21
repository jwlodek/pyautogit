# pyautogit

A command line interface for working with git written in python with the help of [py_cui](https://github.com/jwlodek/py_cui).

### Introduction

The aim of `pyautogit` is to introduce a simple command line interface for managing multiple git repositories from one workspace.
Install `pyautogit` with `pip`:
```
pip install pyautogit
```
and start it from a command line either inside a git repository, or in any non-git repo. If you open a git repo, you will
see a repository control screen, while otherwise a workspace will be created, and any git repositories found as subdirectories
will be listed for control.

From here, you can select a repository, or clone and create new ones. I hope `pyautogit` proves as useful for you as it has for
me!

### Demo

Below is a quick demo of using `pyautogit to do some common git actions.

<p align="center">
    <img src="assets/pyautogit-demo.gif">
</p>
