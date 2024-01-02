# Action example

```
$ python action.py
user_proxy (to assistant):


        6人のユーザーが3つのりんごを購入しました。
        3人のユーザーが2つのりんごを購入しました。
        2人のユーザーが1つのりんごを購入しました。
        1人のユーザーが0個のりんごを購入しました。
        10人のユーザーは何個のりんごを購入しましたか？
        

--------------------------------------------------------------------------------
assistant (to user_proxy):

***** Suggested function Call: ask_constructor *****
Arguments: 
{"message":"Please generate a math expression to represent the total number of apples purchased by 10 users, given that 6 users bought 3 apples each, 3 users bought 2 apples each, 2 users bought 1 apple each, and 1 user bought 0 apples."}
****************************************************

--------------------------------------------------------------------------------

>>>>>>>> USING AUTO REPLY...

>>>>>>>> EXECUTING FUNCTION ask_constructor...
user_proxy (to assistant):

***** Response from calling function "ask_constructor" *****
6 users bought 3 apples each:
3 + 3 + 3 + 3 + 3 + 3

3 users bought 2 apples each:
+ 2 + 2 + 2

2 users bought 1 apple each:
+ 1 + 1

1 user bought 0 apples:
+ 0

Complete math expression without evaluating:
(3 + 3 + 3 + 3 + 3 + 3) + (2 + 2 + 2) + (1 + 1) + 0
************************************************************

--------------------------------------------------------------------------------
assistant (to user_proxy):

***** Suggested function Call: calc_sum *****
Arguments: 
{"numbers":[3,3,3,3,3,3,2,2,2,1,1,0]}
*********************************************

--------------------------------------------------------------------------------

>>>>>>>> USING AUTO REPLY...

>>>>>>>> EXECUTING FUNCTION calc_sum...
user_proxy (to assistant):

***** Response from calling function "calc_sum" *****
26
*****************************************************

--------------------------------------------------------------------------------
assistant (to user_proxy):

The 10 users purchased a total of 26 apples.
```
