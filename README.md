# blindify

This is a tool for instructors to anonymize assignments that may have student names in the file names.

# What is blindify?

Blind grading assessments or assignments helps to reduce implicit bias. Some learning management systems (LMS) have a "blind grade" feature, but this is essentially useless when the student appends their name to a file e.g., `A1_JaneDoe`. Telling students to not put their name in the assignment is a mixed bag - on one hand, it allows for easy blind grading. On the other, it could cause for mixups in assignments. Additionally, asking students to remove their names may incentivize cheating. 

*blindify* attempts to fix this issue by allowing instructors to download file/directory submissions from either their LMS or even GitHub classroom and anonymizes submissions locally. A file, called the anonymize-map, is a .csv of "identifier,name" pairings e.g., `123456789,JaneDoe`, using a random 64-bit value as the identifier, and the original file name as the name. After grading is complete, the files can be de-anonymized to prevent corruption and ambiguity.   

# How to Use blindify

... To write later.

# Version History

... To write later.