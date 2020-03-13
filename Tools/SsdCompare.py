import ssdeep

ssdeep1 = "12288:F/OZCxVMDS9hD8yC6a15tV9CJ8+lx4pep:FGZCxVOYtXC6aLtGJfiI"
ssdeep2 = "12288:X/OZCxVMDS9hD8yC6a15tV9CJ8+lx4pe:XGZCxVOYtXC6aLtGJfi"
print(ssdeep.compare(ssdeep1, ssdeep2))