# GradeGetter
A CLI tool to allow analyze grade distribution big data in computing the most efficient course schedule pursuant to a student's schedule


## Getting Started

1. Clone the repo with the following command and change to its directory:

    ```
    git clone https://github.com/benniferLopez/GradeGetter.git
    cd GradeGetter/
    ```
2. Next, there are two options for running the application
  a.) Firstly, the script can be run directly using python.
  
      If running the script must first install the required modules
      
      ```
      pip install -r requirements.txt
      ```
      
      After successfully installing the requirements.txt, the command line options may be displayed by running:

      ```
      python ./gradeGetter -h
      ```
      
  b.) Optionally, if using a Windows, the bundled executable can be used instead of running the source code directly.
  
      ./gradeGetter.exe -h
      
      
  Regardless of the method selected, upon submitting the -h flag, the following documentation will be displayed:
  
      usage: gradeGetter.py [-h] [-u USERNAME] [-p PASSWORD] [-r REQUIREMENT] [-a]
                            [-o] [-ng] [-m MIN_UNITS] [-s] [-cs COURSE_SUBJECT]
                            [-cn COURSE_NUMBER] [-w {lt,gt}]

      optional arguments:
        -h, --help            show this help message and exit
        -u USERNAME, --username USERNAME
                              User name (unity ID)
        -p PASSWORD, --password PASSWORD
                              Password
        -r REQUIREMENT, --requirement REQUIREMENT
                              Degree audit requirement number
        -a, --all_classes     flag to get all classes for ranking
        -o, --online_only     flag to get only online classes for ranking
        -ng, --non_grad       flag to get only non graduate-level classes for
                              ranking
        -m MIN_UNITS, --min_units MIN_UNITS
                              flag to get only online classes for ranking
        -s, --specific_class  flag to denote specific class to compile historical
                              statistics
        -cs COURSE_SUBJECT, --course_subject COURSE_SUBJECT
                              subject of a specific course (string)
        -cn COURSE_NUMBER, --course_number COURSE_NUMBER
                              subject of a specific course (string)
        -w {lt,gt}, --wildcard {lt,gt}
                              wild card search with specific course information
                              
## Documentation

From the command line the following arguments are required:

    * at least one of the following:
        * -a --all_classes - Flag to denote the analysis should include all possible classes which fit the user's schedule
        * -s --spec_class - Flag to denote the analysis will be based on a specific class (either the class itself or used to wilcard a certain subset of class e.g. CSC classes with course numbers greater than or equal to 400)
        * -r --requirement REQUIREMENT - input for requirement number to find available classes for given the user's current schedule. Requirement numbers can be found on mypack > pal
        
       


## Examples
