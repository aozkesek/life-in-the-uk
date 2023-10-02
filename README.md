# Life In The UK Test

Test your knowledge of the life in the UK exam and prepare yourself to pass the 
test.

## Requirements

Application and libraries fo running the exam are; 

1. **Python**: must have
2. **enscript**: optional, print only
3. **ps2pdf**: optional, print only
4. **textdistance**: optional, dist only

## Install

Copy **lifeintheuk.py** and **life-in-the-uk.qa.txt** files under same folder.

Depend on the Linux distro you are using, install *enscript* and *ps2pdf* to 
use print feature for create a PDF file of exams, install **python3-textdistance**
for detecting duplicates -or similiars-.

## Usage

Open a terminal, change the current folder to where script is, then run this; 

**python lifeintheuk.py [print|dump|dist]**

Command line arguments -use only one at a time- 

**print**: creates a **lituk-test.pdf** PDF file within full exams.

**dump**: shows list of the questions in ordered.

**dist**: shows similiar questions to avoid dublicates

**NO-ARG-**: starts exam(s) 
 
