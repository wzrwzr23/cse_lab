# Banker's Algorithm Lab

1. Implement your answer inside `banker.py`, there are TWO tasks; Task 1 and Task 2
2. **DO NOT PRINT ANYTHING ELSE** to the console. All debug messages must be commented out. 
3. Test your implementation using `banker_test.py`

There are 6 test cases in total inside `test_files/`, each testing different scenarios.
1. q0: Will PASS by default, simply setup all matrices only
2. q1: Will PASS by default, P0 request `i` rejected because > `NEED[i]`
3. q2: Will PASS by default, simply perform granted safe request
4. q3-q5 will FAIL by default, there are many unsafe requests. It will PASS if you implement `check_safe` algorithm properly inside `Banker.py` and use it in `request_resource` algorithm.

In order for `banker_test.py` to print PASS, you **MUST NOT PRINT ANYTHING ELSE** to the console, we simply perform string matching. 

**DO NOT CHANGE ANY OTHER FILE** besides the dedicated places in `banker.py`. 
