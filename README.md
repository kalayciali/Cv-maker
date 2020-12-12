#cv maker

Cv maker which generate cvs char by char with the 
help of python generators. It is almost finished on back side. It needs
some refactoring and frontend arrangements. It uses Django as a back end framework. It uses
Weasyprint for pdf rendering. Site needs frontend arrangements.

There is one to one relation between User and Profile models. Each Profile model
has many Experiences, Bars(skills), and other related models.
ProfileCv model is the through model between Profile and Cv.
İt has also newly created html as a string form with the required form fields filled.

Firstly, with createTemplate func., I find the loc data of each required field within html
by writing suitable regex for it. It works locally, than add Cv model with loc data to database.
Main func for generating new html from plain one is within cvs/views.py. It looks messy.
It needs refactoring but it works.

For future improvements, i need to add parallel programming to show cv images.

