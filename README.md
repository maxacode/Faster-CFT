# Visualize Cloud-formation Stacks similar to CDK Deploy.

## Steps: 
1. AWS CLI must be installed. https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
2. Change input file name variable (cftName line 4) in "AutomateCFT.py".
3. Run "AutomateCFT.py" from the same directory as the Cloudformation template is in. 
4. Follow prompts and watch the colorful outputs come in. 


## Tip: 
1. Change line 189 action = input() to action = '' for no interaction deployment. 




# Console Output:
![Alt text](ConsoleOutput.png?raw=true "ConsoleOutput")

---
---

# Sample Output:
![Alt text](Faster-CFT-Sample-Output.png?raw=true "SampleCodeOutput")

---
---

# Bandit Report Output: 
![Alt text](Bandit-Output.png?raw=true "Bandit")