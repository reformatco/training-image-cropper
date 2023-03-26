# Image cropper

Simple image cropper that allows you to specify a directory and then crop all images inside to the required size. Created for making dataset images for training Stable Diffusion.

Any images smaller than the crop size will be deleted.

## Built With

- Python - The programming language used
- OpenCV - The computer vision library used

## Authors

- Ben Palmer

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

- Hat tip to ChatGPT for making all this

## Instructions

Install virtualenv using pip on the new computer (if it's not already installed):
```
pip install virtualenv
```
Navigate to your project directory on the new computer and create a new virtual environment:
```
virtualenv venv
```
Activate the virtual environment:
```
source venv/bin/activate
```
Install your project dependencies using pip:
```
pip install -r requirements.txt
```
When you're done working on your project, you can deactivate the virtual environment:
```
deactivate
```
This will deactivate the virtual environment and return you to the global Python environment.