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
      

## Documentation

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
                              


From the command line the following arguments are required:



| flag | full flag name  | argument | description | required |
|---|---|---|---|---|
| -a  | --all_classes | None | Flag to denote the analysis should include all possible classes which fit the user's schedule | Yes (one of -a, -s, or -r)|
| -s  | --specific_class | None | Flag to denote the analysis will be based on a specific class (either the class itself or used to wilcard a certain subset of class e.g. CSC classes with course numbers greater than or equal to 400) | Yes (one of -a, -s, or -r)|
| -r  | --requirement | REQUIREMENT - reqirement number (Integer) | input for requirement number to find available classes for given the user's current schedule. Requirement numbers can be found on mypack > Planning & Enrollment > Undergraduate degree audit > Select your pertinent major/minor >  Details (for specific requirement and requirement number will be in top left corner "Requirement: <REQUIREMENT>"  | Yes (one of -a, -s, or -r)|
    

If the username and/or password is not specified by the user, they will be prompted for their Username (Unity ID) and password.

```
**Note**: The user's username and password are never stored or recorded in anyway but remain entirely local to the user's machine for security and privacy purposes
```
        
## Examples

```
./gradeGetter.exe -u username -p password -r 32749
```

Here, the user has requested an analysis of classes fulfilling the general chemistry requirement (Requirement #: 32749) which fits their current schedule (this includes classes in the user's shopping cart)

```
./gradeGetter.exe -u username -p password -ao -ng -m 3
```

In this case, the user has specified that all available classes should be analyzed (-a) and that online classes which are online (-o) and non-grade (-ng) (course section >= 500) as well as a minimum number of credit hours of 3 for the given course.

```
./gradeGetter.exe -s -cs CSC -cn 400 -w gt
```

These arguments pertain to a specific course (-s) CSC 400 and use a wilcard (-w gt) to get all CSC courses with course numbers >= 400.



