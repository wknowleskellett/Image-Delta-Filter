# Image-Delta-Filter

This project uses the Pillow library to run this filter I thought of on images. I'm pretty sure it's been done before.

## Setup

In the main directory, run `pipenv install`.

## Usage

In the `pipenv` environment (open with `pipenv shell` or run commands individually with `pipenv run <command>`), run `python im_diff.py`.

For now, this opens a file chooser in your native system. Select an image.

When the program finishes, it will display the filtered image and ask if you'd like to save it for later.

Enter `Y` or `n` to either select a save path or exit without saving.

## Why?

I thought it would help with this project I was working on. It didn't. I'm left with a cool filter that I'll probably still use for photo editing projects.

Edge detection is cool.

## Future work

Really easy: rewrite this as optionally a CLI that takes an input/output file name as command line arguments.
Maybe somewhat harder: when called without arguments, open a GUI with tuning parameters and a live updating image. 
