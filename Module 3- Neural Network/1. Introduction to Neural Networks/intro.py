import random

# Define the input data
inputs1=[9,1,8]
inputs2=[-5,0,-3]

# Initialize weights and bias with random values between -1 and 1
weights = [random.uniform(-1,1) for _ in range(3)]
bias = random.uniform(-1,1)

# Calculate the weighted sum of inputs
weighted_sum1=sum([inputs1[i]*weights[i] for i in range(len(inputs1))])
weighted_sum2=sum([inputs2[i]*weights[i] for i in range(len(inputs2))])

# Apply the activation function (Step function in this case)
if weighted_sum1>bias:
    output1=1
else:
    output1=0

if weighted_sum2>bias:
    output2=1
else:
    output2=0

# Print the results
print("Inputs1:", inputs1)
print("Weights:", weights)
print("Bias:", bias)
print("Weighted Sum1:", weighted_sum1)
print("Output1:", output1)

print("----------------")

print("Inputs2:", inputs2)
print("Weights:", weights)
print("Bias:", bias)
print("Weighted Sum2:", weighted_sum2)
print("Output2:", output2)
